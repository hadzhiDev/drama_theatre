from django.db import models
from django.core.exceptions import ObjectDoesNotExist

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
    performance_hall = models.ForeignKey('core.Hall', models.SET_NULL, verbose_name='концертный зал',
                                         null=True, blank=True)
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
    BLUE = ('blue', 'синий')
    ORANGE = ('orange', 'оранжевый')
    RED = ('red', 'красный')
    PURPLE = ('purple', 'фиолетовый')
    LIGHT_BLUE = ('light_blue', 'голубой')
    PINK = ('pink', 'розовый')
    TURQUOISE = ('turquoise', 'бирюзовый')

    COLORS = (
        BLUE,
        ORANGE,
        RED,
        PURPLE,
        LIGHT_BLUE,
        PINK,
        TURQUOISE,
    )

    class Meta:
        verbose_name = 'тип билета'
        verbose_name_plural = 'типы билетов'

    seance = models.ForeignKey('core.PerformanceSeance', on_delete=models.CASCADE, related_name='ticket_types',
                               verbose_name='сеанс')
    price = models.IntegerField(verbose_name='цена')
    from_row = models.IntegerField(verbose_name='из ряда:')
    to_row = models.IntegerField(verbose_name='до ряда:')
    color = models.CharField(verbose_name='цвет', choices=COLORS, max_length=10)
    hex_code = models.CharField(verbose_name='hex код цвета', max_length=7, blank=True)

    COLOR_TO_HEX = {
        'blue': '0053B5',
        'orange': 'DE6B00',
        'red': 'D30000',
        'purple': '95007D',
        'light_blue': '00B2FF',
        'pink': 'FF00A8',
        'turquoise': '00FFD1',
    }

    # def delete_invalid_tickets(self):
    #     tickets = self.tickets.all()
    #
    #     for ticket in tickets:
    #         try:
    #             # Check if the corresponding HallRow exists
    #             HallRow.objects.get(number=ticket.row_number)
    #         except HallRow.DoesNotExist:
    #             # If HallRow does not exist, delete the ticket
    #             print(f"Deleting ticket with row_number {ticket.row_number}")
    #             ticket.delete()

    def create_tickets(self):
        try:
            hall = Hall.objects.get(id=self.seance.repertoire.performance_hall.id)

            row_numbers = range(self.from_row, self.to_row + 1)
            rows = HallRow.objects.filter(number__in=row_numbers, hall_id=hall.id)

            for ticket in self.tickets.all():
                try:
                    HallRow.objects.get(number=ticket.row_number)
                except HallRow.DoesNotExist:
                    print(f"Deleting ticket with row_number {ticket.row_number}")
                    ticket.delete()

            if not rows.exists():
                raise ValueError(
                    f"No rows found for the given range {self.from_row} to {self.to_row} in hall {hall.id}")

            for row in rows:
                seats = Seat.objects.filter(row_id=row.id)
                self.tickets.filter(seat_number__gt=row.length).delete()
                if not seats.exists():
                    raise ValueError(f"No seats found for row {row.number} in hall {hall.id}")

                for seat in seats:
                    if Ticket.objects.filter(
                        seat_number=seat.seat_number,
                        row_number=row.number,
                        type=self
                    ).exists():
                        continue

                    Ticket.objects.create(
                        seat_number=seat.seat_number,
                        row_number=row.number,
                        type=self,
                        repertoire_name=self.seance.repertoire.name
                    )

        except ObjectDoesNotExist as e:
            raise ValueError(f"Error in creating tickets: {str(e)}")
        except Exception as e:
            raise ValueError(f"An unexpected error occurred: {str(e)}")

    def save(self, *args, **kwargs):
        self.hex_code = self.COLOR_TO_HEX.get(self.color, '')
        super().save(*args, **kwargs)
        self.create_tickets()

    def __str__(self):
        return f'{self.price}'


class Ticket(models.Model):
    class Meta:
        verbose_name = 'билет'
        verbose_name_plural = 'билеты'
        unique_together = (('type', 'row_number', 'seat_number'),)

    repertoire_name = models.CharField(max_length=300, verbose_name='название репертуара')
    is_sold = models.BooleanField(default=False, verbose_name='продано?')
    seat_number = models.IntegerField(verbose_name='номер места')
    row_number = models.IntegerField(verbose_name='номер ряда')
    type = models.ForeignKey('core.TicketType', on_delete=models.CASCADE, related_name='tickets',
                             verbose_name='тип билета')
    seat_id = models.ForeignKey('core.Seat', on_delete=models.PROTECT, related_name='tickets')

    @property
    def price(self):
        return self.type.price

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

    hall = models.ForeignKey('core.Hall', on_delete=models.CASCADE, related_name='rows', verbose_name='зал')
    length = models.IntegerField(verbose_name='длина ряда')
    number = models.IntegerField(verbose_name='номер ряда')

    def create_seats(self):
        existing_seat_numbers = self.seats.values_list('seat_number', flat=True)

        self.seats.filter(seat_number__gt=self.length).delete()

        for i in range(1, self.length + 1):
            if i not in existing_seat_numbers:
                Seat.objects.create(row=self, seat_number=i, row_number=self.number)
        print(existing_seat_numbers.last(), self.length + 1)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # After saving the HallRow, create seats based on row length
        self.create_seats()

    def __str__(self):
        return f'{self.hall.name} - Row {self.number}'


class EmptySpace(TimeStampAbstractModel):
    class Meta:
        verbose_name = 'пустое место'
        verbose_name_plural = 'пустые места'

    from_seat = models.IntegerField(verbose_name='от')
    empty_spots = models.IntegerField(verbose_name='пустые точки')
    to_seat = models.IntegerField(verbose_name='до')
    row = models.ForeignKey(HallRow, on_delete=models.CASCADE, related_name='empty_spaces', verbose_name='ряд')

    def __str__(self):
        return f'Row {self.row.number} - {self.from_seat} to {self.to_seat}'


class Seat(models.Model):
    class Meta:
        verbose_name = 'место'
        verbose_name_plural = 'места'
        unique_together = (('row', 'seat_number'),)  # Ensure unique seat numbers within each row

    row = models.ForeignKey('HallRow', on_delete=models.CASCADE, related_name='seats', verbose_name='ряд')
    seat_number = models.IntegerField(verbose_name='номер места')
    row_number = models.IntegerField(verbose_name='номер ряда')

    def __str__(self):
        return f'Row {self.row_number} - Seat {self.seat_number}'



