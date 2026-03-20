# DASS-ASSIGNMENT-2

## Run And Test Guide (Windows PowerShell)

Use these commands from the repository root:

C:\Users\Lenovo\Desktop\DASS Assignment 2\DASS-ASSIGNMENT-2

### 1) Whitebox Part 1.2 (MoneyPoly)

Run the MoneyPoly program:

Set-Location "C:\Users\Lenovo\Desktop\DASS Assignment 2\DASS-ASSIGNMENT-2\whitebox\part 1.2\moneypoly"
python .\main.py

Run pylint checks used in Part 1.2:

Set-Location "C:\Users\Lenovo\Desktop\DASS Assignment 2\DASS-ASSIGNMENT-2\whitebox\part 1.2\moneypoly"
python -m pylint moneypoly main.py

### 2) Whitebox Part 1.3 (Test Cases)

Run the whitebox test cases:

Set-Location "C:\Users\Lenovo\Desktop\DASS Assignment 2\DASS-ASSIGNMENT-2"
python -m unittest -v "whitebox/part 1.3/test_whitebox_cases.py"

### 3) Integration Part (Part 2)

Important: run integration modules from repository root using -m so package imports work.

Run each module individually (module import check):

Set-Location "C:\Users\Lenovo\Desktop\DASS Assignment 2\DASS-ASSIGNMENT-2"
python -m integration.code.registration
python -m integration.code.crew_management
python -m integration.code.inventory
python -m integration.code.race_management
python -m integration.code.results
python -m integration.code.mission_planning
python -m integration.code.vehicle_maintenance
python -m integration.code.sponsorship_budget

Run each integration unit test file individually:

Set-Location "C:\Users\Lenovo\Desktop\DASS Assignment 2\DASS-ASSIGNMENT-2"
python -m unittest -v integration/tests/test_registration.py
python -m unittest -v integration/tests/test_crew_management.py
python -m unittest -v integration/tests/test_inventory.py
python -m unittest -v integration/tests/test_race_management.py
python -m unittest -v integration/tests/test_results.py
python -m unittest -v integration/tests/test_mission_planning.py
python -m unittest -v integration/tests/test_vehicle_maintenance.py
python -m unittest -v integration/tests/test_sponsorship_budget.py

Run all integration tests together:

Set-Location "C:\Users\Lenovo\Desktop\DASS Assignment 2\DASS-ASSIGNMENT-2"
python -m unittest discover -s integration/tests -p "test_*.py" -v

Run Part 2.2 integration tests (cross-module scenarios) from integrationn tests folder:

Set-Location "C:\Users\Lenovo\Desktop\DASS Assignment 2\DASS-ASSIGNMENT-2"
python -m unittest discover -s "integration/integrationn tests" -p "test_*.py" -v

Run all integration tests from both folders:

Set-Location "C:\Users\Lenovo\Desktop\DASS Assignment 2\DASS-ASSIGNMENT-2"
python -m unittest discover -s integration/tests -p "test_*.py" -v
python -m unittest discover -s "integration/integrationn tests" -p "test_*.py" -v

Run coverage for integration code (target 100%):

Set-Location "C:\Users\Lenovo\Desktop\DASS Assignment 2\DASS-ASSIGNMENT-2"
python -m coverage erase
python -m coverage run -m unittest discover -s integration/tests -p "test_*.py"
python -m coverage run --append -m unittest discover -s "integration/integrationn tests" -p "test_*.py"
python -m coverage report -m integration/code/*.py

### Optional: Use the project virtual environment interpreter explicitly

If python is not mapped to your active environment, replace python with:

"c:/Users/Lenovo/Desktop/DASS Assignment 2/.venv/Scripts/python.exe"