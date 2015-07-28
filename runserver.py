#this cannot be called app. for some unknown reason, it breaks wsgi and ngnix
from flasksite import app as application

if __name__ == "__main__":
    application.run(debug=True)
