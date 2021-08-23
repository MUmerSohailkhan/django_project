from django.contrib.auth.models import User
from blog.models import post

user2=User.objects.first()

print(user2)
