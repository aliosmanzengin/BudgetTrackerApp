# tests/test_categories.py
def test_create_category(test_client):
    # Test creating a new category
    response = test_client.post('/categories', json={'name': 'Groceries'})
    assert response.status_code == 201
    assert response.json['message'] == 'Category created successfully'
    assert 'categories' in response.json

    # Test creating a duplicate category
    response = test_client.post('/categories', json={'name': 'Groceries'})
    assert response.status_code == 400
    assert response.json['error'] == 'Category already exists'


def test_get_categories(test_client):
    # Test retrieving all categories
    response = test_client.get('/categories')
    assert response.status_code == 200
    assert 'categories' in response.json


def test_update_category(test_client):
    # Test updating a category
    response = test_client.post('/categories', json={'name': 'Books'})
    category_id = response.json['categories'][0]['id']

    response = test_client.put(f'/categories/{category_id}', json={'name': 'Updated Books'})
    assert response.status_code == 200
    assert response.json['message'] == 'Category updated successfully'
    assert response.json['category']['name'] == 'Updated Books'


def test_delete_category(test_client):
    # Test deleting a category
    response = test_client.post('/categories', json={'name': 'Electronics'})
    category_id = response.json['categories'][0]['id']

    response = test_client.delete(f'/categories/{category_id}')
    assert response.status_code == 200
    assert response.json['message'] == 'Category deleted successfully'