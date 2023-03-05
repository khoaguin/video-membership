import json
import pathlib

from cassandra.cqlengine.management import sync_table
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic.error_wrappers import ValidationError

from . import config, db, utils
from .shortcuts import render
from .users.models import User
from .users.schemas import UserLoginSchema, UserSignupSchema

BASE_DIR = pathlib.Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"

app = FastAPI()
templates = Jinja2Templates(directory=TEMPLATE_DIR)

# the global database session. We do not want
# to initialize a new session every time
DB_SESSION = None


# sync the tables when the app starts
@app.on_event("startup")
def on_startup():
    print("Syncing tables...")
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(User)


@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    context = {"abc": 123}
    return render(request, "home.html", context)


@app.get("/login", response_class=HTMLResponse)
def login_get_view(request: Request):
    session_id = request.cookies.get("session_id") or None
    return render(request, "auth/login.html", {"logged_in": session_id is not None})


@app.post("/login", response_class=HTMLResponse)
def login_post_view(
    request: Request, email: str = Form(...), password: str = Form(...)
):
    raw_data = {
        "email": email,
        "password": password,
    }
    data, errors = utils.valid_schema_data_or_error(raw_data, UserLoginSchema)
    context = {
        "data": data,
        "error": errors,
    }
    if len(errors) > 0:
        return render(
            request,
            "auth/login.html",
            context,
            status_code=400,
        )
    print(data)
    return render(request, "auth/login.html", {"logged_in": True}, cookies=data)


@app.get("/signup", response_class=HTMLResponse)
def signup_get_view(request: Request):
    return render(request, "auth/signup.html")


@app.post("/signup", response_class=HTMLResponse)
def signup_post_view(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    password_confirm: str = Form(...),
):
    raw_data = {
        "email": email,
        "password": password,
        "password_confirm": password_confirm,
    }
    data, errors = utils.valid_schema_data_or_error(raw_data, UserSignupSchema)
    return render(
        request,
        "auth/signup.html",
        {
            "data": data,
            "errors": errors,
        },
    )


@app.get("/users")
def users_list_view():
    q = User.objects.all().limit(10)
    User.objects.de
    return list(q)
