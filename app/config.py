import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cb8b70ee8ac37bd671027cac0af82b49'
