
from models import db, User, Post, PostTag, Tag
from app import app

db.drop_all()
db.create_all()

# User
u1 = User(first_name='John', last_name='Smith')
u2 = User(first_name='Mary', last_name='Sue')
u3 = User(first_name='Colt', last_name='Salas')
u4 = User(first_name='Olivia', last_name='Lee')

db.session.add_all([u1, u2, u3, u4])
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

# Tags
t1 = Tag(name='Coding')
t2 = Tag(name='Python')
t3 = Tag(name='Flask')
t4 = Tag(name='Vacation')
t5 = Tag(name='Beach')
t6 = Tag(name='Excited')

db.session.add_all([t1, t2, t3, t4, t5, t6])
db.session.commit()

# Posts-Tags
pt1 = PostTag(post_id='1', tag_id='6')
pt2 = PostTag(post_id='2', tag_id='1')
pt3 = PostTag(post_id='2', tag_id='2')
pt4 = PostTag(post_id='3', tag_id='1')
pt5 = PostTag(post_id='3', tag_id='3')
pt6 = PostTag(post_id='3', tag_id='6')
pt7 = PostTag(post_id='4', tag_id='6')
pt8 = PostTag(post_id='5', tag_id='4')
pt9 = PostTag(post_id='5', tag_id='5')
pt10 = PostTag(post_id='6', tag_id='1')
pt11 = PostTag(post_id='6', tag_id='2')

db.session.add_all([pt1, pt2, pt3, pt4, pt5, pt6, pt7, pt8, pt9, pt10, pt11])
db.session.commit()