from dal import autocomplete
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils import timezone

from .models import Country, Film, Genre, Person, Screening, Cart, Seat, Cinema, Hall
from .forms import CountryForm, GenreForm, FilmForm, PersonForm, ScreeningForm, CinemaForm, HallForm, CartForm, SeatForm
from .helpers import paginate
from django.contrib import messages


def check_admin(user):
    return user.is_superuser


def country_list(request):
    countries = Country.objects.all()
    return render(request, 'films/country/list.html', {'countries': countries})


def country_detail(request, id):
    country = get_object_or_404(Country, id=id)
    films = Film.objects.filter(country=country)

    films = paginate(request, films)
    return render(request, 'films/country/list.html',
                  {'country': country, 'films': films})


@user_passes_test(check_admin)
def country_create(request):
    if request.method == 'POST':
        form = CountryForm(request.POST)
        if form.is_valid():
            country = form.save()
            messages.success(request, 'Страна добавлена')
            return redirect('films:country_detail', id=country.id)
    else:
        form = CountryForm()
    return render(request, 'films/country/create.html', {'form': form})


@user_passes_test(check_admin)
def country_update(request, id):
    country = get_object_or_404(Country, id=id)
    if request.method == 'POST':
        form = CountryForm(request.POST, instance=country)
        if form.is_valid():
            form.save()
            messages.success(request, 'Страна изменена')
            return redirect('films:country_detail', id=country.id)
    else:
        form = CountryForm(instance=country)
    return render(request, 'films/country/update.html',
                  {'form': form})


@user_passes_test(check_admin)
def country_delete(request, id):
    country = get_object_or_404(Country, id=id)
    if request.method == 'POST':
        country.delete()
        messages.success(request, 'Страна удалена')
        return redirect('films:country_list')
    return render(request, 'films/country/delete.html',
                  {'country': country})


def genre_list(request):
    genres = Genre.objects.all()
    return render(request, 'films/genre/list.html', {'genres': genres})


def genre_detail(request, id):
    genre = get_object_or_404(Genre, id=id)
    films = Film.objects.filter(genres=genre)

    films = paginate(request, films)
    return render(request, 'films/genre/list.html',
                  {'genre': genre, 'films': films})


@user_passes_test(check_admin)
def genre_create(request):
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            genre = form.save()
            messages.success(request, 'Жанр добавлен')
            return redirect('films:genre_detail', id=genre.id)
    else:
        form = GenreForm()
    return render(request, 'films/genre/create.html', {'form': form})


@user_passes_test(check_admin)
def genre_update(request, id):
    genre = get_object_or_404(Genre, id=id)
    if request.method == 'POST':
        form = GenreForm(request.POST, instance=genre)
        if form.is_valid():
            form.save()
            messages.success(request, 'Жанр изменён')
            return redirect('films:genre_detail', id=genre.id)
    else:
        form = GenreForm(instance=genre)
    return render(request, 'films/genre/update.html',
                  {'form': form})


@user_passes_test(check_admin)
def genre_delete(request, id):
    genre = get_object_or_404(Genre, id=id)
    if request.method == 'POST':
        genre.delete()
        messages.success(request, 'Жанр удалён')
        return redirect('films:genre_list')
    return render(request, 'films/genre/delete.html',
                  {'genre': genre})


def film_list(request):
    films = Film.objects.all()
    query = request.GET.get('query', '')
    if query:
        films = films.filter(name__icontains=query)
    films = paginate(request, films)
    return render(request, 'films/film/list.html', {'films': films,
                                                    'query': query})


def film_detail(request, id):
    queryset = Film.objects.prefetch_related("country", "genres", "director",
                                             "people")
    film = get_object_or_404(queryset, id=id)
    return render(request, 'films/film/list.html',
                  {'film': film})


@user_passes_test(check_admin)
def film_create(request):
    if request.method == 'POST':
        form = FilmForm(request.POST, request.FILES)
        if form.is_valid():
            film = form.save()
            messages.success(request, 'Фильм добавлен')
            return redirect('films:film_detail', id=film.id)
    else:
        form = FilmForm()
    return render(request, 'films/film/create.html', {'form': form})


@user_passes_test(check_admin)
def film_update(request, id):
    film = get_object_or_404(Film, id=id)
    if request.method == 'POST':
        form = FilmForm(request.POST, request.FILES, instance=film)
        if form.is_valid():
            form.save()
            messages.success(request, 'Фильм изменён')
            return redirect('films:film_detail', id=film.id)
    else:
        form = FilmForm(instance=film)
    return render(request, 'films/film/update.html',
                  {'form': form})


@user_passes_test(check_admin)
def film_delete(request, id):
    film = get_object_or_404(Film, id=id)
    if request.method == 'POST':
        film.delete()
        messages.success(request, 'Фильм удалён')
        return redirect('films:film_list')
    return render(request, 'films/film/delete.html',
                  {'film': film})


def person_list(request):
    people = Person.objects.all()
    query = request.GET.get('query', '')
    if query:
        people = people.filter(name__icontains=query)
    people = paginate(request, people)
    return render(request, 'films/person/list.html', {'people': people,
                                                      'query': query})


def person_detail(request, id):
    queryset = Person.objects.prefetch_related("film_set", "directed_films")
    person = get_object_or_404(queryset, id=id)
    return render(request, 'films/person/list.html',
                  {'person': person})


@user_passes_test(check_admin)
def person_create(request):
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES)
        if form.is_valid():
            person = form.save()
            messages.success(request, 'Персона добавлена')
            return redirect('films:person_detail', id=person.id)
    else:
        form = PersonForm()
    return render(request, 'films/person/create.html', {'form': form})


@user_passes_test(check_admin)
def person_update(request, id):
    person = get_object_or_404(Person, id=id)
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            form.save()
            messages.success(request, 'Персона изменена')
            return redirect('films:person_detail', id=person.id)
    else:
        form = PersonForm(instance=person)
    return render(request, 'films/person/update.html',
                  {'form': form})


@user_passes_test(check_admin)
def person_delete(request, id):
    person = get_object_or_404(Person, id=id)
    if request.method == 'POST':
        person.delete()
        messages.success(request, 'Персона удалена')
        return redirect('films:person_list')
    return render(request, 'films/person/delete.html',
                  {'person': person})


def cinema_list(request):
    cinemas = Cinema.objects.all()
    query = request.GET.get('query', '')
    if query:
        cinemas = cinemas.filter(name__icontains=query)
    cinemas = paginate(request, cinemas)
    return render(request, 'films/cinema/list.html',
                  {'cinemas': cinemas, 'query': query})


def cinema_detail(request, id):
    queryset = Cinema.objects.prefetch_related()
    cinema = get_object_or_404(queryset, id=id)
    return render(request, 'films/cinema/detail.html',
                  {'cinema': cinema})


@user_passes_test(check_admin)
def cinema_create(request):
    if request.method == 'POST':
        form = CinemaForm(request.POST, request.FILES)
        if form.is_valid():
            cinema = form.save()
            messages.success(request, 'Кинотеатр добавлен')
            return redirect('films:cinema_detail', id=cinema.id)
    else:
        form = CinemaForm()
    return render(request, 'films/cinema/create.html',
                  {'form': form})


@user_passes_test(check_admin)
def cinema_update(request, id):
    cinema = get_object_or_404(Cinema, id=id)
    if request.method == 'POST':
        form = CinemaForm(request.POST, request.FILES, instance=cinema)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные о кинотеатре изменены')
            return redirect('films:cinema_detail', id=cinema.id)
    else:
        form = CinemaForm(instance=cinema)
    return render(request, 'films/cinema/update.html',
                  {'form': form})


@user_passes_test(check_admin)
def cinema_delete(request, id):
    cinema = get_object_or_404(Cinema, id=id)
    if request.method == 'POST':
        cinema.delete()
        messages.success(request, 'Кинотеатр удалён')
        return redirect('films:cinema_list')
    return render(request, 'films/cinema/delete.html',
                  {'cinema': cinema})


def hall_list(request, cinema_id):
    cinema = get_object_or_404(Cinema, id=cinema_id)
    halls = Hall.objects.filter(cinema=cinema)
    query = request.GET.get('query', '')
    if query:
        halls = halls.filter(name__icontains=query)
    halls = paginate(request, halls)
    return render(request, 'films/cinema/hall/list.html',
                  {'cinema': cinema, 'halls': halls, 'query': query})


def hall_detail(request, cinema_id, hall_id):
    queryset = Hall.objects.prefetch_related()
    cinema = get_object_or_404(Cinema, id=cinema_id)
    hall = get_object_or_404(queryset, id=hall_id, cinema=cinema)
    return render(request, 'films/cinema/hall/detail.html',
                  {'cinema': cinema, 'hall': hall})


@user_passes_test(check_admin)
def hall_create(request, cinema_id):
    cinema = get_object_or_404(Cinema, id=cinema_id)
    if request.method == 'POST':
        form = HallForm(request.POST, request.FILES, cinema=cinema)
        if form.is_valid():
            hall = form.save(commit=False)
            hall.cinema = cinema
            hall.save()
            messages.success(request, 'Зал добавлен')
            return redirect('films:hall_detail', cinema_id=cinema.id, hall_id=hall.id)
    else:
        form = HallForm()
    return render(request, 'films/cinema/hall/create.html',
                  {'form': form, 'cinema': cinema})


@user_passes_test(check_admin)
def hall_update(request, cinema_id, hall_id):
    cinema = get_object_or_404(Cinema, id=cinema_id)
    hall = get_object_or_404(Hall, id=hall_id, cinema=cinema)
    if request.method == 'POST':
        form = HallForm(request.POST, request.FILES, instance=hall, cinema=cinema)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные о зале изменены')
            return redirect('films:hall_detail', cinema_id=cinema.id, hall_id=hall.id)
    else:
        form = HallForm(instance=hall)
    return render(request, 'films//cinema/hall/update.html',
                  {'form': form, 'cinema': cinema})


@user_passes_test(check_admin)
def hall_delete(request, cinema_id, hall_id):
    cinema = get_object_or_404(Cinema, id=cinema_id)
    hall = get_object_or_404(Hall, id=hall_id, cinema=cinema)
    if request.method == 'POST':
        hall.delete()
        messages.success(request, 'Зал удалён')
        return redirect('films:hall_list', cinema_id=cinema.id)
    return render(request, 'films/cinema/hall/delete.html',
                  {'cinema': cinema, 'hall': hall})


def screening_list(request):
    screenings = Screening.objects.filter(start_time__gte=timezone.now()).order_by('start_time')
    query = request.GET.get('query', '')
    if query:
        screenings = screenings.filter(name__icontains=query)
    screenings = paginate(request, screenings)
    return render(request, 'films/screening/list.html',
                  {'screenings': screenings, 'query': query})


def screening_detail(request, id):
    queryset = Screening.objects.prefetch_related()
    screening = get_object_or_404(queryset, id=id)
    return render(request, 'films/screening/detail.html',
                  {'screening': screening})


@user_passes_test(check_admin)
def screening_create(request):
    cinema_id = request.GET.get('cinema_id')
    if request.method == 'POST':
        form = ScreeningForm(request.POST, cinema_id=cinema_id)
        if form.is_valid():
            screening = form.save(commit=False)
            price = form.cleaned_data['price']
            screening.create_seats(price)
            messages.success(request, 'Сеанс добавлен')
            return redirect('films:screening_detail', id=screening.id)
    else:
        form = ScreeningForm(cinema_id=cinema_id)

    cinemas = Cinema.objects.all()
    context = {
        'form': form,
        'cinemas': cinemas,
        'selected_cinema': int(cinema_id) if cinema_id else None
    }
    return render(request, 'films/screening/create.html', context)


@user_passes_test(check_admin)
def screening_update(request, id):
    screening = get_object_or_404(Screening, id=id)
    cinema_id = request.GET.get('cinema_id')
    if request.method == 'POST':
        form = ScreeningForm(request.POST, cinema_id=cinema_id, instance=screening)
        if form.is_valid():
            form.save()
            messages.success(request, 'Сеанс изменён')
            return redirect('films:screening_detail', id=screening.id)
    else:
        form = ScreeningForm(cinema_id=cinema_id, instance=screening)

    cinemas = Cinema.objects.all()
    context = {
        'form': form,
        'cinemas': cinemas,
        'selected_cinema': int(cinema_id) if cinema_id else None,
        'screening': screening
    }
    return render(request, 'films/screening/update.html', context)


@user_passes_test(check_admin)
def screening_delete(request, id):
    screening = get_object_or_404(Screening, id=id)
    if request.method == 'POST':
        screening.delete()
        messages.success(request, 'Сеанс удалён')
        return redirect('films:screening_list')
    return render(request, 'films/screening/delete.html',
                  {'screening': screening})


def seat_list(request, id):
    screening = get_object_or_404(Screening, id=id)
    seats_status = screening.get_seats_status(user=request.user)

    seats = {}
    for (row, seat), available in seats_status.items():
        if row not in seats:
            seats[row] = {}
        seats[row][seat] = available

    context = {
        'screening': screening,
        'seats': seats,
        'rows': screening.hall.rows,
        'seats_per_row': screening.hall.seats_per_row
    }
    return render(request, 'films/screening/seat/list.html', context)


def seat_detail(request, id, row, seat):
    screening = get_object_or_404(Screening, id=id)
    seat_status = screening.is_seat_available(row, seat, user=request.user)
    seat_object = Seat.objects.get(screening=screening, row=row, seat=seat)
    price = seat_object.price

    return render(request, 'films/screening/seat/detail.html', {
        'screening': screening,
        'row': row,
        'seat': seat,
        'price': price,
        'is_available': seat_status,
    })


def cart_list(request):
    carts = Cart.objects.filter(user=request.user)
    query = request.GET.get('query', '')
    if query:
        carts = carts.filter(name__icontains=query)
    carts = paginate(request, carts)
    return render(request, 'films/cart/list.html',
                  {'carts': carts, 'query': query})


def cart_detail(request, id):
    queryset = Cart.objects.prefetch_related()
    cart = get_object_or_404(queryset, id=id)
    total_cost = sum(seat.price for seat in cart.seats.all())
    cart.clean_expired_seats()

    screenings = {}
    for seat in cart.seats.all():
        screening = seat.screening
        if screening not in screenings:
            screenings[screening] = []
        screenings[screening].append(seat)

    return render(request, 'films/cart/detail.html',
                  {'cart': cart, 'total_cost': total_cost, 'screenings': screenings})


@login_required
def cart_create(request, screening_id=None, row=None, seat=None):
    if request.method == 'POST':
        form = CartForm(request.POST)
        if form.is_valid():
            cart = form.save(commit=False)
            cart.user = request.user
            cart.save()
            messages.success(request, 'Корзина создана')
            if screening_id and row and seat:
                return redirect('films:cart_select', id=screening_id, row=row, seat=seat)
            else:
                return redirect('films:cart_detail', id=cart.id)
    else:
        form = CartForm()

    return render(request, 'films/cart/create.html',
                  {'form': form})


@login_required
def cart_update(request, id):
    cart = get_object_or_404(Cart, id=id, user=request.user)
    if request.method == 'POST':
        form = CartForm(request.POST, instance=cart)
        if form.is_valid():
            cart = form.save(commit=False)
            cart.user = request.user
            cart.save()
            messages.success(request, 'Название корзины изменено')
            return redirect('films:cart_detail', id=cart.id)
    else:
        form = CartForm(instance=cart)

    return render(request, 'films/cart/update.html',
                  {'form': form, 'cart': cart})


@login_required
def cart_delete(request, id):
    cart = get_object_or_404(Cart, id=id, user=request.user)
    if request.method == 'POST':
        if cart.is_booked:
            cart.seats.update(is_booked=False)
        cart.seats.update(cart=None)
        cart.delete()
        messages.success(request, 'Корзина удалена')
        return redirect('films:cart_list')

    return render(request, 'films/cart/delete.html',
                  {'cart': cart})


@login_required
def cart_select(request, id, row, seat):
    screening = get_object_or_404(Screening, id=id)
    seat_obj = get_object_or_404(Seat, screening=screening, row=row, seat=seat)

    if seat_obj.cart and seat_obj.cart.is_booked:
        messages.error(request, f"Место {row}-{seat} уже забронировано")
        return redirect('films:seat_detail', id=id, row=row, seat=seat)

    carts = Cart.objects.filter(user=request.user, is_booked=False)

    if request.method == 'POST':
        cart_id = request.POST.get('cart_id')
        if cart_id:
            cart = get_object_or_404(Cart, id=cart_id, user=request.user, is_booked=False)

            seat_obj.cart = cart
            seat_obj.save()

            messages.success(request, f"Место {row}-{seat} добавлено в корзину {cart.name}")
            return redirect('films:seat_detail', id=screening.id, row=row, seat=seat)

        messages.error(request, "Корзина не выбрана")
        return redirect('films:seat_detail', id=screening.id, row=row, seat=seat)

    return render(request, 'films/cart/select.html', {
        'screening': screening,
        'row': row,
        'seat': seat,
        'price': seat_obj.price,
        'carts': carts
    })


@login_required
def cart_book(request, id):
    cart = get_object_or_404(Cart, id=id, user=request.user, is_booked=False)

    try:
        cart.book_cart()
        messages.success(request, "Корзина забронирована")
    except ValueError as e:
        messages.error(request, str(e))
    return redirect('films:cart_detail', id=cart.id)


@login_required
def cart_cancel(request, id):
    cart = get_object_or_404(Cart, id=id, user=request.user, is_booked=True)

    try:
        cart.cancel_cart()
        messages.success(request, "Бронь корзины отменена")
    except ValueError as e:
        messages.error(request, str(e))
    return redirect('films:cart_detail', id=cart.id)


@login_required
def seat_delete(request, screening_id, row, seat):
    seat = get_object_or_404(
        Seat,
        cart__user=request.user,
        screening__id=screening_id,
        row=row,
        seat=seat,
    )

    cart_id = seat.cart.id

    if seat.is_booked:
        seat.is_booked = False

    seat.cart = None
    seat.save()

    messages.success(request, "Место успешно удалено из корзины")
    return redirect('films:cart_detail', id=cart_id)


def seat_update(request, screening_id, row, seat):
    seat_obj = get_object_or_404(Seat, screening__id=screening_id, row=row, seat=seat)

    if not request.user.is_superuser:
        messages.error(request, "У вас нет прав для изменения цены")
        return redirect('films:seat_list')

    if request.method == 'POST':
        form = SeatForm(request.POST, instance=seat_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Цена места обновлена")
            return redirect('films:seat_detail', id=screening_id, row=row, seat=seat)
    else:
        form = SeatForm(instance=seat_obj)

    return render(request, 'films/screening/seat/update.html',
                  {'form': form, 'seat': seat_obj})



class PersonAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        people = Person.objects.all()
        if self.q:
            people = people.filter(name__istartswith=self.q)
        return people


class CountryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        countries = Country.objects.all()
        if self.q:
            countries = countries.filter(name__istartswith=self.q)
        return countries
