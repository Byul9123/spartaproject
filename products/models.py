from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/', blank=True)
    author = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='products')
    like_users = models.ManyToManyField('accounts.User', related_name='like_product')
    def __str__(self):
        return self.title
    