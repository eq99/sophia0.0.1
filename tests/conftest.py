import pytest
from app import create_app
from plugins import db


@pytest.fixture
def app():
    app = create_app()
    app.config.from_object('config.Production')
    with app.app_context():   
        db.create_all()
    return app