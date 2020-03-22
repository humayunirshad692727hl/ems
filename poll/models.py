from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Question(models.Model):
    title=models.TextField(null=True,blank=True)
    status=models.CharField(default='inactive',max_length=50)
    created_by=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    start_date=models.DateTimeField(null=True,blank=True)
    end_date=models.DateTimeField(null=True,blank=True)
    @property
    def all_choice(self):
        return self.choice_set.all()

    def __str__(self):
        return self.title
class Choice(models.Model):
    question=models.ForeignKey('poll.Question',on_delete=models.CASCADE)
    text=models.TextField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.text
    def votes(self):
        return self.answer_set.count()
class Answer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    choice=models.ForeignKey(Choice,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.user.first_name + '-' + self.user.last_name

    


