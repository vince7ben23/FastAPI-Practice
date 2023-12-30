# FastAPI-Practice

## Create Conda Env
- `conda create -n fast_api_3.9 python=3.9`
- `pip install poetry`
- `poetry install --no-root`

## Run API service
- `conda activate fast_api_3.9`
- `uvicorn main:app --reload`

## Run Test Cases
- `python -m pytest`