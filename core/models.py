from django.db import models

from utils.models import TimeStampAbstractModel


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
    content = models.CharField(max_length=400, verbose_name='контент',)
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


class Director(TimeStampAbstractModel):
    class Meta:
        verbose_name = 'режиссер'
        verbose_name_plural = 'режиссеры'

    full_name = models.CharField(max_length=300, verbose_name='ФИО')

    def __str__(self):
        return f'{self.full_name}'


class Actor(TimeStampAbstractModel):
    class Meta:
        verbose_name = 'актер'
        verbose_name_plural = 'актеры'

    full_name = models.CharField(max_length=300, verbose_name='ФИО')

    def __str__(self):
        return f'{self.full_name}'


class Repertoire(TimeStampAbstractModel):
    WAITING = 'waiting'
    CANCELED = 'canceled'
    COMPLETED = 'completed'

    STATUS = (
        (WAITING, 'В ожидание'),
        (CANCELED, 'Отменено'),
        (COMPLETED, 'Завершенный')
    )

    class Meta:
        verbose_name = 'репертуар'
        verbose_name_plural = 'репертуары'
        ordering = ('-created_at',)

    name = models.CharField(max_length=200, verbose_name='название',)
    description = models.CharField(max_length=250, verbose_name='описание',)
    genres = models.ManyToManyField('core.Genre', verbose_name='жанры', related_name='кepertoire')
    duration = models.CharField(max_length=200, verbose_name='длительность',)
    pg = models.CharField(max_length=100, verbose_name='рекомендуется родительское руководство:')
    director = models.ForeignKey('core.Director', on_delete=models.PROTECT, verbose_name='режиссер')
    scriptwriter = models.CharField(max_length=200, verbose_name='автор сценарий',)
    actors = models.ManyToManyField('core.Actor', verbose_name='актеры', related_name='repertoire')
    performance_hall = models.ForeignKey('core.Hall', models.PROTECT, verbose_name='концертный зал')
    image = models.ImageField(upload_to='repertoireImages/', verbose_name='фотография')
    status = models.CharField('статус', choices=STATUS, default=WAITING, max_length=50)

    def __str__(self):
        return f'{self.name} - {self.duration}'


# class PerformanceDay(TimeStampAbstractModel):
#     class Meta:
#         verbose_name = 'день выступления'
#         verbose_name_plural = 'дни выступлений'
#         ordering = ('-created_at',)
#
#     repertoire = models.ForeignKey('core.Repertoire', models.CASCADE,
#                                    'performance_days', verbose_name='репертуар')
#     date = models.DateField(verbose_name='дата')

    # def __str__(self):
    #     return f'{self.date} - {self.repertoire.name}'


class PerformanceSeance(TimeStampAbstractModel):
    class Meta:
        verbose_name = 'сеанс'
        verbose_name_plural = 'сеансы'
        ordering = ('-created_at',)

    time = models.TimeField(verbose_name='время начала')
    date = models.DateField(verbose_name='дата')
    repertoire = models.ForeignKey('core.Repertoire', on_delete=models.CASCADE, related_name='seances',
                                   verbose_name='репертуар')

    def __str__(self):
        return f'{self.time} - {self.date}'


class TicketType(models.Model):
    class Meta:
        verbose_name = 'тип билета'
        verbose_name_plural = 'типы билетов'

    seance = models.ForeignKey('core.PerformanceSeance', models.CASCADE, 'ticket_types',
                               verbose_name='сеанс')
    price = models.IntegerField(verbose_name='цена')
    from_row = models.IntegerField(verbose_name='из ряда:')
    to_row = models.IntegerField(verbose_name='до ряда:')

    def create_tickets(self):
        hall = Hall.objects.get(id=self.seance.repertoire.performance_hall.id)
        row_list = HallRow.objects.filter(number__in=[self.from_row, self.to_row], hall_id=hall.id)
        for row in row_list:
            seats = Seat.objects.filter(row_id=row.id)
            for seat in seats:
                ticket = Ticket.objects.create(seat_number=seat.seat_number, row_number=row.number,
                                               type=self, repertoire_name=self.seance.repertoire.name)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # After saving the HallScheme, create seats based on rows length
        self.create_tickets()

    def __str__(self):
        return f'{self.price}'


class Ticket(models.Model):

    class Meta:
        verbose_name = 'билет'
        verbose_name_plural = 'билеты'

    repertoire_name = models.CharField(max_length=300, verbose_name='название репертуара')
    is_sold = models.BooleanField(default=False, verbose_name='продано?')
    seat_number = models.IntegerField(verbose_name='номер места')
    row_number = models.IntegerField(verbose_name='номер ряда')
    type = models.ForeignKey('core.TicketType', on_delete=models.CASCADE, related_name='tickets',
                             verbose_name='тип билета')

    def __str__(self):
        return f'{self.type.seance} - {self.type.price}'


class Hall(TimeStampAbstractModel):
    class Meta:
        verbose_name = 'зал'
        verbose_name_plural = 'залы'
        ordering = ('-created_at',)

    name = models.CharField(max_length=200, verbose_name='название', unique=True)
    image = models.ImageField(verbose_name='фотография', upload_to='hallImages')

    def __str__(self):
        return self.name


class HallRow(TimeStampAbstractModel):
    class Meta:
        verbose_name = 'ряд'
        verbose_name_plural = 'ряды'
        ordering = ('-created_at',)

    hall_id = models.ForeignKey('core.Hall', models.CASCADE, 'hall_rows', verbose_name='зал')
    length = models.IntegerField(verbose_name='длина ряда')
    number = models.IntegerField(verbose_name='номер ряда')

    def create_seats(self):
        for i in range(1, self.length + 1):
            Seat.objects.create(row_id=self, seat_number=i, row_number=self.number)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # After saving the HallScheme, create seats based on rows length
        self.create_seats()

    def __str__(self):
        return f'{self.hall_id.name}'


class Seat(models.Model):
    class Meta:
        verbose_name = 'место'
        verbose_name_plural = 'места'

    row_id = models.ForeignKey('core.HallRow', models.CASCADE, 'seats', verbose_name='ряд')
    seat_number = models.IntegerField(verbose_name='номер места')
    row_number = models.IntegerField(verbose_name='номер ряда', default=3)

    def __str__(self):
        return f'{self.row_number} - {self.seat_number}'



