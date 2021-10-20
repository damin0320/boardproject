from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-q5d-r9cfst_m7*hd-c$_n6$y-qan!mw$*2r=09zz7z-((3!hts'
HASHING_ALGORITHM = 'HS256'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
