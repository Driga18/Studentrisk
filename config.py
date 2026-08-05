import os
import ssl
from urllib.parse import quote

basedir = os.path.abspath(os.path.dirname(__file__))

try:
    import certifi
except ImportError:
    certifi = None


def get_ssl_ca_file():
    candidates = []

    env_path = os.getenv("MYSQL_SSL_CA")
    if env_path:
        candidates.append(env_path)

    candidates.append(os.path.join(os.path.dirname(__file__), "MysqlflexGlobalRootCA.crt.pem"))

    default_paths = ssl.get_default_verify_paths()
    if default_paths.cafile:
        candidates.append(default_paths.cafile)

    if certifi is not None:
        candidates.append(certifi.where())

    for candidate in candidates:
        if candidate and os.path.exists(candidate):
            return candidate

    return candidates[0] if candidates else None


class Config:
    MYSQL_HOST = os.getenv("MYSQL_HOST", "studentrisk.mysql.database.azure.com")
    MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "flexibleserverdb")
    MYSQL_USER = os.getenv("MYSQL_USER", "Driga@studentrisk")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "Tanatswa@1212")  # plain text

    encoded_user = quote(MYSQL_USER, safe="")
    encoded_password = quote(MYSQL_PASSWORD, safe="")

    SSL_CA_FILE = get_ssl_ca_file()

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{encoded_user}:{encoded_password}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {}
    if SQLALCHEMY_DATABASE_URI.startswith("mysql") and SSL_CA_FILE:
        SQLALCHEMY_ENGINE_OPTIONS = {"connect_args": {"ssl": {"ca": SSL_CA_FILE}}}

print("MYSQL_USER:", os.getenv("MYSQL_USER"))
print("MYSQL_PASSWORD:", os.getenv("MYSQL_PASSWORD"))
     
