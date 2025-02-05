import click, sys
from models import db, User, Todo
from app import app
from sqlalchemy.exc import IntegrityError

@app.cli.command("init", help="Creates and initializes the database")
def initialize():
  db.drop_all()
  db.create_all()
  bob = User('bob', 'bob@mail.com', 'bobpass')

  bob.todos.append(Todo('wash car'))

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

@app.cli.command("get-todos")
@click.argument('username', default='bob')
def get_user_todos(username):
  user = User.query.filter_by(username=username).first()
  if not user:
    print(f'{username} not found')
    return
  print(user.todos)

@app.cli.command("add-todo")
@click.argument('username', default='bob')
@click.argument('text', default='wash car')
def add_task(username, text):
  user = User.query.filter_by(username=username).first()
  if not user:
    print(f'{username} not found')
    return
  newTodo = Todo(text)
  user.todos.append(newTodo)
  db.session.add(user)
  db.session.commit()

@app.cli.command("toggle-todo")
@click.argument('username', default='bob')
@click.argument('todo_id', default=1)
def toggle_todo_command(todo_id, username):
  user = User.query.filter_by(username=username).first()
  if not user:
    print(f'{username} not found')
    return
  
  todo = Todo.query.filter_by(id=todo_id,userId=user.id).first()
  if not todo:
    print(f'{username} has no todo id {todo_id}')
    return

  todo.toggle()
  print(f'{todo.text} is {"done" if todo.done else "not done"}!')


@app.cli.command("add-category", help="Adds a category to a todo")
@click.argument('username', default='bob')
@click.argument('todo_id', default=6)
@click.argument('category', default='chores')
def add_todo_category_command(username, todo_id, category):
  user = User.query.filter_by(username=username).first()
  if not user:
    print(f'{username} not found')
    return

  res = user.add_todo_category(todo_id, category)
  if not res:
    print(f'{username} has no todo id {todo_id}')
    return

  print('Category added!')