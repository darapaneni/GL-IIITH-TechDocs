# MVP for TechDocs
# It contains the Flask server setup (with dependencies in requirements.txt)
# The file structure has src directory with app.py file
# the src directory has templates directory which has index.html


from distutils.log import debug
from flask_bcrypt import Bcrypt
import sentry_sdk
from flask import Flask, jsonify, render_template
import socket
import yaml
import sys

sys.path.append('../')

from flask_cors import CORS
from services.UserRegistration.register import register_bp
from services.FileManager.FileManager import fileManagerBlueprint
from services.UserAuthentication.Login import userLogin_bp
from services.UserAuthentication.Logout import userLogout_bp
from services.UserProfileManagement.getprofile import getUserProfile_bp
from services.UserProfileManagement.updateprofile import updateUserProfile_bp
from services.UserProfileManagement.deleteprofile import deletecode_bp
from services.ForgotPassword.forgotpassword import forgotpassword_bp
from services.ChangePassword.changepassword1 import changepassword_bp
from services.ForgotPassword.mail import mail_bp
from services.DocumentVersionManager.DocumentVersionManager import documentVersionManagerBlueprint
from services.UserHistoryManager.UserHistoryManager import userHistoryManagerBlueprint
from services.RazorpayIntegration.razorPay import razorPayBlueprint
from services.Permissions.permissions import permissions_bp
# For logging 
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="https://4ed42bcd9de142069657a04b0db4c13a@o4504110696824832.ingest.sentry.io/4504110699118592",
    integrations=[
        FlaskIntegration(),
    ],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # By default the SDK will try to use the SENTRY_RELEASE
    # environment variable, or infer a git commit
    # SHA as release, however you may want to set
    # something more human-readable.
    # release="myapp@1.0.0",
)

app= Flask(__name__)
CORS(app, resources={r"/*":{"origins":"*"}})
app.config.from_object('config.ProdConfig')

app.register_blueprint(register_bp)
app.register_blueprint(documentVersionManagerBlueprint)
app.register_blueprint(userHistoryManagerBlueprint)
app.register_blueprint(fileManagerBlueprint)
app.register_blueprint(userLogin_bp)
app.register_blueprint(userLogout_bp)
app.register_blueprint(getUserProfile_bp)
app.register_blueprint(updateUserProfile_bp)
app.register_blueprint(deletecode_bp)
app.register_blueprint(forgotpassword_bp)
app.register_blueprint(changepassword_bp)
app.register_blueprint(mail_bp)
app.register_blueprint(razorPayBlueprint)
app.register_blueprint(permissions_bp)

# This function get the hostname and IP deatils of server, required for microservices
def fetchDetails():
	hostname = socket.gethostname()
	host_ip = socket.gethostbyname(hostname)
	return str(hostname) , str(host_ip)

# This is main / landing page API 
@app.route("/")
def hello_world():
	return "<h3>TechDocs API server</h3>"

# This is for endpoint "Health" to healthcheck the container health in microservices
@app.route("/health")
def health():
	return jsonify(Status ="UP")

# Endpoint for dynamic page 
@app.route("/details")
def details():
	hostname, ip = fetchDetails()
	return render_template('index.html', HOSTNAME=hostname, IP=ip)

if __name__ == '__main__':
	app.run(debug=True)
