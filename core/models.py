from django.db import models

from utils.models import TimeStampAbstractModel


class News(TimeStampAbstractModel):
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    title = models.CharField(max_length=150, verbose_name='название')
    image = models.ImageField(upload_to='news_images/', verbose_name='обложка')
    description = models.CharField(max_length=250, verbose_name='Краткое описание')
    content = models.TextField(verbose_name='контент',)
    date = models.DateTimeField(verbose_name='дата добавление', auto_now_add=True)

    def __str__(self):
        return f'{self.title} - {self.date}'


class Photo(TimeStampAbstractModel):
    class Meta:
        verbose_name = 'фотография'
        verbose_name_plural = 'фотографии'

    image = models.ImageField(upload_to='gallery_images/', verbose_name='фотография')
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