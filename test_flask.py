from unittest import TestCase

from app import app
from models import db, User, Post, DEFAULT_IMAGE_URL

# Use a test database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_test'
app.config['SQLALCHEMY_ECHO'] = False

# Generate real errors rather than HTML error pages
app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class FlaskTests(TestCase):
    '''Test flask app's routes'''

    def setUp(self):
        '''Add sample user'''

        Post.query.delete()
        User.query.delete()

        user = User(first_name='Ftest', last_name='Ltest')
        db.session.add(user)
        db.session.commit()

        post = Post(title='Ftest''s test post!', content='Its just a test post', user_id=user.id)
        db.session.add(post)
        db.session.commit()

        self.user_id = user.id
        self.post_id = post.id


    
    def tearDown(self):
        '''Clean up any transactions'''
        db.session.rollback()

    def test_homepage(self):
        '''Test / route content'''
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('By Ftest Ltest', html)

    def test_users_page(self):
        '''Test /user route content'''
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Ftest Ltest', html)

    def test_newUser(self):
        '''Test /user/new route content, through GET method'''
        with app.test_client() as client:
            resp = client.get('/users/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Create a user', html)

    def test_do_newUser(self):
        '''Test /user/new route content, through POST method'''
        with app.test_client() as client:
            d = {'first':'Fnew', 'last':'Lnew', 'image':f'{DEFAULT_IMAGE_URL}'}

            resp = client.post('/users/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Fnew Lnew', html)

    def test_userDetails(self):
        '''Test /users/<int:user_id> route content'''
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(DEFAULT_IMAGE_URL, html)
            self.assertIn('Ftest Ltest', html)
            self.assertIn('<h3>Posts</h3>', html)

    def test_editUser(self):
        '''Test /users/<int:user_id>/edit route content, through GET method'''
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}/edit')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<input type="text" class="form-control" name="first" value="Ftest">', html)
            self.assertIn('<input type="text" class="form-control" name="last" value="Ltest">', html)
            self.assertIn(f'<input type="text" class="form-control" name="image" value="{DEFAULT_IMAGE_URL}">', html)
            
    def test_do_editUser(self):
        '''Test /users/<int:user_id>/edit route content, through POST method'''
        with app.test_client() as client:
            d = {'first':'Fedit', 'last':'Ledit', 'image':f'{DEFAULT_IMAGE_URL}'}

            resp = client.post(f'/users/{self.user_id}/edit', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Fedit Ledit', html)

    def test_do_deleteUser(self):
        '''Test /users/<int:user_id>/delete route content, through POST method'''
        with app.test_client() as client:

            resp = client.post(f'/users/{self.user_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            # Check that the Users page has loaded, but no user exists in the displayed list
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Users', html)
            self.assertIn('<ul>', html)
            self.assertNotIn('<li>', html)

    def test_newPost(self):
        '''Test /users/<int:user_id>/posts/new'''
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}/posts/new')
            html = resp.get_data(as_text=True)
                
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Add Post for', html)

    def test_do_newPost(self):
        '''Test /users/<int:user_id>/posts/new' route content, through POST method'''
        with app.test_client() as client:
            d={'title': 'New Title', 'content': 'Some Content', 'user_id':f'self.user_id'}

            resp = client.post(f'/users/{self.user_id}/posts/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            print(html)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<title>User</title>', html)
            self.assertIn('Ftest''s test post!', html)
            self.assertIn('New Title', html)

    def test_show_post(self):
        '''Test /posts/<int:post_id>'''
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}')
            html = resp.get_data(as_text=True)
                
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<title>Post Details</title>', html)
            self.assertIn('Ftest''s test post!', html)
            self.assertIn('Its just a test post', html)

    def test_editPost(self):
        '''Test /posts/<int:post_id>/edit'''
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}/edit')
            html = resp.get_data(as_text=True)
                
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Edit Post</h1>', html)
            self.assertIn('Title</label>', html)
            self.assertIn('Ftest''s test post!', html)
            self.assertIn('Post Content</label>', html)
            self.assertIn('Its just a test post', html)

    def test_do_editPost(self):
        '''Test /posts/<int:post_id>/edit' route content, through POST method'''
        with app.test_client() as client:
            d = {'title':'Edited Title', 'content':'Changed Content'}
            resp = client.post(f'/posts/{self.post_id}/edit', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            print(html)
                
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<title>Post Details</title>', html)
            self.assertIn('<h1>Edited Title</h1>', html)
            self.assertIn('<p>Changed Content</p>', html)
    
    def test_do_deletePost(self):
        '''Test /posts/<int:post_id>/delete' route content, through POST method'''
        with app.test_client() as client:

            resp = client.post(f'/posts/{self.post_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            # Check that the Profile page has loaded, but the post no longer exists in the displayed list
            self.assertEqual(resp.status_code, 200)
            self.assertIn(DEFAULT_IMAGE_URL, html)
            self.assertIn('Ftest Ltest', html)
            self.assertIn('<h3>Posts</h3>', html)
            self.assertIn('<ul>', html)
            self.assertNotIn('<li>', html)

    def test_page_err_404(self):
        '''Test the 404 page'''
        with app.test_client() as client:
            resp = client.get('/zzz-not-a-real-page')
            html = resp.get_data(as_text=True)
                
            self.assertEqual(resp.status_code, 404)
            self.assertIn('<h1>404 - Page Not Found</h1>', html)