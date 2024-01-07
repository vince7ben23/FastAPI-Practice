# Build Social Media APIs with FastAPI

## Create Conda Env
- `conda create -n fast_api_3.9 python=3.9`
- `pip install poetry`
- `poetry install --no-root`

## Run API Service
- Note the working directory is the root of this project
- `conda activate fast_api_3.9`
- `uvicorn src.main:app --reload`

## Run Test Cases
- `export ENV=run_test_cases`
- `conda activate fast_api_3.9`
- `python -m pytest`