from os import environ

def test_development_config(app):
    app.config.from_object('config.Dev')
    assert app.config['DEBUG']
    assert app.config['TESTING']
    if environ.get('FLASK_ENV') == 'development':
        assert 'dev' in app.config['SQLALCHEMY_DATABASE_URI']


def test_production_config(app):
    '''
    We should run tests before deploy.
    '''
    app.config.from_object('config.Production')
    assert not app.config['DEBUG']
    assert not app.config['TESTING']
    if environ.get('FLASK_ENV') == 'production':
        assert 'dev' not in app.config['SQLALCHEMY_DATABASE_URI']
