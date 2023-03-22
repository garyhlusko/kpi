import os

DATABASES = {
    'default': {
        'ENGINE': 'clients.postgresql_backend',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST':os.getenv("DB_HOST"),
    }
}