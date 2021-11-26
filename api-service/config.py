from dotenv import dotenv_values

config = dotenv_values(".env")

SQLALCHEMY_DATABASE_URI = f"mysql+mysqldb://{config['DB_USER']}:{config['DB_PASSWORD']}@{config['DB_HOST']}/" \
                          f"{config['DB_NAME']}?charset=utf8mb4"
FORMAT_STRING_DATETIME = '%Y/%m/%d, %H:%M:%S'
JWT_SECRET_KEY = f"{config['JWT_SECRET_KEY']}"
SECRET_KEY = f"{config['SECRET_KEY']}"
WTF_CSRF_SECRET_KEY = f"{config['WTF_CSRF_SECRET_KEY']}"
MAIL_SERVER = config['MAIL_SERVER']
MAIL_PORT = config['MAIL_PORT']
MAIL_USE_TLS = config['MAIL_USE_TLS']
MAIL_USERNAME = config['MAIL_USERNAME']
MAIL_PASSWORD = config['MAIL_PASSWORD']