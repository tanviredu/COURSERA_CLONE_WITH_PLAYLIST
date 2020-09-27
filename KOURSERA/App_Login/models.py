from django.db import models
from django.utils.translation import ugettext_lazy
from django.contrib.auth.models import BaseUserManager    ## for creating customize user manager
from django.contrib.auth.models import AbstractBaseUser   ## creating User model
from django.contrib.auth.models import PermissionsMixin   ## controlls the permission


from django.db.models.signals import post_save
from django.dispatch import receiver

class MyUserManager(BaseUserManager):
    ''' Create A Custom functionality That Handles '''
    ''' default User differently                   '''
    ''' only use the email and password the username  '''
    ''' username will be replaced by email'''

    def _create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError("Email is not set")
        
        email = self.normalize_email(email)
        user  = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user 

    def create_superuser(self,email,password,**extra_fields):
        ''' Super user settings '''
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        ## raise error if not exists
        if extra_fields.get('is_staff') is not True:
            raise ValueError("SUPERUSER MUST BE STAFF")
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("YOU HAVE TO BE A SUPER USER")

        return self._create_user(email,password,**extra_fields)


class User(AbstractBaseUser,PermissionsMixin):
    '''Making Custom User without replacing 
    username with email '''

    email     = models.EmailField(unique=True)
    is_staff  = models.BooleanField(ugettext_lazy("STAFF STATUS"),default=False,help_text=("DETERMINE IF YOU ARE ELIGIBLE FOR ENTERING ADMIN PANEL"))
    is_active = models.BooleanField(ugettext_lazy("ACTIVE"),default=True,help_text=("DETERMINE IF YOU ARE ACTIVE USER")) 
    
    ## email will be counted as a username field
    USERNAME_FIELD = 'email'

    ## leverage the custom user two method 
    ## with user.objects.method() like fashion
    objects = MyUserManager()

    def __str__(self):
        return self.email 
    
    def get_full_name(self):
        return self.email 
    
    def get_short_name(self):
        return self.email



class Profile(models.Model):
    """profile table for additional information  needed for the payment gateway"""

    user        = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    username    = models.CharField(max_length=204,blank=True)
    full_name   = models.CharField(max_length=204,blank=True)
    address_1   = models.TextField(max_length=300,blank=True)
    city        = models.CharField(max_length=40,blank=True)
    zipcode     = models.CharField(max_length=40,blank=True)
    country     = models.CharField(max_length=20,blank=True)
    phone       = models.CharField(max_length=20,blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


    def is_fully_filled(self):
        ''' check if all the field is fully filled '''

        fields_name = [f.name for f in self._meta.get_fields()] ## return all the fields name

        for field_name  in fields_name:
            value = getattr(self,field_name)
            if value is None or value == "":
                return False 
        return True 

class Video_Content(models.Model):
    user       = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_content")
    video_slug = models.SlugField(max_length=400) 

    def __str__(self):
        return str(self.user)




@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    ''' AFTER USER IS SUCCESSFULLY SAVED IN THE USER MODEL '''
    ''' THIS FUNCTION WILL CATCH THE INSTANCE AND CREATE PROFILE'''
    ''' WITH THE USER INSTANCE '''
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save,sender=User)
def save_profile(sender,instance,**kwargs):
    ''' TAKE THE USER INSTANCE CALL THE PROFILE USING RELATED NAME '''
    ''' THEN SAVE THE PROFILE'''
    instance.profile.save()


