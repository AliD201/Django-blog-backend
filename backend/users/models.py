from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.

class Profile (models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default ='default.jpg', upload_to='profile_pics')


    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        # call the old save
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300 :
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class MyLog(models.Model):
    LOG_ACTIONS = (
        ('login', 'User login'),
        ('delete_object', 'User delete object'),
        ('create_object', 'User create object'),
        ('edit_object', 'User edit object'),
 
    )
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    action = models.CharField(max_length=20, default='login', choices=LOG_ACTIONS, verbose_name= 'action')
    date = models.DateTimeField(auto_now_add=True, verbose_name='date')
    description = models.CharField(max_length=120)

    def __str__(self):
        return f'{self.user.username} {self.action}: {self.description}'
    class Meta:
        ordering = ['-date']
        verbose_name = 'Action log'
        verbose_name_plural = 'Actions log'