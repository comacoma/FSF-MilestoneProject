from django.test import TestCase
from blog.templatetags import helper

"""
To test if helper template filters behave as expected
"""
class TestHelpers(TestCase):
    def test_helper(self):
        expected = helper.splitpart('original string', 0, ' ')
        self.assertEquals(expected, 'original')
