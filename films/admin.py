from django.contrib import admin
from .models import Country, Film, Person, Genre, Screening, Cart, Seat, Cinema, Hall

admin.site.register(Film)
admin.site.register(Person)
admin.site.register(Country)
admin.site.register(Genre)
admin.site.register(Cinema)
admin.site.register(Hall)
admin.site.register(Screening)
admin.site.register(Cart)
admin.site.register(Seat)
