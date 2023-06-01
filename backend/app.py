from flask import Flask
from routes import users, songs
from extensions import (
    bcrypt,
    db,
    migrate,
    guard, 
    cors
)
from models.User import User

def create_app(config_object="config"):
  app = Flask(__name__)
  app.config.from_object(config_object)
  with app.app_context():
    bcrypt.init_app(app)
    guard.init_app(app, User)
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
  return app

app = create_app()

app.register_blueprint(users, url_prefix="/users")
app.register_blueprint(songs, url_prefix="/songs")

from models.User import User

if __name__ == '__main__':
    app.run(debug=True)

