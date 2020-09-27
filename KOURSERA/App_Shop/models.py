from django.db import models
import uuid



def autoslug():
    return str(uuid.uuid4())


class Category(models.Model):
    title   = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    category      = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="category")
    mainimage     = models.ImageField(upload_to="Thumnail")
    name          = models.CharField(max_length=254)
    slug          = models.SlugField(max_length=255,default=autoslug)
    preview_text  = models.TextField(max_length=200,verbose_name="Preview Text")
    detail_text   = models.TextField(max_length=1000,verbose_name="Description")
    author        = models.CharField(max_length=200)
    video_content = models.FileField(upload_to="courses")
    price         = models.FloatField()
    old_price     = models.FloatField(default=0.00)
    created       = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "COURSE NAME : {} -- AUTHOR : {}".format(self.name,self.author)

    class Meta:
        ordering = ['-created']

        


