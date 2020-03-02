from pytest import fixture


@fixture(scope='module')
def api_client():
    from app import app
    app.testing = True
    return app.test_client()
