from django.db import models

from utils.models import TimeStampAbstractModel
# from allauth.account import models
# models


class News(TimeStampAbstractModel):
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ('-created_at',)

    title = models.CharField(max_length=150, verbose_name='название')
    image = models.ImageField(upload_to='newsImages/', verbose_name='обложка')
    description = models.CharField(max_length=250, verbose_name='Краткое описание')
    content = models.TextField(verbose_name='контент',)
    date = models.DateTimeField(verbose_name='дата добавление', auto_now_add=True)

    def __str__(self):
        return f'{self.title} - {self.date}'


class Photo(TimeStampAbstractModel):
    class Meta:
        verbose_name = 'фотография'
        verbose_name_plural = 'фотографии'
        ordering = ('-created_at',)


    image = models.ImageField(upload_to='galleryImages/', verbose_name='фотография')
    photo_cat = models.ForeignKey('core.PhotoCategory', on_delete=models.CASCADE, verbose_name='категории фотографии')

    def __str__(self):
        return f'{self.created_at}'


class PhotoCategory(TimeStampAbstractModel):
    class Meta:
        verbose_name = 'фото категория'
        verbose_name_plural = 'фото категории'

    name = models.CharField(max_length=150, verbose_name='название',)

    def __str__(self):
        return self.name


class Event(TimeStampAbstractModel):
    class Meta:
        verbose_name = 'событие'
        verbose_name_plural = 'события'
        ordering = ('-created_at',)

    name = models.CharField(max_length=200, verbose_name='название',)
    description = models.CharField(max_length=400, verbose_name='описание',)
    image = models.ImageField(upload_to='eventImages/', verbose_name='фотография')

    def __str__(self):
        return f'{self.name} - {self.created_at}'


class Genre(TimeStampAbstractModel):

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    name = models.CharField(max_length=100, verbose_name='название')

    def __str__(self):
        return f'{self.name}'


class Repertoire(TimeStampAbstractModel):
    class Meta:
        verbose_name = 'репертуар'
        verbose_name_plural = 'репертуары'
        ordering = ('-created_at',)

    name = models.CharField(max_length=200, verbose_name='название',)
    description = models.CharField(max_length=400, verbose_name='описание',)
    genres = models.ManyToManyField('core.Genre', verbose_name='жанры', related_name='кepertoire')
    





