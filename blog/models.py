"""
Imports for the functionality of the model

"""

from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

STATUS = ((0, "Draft"), (1, "Published"))

"""
Category functions for model

"""


class Category(models.Model):
    title = models.CharField(max_length=250, unique=True)
    category_id = models.IntegerField(default=1, null=False)

    class Meta:
        """ The order of the category by title """
        ordering = ['title']
        """ To set category to plural in admin """
        verbose_name_plural = 'Categories'

    def __str__(self):
        """ To set category with its title """
        return self.title


"""
Post functions for model

"""


class Post(models.Model):
    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    category = models.ForeignKey(Category, related_name='posts', null=True, on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='blog_posts', on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now=True)
    body = models.TextField()
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)

    class Meta:
        """ Ordering of posts by date added """
        ordering = ['-date_added']

    def __str__(self):
        """ Sets post by its name"""
        return self.title

    def number_of_likes(self):
        """ Returns amount of likes """
        return self.likes.count()


"""
Comment functions for model

"""


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        """ Ordering of comments by date added """
        ordering = ['date_added']

    def __str__(self):
        """ Sets comment with name and body of comment """
        return f"Comment {self.body} by {self.name}"
