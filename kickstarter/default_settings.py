import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLALCHEMY_DATABSE_URI = "sqlite:///" + BASE_DIR + "/app.db"