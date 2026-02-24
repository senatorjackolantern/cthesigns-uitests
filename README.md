# cthesigns-uitests
UI test project for c the signs interview process

2/24/26 Saul Jacobowitz

Setup Instructions
1. navigate to `/cthesigns-uitests/web-ui-tests/`

2. start the virtual environment:
`python3 -m venv .venv`

3. Install pytest
`pip install selenium pytest`

4. Run tests
`pytest`  #to run all tests
`pytest tests/test_homepage.py::test_name -v`  #to run a specific test