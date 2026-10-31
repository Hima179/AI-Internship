import os
import logging
from flask import Flask, redirect, url_for, render_template
from flask_login import LoginManager
from models.user import db, User

# Set up basic logging so we know what's happening
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    
    # Grab secret key from env, fallback to a dev key if not set
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-12345')
    
    # Connecting to local SQLite database as fallback
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///space_spy.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.student_login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        # Import models so SQLAlchemy knows about them before creating tables
        from models import survey
        
        # Make sure our tables exist before we start serving
        db.create_all()
        logger.info("Database tables verified.")

    # Register our blueprints
    from routes.auth import auth_bp
    from routes.survey import survey_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(survey_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)
