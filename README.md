# lts-fastapi

API for traffic stress analysis using FastAPI

## Development Environment

Create the virtual environment:

```
python -m venv env
```

Activate the environment:

```
source env/bin/activate
```

Install requirements:

```
pip install -r requirements.txt
```

Create a `.env` file that defines a `DATABASE_URL`. For example:

```
DATABASE_URL = postgresql://username:password@host:port/database
```

Run the API locally:

```
uvicorn src.main:app --reload
```
