# DASS-ASSIGNMENT-2

## Run And Test Guide (Windows PowerShell)

Use these commands from the repository root:

```powershell
Set-Location "C:\Users\Lenovo\Desktop\DASS Assignment 2\DASS-ASSIGNMENT-2"
```

### 1) Whitebox Part 1.2 (MoneyPoly)

Run the MoneyPoly program:

```powershell
Set-Location "C:\Users\Lenovo\Desktop\DASS Assignment 2\DASS-ASSIGNMENT-2\whitebox\part 1.2\moneypoly"
python .\main.py
```

Run pylint checks used in Part 1.2:

```powershell
Set-Location "C:\Users\Lenovo\Desktop\DASS Assignment 2\DASS-ASSIGNMENT-2\whitebox\part 1.2\moneypoly"
python -m pylint moneypoly main.py
```

### 2) Whitebox Part 1.3 (Test Cases)

Run the whitebox test cases:

```powershell
Set-Location "C:\Users\Lenovo\Desktop\DASS Assignment 2\DASS-ASSIGNMENT-2"
python -m unittest -v "whitebox/part 1.3/test_whitebox_cases.py"
```

### 3) Integration Part (Part 2)

Important: run integration modules from repository root using -m so package imports work.

Run each module individually (module import check):

```powershell
Set-Location "C:\Users\Lenovo\Desktop\DASS Assignment 2\DASS-ASSIGNMENT-2"
python -m integration.code.registration
python -m integration.code.crew_management
python -m integration.code.inventory
python -m integration.code.race_management
python -m integration.code.results
python -m integration.code.mission_planning
python -m integration.code.vehicle_maintenance
python -m integration.code.sponsorship_budget
```

Run each integration unit test file individually:

```powershell
Set-Location "C:\Users\Lenovo\Desktop\DASS Assignment 2\DASS-ASSIGNMENT-2"
python -m unittest -v integration/tests/test_registration.py
python -m unittest -v integration/tests/test_crew_management.py
python -m unittest -v integration/tests/test_inventory.py
python -m unittest -v integration/tests/test_race_management.py
python -m unittest -v integration/tests/test_results.py
python -m unittest -v integration/tests/test_mission_planning.py
python -m unittest -v integration/tests/test_vehicle_maintenance.py
python -m unittest -v integration/tests/test_sponsorship_budget.py
```

Run all integration tests together:

```powershell
Set-Location "C:\Users\Lenovo\Desktop\DASS Assignment 2\DASS-ASSIGNMENT-2"
python -m unittest discover -s integration/tests -p "test_*.py" -v
```

Run Part 2.2 integration tests (cross-module scenarios) from integrationn tests folder:

```powershell
Set-Location "C:\Users\Lenovo\Desktop\DASS Assignment 2\DASS-ASSIGNMENT-2"
python -m unittest discover -s "integration/integrationn tests" -p "test_*.py" -v
```

Run all integration tests from both folders:

```powershell
Set-Location "C:\Users\Lenovo\Desktop\DASS Assignment 2\DASS-ASSIGNMENT-2"
python -m unittest discover -s integration/tests -p "test_*.py" -v
python -m unittest discover -s "integration/integrationn tests" -p "test_*.py" -v
```

Run coverage for integration code (target 100%):

```powershell
Set-Location "C:\Users\Lenovo\Desktop\DASS Assignment 2\DASS-ASSIGNMENT-2"
python -m coverage erase
python -m coverage run -m unittest discover -s integration/tests -p "test_*.py"
python -m coverage run --append -m unittest discover -s "integration/integrationn tests" -p "test_*.py"
python -m coverage report -m integration/code/*.py
```

### Optional: Use the project virtual environment interpreter explicitly

If python is not mapped to your active environment, replace python with:

```powershell
"c:/Users/Lenovo/Desktop/DASS Assignment 2/.venv/Scripts/python.exe"
```

### 4) Blackbox Part (Part 3 - QuickCart API)

Important: run Docker/API commands from the blackbox folder, and run pytest from repository root.

Go to blackbox folder:

```powershell
Set-Location "C:\Users\Lenovo\Desktop\DASS Assignment 2\DASS-ASSIGNMENT-2\blackbox"
```

Load the API Docker image (if not loaded yet):

```powershell
docker load -i quickcart_image_x86.tar
```

If a container with same name already exists, remove it first:

```powershell
docker stop quickcart-api
docker rm quickcart-api
```

Run API container:

```powershell
docker run --name quickcart-api -p 8080:8080 quickcart
```

In a new PowerShell terminal, run blackbox tests:

```powershell
Set-Location "C:\Users\Lenovo\Desktop\DASS Assignment 2\DASS-ASSIGNMENT-2"
$env:QUICKCART_ROLL_NUMBER="2024101020"
python -m pytest -q blackbox/tests
```

Run blackbox coverage:

```powershell
Set-Location "C:\Users\Lenovo\Desktop\DASS Assignment 2\DASS-ASSIGNMENT-2"
python -m coverage erase
python -m coverage run -m pytest -q blackbox/tests
python -m coverage report -m blackbox/tests/*.py
```

Stop and remove API container after testing:

```powershell
docker stop quickcart-api
docker rm quickcart-api
```

## Python Libraries Installed In Project venv

Python version in venv: 3.13.7

Directly installed/used for this assignment:

- pylint (4.0.5)
- pytest (9.0.2)
- requests (2.32.5)
- coverage (7.13.5)

Dependencies currently present in venv:

- astroid (4.0.4)
- certifi (2026.2.25)
- charset-normalizer (3.4.6)
- colorama (0.4.6)
- dill (0.4.1)
- idna (3.11)
- iniconfig (2.3.0)
- isort (8.0.1)
- mccabe (0.7.0)
- packaging (26.0)
- pip (26.0.1)
- platformdirs (4.9.4)
- pluggy (1.6.0)
- Pygments (2.19.2)
- tomlkit (0.14.0)
- urllib3 (2.6.3)