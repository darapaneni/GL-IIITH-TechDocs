from mailjet_rest import Client
import os
import json
from flask import Blueprint
from flask import current_app
from flask import url_for
from sqlalchemy import create_engine, select, update
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from collections import namedtuple
from urllib.parse import urljoin, urlencode, urlparse, urlunparse
import os
from dotenv import load_dotenv


mail_bp = Blueprint("mail_bp", __name__)

basedir = os.path.abspath(os.path.dirname(__file__))
env = os.path.join(basedir,'../.env.local')
if os.path.exists(env):
    load_dotenv(env)
fe_url = os.environ.get('FE_URL')
# namedtuple to match the internal signature of urlunparse
Components = namedtuple(
    typename='Components',
    field_names=['scheme', 'netloc', 'url', 'path', 'query', 'fragment']
)

EXPIRES_SEC = 1800

api_key = 'b64d34f557d5b9dec28c1cd110d5ffc9'
api_secret = '4cef7e3e4a6e90db19bcc9070db8b58b'

mailjet = Client(auth=(api_key, api_secret), version='v3.1')

def send_reset_email(user_id, email):

  token = get_reset_token(user_id, EXPIRES_SEC)

  query_params = {
    'token': token
  }

  url = urlunparse(
    Components(
      scheme='http',
      netloc=fe_url,
      query=urlencode(query_params),
      path='',
      url='',
      fragment='anchor'
    )
  )

  print(url)

  #userprofile = UserProfile.query.filter_by(UserId=user_id).first()
  #name = userprofile.FirstName
  name = ''

  data = {
    'Messages': [
      {
        "From": {
          "Email": "techdoc.gl@gmail.com",
          "Name": "Techdoc"
        },
        "To": [
          {
            "Email": email,
            "Name": name
          }
        ],
        "Subject": "Password Reset Request",
        "TextPart": "To reset your password, visit the following link:",
        "HTMLPart": "<h3>Dear " +name+"</h3> <br> To reset your password visit the following link "+url+" <br> or <a href='"+url+"'>click here </a>to reset password<br>",
        #"CustomID": "AppGettingStartedTest"
      }
    ]
  }
  result = mailjet.send.create(data=data)
  print(result.status_code)
  print(result.json())



def get_reset_token(user_id, expires_sec):
  s = Serializer(current_app.config['SECRET'], expires_sec)
  return (s.dumps({'Id': user_id}).decode('utf-8'))

def verify_reset_token(token):
  s = Serializer(current_app.config['SECRET'])
  try:
    user_id = s.loads(token)['Id']
  except Exception as e:
    return None
  return user_id