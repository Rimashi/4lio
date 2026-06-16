import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret')
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{os.getenv('PG_USER','postgres')}:"
        f"{os.getenv('PG_PASSWORD','')}@"
        f"{os.getenv('PG_HOST','localhost')}:"
        f"{os.getenv('PG_PORT','5432')}/"
        f"{os.getenv('PG_DB','folio')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'static/uploads')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB