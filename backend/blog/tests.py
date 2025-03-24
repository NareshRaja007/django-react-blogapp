
from django.test import TestCase
from .models import *

class UserDetailsModelTest(TestCase):
    def setUp(self):
        """
        This method runs before every test method.
        It creates a test user that we can use in our test cases.
        """
        self.user = UserDetails.objects.create(
            user_id="user123",
            name="Test User",
            contact_number="9876543210",
            password="securepassword"
        )

    def test_user_creation(self):
        """Test if a user is created successfully"""
        self.assertEqual(self.user.user_id, "user123")  
        self.assertEqual(self.user.name, "Test User") 
        self.assertEqual(self.user.contact_number, "9876543210")  
        self.assertTrue(self.user.is_authenticated) 

    def test_user_string_representation(self):
        """Test if the string representation of the user is the user's name"""
        self.assertEqual(str(self.user), "Test User")



class BlogPostModelTest(TestCase):
    def setUp(self):
        """Set up test data before each test runs"""
        self.user = UserDetails.objects.create(
            user_id="user123",
            name="Test User",
            contact_number="9876543210",
            password="testpassword"
        )
        self.blog_post = BlogPost.objects.create(
            user=self.user,
            title="Test Blog Post",
            content="This is a test blog post.",
            created_by="Test User"
        )

    def test_blog_post_creation(self):
        """Test if the blog post is created successfully"""
        post = BlogPost.objects.get(title="Test Blog Post")
        self.assertEqual(post.content, "This is a test blog post.")
        self.assertEqual(post.created_by, "Test User")
        self.assertEqual(post.user, self.user)

    def test_blog_post_string_representation(self):
        """Test the string representation of the blog post"""
        self.assertEqual(str(self.blog_post), "Test Blog Post")

    def test_blog_post_update(self):
        """Test updating a blog post"""
        self.blog_post.title = "Updated Blog Post"
        self.blog_post.content = "This content has been updated."
        self.blog_post.save()

        updated_post = BlogPost.objects.get(id=self.blog_post.id)
        self.assertEqual(updated_post.title, "Updated Blog Post")
        self.assertEqual(updated_post.content, "This content has been updated.")

    def test_blog_post_delete(self):
        """Test deleting a blog post"""
        post_id = self.blog_post.id
        self.blog_post.delete()

        with self.assertRaises(BlogPost.DoesNotExist):
            BlogPost.objects.get(id=post_id)