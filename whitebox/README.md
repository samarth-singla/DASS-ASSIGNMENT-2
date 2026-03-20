# Whitebox Code Quality Log

## Part 1.2 - MoneyPoly

Baseline pylint score: 9.08/10

### Iteration 1: Basic cleanup
- Removed unused import from bank module.
- Removed unused import and variable from player module.
- Replaced bare except with explicit exceptions in input parser.
- Pylint score: 9.08/10 -> 9.14/10.

### Iteration 2: Dice cleanup
- Removed unused BOARD_SIZE import in dice module.
- Initialized doubles_streak inside constructor.
- Pylint score: 9.14/10 -> 9.17/10.
