from flask import Flask
from flask import send_from_directory


app = Flask(__name__,instance_relative_config=True,static_url_path='')

app.config['SECRET_KEY'] = 'secret_key'



@app.route('/site.webmanifest')
def manifest():
    return send_from_directory('static', 'site.webmanifest')


from app import views
