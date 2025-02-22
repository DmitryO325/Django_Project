from django.urls import path
from . import views

app_name = "films"
urlpatterns = [
    path('', views.film_list, name='home'),
    path('countries/', views.country_list, name='country_list'),
    path('countries/<int:id>/', views.country_detail, name='country_detail'),
    path('countries/create/', views.country_create, name='country_create'),
    path('countries/<int:id>/update/',
         views.country_update, name='country_update'),
    path('countries/<int:id>/delete/',
         views.country_delete, name='country_delete'),
    path('countries/autocomplete/',
         views.CountryAutocomplete.as_view(), name='country_autocomplete'),

    path('genres/', views.genre_list, name='genre_list'),
    path('genres/<int:id>/', views.genre_detail, name='genre_detail'),
    path('genres/create/', views.genre_create, name='genre_create'),
    path('genres/<int:id>/update/',
         views.genre_update, name='genre_update'),
    path('genres/<int:id>/delete/',
         views.genre_delete, name='genre_delete'),

    path('films/', views.film_list, name='film_list'),
    path('films/<int:id>/', views.film_detail, name='film_detail'),
    path('films/create/', views.film_create, name='film_create'),
    path('films/<int:id>/update/',
         views.film_update, name='film_update'),
    path('film/<int:id>/delete/',
         views.film_delete, name='film_delete'),

    path('people/', views.person_list, name='person_list'),
    path('people/<int:id>/', views.person_detail, name='person_detail'),
    path('people/create/', views.person_create, name='person_create'),
    path('people/<int:id>/update/',
         views.person_update, name='person_update'),
    path('people/<int:id>/delete/',
         views.person_delete, name='person_delete'),
    path('people/autocomplete/',
         views.PersonAutocomplete.as_view(), name='person_autocomplete'),

    path('cinemas', views.cinema_list, name='cinema_list'),
    path('cinemas/<int:id>/', views.cinema_detail, name='cinema_detail'),
    path('cinemas/create/', views.cinema_create, name='cinema_create'),
    path('cinemas/<int:id>/update/', views.cinema_update, name='cinema_update'),
    path('cinemas/<int:id>/delete/', views.cinema_delete, name='cinema_delete'),

    path('cinemas/<int:cinema_id>/halls/', views.hall_list, name='hall_list'),
    path('cinemas/<int:cinema_id>/halls/<int:hall_id>/', views.hall_detail, name='hall_detail'),
    path('cinemas/<int:cinema_id>/halls/create/', views.hall_create, name='hall_create'),
    path('cinemas/<int:cinema_id>/halls/<int:hall_id>/update/', views.hall_update, name='hall_update'),
    path('cinemas/<int:cinema_id>/halls/<int:hall_id>/delete/', views.hall_delete, name='hall_delete'),

    path('screenings', views.screening_list, name='screening_list'),
    path('screenings/<int:id>/', views.screening_detail, name='screening_detail'),
    path('screenings/create/', views.screening_create, name='screening_create'),
    path('screenings/<int:id>/update/', views.screening_update, name='screening_update'),
    path('screenings/<int:id>/delete/', views.screening_delete, name='screening_delete'),
    path('screenings/<int:id>/seats/', views.seat_list, name='seat_list'),
    path('screenings/<int:id>/seats/<int:row>/<int:seat>/', views.seat_detail, name='seat_detail'),
    path('screenings/<int:id>/seats/<int:row>/<int:seat>/select_cart/', views.cart_select, name='cart_select'),
    path('screenings/<int:screening_id>/seats/<int:row>/<int:seat>', views.cart_create, name='cart_create_with_seat'),
    path('screenings/<int:screening_id>/seats/<int:row>/<int:seat>/seat_delete/',
         views.seat_delete, name='seat_delete'),
    path('screenings/<int:screening_id>/seats/<int:row>/<int:seat>/seat_update',
         views.seat_update, name='seat_update'),

    path('carts', views.cart_list, name='cart_list'),
    path('carts/<int:id>/', views.cart_detail, name='cart_detail'),
    path('carts/create/', views.cart_create, name='cart_create'),
    path('carts/<int:id>/update/', views.cart_update, name='cart_update'),
    path('carts/<int:id>/delete/', views.cart_delete, name='cart_delete'),
    path('carts/<int:id>/book/', views.cart_book, name='cart_book'),
    path('carts/<int:id>/cancel/', views.cart_cancel, name='cart_cancel'),
]
