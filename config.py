# config.py

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # URI di esempio: sqlite (file locale). In produzione potresti usare PostgreSQL, MySQL, ecc.
    SQLALCHEMY_DATABASE_URI = (
        os.getenv('DATABASE_URL') or 
        "sqlite:///" + os.path.join(basedir, "database", "chinook.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Chiavi segrete (devono essere lunghe e randomiche)
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'che-brutto-il-debugging')
