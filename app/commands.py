import click
from flask.cli import with_appcontext
from .models import db, User, StudentProfile
from . import bcrypt
import os

@click.command('init-db')
@with_appcontext
def init_db():
    """Create all database tables."""
    db.create_all()
    click.echo("Database tables created!")

@click.command('seed-questions')
@with_appcontext
def seed_questions_cmd():
    """Seed assessment questions."""
    from seed_questions import seed_questions
    seed_questions()
    click.echo("Questions seeded!")

@click.command('create-admin')
@click.option('--uai_id', prompt='Admin UAi ID', help='UAi ID for the admin user.')
@click.option('--name', prompt='Admin Name', help='Full name of the admin user.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Password for the admin user.')
@with_appcontext
def create_admin(uai_id, name, password):
    """Create an admin user."""
    if User.query.filter_by(uai_id=uai_id).first():
        click.echo("Error: User with this UAi ID already exists.")
        return
    
    user = User(uai_id=uai_id, name=name, role='admin')
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    click.echo(f"Admin user {name} created successfully!")

@click.command('reset-db')
@with_appcontext
def reset_db():
    """Drop and recreate all database tables (DEV ONLY)."""
    if click.confirm('This will delete all data. Are you sure?', abort=True):
        db.drop_all()
        db.create_all()
        click.echo("Database reset successfully!")

def register_commands(app):
    app.cli.add_command(init_db)
    app.cli.add_command(seed_questions_cmd)
    app.cli.add_command(create_admin)
    app.cli.add_command(reset_db)
