from cassandra.cqlengine.management import sync_table
from fastapi import FastAPI

from . import config, db
from .users.models import User

app = FastAPI()
# the global session. We do not want to initialize
# a new session every time
DB_SESSION = None


# sync the tables when the app starts
@app.on_event("startup")
def on_startup():
    print("Syncing tables...")
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(User)


@app.get("/")
def homepage():
    return {
        "Hello": "World",
    }  # json data -> REST API


@app.get("/users")
def users_list_view():
    q = User.objects.all().limit(10)
    return list(q)
