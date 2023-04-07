from unittest import TestCase

from app import app
from models import db, User, DEFAULT_IMAGE_URL

# Use a test database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_test'
app.config['SQLALCHEMY_ECHO'] = False

class UserModelTests(TestCase):
    '''Tests for model of Users'''

    # def setUp(self):
    #     '''Clean up any existing users'''
    #      with app.app_context():
    #          User.query.delete()
    
    def tearDown(self):
        '''Clean up any transactions'''
        with app.app_context():
            db.session.rollback()

    def test_full_name(self):
        '''Test the full_name property, ensuring it returns the "first_name last_name" value'''
        with app.app_context():
            user = User(first_name='Colt', last_name='Steele', image_url=DEFAULT_IMAGE_URL)
            self.assertEquals(user.full_name, "Colt Steele")