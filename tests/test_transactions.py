# tests/test_transactions.py
import pytest
from datetime import datetime

def test_create_transaction_valid_date(test_client):
    # Create a category first, since transactions need a valid category_id
    test_client.post('/categories', json={'name': 'Entertainment'})
    response = test_client.get('/categories')
    category_id = response.json['categories'][0]['id']

    # Test creating a new transaction with a valid date
    response = test_client.post('/transactions', json={
        'date': '2023-10-31',
        'amount': 50.0,
        'category_id': category_id,
        'notes': 'Movie ticket'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'Transaction created successfully'
    assert 'transaction' in response.json
    assert response.json['transaction']['date'] == '2023-10-31'  # Confirm date is in string format


def test_create_transaction_invalid_date_format(test_client):
    # Create a category first
    test_client.post('/categories', json={'name': 'Food'})
    response = test_client.get('/categories')
    category_id = response.json['categories'][0]['id']

    # Test creating a new transaction with an invalid date format
    response = test_client.post('/transactions', json={
        'date': '31-10-2023',  # Incorrect format
        'amount': 25.0,
        'category_id': category_id,
        'notes': 'Lunch'
    })
    assert response.status_code == 400
    assert response.json['error'] == 'Invalid date format. Use YYYY-MM-DD.'

    # Test creating a transaction without a date
    response = test_client.post('/transactions', json={
        'amount': 25.0,
        'category_id': category_id,
        'notes': 'Lunch'
    })
    assert response.status_code == 400
    assert response.json['error'] == 'Date, amount, and category_id are required fields'


def test_get_transactions_with_correct_date_format(test_client):
    # Create a category and a transaction first
    test_client.post('/categories', json={'name': 'Utilities'})
    response = test_client.get('/categories')
    category_id = response.json['categories'][0]['id']

    test_client.post('/transactions', json={
        'date': '2023-10-31',
        'amount': 100.0,
        'category_id': category_id,
        'notes': 'Electric bill'
    })

    # Retrieve all transactions and check date format
    response = test_client.get('/transactions')
    assert response.status_code == 200
    for transaction in response.json['transactions']:
        try:
            datetime.strptime(transaction['date'], '%Y-%m-%d')  # Validate date format
        except ValueError:
            pytest.fail("Transaction date is not in YYYY-MM-DD format")
