# tests/test_routes.py
def test_get_categories_page(client):
    response = client.get('/categories-page')
    assert response.status_code == 200
    assert b'Categories' in response.data  # Check for a keyword on the page


def test_create_category_via_form(client):
    response = client.post('/categories', data={'name': 'Test Category'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Category created successfully' in response.data
