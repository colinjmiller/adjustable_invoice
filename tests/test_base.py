import os
import tempfile
import pytest
from adjustable_invoice import app


@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def test_homepage(client):
    rv = client.get('/')
    assert(rv.status_code == 200)
    assert(b'Invoice Adjuster' in rv.data)


def test_signup_page(client):
    rv = client.get('/signup')
    assert(rv.status_code == 200)
    assert(b'Sign up for Adjustable Invoices' in rv.data)

# With more time, add tests for logging in, signing up, creating invoices, etc.
