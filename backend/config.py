import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
env = os.path.join(basedir,'./.env.local')
if os.path.exists(env):
    load_dotenv(env)

class Config(object):
    DEBUG=False

class DevConfig(Config):
    FLASK_ENV='developement'
    DEBUG=True


class ProdConfig(Config):
    FLASK_ENV='production'
    TESTING=True
    DEBUG=False
    SECRET=os.environ.get('SECRET')
    DIR_ROOT=os.environ.get('DIR_ROOT')
    DIR_DATA=os.environ.get('DIR_DATA')
    DIR_LOG=os.environ.get('DIR_LOG')
    PGKEY_RID=os.environ.get('R_ID')
    PGKEY_RKEY=os.environ.get('R_KEY')
