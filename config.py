import os
from urllib.parse import quote


class Config:
    MYSQL_HOST = os.getenv("MYSQL_HOST", "studentrisk.mysql.database.azure.com")
    MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "flexibleserverdb")
    MYSQL_USER = os.getenv("MYSQL_USER", "Driga")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "Tanatswa@1212")

    encoded_user = quote(MYSQL_USER, safe="")
    encoded_password = quote(MYSQL_PASSWORD, safe="")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"mysql+pymysql://{encoded_user}:{encoded_password}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?ssl_ca=none&ssl_verify_cert=false",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
