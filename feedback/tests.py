# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from .models import Restaurant, Review
# from .forms import ReviewForm

# User = get_user_model()

# class ReviewSubmissionTest(TestCase):
#     def setUp(self):
#         # Create a test user
#         self.user = User.objects.create_user(username='testuser', password='testpassword')
#         self.user.is_user = True
#         self.user.save()

#         # Create a test restaurant
#         self.restaurant = Restaurant.objects.create(
#             name='Test Restaurant',
#             street_address='123 Test St',
#             city='Testville',
#             state='TS',
#             lat=0.0,
#             lng=0.0
#         )

#     def test_review_submission(self):
#         # Log in the test user
#         self.client.login(username='testuser', password='testpassword')

#         # Simulate a GET request to the restaurant detail page
#         response = self.client.get(f'/feedback/restaurant/{self.restaurant.id}/')

#         # Check if the ReviewForm is present in the context
#         self.assertIn('review_form', response.context)

#         # Simulate a POST request to submit a review
#         form_data = {
#             'content': 'This is a test review content',
#             'rating': 4 
#         }

#         response = self.client.post(f'/feedback/restaurant/{self.restaurant.id}/', form_data)

#         # Check if the review is created in the database
#         self.assertEqual(Review.objects.count(), 1)

#         # Check the review details
#         review = Review.objects.first()
#         self.assertEqual(review.content, 'This is a test review content')
#         self.assertEqual(review.rating, 4)  # You should adjust this value as needed
#         self.assertEqual(review.user, self.user)
#         self.assertEqual(review.restaurant, self.restaurant)
#         self.assertFalse(review.approved)  # Assuming reviews are not approved by default

#     def tearDown(self):
#         # Clean up after the test
#         self.client.logout()
#         User.objects.all().delete()
#         Restaurant.objects.all().delete()
#         Review.objects.all().delete()
