import main
import pytest
import json

@pytest.fixture
def app():
    app = main.create_app()
    app.debug = True
    return app.test_client()

def test_success(app):
    request_form = {
        'search_input': 'java',
        'search_type': 'language'
    }

    response = app.post("/search",data=request_form)

    data = response.data
    status = response.status

    assert data is not None
    assert status =="200 OK"

def test_failed(app):
    request_form = {
        'search_input': 'java!!!!!',
        'search_type': 'language'
    }

    response = app.post("/search",data=request_form)

    data = json.loads(response.data)
    status = response.status

    assert data == [
        {
            "code":"invalid",
            "field":"q",
            "message":"None of the search qualifiers apply to this search type.",
            "resource":"Search"
        }
    ]
    assert status =="400 BAD REQUEST"