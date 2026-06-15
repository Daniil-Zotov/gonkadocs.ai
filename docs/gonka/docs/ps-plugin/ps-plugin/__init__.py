import os
import requests


def get_latest_release(
    org: str,
    repo: str,
    token: str
):
    try:
        response = requests.get(
            f"https://api.github.com/repos/{org}/{repo}/releases/latest",
            headers={'Authorization': f"token {token}"}
        )
        release = response.json()["tag_name"]
        release = release.split("/")[-1]
        return release[1:]
    except Exception as e:
        return "latest"


def android_release():
    token = os.environ["PS_GITHUB_TOKEN"]
    return get_latest_release(
        "product-science",
        "PSAndroidModuleCodeInjector",
        token
    )


def ios_release():
    token = os.environ["PS_GITHUB_TOKEN"]
    return get_latest_release(
        "product-science",
        "PSios",
        token
    )


def define_env(env):
    for fn in [android_release]:
        env.macro(fn)