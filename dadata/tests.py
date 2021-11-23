# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from django.contrib.auth import authenticate
# from datetime import date, timedelta
# from .models import Address
# from collections import OrderedDict

# class AddressTest(TestCase):

#     def setUp(self):
#         self.user = get_user_model().objects.create_user(username='test_address', password='123test123')
#         self.user.save()
#         self.timestamp = date.today()
#         self.address = Address(author=self.user, address='Карла Маркса проспект, 20', date=self.timestamp + timedelta(days=1))
#         self.address.save()

#     def tearDown(self):
#         self.user.delete()

#     def test_read_address(self):
#         self.assertEqual(self.address.author, self.user)
#         self.assertEqual(self.address.address, 'Карла Маркса проспект, 20')
#         self.assertEqual(self.address.date, self.timestamp + timedelta(days=1))

#     def test_update_address_address(self):
#         self.address.address = '​Немировича-Данченко, 138'
#         self.address.save()
#         self.assertEqual(self.address.address, '​Немировича-Данченко, 138')

#     def test_update_address_date(self):
#         self.address.date = self.timestamp + timedelta(days=2)
#         self.address.save()
#         self.assertEqual(self.address.date, self.timestamp + timedelta(days=2))

