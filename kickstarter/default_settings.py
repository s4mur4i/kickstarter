import os
import cloudinary

DEBUG = True
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + BASE_DIR + "/app.db"

SECURITY_REGISTERABLE = True
SECURITY_SEND_REGISTER_EMAIL = True
SECURITY_EMAIL_SENDER = "Kickstarter"
SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
SECURITY_PASSWORD_SALT = "kickstarter"
SECRET_KEY = "\xf3\xd2\xb0\xad\x8e\x81\x05\x96Z\xf5\tB\x0c\x8b\xef\x0e\x10b+KQ\xe0q\x02"
MAIL_SERVER = "smtp.sendgrid.net"
MAIL_PORT = "2525"
MAIL_USERNAME = "kickstarter-demo"
MAIL_PASSWORD = "password1"
STRIPE_API_KEY = "sk_test_qLtfhTOgpXiAdk306NJBr8rk"
STRIPE_PUBLISHABLE_KEY = "pk_test_CIweTbhgaGOp2IhCRF5YG6Jk"
PROJECT_TOKEN = "2e8fa7f5a2cb84cf9d3fda1394150b47"

cloudinary.config(
    cloud_name="s4mur4i",
    api_key="771132351999124",
    api_secret="NiLiuCXH0TmCwNACnQG5h0VK5_o"
)
