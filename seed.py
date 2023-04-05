
from models import db, User, Post
from app import app

db.drop_all()
db.create_all()

# User
john = User(first_name='John', last_name='Smith')
mary = User(first_name='Mary', last_name='Sue')
colt = User(first_name='Colt', last_name='Salas')
olivia = User(first_name='Olivia', last_name='Lee')

db.session.add_all([john, mary, colt, olivia])
db.session.commit()

# Post
j1 = Post(title='John''s first post!', content='Its my first post!', user_id=1)
j2 = Post(title='Python is cool', content='Love python!', user_id=1)
j3 = Post(title='Flask', content='Flask is amazing!', user_id=1)
m1 = Post(title='Mary''s 1st post!', content='The very first!', user_id=2)
m2 = Post(title='Vacation', content='I love the beach!', user_id=2)
c1 = Post(title='Coding', content='Python is an esscential language!', user_id=3)

db.session.add_all([j1, j2, j3, m1, m2, c1])
db.session.commit()