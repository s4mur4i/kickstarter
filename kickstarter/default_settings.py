import os
import cloudinary

DEBUG = True
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + BASE_DIR + "/app.db"

cloudinary.config(
  cloud_name="s4mur4i",
  api_key="771132351999124",
  api_secret="NiLiuCXH0TmCwNACnQG5h0VK5_o"
)
