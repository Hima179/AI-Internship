from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
bcrypt = Bcrypt()
migrate = Migrate()
csrf = CSRFProtect()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Register blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .student import student as student_blueprint
    app.register_blueprint(student_blueprint, url_prefix='/student')

    from .counsellor import counsellor as counsellor_blueprint
    app.register_blueprint(counsellor_blueprint, url_prefix='/counsellor')

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .faculty import faculty as faculty_blueprint
    app.register_blueprint(faculty_blueprint, url_prefix='/faculty')

    # Default route
    @app.route('/')
    def index():
        return render_template('welcome.html')

    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return "404 Error: Page Not Found", 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return "500 Error: Internal Server Error", 500

    # Register commands
    from .commands import register_commands
    register_commands(app)

    return app
