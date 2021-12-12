from django.test import TestCase
from django.test import Client
from .models import Posts
import json

# https://docs.djangoproject.com/en/4.0/topics/testing/overview/
# https://docs.djangoproject.com/en/3.2/topics/testing/tools/
class BoardTestCase(TestCase):
    # def setUp(self): test initial setting
    # def tearDown(self): test cleanup setting
    databases = {"postgresql"}

    def test_get_posts(self):
        c = Client()
        print(type(json.dumps({"a": 1})))
        res = c.get("/api/board/posts/")
        # print(json.loads(res.content.decode("utf-8")))
        self.assertEqual(res.status_code, 200)
