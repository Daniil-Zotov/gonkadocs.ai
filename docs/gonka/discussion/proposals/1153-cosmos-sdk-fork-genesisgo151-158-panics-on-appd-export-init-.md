---
title: "#1153 — cosmos-sdk fork: genesis.go:151-158 panics on `appd export → init` — mirror existing PoC skip pattern from delegation.go?"
source: https://github.com/gonka-ai/gonka/discussions/1153
discussion_number: 1153
category: proposals
synced_at: 2026-06-28T14:17:07Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #1153](https://github.com/gonka-ai/gonka/discussions/1153) каждые 6 часов. 

# cosmos-sdk fork: genesis.go:151-158 panics on `appd export → init` — mirror existing PoC skip pattern from delegation.go?

**Автор:** [@vitaly-andr](https://github.com/vitaly-andr) · **Категория:** :bulb: Proposals · **Создано:** 2026-05-08 11:47 UTC · **Обновлено:** 2026-05-08 12:14 UTC

---

## 📝 Описание

Posting this for maintainer validation before opening a PR against
`gonka-ai/cosmos-sdk`. Discovered while implementing simulation tests for
gonka-ai/gonka#982 Phase 1.

### Summary

`gonka-ai/cosmos-sdk@v0.53.3-ps17` deliberately disables token bonding for PoC
validators. `compute.go:SetComputeValidators` creates bonded validators with
`validator.Tokens` set but no corresponding bank coins in the BondedPool module
account. This is the documented design (see `gonka/docs/cosmos_changes.md`
"No Token Bonding" section).

The fork **already** applies the matching modifications to keep this design
consistent across runtime paths:

- `x/staking/keeper/pool.go:78-92` — `TotalBondedTokens` iterates validators
  manually instead of querying bank (explicit `// PoC OVERRIDE` comment).
- `x/staking/keeper/delegation.go` — `Delegate` skips coin transfer when
  `validator.Description.Details == "Created after Proof of Compute"`.
- `x/staking/keeper/val_state_change.go` — removed transfers between bonded /
  not-bonded pools.

The only remaining gap is `x/staking/keeper/genesis.go:151-158`, which still
enforces the upstream invariant:

```go
bondedBalance := k.bankKeeper.GetAllBalances(ctx, bondedPool.GetAddress())
// ...
// if balance is different from bonded coins panic because genesis is most likely malformed
if !bondedBalance.Equal(bondedCoins) {
    panic(fmt.Sprintf("bonded pool balance is different from bonded coins: %s <-> %s", bondedBalance, bondedCoins))
}
```

This invariant is upstream cosmos-sdk and is **incompatible** with the PoC
design — `bondedBalance` is always zero (PoC validators don't fund bonded
pool), but `bondedCoins` is `sum(validator.Tokens)` which is non-zero for any
cycle past the first PoC epoch transition.

### Impact

`inferenced export` (which calls `bApp.ExportAppStateAndValidators`) produces
a JSON genesis. `inferenced init <chain> --genesis <that file>` then panics on
boot because staking InitGenesis hits this invariant.

This means `gonka-ai/gonka` cannot perform a vanilla `appd export → init` chain
upgrade. Production has worked around this by using `x/upgrade` in-place
handlers exclusively (see `inference-chain/app/upgrades/v0_2_*`), which migrate
live state instead of re-initing from exported genesis. So the bug is latent
but not blocking today — until someone needs disaster recovery from a known-good
export, or a fork-from-genesis, or any other vanilla import-from-export flow.

### Reproduction

(Once gonka-ai/gonka#982 Phase 1 lands.) Run any simulation that crosses an
epoch boundary, then:

```go
exported, _ := bApp.ExportAppStateAndValidators(false, []string{}, []string{})
newApp := /* fresh App via app.New */
newApp.ModuleManager.InitGenesis(ctxB, newApp.AppCodec(), genesisState)
// panics: bonded pool balance is different from bonded coins:  <-> 906008476161stake
```

The panic site is `x/staking/keeper/genesis.go:158`.

The new `TestAppImportExport_Postrun` in `inference-chain/app/sim_test.go`
reproduces this on the first PoC epoch transition.

### Proposed fix

Apply the same skip pattern that already exists in `delegation.go`:

```diff
 bondedBalance := k.bankKeeper.GetAllBalances(ctx, bondedPool.GetAddress())
 // ...
+// PoC validators are unbonded by design; their tokens are not backed by
+// bank coins (see compute.go:SetComputeValidators and the "No Token Bonding"
+// section in gonka/docs/cosmos_changes.md). Subtract their token sum before
+// comparing against bondedBalance.
+pocBonded := sdk.ZeroInt()
+for _, validator := range data.Validators {
+    if validator.Status == types.Bonded && validator.Description.Details == "Created after Proof of Compute" {
+        pocBonded = pocBonded.Add(validator.Tokens)
+    }
+}
+expected := bondedCoins.Sub(sdk.NewCoin(data.Params.BondDenom, pocBonded))
-if !bondedBalance.Equal(bondedCoins) {
+if !bondedBalance.Equal(expected) {
     panic(fmt.Sprintf("bonded pool balance is different from bonded coins: %s <-> %s", bondedBalance, bondedCoins))
 }
```

(Same pattern needed for the `notBondedBalance` check at line 173-175 — though
it's less likely to fire in practice because PoC validators are always Bonded
status.)

### Open questions for maintainers

1. Does the framing match your intent? Specifically: is `appd export → init`
   considered a supported flow for this fork, or has it been intentionally
   given up in favor of `x/upgrade` in-place handlers?
2. The `Description.Details == "Created after Proof of Compute"` string match
   is fragile (already used in `delegation.go`, so consistent with existing
   fork convention). Would a typed flag on `Validator` be preferable, or is the
   string-match convention something you'd like preserved for now?
3. The fix is intentionally local to the fork — upstream cosmos-sdk should not
   carry a PoC-specific check. Confirm this matches your architectural
   direction?

### Existing fork modifications referenced

The proposed fix mirrors patterns already present in this fork:

- `x/staking/keeper/delegation.go` — `Delegate` skip for PoC validators (commit
  by `johnlong`, 2024-08 "Working version"; reinforced 2025-01-10 "Add delegation
  to our staking override"; later "Genesis only protection" by `Gleb Morgachev`
  2025-09-30 added a hard post-genesis ban).
- `x/staking/keeper/pool.go` — `TotalBondedTokens` manual iteration ("Genesis
  only protection", "Handle missed blocks" by `Gleb Morgachev`, 2025-09).
- `x/staking/keeper/val_state_change.go` — removed bonded/not-bonded transfers.
- `x/staking/keeper/compute.go` — `SetComputeValidators` (multiple commits
  through 2025-12-21, mainly `Gleb Morgachev` and `dima`).

The missing modification in `genesis.go:157-158` is the only gap in this set.

### Ready to PR

Happy to open a PR against `gonka-ai/cosmos-sdk` implementing the fix above
(genesis.go only, ~10 lines mirroring existing convention) if my understanding
of the design intent is correct. Holding off until a maintainer confirms so I
don't waste a roundtrip.

