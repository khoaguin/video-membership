import pytest

from app import db
from app.users.models import User


@pytest.fixture(scope="module")
def setup():
    session = db.get_session()
    yield session
    q = User.objects.filter(email="test@teamcfe.com")
    if q.count() != 0:
        q.delete()
    session.shutdown()


def test_create_user(setup):
    User.create_user(email="test@teamcfe.com", password="abc123")


def test_duplicate_user(setup):
    # expect this to fail and raise an exception
    with pytest.raises(Exception):
        User.create_user(email="test@teamcfe.com", password="abc123123")


def test_invalid_email(setup):
    # expect this to fail and raise an exception
    with pytest.raises(Exception):
        User.create_user(email="test@teamcfe", password="abc123123")


def test_valid_password(setup):
    q = User.objects.filter(email="test@teamcfe.com")
    assert q.count() == 1
    user_obj = q.first()
    assert user_obj.verify_password("abc123") == True
    assert user_obj.verify_password("abc123123") == False
