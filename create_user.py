from app import create_app, db
from app.models import User, StudentProfile

app = create_app('development')
with app.app_context():
    # Check if user exists
    user = User.query.filter_by(uai_id='himanshu.pathak@universalai.in').first()
    if not user:
        user = User(
            uai_id='himanshu.pathak@universalai.in',
            name='Himanshu Pathak',
            email='himanshu.pathak@universalai.in',
            role='student'
        )
        user.set_password('Mahazan@486828')
        db.session.add(user)
        db.session.commit()
        print(f"Created user: {user.uai_id}")
        
        profile = StudentProfile(user_id=user.id)
        db.session.add(profile)
        db.session.commit()
        print(f"Created student profile for: {user.uai_id}")
    else:
        print(f"User {user.uai_id} already exists")
