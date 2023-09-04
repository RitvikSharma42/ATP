from django.test import TestCase

client = Client()
response = client.post(url, content_type='application/json')