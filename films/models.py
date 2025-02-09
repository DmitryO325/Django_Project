from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

from django.utils import timezone


class MyModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Country(MyModel):
    name = models.CharField("Название", max_length=200, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    def __str__(self):
        return self.name


class Genre(MyModel):
    name = models.CharField("Название", max_length=200, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Person(MyModel):
    name = models.CharField("Имя", max_length=400)
    origin_name = models.CharField("Имя в оригинале", max_length=400,
                                   blank=True, null=True)
    birthday = models.DateField("Дата рождения", blank=True, null=True,
                                validators=[
                                    MaxValueValidator(
                                        limit_value=datetime.date.today)
                                ])
    photo = models.ImageField(
        "Фото", upload_to='photos/', blank=True, null=True)
    kinopoisk_id = models.PositiveIntegerField(
        "Kinopoisk ID", blank=True, null=True)

    def age(self):
        if not self.birthday:
            return None
        today = datetime.date.today()
        return today.year - self.birthday.year \
            - ((today.month, today.day) < (self.birthday.month,
                                           self.birthday.day))

    class Meta:
        ordering = ["name"]
        verbose_name = "Персона"
        verbose_name_plural = "Персоны"

    def __str__(self):
        return self.name


class Film(MyModel):
    name = models.CharField("Имя", max_length=1024)
    origin_name = models.CharField(
        "Название (в оригинале)", max_length=1024, blank=True, null=True)
    slogan = models.CharField("Девиз", max_length=2048, blank=True, null=True)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, verbose_name="Страна")
    genres = models.ManyToManyField(Genre, verbose_name="Жанр")
    director = models.ForeignKey(
        Person, on_delete=models.CASCADE, verbose_name="Режиссер",
        related_name="directed_films")
    length = models.PositiveIntegerField(
        "Продолжительность", blank=True, null=True)
    year = models.PositiveIntegerField("Год выпуска", blank=True, null=True,
                                       validators=[MinValueValidator(
                                           limit_value=1885)])
    trailer_url = models.URLField("Трейлер", blank=True, null=True)
    cover = models.ImageField(
        "Постер", upload_to='covers/', blank=True, null=True)
    description = models.TextField("Описание", blank=True, null=True)
    people = models.ManyToManyField(Person, verbose_name="Актеры")
    kinopoisk_id = models.PositiveIntegerField(
        "Kinopoisk ID", blank=True, null=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"

    def __str__(self):
        return self.name


class Cinema(MyModel):
    name = models.CharField(max_length=100, verbose_name="Название кинотеатра")
    photo = models.ImageField(verbose_name="Фото", upload_to='photos/', blank=True, null=True)
    city = models.CharField(verbose_name="Город", max_length=50)
    address = models.CharField(verbose_name="Адрес", max_length=200)
    description = models.TextField(verbose_name="О кинотеатре", blank=True, null=True)

    class Meta:
        verbose_name = 'Кинотеатр'
        verbose_name_plural = 'Кинотеатры'

    def __str__(self):
        return self.name


class Hall(MyModel):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, verbose_name='Кинотеатр', related_name='halls')
    name = models.CharField(verbose_name='Название зала', max_length=50)
    rows = models.PositiveIntegerField(verbose_name='Количество рядов')
    seats_per_row = models.PositiveIntegerField(verbose_name='Количество мест в ряду')

    class Meta:
        constraints = (models.UniqueConstraint(fields=('cinema', 'name'), name='unique_hall_name_per_cinema'),)
        verbose_name = 'Зал'
        verbose_name_plural = 'Залы'

    def total_seats(self):
        return self.rows * self.seats_per_row

    def __str__(self):
        return self.name


class Screening(MyModel):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, verbose_name='Зал', related_name='screening')
    film = models.ForeignKey(Film, on_delete=models.CASCADE, verbose_name='Фильм')
    start_time = models.DateTimeField(verbose_name='Дата и время начала сеанса')

    class Meta:
        verbose_name = "Сеанс"
        verbose_name_plural = "Сеансы"

    def __str__(self):
        return f'{self.film.name}: {self.start_time.strftime("%d.%m.%Y %H:%M")}'

    def is_seat_available(self, row, seat, user=None):
        seat_obj = Seat.objects.filter(screening=self, row=row, seat=seat).first()

        if seat_obj.is_booked:
            return 0

        if seat_obj.cart is not None and seat_obj.cart.user == user:
            return 1

        return 2

    def get_seats_status(self, user=None):
        seats = {(row, seat): self.is_seat_available(row, seat, user)
                 for row in range(1, self.hall.rows + 1)
                 for seat in range(1, self.hall.seats_per_row + 1)}
        return seats

    def create_seats(self, price):
        if self.id is None:
            self.save()

        seats = [
            Seat(
                screening=self,
                row=row,
                seat=seat,
                price=price
            )
            for row in range(1, self.hall.rows + 1)
            for seat in range(1, self.hall.seats_per_row + 1)
        ]
        Seat.objects.bulk_create(seats)


class Cart(MyModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Имя пользователя")
    name = models.CharField(verbose_name='Название корзины', max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_booked = models.BooleanField(default=False, verbose_name='Корзина забронирована')

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return self.name

    def book_cart(self):
        if self.is_booked:
            raise ValueError("Корзина уже забронирована")
        if not self.seats.exists():
            raise ValueError("Корзина пуста, невозможно забронировать")
        if self.seats.filter(is_booked=True).exists():
            raise ValueError("Одно или несколько мест уже забронированы, невозможно забронировать корзину")

        self.seats.update(is_booked=True)
        self.is_booked = True
        self.save()

    def cancel_cart(self):
        if not self.is_booked:
            raise ValueError("Корзина не забронирована, нечего отменять")

        self.seats.update(is_booked=False)
        self.is_booked = False
        self.save()

    def clean_expired_seats(self):
        for seat in self.seats.all():
            if seat.screening.start_time <= timezone.now():
                seat.cart = None
                seat.save()


class Seat(MyModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина', null=True, related_name='seats')
    screening = models.ForeignKey(Screening, on_delete=models.CASCADE, verbose_name="Сеанс")
    row = models.PositiveIntegerField(verbose_name="Ряд")
    seat = models.PositiveIntegerField(verbose_name="Место")
    price = models.DecimalField(verbose_name="Цена", decimal_places=2, max_digits=7, default=500)
    is_booked = models.BooleanField(default=False, verbose_name="Место забронировано")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    class Meta:
        unique_together = ('screening', 'row', 'seat')
        verbose_name = "Место"
        verbose_name_plural = "Места"

    def __str__(self):
        return f"Ряд {self.row}, место {self.seat} ({self.screening})"

    def save(self, *args, **kwargs):
        if self.cart is None:
            super().save(*args, **kwargs)
            return

        if not self.screening.is_seat_available(self.row, self.seat):
            raise ValueError(f"Место {self.row}-{self.seat} уже занято")
        super().save(*args, **kwargs)
