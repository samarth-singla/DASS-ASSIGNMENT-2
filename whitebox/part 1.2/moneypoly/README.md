# Instructions To Run

```
python main.py
```

## Part 1.2 - Code Quality Analysis (pylint)

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

### Iteration 3: Game module style cleanup
- Removed unused imports in game module.
- Fixed superfluous f-string usage and no-else-break style issue.
- Simplified range checks and added missing final newline.
- Pylint score: 9.17/10 -> 9.28/10.

### Iteration 4: Board and property style fixes
- Replaced singleton comparison in board purchasable check.
- Simplified unmortgage return flow in property module.
- Pylint score: 9.28/10 -> 9.31/10.

### Iteration 5: Entrypoint and bank documentation
- Added module/function docstrings in main.py.
- Added module/class docstrings in bank.py.
- Pylint score: 9.31/10 -> 9.39/10.

### Iteration 6: Remaining module documentation
- Added module docstrings to board, cards, config, dice, game, player, property, and ui.
- Added missing PropertyGroup class docstring.
- Fixed missing final newline in player.py.
- Pylint score: 9.39/10 -> 9.54/10.

### Iteration 7: Final lint pass and correctness updates
- Reformatted card definitions to resolve all line-length warnings.
- Added targeted pylint suppressions for intentional class complexity.
- Fixed dice roll bounds to standard 1-6.
- Fixed winner selection to highest net worth.
- Fixed rent transfer to property owner.
- Fixed full-group ownership check logic in PropertyGroup.
- Corrected exact-cash property purchase condition.
- Pylint score: 9.54/10 -> 10.00/10.
