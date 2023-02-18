
## Install requirements
You need `python 3.10.8`


```
python -m venv .venv  # create the virtual environment
source .venv/bin/activate  # activate the virtual environment
pip install --upgrade pip  # update pip
pip install -r requirements.txt  # install the required packages
```

## Run the server
```
uvicorn app.main:app --reload
```