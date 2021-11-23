# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from django.contrib.auth import authenticate, login, update_session_auth_hash

# class SigninTest(TestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(username='test', password='123test')
#         self.user.save()
#     def tearDown(self):
#         self.user.delete()
#     def test_correct(self):
#         user = authenticate(username='test', password='123test')
#         self.assertTrue((user is not None) and user.is_authenticated)
#     def test_wrong_username(self):
#         user = authenticate(username='nottest', password='123test')
#         self.assertFalse(user is not None and user.is_authenticated)
#     def test_wrong_pssword(self):
#         user = authenticate(username='test', password='not123test')
#         self.assertFalse(user is not None and user.is_authenticated)

# class TaskTest(TestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(username='test_', password='12test12')
#         self.user.save()
#         self.timestamp = date.today()
#         self.task = Task(user=self.user,
#                          description='description',
#                          due=self.timestamp + timedelta(days=1))
#         self.task.save()
#     def tearDown(self):
#         self.user.delete()
#     def test_read_task(self):
#         self.assertEqual(self.task.user, self.user)
#         self.assertEqual(self.task.description, 'description')
#         self.assertEqual(self.task.due, self.timestamp + timedelta(days=1))
#     def test_update_task_description(self):
#         self.task.description = 'new description'
#         self.task.save()
#         self.assertEqual(self.task.description, 'new description')
#     def test_update_task_due(self):
#         self.task.due = self.timestamp + timedelta(days=2)
#         self.task.save()
#         self.assertEqual(self.task.due, self.timestamp + timedelta(days=2))

# class URLTests(TestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(username='test1', password='123test')
#         self.user.save()

#     def tearDown(self):
#         self.user.delete()
    # def test_correct(self):
    #     user = authenticate(username='test', password='123test')
    #     self.assertTrue((user is not None) and user.is_authenticated)

    # def test_home(self):
    #     user = authenticate(username='test1', password='123test')
    #     if user is not None:

    #         session = self.client.session
    #     response = self.client.get('home')
        
    #     self.assertEqual(response.status_code, 200)