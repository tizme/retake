from __future__ import unicode_literals
import bcrypt, re
from django.db import models
import datetime
# Create your models here.
class UserManager(models.Manager):
    def login(self, postData):
        error_msgs = []
        password = bcrypt.hashpw(postData['pass'].encode(), bcrypt.gensalt())

        try:
            user = User.objects.get(email=postData['email'])
        except:
            error_msgs.append("Invalid user!")
            return {'errors':error_msgs}

        if not bcrypt.hashpw(postData['pass'].encode(), user.password.encode()) == user.password.encode():
            error_msgs.append("Wrong Password!")

        if error_msgs:
            return {'errors':error_msgs}
        else:
            return {'theuser':user.name, 'userid':user.id}

    def register(self, postData):
        error_msgs = []
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        try:
            if User.objects.get(email=postData['email']):
                error_msgs.append("Email already in use!")
        except:
            pass

        if len(postData['name']) < 2:
            error_msgs.append("Invalid Name")

        if not email_regex.match(postData['email']):
            error_msgs.append("Invalid email!")

        if len(postData['pass']) < 8:
            error_msgs.append("Invalid Password!")

        if not postData['pass'] == postData['pass_conf']:
            error_msgs.append("Invalid Password!")


        if postData['dob'] == '':
            error_msgs.append('enter a valid birthday')

        if error_msgs:
            return {'errors':error_msgs}
        else:
            dob = postData['dob']
            # dob = datetime.datetime.strptime(postData['dob'], '%Y-%m-%d')
            hashed = bcrypt.hashpw(postData['pass'].encode(), bcrypt.gensalt())
            user = User.objects.create(email=postData['email'],name=postData['name'], alias=postData['alias'], password=hashed, dob=dob)
            return {'theuser':user.name, 'userid': user.id}

class User(models.Model):
    email = models.CharField(max_length=255)
    name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    dob = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class QuoteManager(models.Manager):
    def add(self,postData, userid):
        error_msgs = []
        if len(postData['author']) < 3:
            error_msgs.append('Quoted Author name not valid')
        if len(postData['quote']) < 10:
            error_msgs.append('Quote is not valid')
        user = {'user': User.objects.get(id=userid)}
        if error_msgs:
            return {'errors':error_msgs}
        else:
            quote = Quote.objects.create(quote=postData['quote'], author=postData['author'], posted=user['user'])
            return{'quote' :quote.quote}

class Quote(models.Model):
    quote = models.TextField()
    author = models.CharField(max_length=50)
    posted = models.ForeignKey(User, related_name='poster')
    favorite = models.ManyToManyField(User, related_name='fav')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()
