import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://devroot:Root@ass3db.csetddxyihfv.us-east-1.rds.amazonaws.com:3306/testDB'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
