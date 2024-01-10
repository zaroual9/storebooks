# Import necessary modules and fixtures
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from books.models import Book
from django.test import Client

# Fixture to create a Django test client
@pytest.fixture
def client():
    return Client()

# Fixture providing user data for testing
@pytest.fixture
def user_data():
    return {
        'username': 'khalil',
        'email': 'khalilmarmat08@gmail.com',
        'password': 'secret',
    }

# Fixture providing book data for testing
@pytest.fixture
def book_data():
    return {
        'title': 'django for beginners',
        'author': 'WS Vinvcent',
        'description': 'anything',
        'price': '30',
        'image_url': 'https://forexample.jpg',
        'follow_author': 'https://twitter.com/?lang=en',
        'book_available': 'True',
    }

# Fixture creating a user instance in the database
@pytest.fixture
def user(db, user_data):
    return get_user_model().objects.create_user(**user_data)

# Fixture creating a book instance in the database
@pytest.fixture
def book(db, book_data):
    return Book.objects.create(**book_data)

# Unit Test: Test the string representation of the Book model
@pytest.mark.django_db
def test_string_representation():
    book = Book(title='new book')
    assert str(book) == book.title

# Unit Test: Test the content of various fields in the Book model
@pytest.mark.django_db
def test_book_model_fields_content(book):
    assert str(book.title) == 'django for beginners'
    assert str(book.author) == 'WS Vinvcent'
    assert str(book.description) == 'anything'
    assert str(book.price) == '30'
    assert str(book.image_url) == 'https://forexample.jpg'
    assert str(book.follow_author) == 'https://twitter.com/?lang=en'
    assert str(book.book_available) == 'True'

# Integration Test: Test the behavior of the book list view for a logged-in user
@pytest.mark.django_db
def test_book_list_view_for_logged_in_user(client, user, book):
    client.login(username='khalil', email='khalilmarmat08@gmail.com', password='secret')
    response = client.get(reverse('list'))
    assert response.status_code == 200
    assert book.title in response.content.decode('utf-8')
    assert book.price in response.content.decode('utf-8')

# Integration Test: Test the behavior of the book list view for an anonymous user
@pytest.mark.django_db
def test_book_list_view_for_anonymous_user(client, book):
    client.logout()
    response = client.get(reverse('list'))
    assert response.status_code == 200
    assert book.title in response.content.decode('utf-8')
    assert book.price in response.content.decode('utf-8')

# Integration Test: Test the behavior of the book detail view for a logged-in user
@pytest.mark.django_db
def test_book_detail_view_for_logged_in_user(client, user, book):
    client.login(username='khalil', email='khalilmarmat08@gmail.com', password='secret')
    response = client.get(reverse('detail', args=[str(book.pk)]))
    assert response.status_code == 200
    assert book.title in response.content.decode('utf-8')
    assert book.author in response.content.decode('utf-8')
    assert book.price in response.content.decode('utf-8')

# Integration Test: Test the behavior of the book detail view for an anonymous user
@pytest.mark.django_db
def test_book_detail_view_for_anonymous_user(client, book):
    client.logout()
    response = client.get(reverse('detail', args=[str(book.pk)]))
    assert response.status_code == 200
    assert book.title in response.content.decode('utf-8')
    assert book.author in response.content.decode('utf-8')
    assert book.price in response.content.decode('utf-8')

# Integration Test: Test the behavior of the checkout view for a logged-in user
@pytest.mark.django_db
def test_checkout_view_for_logged_in_user(client, user, book):
    client.login(username='khalil', email='khalilmarmat08@gmail.com', password='secret')
    response = client.get(reverse('checkout', args=[str(book.pk)]))
    assert response.status_code == 200
    assert book.title in response.content.decode('utf-8')
    assert book.price in response.content.decode('utf-8')

# Integration Test: Test the behavior of the checkout view for an anonymous user
@pytest.mark.django_db
def test_checkout_view_for_anonymous_user(client, book):
    client.logout()
    response = client.get(reverse('checkout', args=[str(book.pk)]))
    assert response.status_code == 302
    assert '/accounts/login/' in response.url

# Integration Test: Test the behavior of the book detail view when the book is available
@pytest.mark.django_db
def test_book_when_available(client, book):
    response = client.get(reverse('detail', args=[str(book.pk)]))
    assert response.status_code == 200
    assert 'Buy Now' in response.content.decode('utf-8')
    assert 'Out of Stock !' not in response.content.decode('utf-8')

# Integration Test: Test the behavior of the book detail view when the book is out of stock
@pytest.mark.django_db
def test_book_when_out_of_stock(client, book):
    Book.objects.create(
        title='new book',
        author='khalil',
        description='anything',
        price='30',
        image_url='https://forexample.jpg',
        follow_author='https://twitter.com/?lang=en',
        book_available='False',
    )
    response = client.get(reverse('detail', args=['2']))
    assert response.status_code == 200
    assert 'Out of Stock !' in response.content.decode('utf-8')
    assert 'Buy Now' not in response.content.decode('utf-8')
