from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


User = settings.AUTH_USER_MODEL

class Season(models.Model):
    season_name = models.CharField(max_length=255, null=True, blank=False)

    def __str__(self):
        return f'{self.season_name}'


class Year(models.Model):
    album_year = models.IntegerField(
        validators=[MinValueValidator(1990), MaxValueValidator(2024)], default=2024
    )
    def __str__(self):
        return f'{self.album_year}'
    
    class Meta:
        ordering = ['-album_year']


class Album(models.Model):
    album_name = models.CharField(max_length=255, null=True)
    album_owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    season_name = models.ForeignKey(Season, on_delete=models.CASCADE, null=True)
    album_year = models.ForeignKey(Year, on_delete=models.CASCADE, null=True)
    album_created = models.DateTimeField(auto_now_add=True, null=True)
    hidden = models.BooleanField(blank=True, null=True, default=False)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')

    def __str__(self):
        return f'{self.album_name}, {self.season_name}, {self.album_created.date()}'
    
    class Meta:
        ordering = ['-album_created']

# from django.db.models.signals import post_save, pre_save
# from django.core.mail import send_mail

# def save_album(sender, instance, **kwargs):
#     email = 'album owner'
#     subject = 'Album created'
#     message = f"Album successfully created, check it here https://deki90to.pythonanywhere.com/"
#     print(sender.objects.all)

#     send_mail(
#         subject,
#         message,
#         email,
#         ['deki90to@gmail.com']
#     )
# pre_save.connect(save_album, sender=Album)
# post_save.connect(save_album, sender=Album)

class Images(models.Model):
    images = models.ImageField(upload_to='images/')
    album_images = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=False)

    def __str__(self):
        return f'{self.album_images}'


class Comment(models.Model):
    comment = models.CharField(max_length=1000, null=True, blank=False)
    commented_album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=False)
    comment_owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    comment_created = models.DateTimeField(auto_now_add=True, null=True, blank=False)
    
    def __str__(self):
        return f'{self.comment_owner}, {self.comment}, {self.commented_album}, {self.comment_created.date()}'
    
    class Meta:
        ordering = ['-comment_created']


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    liked_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.album}/{self.liked_on}'