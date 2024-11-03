# tests/test_transactions.py
from datetime import datetime


def test_create_transaction_with_valid_date(test_client):
    # Create a category first, as transactions need a valid category_id
    test_client.post('/categories', json={'name': 'Entertainment'})
    response = test_client.get('/categories')
    category_id = response.json['categories'][0]['id']

    # Test creating a transaction with a valid date format
    response = test_client.post('/transactions', json={
        'date': '2023-10-31',
        'amount': 50.0,
        'category_id': category_id,
        'notes': 'Movie ticket'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'Transaction created successfully'
    assert response.json['transaction']['date'] == '2023-10-31'  # Check date format in response


def test_create_transaction_with_invalid_date(test_client):
    # Create a category first, as transactions need a valid category_id
    test_client.post('/categories', json={'name': 'Food'})
    response = test_client.get('/categories')
    category_id = response.json['categories'][0]['id']

    # Test creating a transaction with an invalid date format
    response = test_client.post('/transactions', json={
        'date': '31-10-2023',  # Invalid date format
        'amount': 20.0,
        'category_id': category_id,
        'notes': 'Lunch'
    })
    assert response.status_code == 400
    assert response.json['error'] == 'Invalid date format. Use YYYY-MM-DD.'


def test_create_transaction_missing_date(test_client):
    # Create a category first, as transactions need a valid category_id
    test_client.post('/categories', json={'name': 'Utilities'})
    response = test_client.get('/categories')
    category_id = response.json['categories'][0]['id']

    # Test creating a transaction without a date
    response = test_client.post('/transactions', json={
        'amount': 100.0,
        'category_id': category_id,
        'notes': 'Electric bill'
    })
    assert response.status_code == 400
    assert response.json['error'] == 'Date, amount, and category_id are required fields'
