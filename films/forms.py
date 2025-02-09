from django import forms
from dal import autocomplete
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.timezone import timedelta

from .models import Country, Genre, Film, Person, Seat, Screening, Cinema, Hall, Cart


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['name']


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']


class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = ['name', 'origin_name', 'slogan', 'length', 'year',
                  'trailer_url', 'cover', 'description', 'country', 'genres',
                  "director", 'people']
        widgets = {
            'people': autocomplete.ModelSelect2Multiple(
                url='films:person_autocomplete'),
            'director': autocomplete.ModelSelect2(
                url='films:person_autocomplete'),
            'country': autocomplete.ModelSelect2(
                url='films:country_autocomplete'),
        }


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'origin_name', 'birthday', 'photo']
        widgets = {
            "birthday": forms.DateInput(attrs={'type': 'date'},
                                        format="%Y-%m-%d")
        }


class CinemaForm(forms.ModelForm):
    class Meta:
        model = Cinema
        fields = ['name', 'photo', 'city', 'address', 'description']


class HallForm(forms.ModelForm):
    class Meta:
        model = Hall
        fields = ['name', 'rows', 'seats_per_row']

    def __init__(self, *args, **kwargs):
        self.cinema = kwargs.pop('cinema', None)
        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data['name']
        if Hall.objects.filter(name=name, cinema=self.cinema).exclude(id=self.instance.id).exists():
            raise ValidationError("Зал с таким названием уже существует в этом кинотеатре.")
        return name

    def clean_rows(self):
        rows = self.cleaned_data['rows']
        if rows <= 0:
            raise forms.ValidationError("Количество рядов должно быть больше нуля.")
        return rows

    def clean_seats_per_row(self):
        seats_per_row = self.cleaned_data['seats_per_row']
        if seats_per_row <= 0:
            raise forms.ValidationError("Количество мест в ряду должно быть больше нуля.")
        return seats_per_row


class ScreeningForm(forms.ModelForm):
    class Meta:
        model = Screening
        fields = ['hall', 'film', 'start_time']

    price = forms.DecimalField(
        max_digits=7,
        decimal_places=2,
        initial=500,
        label="Цена билета",
        required=True
    )

    def __init__(self, *args, **kwargs):
        cinema_id = kwargs.pop('cinema_id', None)
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.id:
            self.fields['hall'].widget = forms.HiddenInput()
            self.fields['start_time'].initial = self.instance.start_time.strftime('%Y-%m-%dT%H:%M')

        else:
            if cinema_id:
                self.fields['hall'].queryset = Hall.objects.filter(cinema_id=cinema_id)
            else:
                self.fields['hall'].queryset = Hall.objects.none()

            self.fields['start_time'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})

    def clean_start_time(self):
        start_time = self.cleaned_data['start_time']
        now = timezone.now()

        if start_time < now:
            raise ValidationError("Время начала сеанса не может быть в прошлом")

        if start_time < now + timedelta(minutes=15):
            raise ValidationError("Сеанс должен начинаться через 15 минут или больше")

        hall = self.cleaned_data['hall']

        overlapping_screenings = Screening.objects.filter(
            hall=hall
        ).exclude(id=self.instance.id)

        for screening in overlapping_screenings:
            screening_start = screening.start_time
            screening_end = screening_start + timedelta(minutes=screening.film.length)

            if not (screening_end + timedelta(minutes=15) <= start_time or
                    start_time + timedelta(minutes=screening.film.length) <= screening_start - timedelta(minutes=15)):
                raise ValidationError(f'В это время в зале запланирован другой сеанс')

        return start_time


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['name']


class SeatForm(forms.ModelForm):
    class Meta:
        model = Seat
        fields = ['price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['price'].widget = forms.NumberInput(attrs={'step': '0.01', 'min': '0'})