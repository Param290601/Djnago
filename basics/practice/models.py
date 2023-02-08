from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User,null=True,blank=True, on_delete=models.CASCADE)
    name = models.CharField(null = "true", max_length=50)
    phone = models.IntegerField(null = "true" ) 
    email = models.EmailField(null = "true")
    forget_password_token = models.CharField(max_length=100,null=True)
    profile = models.ImageField(default="profile.jpg", null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add= True , null=True)

    def __str__(self):
        return self.name
    
class Tags(models.Model):
    name = models.CharField(null = "true", max_length=50)

    def __str__(self):
        return self.name
    
class Product(models.Model):
        CATEGORY = (
        ('Indoor','Indoor'),
        ('Outdoor','Outdoor'),
        )
        name = models.CharField(max_length=100, null=True)
        price = models.FloatField(null=True)
        category = models.CharField(max_length=100, null=True,choices=CATEGORY)
        description = models.CharField(max_length=200 , null=True)
        date_created = models.DateTimeField(auto_now_add= True , null=True)
        def __str__(self):
            return self.name


class Order(models.Model):
    STATUS = (
        ('Pending','Pending'),
        ('Out for deleivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )
    customer = models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)
    product = models.ForeignKey(Product , null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add= True , null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    tags = models.ManyToManyField(Tags)

    # def __str__(self):
    #      return self.product.name


# name = Customer.objects.filter(name = 'Hardik')
# value = Customer.objects.filter(name = 'Hardik').values()
# name = Customer.objects.filter(name__startswith='P')
# print(value)
# print(name)

# class Blog(models.Model):
#     name = models.CharField(max_length=100)
#     tagline = models.TextField()

#     def __str__(self):
#         return self.name

# class Author(models.Model):
#     name = models.CharField(max_length=200)
#     email = models.EmailField()

#     def __str__(self):
#         return self.name

# class Entry(models.Model):
#     blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
#     headline = models.CharField(max_length=255)
#     body_text = models.TextField()
#     pub_date = models.DateField()
#     mod_date = models.DateField(default=date.today)
#     authors = models.ManyToManyField(Author)
#     number_of_comments = models.IntegerField(default=0)
#     number_of_pingbacks = models.IntegerField(default=0)
#     rating = models.IntegerField(default=5)

#     def __str__(self):
#         return self.headline
    

# print(Blog.objects)
# b = Blog(name='Foo', tagline='Bar')
# print(b.objects)

# Blog.objects.filter(entry__authors__name='Lennon')

# for the same modle use F functionss
#  Entry.objects.filter(number_of_comments__gt=F('number_of_pingbacks'))