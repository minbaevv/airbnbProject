import os
import django
import random
from datetime import datetime, timedelta
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from AirBNB_app.models import Country, City, UserProfile, Rules, Property, PropertyImage, Booking, Review
from django.contrib.auth.hashers import make_password


# ------------------------------
# 1. Очистка базы
# ------------------------------
def clear_data():
    print("Очистка базы данных...")
    Review.objects.all().delete()
    Booking.objects.all().delete()
    PropertyImage.objects.all().delete()
    Property.objects.all().delete()
    Rules.objects.all().delete()
    UserProfile.objects.all().delete()
    City.objects.all().delete()
    Country.objects.all().delete()
    print("База данных очищена!")


# ------------------------------
# 2. Страны и города
# ------------------------------
def create_countries_and_cities():
    countries_data = [
        {'en': 'Kyrgyzstan', 'ru': 'Кыргызстан', 'cities': [
            {'en': 'Bishkek', 'ru': 'Бишкек'},
            {'en': 'Osh', 'ru': 'Ош'},
            {'en': 'Issyk-Kul', 'ru': 'Иссык-Куль'},
            {'en': 'Karakol', 'ru': 'Каракол'}
        ]},
        {'en': 'Kazakhstan', 'ru': 'Казахстан', 'cities': [
            {'en': 'Almaty', 'ru': 'Алматы'},
            {'en': 'Astana', 'ru': 'Астана'},
            {'en': 'Shymkent', 'ru': 'Шымкент'}
        ]},
        {'en': 'Uzbekistan', 'ru': 'Узбекистан', 'cities': [
            {'en': 'Tashkent', 'ru': 'Ташкент'},
            {'en': 'Samarkand', 'ru': 'Самарканд'}
        ]}
    ]

    countries = []
    cities = []

    for c_data in countries_data:
        country = Country.objects.create(
            country_name=c_data['en'],
            country_name_ru=c_data['ru']
        )
        countries.append(country)
        for city_data in c_data['cities']:
            city = City.objects.create(
                city_name=city_data['en'],
                city_name_ru=city_data['ru'],
                country=country
            )
            cities.append(city)

    print(f"Создано {len(countries)} стран и {len(cities)} городов")
    return countries, cities


# ------------------------------
# 3. Пользователи
# ------------------------------
def create_users():
    hosts = []
    guests = []

    for i in range(1, 16):
        host = UserProfile.objects.create(
            username=f"host{i}",
            first_name=f"Host{i}",
            last_name=f"Smith",
            email=f"host{i}@example.com",
            password=make_password("password123"),
            role='host',
            age=random.randint(25, 60),
            phone_number=f'+996700000{i}',
            avatar=f'avatars/host{i}.png',
            date_registered=datetime.now() - timedelta(days=random.randint(1, 365))
        )
        hosts.append(host)

    for i in range(1, 31):
        guest = UserProfile.objects.create(
            username=f"guest{i}",
            first_name=f"Guest{i}",
            last_name=f"Lee",
            email=f"guest{i}@example.com",
            password=make_password("password123"),
            role='guest',
            age=random.randint(20, 50),
            phone_number=f'+996700001{i}',
            avatar=f'avatars/guest{i}.png',
            date_registered=datetime.now() - timedelta(days=random.randint(1, 365))
        )
        guests.append(guest)

    print(f"Создано {len(hosts)} хозяев и {len(guests)} гостей")
    return hosts, guests


# ------------------------------
# 4. Правила
# ------------------------------
def create_rules():
    rules_list = [
        {'en': 'No Smoking', 'ru': 'Не курить'},
        {'en': 'Pets Allowed', 'ru': 'Можно с питомцами'},
        {'en': 'No Parties', 'ru': 'Без вечеринок'},
        {'en': 'No Loud Music', 'ru': 'Без громкой музыки'}
    ]
    rules = []
    for i, r_data in enumerate(rules_list, 1):
        r = Rules.objects.create(
            rules_name=r_data['en'],
            rules_name_ru=r_data['ru'],
            rules_image=f'rules_images/rule_{i}.png'
        )
        rules.append(r)
    print(f"Создано {len(rules)} правил")
    return rules


# ------------------------------
# 5. Свойства / квартиры / отели
# ------------------------------
def create_properties(cities, hosts, rules):
    property_types = [
        {'en': 'Apartment', 'ru': 'Квартира'},
        {'en': 'House', 'ru': 'Дом'},
        {'en': 'Studio', 'ru': 'Студия'}
    ]
    properties = []

    for i in range(20):
        city = random.choice(cities)
        owner = random.choice(hosts)
        p_type = random.choice(property_types)
        bedrooms = random.randint(1, 4)
        bathrooms = random.randint(1, 3)
        max_guests = bedrooms + random.randint(0, 2)
        price = Decimal(random.randint(50, 200) * bedrooms)

        prop = Property.objects.create(
            title=p_type['en'] + f" in {city.city_name}",
            title_ru=p_type['ru'] + f" в {city.city_name_ru}",
            description=f"Beautiful {p_type['en'].lower()} located in {city.city_name} with {bedrooms} bedrooms and {bathrooms} bathrooms.",
            description_ru=f"Прекрасный {p_type['ru'].lower()} в городе {city.city_name_ru} с {bedrooms} спальнями и {bathrooms} ванными комнатами.",
            country=city.country,
            city=city,
            price=price,
            property_type=p_type['en'],
            max_guests=max_guests,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            owner=owner,
            is_active=True
        )
        prop.rules.set(random.sample(rules, random.randint(1, len(rules))))
        properties.append(prop)

        for j in range(1, random.randint(3, 6)):
            PropertyImage.objects.create(
                property=prop,
                image=f'property_images/property_{i + 1}_{j}.png'
            )

    print(f"Создано {len(properties)} свойств")
    return properties


# ------------------------------
# 6. Бронирования
# ------------------------------
def create_bookings(guests, properties):
    bookings = []
    for i in range(50):
        guest = random.choice(guests)
        prop = random.choice(properties)
        check_in = datetime.now() + timedelta(days=random.randint(-60, 90))
        check_out = check_in + timedelta(days=random.randint(1, 14))
        status = random.choice(['Pending', 'Approved', 'Rejected', 'Cancelled'])
        b = Booking.objects.create(
            property=prop,
            guest=guest,
            check_in=check_in,
            check_out=check_out,
            status=status
        )
        bookings.append(b)
    print(f"Создано {len(bookings)} бронирований")
    return bookings


# ------------------------------
# 7. Отзывы
# ------------------------------
def create_reviews(guests, properties):
    reviews = []
    sample_comments = [
        {'en': "Excellent place, very clean and comfortable.", 'ru': "Отличное место, очень чисто и удобно."},
        {'en': "Great location and friendly host.", 'ru': "Отличное расположение и дружелюбный хозяин."},
        {'en': "Would stay here again!", 'ru': "Останусь здесь снова!"},
        {'en': "Not as expected, but okay.", 'ru': "Не совсем как ожидал, но нормально."}
    ]
    for i in range(50):
        guest = random.choice(guests)
        prop = random.choice(properties)
        comment = random.choice(sample_comments)
        rating = random.randint(3, 5)
        r = Review.objects.create(
            property=prop,
            user=guest,
            rating=rating,
            comment=comment['en'],
            comment_ru=comment['ru'],
            created_date=datetime.now() - timedelta(days=random.randint(1, 365))
        )
        reviews.append(r)
    print(f"Создано {len(reviews)} отзывов")
    return reviews


# ------------------------------
# Главная функция
# ------------------------------
def main():
    print("=" * 60)
    print("НАЧАЛО ЗАПОЛНЕНИЯ БАЗЫ ДАННЫХ AIRBNB (ДВУХЯЗЫЧНО)")
    print("=" * 60)

    clear_data()
    countries, cities = create_countries_and_cities()
    hosts, guests = create_users()
    rules = create_rules()
    properties = create_properties(cities, hosts, rules)
    bookings = create_bookings(guests, properties)
    reviews = create_reviews(guests, properties)

    print("=" * 60)
    print("БАЗА ДАННЫХ УСПЕШНО ЗАПОЛНЕНА!")
    print("=" * 60)
    print(f"Страны: {len(countries)}")
    print(f"Города: {len(cities)}")
    print(f"Пользователи: {len(hosts) + len(guests)}")
    print(f"Правила: {len(rules)}")
    print(f"Свойства: {len(properties)}")
    print(f"Бронирования: {len(bookings)}")
    print(f"Отзывы: {len(reviews)}")


if __name__ == "__main__":
    main()
