import click, sys
from models import db, User
from app import app
from sqlalchemy.exc import IntegrityError

@app.cli.command("init", help="Creates and initializes the database")
def initialize():
  db.drop_all()
  db.create_all()
  bob = User('bob', 'bob@mail.com', 'bobpass')
  db.session.add(bob)
  db.session.commit()
  print(bob)
  print('database initialized')

@app.cli.command("get-user", help="Retrieves a user")
@click.argument('username', default='bob')
def get_user(username):
  user = User.query.filter_by(username = username).first()
  if not user:
    print(f'{username} not found in database')
    return
  print(user)

@app.cli.command("get-users", help='Gets all users')
def get_users():
  users = User.query.all()
  print(users)

@app.cli.command("change-email")
@click.argument('username', default='bob')
@click.argument('email', default='bob@mail.com')
def change_email(username, email):
  user = User.query.filter_by(username=username).first()
  if not user:
    print(f'{username} not found in database')
    return
  user.email = email
  db.session.add(user)
  db.session.commit()
  print(user)

@app.cli.command("create-user")
@click.argument('username', default='rick')
@click.argument('email', default='rick@mail.com')
@click.argument('password', default='rickpass')
def create_user(username, email, password):
  newUser = User(username, email, password)
  try:
    db.session.add(newUser)
    db.session.commit()
  except IntegrityError as e:
    db.session.rollback()
    print("Username or Email address is already taken")
  else:
    print(newUser)

@app.cli.command("delete-user")
@click.argument('username', default='bob')
def delete_user(username):
  user = User.query.filter_by(username=username).first()
  if not user:
    print(f'{username} not found')
    return
  db.session.delete(user)
  db.session.commit()
  print(f'{username} was deleted')