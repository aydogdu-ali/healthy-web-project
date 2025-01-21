from django.db import models

from django.contrib.auth.models import AbstractUser

#kendi user modelimizi oluşturduk ve mail ile girişi sağlıyoruz.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, null=True, blank=True)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        email_username, _ = self.email.split("@")
        if self.username=="" or self.username ==None:
        #if not username(yukarıdaki kodla aynı)    
            self.username = email_username
        super(User, self).save(*args, **kwargs)


