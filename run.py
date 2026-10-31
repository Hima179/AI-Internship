import os
from app import create_app, db
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()

env = os.environ.get('FLASK_ENV', 'development')
app = create_app(env)
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run()
