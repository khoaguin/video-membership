# Video Membership Web App
A video membership web app built with `FastAPI` and `AstraDB` (`Cassandra`).  

## Install requirements
`python==3.10.8` (or higher than 3.6)

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

## References
https://github.com/codingforentrepreneurs/video-membership