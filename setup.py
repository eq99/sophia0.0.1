from setuptools import setup, find_packages

setup(
    name='sophia',
    version='0.0.1',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask>=1.1.2',
        'Flask-Caching>=1.9.0',
        'Flask-Login>=0.5.0',
        'Flask-Migrate>=2.6.0',
        'Flask-RESTful>=0.3.8',
        'Flask-Script>=2.0.6',
        'Flask-SQLAlchemy>=2.4.4',
        'gevent>=21.1.2',
        'gunicorn>=20.0.4',
        'psycopg2>=2.8.6',
        'python-dotenv>=0.15.0',
        'qcloudsms-py>=0.1.4',
        'SQLAlchemy>=1.3.22',
      ]
)