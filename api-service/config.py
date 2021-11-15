from dotenv import dotenv_values

config = dotenv_values(".env")

SQLALCHEMY_DATABASE_URI = f"mysql+mysqldb://{config['DB_USER']}:{config['DB_PASSWORD']}@{config['DB_HOST']}/{config['DB_NAME']}?charset=utf8mb4"
FORMAT_STRING_DATETIME = '%Y/%m/%d, %H:%M:%S'
