import unittest
from flask import url_for
from app import create_app, db, bcrypt
from app.models import User, Task
from app.tasks.forms import TaskForm



class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_password_hashing(self):
        hashed_pw = bcrypt.generate_password_hash('mypassword')
        self.assertFalse(bcrypt.check_password_hash(hashed_pw, 'testing'))
        self.assertTrue(bcrypt.check_password_hash(hashed_pw, 'mypassword'))

    def test_user(self):
        with self.app.app_context():
            u = User(username='fabian', email='fabian@gmail.com', password= bcrypt.generate_password_hash('mypassword'))
            db.session.add(u)
            db.session.commit()

            saved_user = User.query.filter_by(username='fabian').first()
            self.assertIsNotNone(saved_user)  
            self.assertEqual(saved_user.username, 'fabian')
            self.assertEqual(saved_user.email, 'fabian@gmail.com')
            self.assertTrue(bcrypt.check_password_hash(saved_user.password, 'mypassword'))

    def test_add_task(self):
        with self.app.app_context():
            u = User(username='fabian', email='fabian@gmail.com', password= bcrypt.generate_password_hash('mypassword'))

            db.session.add(u)
            db.session.commit()

            task = Task(title='Introduction to Flask', description='Learning the basics of Flask',resources='www.flask.com', user_id=u.id)

            db.session.add(task)
            db.session.commit()

            saved_task = Task.query.filter_by(title='Introduction to Flask').first()

            self.assertIsNotNone(saved_task)
            self.assertEqual(saved_task.title, 'Introduction to Flask')
            self.assertEqual(saved_task.description, 'Learning the basics of Flask')
            self.assertEqual(saved_task.resources, 'www.flask.com')
            self.assertEqual(saved_task.user_id, u.id)


    def test_delete_task(self):
        with self.app.app_context():
            u = User(username='fabian', email='fabian@gmail.com', password= bcrypt.generate_password_hash('mypassword'))

            db.session.add(u)
            db.session.commit()

            task = Task(title='Introduction to Flask', description='Learning the basics of Flask',resources='www.flask.com', user_id=u.id)

            db.session.add(task)
            db.session.commit()

            saved_task = Task.query.filter_by(title='Introduction to Flask').first()

            db.session.delete(task)

            self.assertIsNotNone(saved_task)


if __name__ == '__main__':
    unittest.main()

        