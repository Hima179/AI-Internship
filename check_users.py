from app import create_app, db
from app.models import User

app = create_app('development')
with app.app_context():
    users = User.query.all()
    for user in users:
        print(f"ID: {user.id}, UAI: {user.uai_id}, Role: {user.role}")
