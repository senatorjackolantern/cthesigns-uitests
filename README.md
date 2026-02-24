# cthesigns-uitests
UI test project for C the Signs interview process

2/24/26 Saul Jacobowitz

Setup Instructions (based on NG12 Cancer Risk Assessor page by 0andy at https://ng12assessor.fanai.dev/ -- found here: https://github.com/0andy/ng12_assessor)

UI Tests:
1. navigate to `/cthesigns-uitests/web-ui-tests/`

2. start the virtual environment:
`python3 -m venv .venv`

3. Install pytest
`pip install selenium pytest`

4. Run tests
`pytest`  #to run all tests
`pytest tests/test_homepage.py::test_name -v`  #to run a specific test

API Tests:
1. Navigate to /cthesigns-uitests/api-tests/

2. Run tests
`API_BASE_URL=“https://ng12assessor.fanai.dev” pytest -q`