# Part 1.3 - White Box Test Cases

## Initial White-Box Test Set (Before Fixes)

This section lists all designed tests before any bug-fix commits.
Each test is derived from branch/state analysis of the source code.

1. `test_bank_collect_negative_is_ignored`
- Path covered: `Bank.collect` with negative amount.
- Why needed: The method docstring says negative amounts are ignored.
- Risk covered: Silent balance corruption if negative values reduce reserves.

2. `test_give_loan_reduces_bank_reserves`
- Path covered: `Bank.give_loan` for positive loan value.
- Why needed: Loan operation should transfer money from bank to player.
- Risk covered: Money creation if player gains funds without bank deduction.

3. `test_player_move_passing_go_grants_salary`
- Path covered: `Player.move` wrap-around (`old + steps >= BOARD_SIZE`).
- Why needed: Passing Go should reward salary according to game rules.
- Risk covered: Missing salary on wrap-around movement.

4. `test_jail_voluntary_fine_deducts_player_balance`
- Path covered: `_handle_jail_turn` voluntary fine branch (`confirm -> True`).
- Why needed: Paying fine should reduce player balance and increase bank balance.
- Risk covered: Inconsistent money flow while leaving jail.

5. `test_trade_credits_seller`
- Path covered: `Game.trade` successful path.
- Why needed: Buyer-to-seller cash transfer is required for a valid sale.
- Risk covered: Seller not credited and money disappearing from the system.

## Run Command

From repository root:

```powershell
& "c:/Users/Lenovo/Desktop/DASS Assignment 2/.venv/Scripts/python.exe" -m unittest -v "whitebox/part 1.3/test_whitebox_cases.py"
```

## Error-Fix Commit Log

This section will be appended before each `Error #` commit with:
- failing test(s)
- root cause
- code change summary
- commit hash

## Error 1 Planned Fix

- Failing test: `test_bank_collect_negative_is_ignored`
- Root cause: `Bank.collect` adds negative values directly, reducing bank reserves.
- Change to apply: Return early for negative amounts so they are ignored.

## Error 2 Planned Fix

- Failing test: `test_give_loan_reduces_bank_reserves`
- Root cause: `Bank.give_loan` credits player but does not deduct bank reserves.
- Change to apply: Subtract loan amount from bank funds when loan is issued.

## Error 3 Planned Fix

- Failing test: `test_player_move_passing_go_grants_salary`
- Root cause: `Player.move` awards salary only when landing exactly on Go, not when passing Go.
- Change to apply: Detect wrap-around and award Go salary for any pass-over movement.

## Error 4 Planned Fix

- Failing test: `test_jail_voluntary_fine_deducts_player_balance`
- Root cause: Voluntary jail-fine branch collects bank money but does not deduct the player's balance.
- Change to apply: Deduct `JAIL_FINE` from player before releasing from jail.

## Error 5 Planned Fix

- Failing test: `test_trade_credits_seller`
- Root cause: `Game.trade` deducts cash from buyer but does not credit seller.
- Change to apply: Add seller cash credit when trade succeeds.

## Error 6 Planned Fix

- Failing test: `test_empty_deck_cards_remaining_is_zero`
- Root cause: `CardDeck.cards_remaining` performs modulo with `len(self.cards)` and crashes when deck is empty.
- Change to apply: Return `0` immediately for empty decks.

## Error 7 Planned Fix

- Failing test: `test_empty_deck_repr_does_not_crash`
- Root cause: `CardDeck.__repr__` performs modulo with `len(self.cards)` and crashes when deck is empty.
- Change to apply: Use a safe `next_index` value (`0`) for empty decks.

## Error 8 Planned Fix

- Failing test: `test_empty_property_group_is_not_fully_owned`
- Root cause: `PropertyGroup.all_owned_by` returns `True` for empty groups due to `all([])` semantics.
- Change to apply: Return `False` when the group has zero properties.

## Error 9 Planned Fix

- Failing test: `test_net_worth_includes_property_values`
- Root cause: `Player.net_worth` returns cash balance only, excluding owned property value.
- Change to apply: Include property prices in net-worth calculation.
