from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_ECHO'] = True

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Tests for model for User"""

    def setUp(self):
        """Clean up if table already exists"""

        User.query.delete()

    def tearDown(self):
        """Clean up any errored attempt"""

        db.session.rollback()
    
    def test_whole_name(self):
        """Test that whole_name will display"""

        user = User(first_name="Test", last_name="User")
        self.assertEqual(user.whole_name(), "Test User")