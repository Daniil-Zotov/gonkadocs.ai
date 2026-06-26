#!/usr/bin/env bash
# Сборка сайта gonkadocs.
#
# Сайт состоит из двух независимых сборок MkDocs, объединённых в одном
# каталоге публикации (_site):
#
#   1. Основной сайт  (Главная + Обсуждения + Сообщество + Proposals)
#      -> собирается корневым mkdocs.yml в _site/
#
#   2. Раздел "Gonka" -> ТОЧНАЯ копия документации gonka-ai/gonka-docs.
#      Собирается её РОДНЫМ mkdocs.yml (с плагином i18n: en + zh), который
#      синхронизируется экшеном sync-gonka-ai-docs.yml. Благодаря этому раздел
#      выглядит 1-в-1 как оригинал и автоматически подхватывает любые изменения
#      структуры/навигации/материалов оригинала -> _site/gonka/
#
# Порядок важен: основной сайт собирается ПЕРВЫМ (mkdocs build --clean стирает
# весь site_dir). Сборка Gonka идёт во вложенный каталог _site/gonka и чистит
# только его, не трогая остальной сайт.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SITE_DIR="$ROOT/_site"

echo "==> [1/2] Сборка основного сайта -> $SITE_DIR"
cd "$ROOT"
python3 -m mkdocs build --clean --site-dir "$SITE_DIR"

echo "==> [2/2] Сборка раздела Gonka (родной конфиг оригинала, i18n en+zh) -> $SITE_DIR/gonka/docs"
cd "$ROOT/docs/gonka/docs"

# В оригинале docs/index.md — это ЛЕНДИНГ gonka.ai (template home.html), а не
# документация. Сам оригинал при сборке /docs/ подменяет index.md на
# introduction.md (см. его buildtools/prepare-stages.sh). Повторяем это: на
# время сборки промотируем introduction.md -> index.md, после сборки
# восстанавливаем исходные файлы, чтобы не портить синканутый репозиторий.
DOCS="docs"
declare -a _restore=()
_swap_intro() {
  local dir="$1"            # "" для en, "zh/" для zh
  local idx="$DOCS/${dir}index.md"
  local intro="$DOCS/${dir}introduction.md"
  if [ -f "$intro" ]; then
    if [ -f "$idx" ]; then
      cp "$idx" "$idx.landing.bak"
      _restore+=("$idx")
    fi
    cp "$intro" "$idx"
  fi
}
_restore_intro() {
  for idx in "${_restore[@]}"; do
    if [ -f "$idx.landing.bak" ]; then
      mv "$idx.landing.bak" "$idx"
    fi
  done
}
trap _restore_intro EXIT

_swap_intro ""
_swap_intro "zh/"

# Переопределяем site_url для корректной работы i18n переключателя.
# Оригинальный site_url указывает на gonka.ai — это ломает ссылки на zh/lang
# при развёртывании под путём /gonkadocs/gonka/docs/. Создаём временную копию
# конфига с исправленным site_url и собираем по ней.
SITE_URL="https://daniil-zotov.github.io/gonkadocs/gonka/docs/"
BUILD_CFG=".mkdocs.yml.build"

# Мержим overrides: upstream originals + наши shared-шаблоны.
# mkdocs-material подхватывает custom_dir как overlay поверх стандартной темы.
# Наш overrides идёт вторым → перезаписывает header upstream'а на наш shared.
OVR_DIR=".overrides.merged"
rm -rf "$OVR_DIR"
cp -r overrides "$OVR_DIR"
cp -r "$ROOT/buildtools/gonka-overrides/"* "$OVR_DIR/"

sed -e "s|site_url: .*|site_url: ${SITE_URL}|" \
    -e "s|custom_dir: overrides|custom_dir: ${OVR_DIR}|" \
    mkdocs.yml > "$BUILD_CFG"
python3 -m mkdocs build --config-file "$BUILD_CFG" --site-dir "$SITE_DIR/gonka/docs"
rm -rf "$BUILD_CFG" "$OVR_DIR"

_restore_intro
trap - EXIT

# CNAME принадлежит только корню сайта (домен GitHub Pages задаётся один раз).
# Оригинал кладёт свой CNAME (gonka.ai) в docs/ — удаляем его из подкаталога.
rm -f "$SITE_DIR/gonka/docs/CNAME"

# -----------------------------------------------------------------------
# Пост-обработка: исправление абсолютных путей к изображениям.
#
# В исходниках gonka-ai/gonka-docs изображения указаны абсолютными путями
# вида "/images/foo.png", которые корректно работают на gonka.ai (корень
# сайта = корень документации). В подкаталоге /gonkadocs/gonka/docs/
# эти ссылки ломаются, потому что браузер ищет /images/ в корне нашего
# сайта, а не в корне раздела Gonka.
#
# Папка images/ лежит в корне раздела (/gonkadocs/gonka/docs/images/).
# Относительный путь от страницы до images/ зависит от глубины вложенности:
#   docs/index.html                        -> ../images/
#   docs/architecture/index.html           -> ../images/
#   docs/wallet/create-account/index.html  -> ../../images/
#   docs/cross-chain.../dashboard/index.html -> ../../../images/
#
# Используем Python-скрипт, который вычисляет правильный префикс "../"
# для каждого HTML-файла в зависимости от его пути.
# -----------------------------------------------------------------------
echo "==> [пост-обработка] Исправление путей к изображениям (/images/ -> ..N/images/)"
python3 - "$SITE_DIR/gonka/docs" <<'PYEOF'
import os, re, sys

docs_root = sys.argv[1]

for dirpath, _, filenames in os.walk(docs_root):
    for fn in filenames:
        if not fn.endswith('.html'):
            continue
        fpath = os.path.join(dirpath, fn)
        # Глубина файла относительно docs_root:
        # wallet/create-account/index.html -> 2 -> "../../"
        rel = os.path.relpath(fpath, docs_root)
        depth = rel.count(os.sep)
        prefix = '../' * depth

        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        if '/images/' not in content:
            continue

        new = content.replace('src="/images/', f'src="{prefix}images/')
        new = new.replace('href="/images/', f'href="{prefix}images/')

        if new != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new)
            print(f"  fixed: {rel} ({depth} levels)")
PYEOF

echo "==> Готово. Артефакт: $SITE_DIR"
