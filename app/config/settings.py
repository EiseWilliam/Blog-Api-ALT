from decouple import config

ACCESS_TOKEN_EXPIRES_IN = 60
REFRESH_TOKEN_EXPIRES_IN = 20
URI = config("DB_URL", default="mongodb://localhost:27017", cast=str)
JWT_SECRET_KEY = config("JWT_SECRET_KEY", cast=str)   
JWT_REFRESH_SECRET_KEY = config("JWT_SECRET_KEY", cast=str)
ALGORITHM = config("JWT_ALGORITHM", default="HS256", cast=str)
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRES_IN", default=60, cast=int)
REFRESH_TOKEN_EXPIRE_MINUTES = config("REFRESH_TOKEN_EXPIRES_IN", default=20, cast=int)
