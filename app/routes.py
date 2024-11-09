# routes.py
from datetime import datetime
from typing import Union
from flask import Blueprint, request, jsonify, render_template, Response
from .models import Category, Transaction
from . import db
import logging

logging.basicConfig(level=logging.INFO)

# Create a Blueprint instance
main = Blueprint('main', __name__)


@main.app_errorhandler(404)
def not_found_error(error) -> tuple:
    return jsonify({'error': 'Resource not found'}), 404


@main.app_errorhandler(500)
def internal_error(error) -> tuple:
    logging.error('An internal error occurred: %s', error)
    return jsonify({'error': 'An internal error occurred'}), 500


@main.route('/categories', methods=['POST'])
def create_category() -> Union[Response, tuple]:
    """
    Create a new spending category.

    Expects:
        JSON or form data with a 'name' field for the category name.

    Returns:
        Union[Response, tuple]: A JSON response with a success message and list of categories, or an error message.
    """
    logging.info('Received request to create category')
    data = request.get_json() if request.is_json else request.form
    name = data.get('name')

    if not name:
        logging.warning('Category name is missing')
        return jsonify({'error': 'Category name is required'}), 400

    if Category.query.filter_by(name=name).first():
        logging.warning('Category already exists')
        return jsonify({'error': 'Category already exists'}), 400

    new_category = Category(name=name)
    db.session.add(new_category)
    db.session.commit()
    logging.info(f'Category {name} created successfully')

    if request.is_json:
        return jsonify({
            'message': 'Category created successfully',
            'category': {
                'id': new_category.id,
                'name': new_category.name
            }
        }), 201
    else:
        categories = Category.query.all()
        logging.info('Rendering template for category creation response')
        return render_template('categories.html', categories=categories), 200


@main.route('/categories', methods=['GET'])
def get_categories() -> tuple:
    """
    Retrieve all spending categories.

    Returns:
        tuple: A JSON response with a list of all categories.
    """
    logging.info('Retrieving categories')
    limit = request.args.get('limit', 10, type=int)  # Default limit is 10
    offset = request.args.get('offset', 0, type=int)  # Default offset is 0
    categories = Category.query.offset(offset).limit(limit).all()
    category_list = [{'id': cat.id, 'name': cat.name} for cat in categories]
    return jsonify({'categories': category_list}), 200


@main.route('/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id: int) -> tuple:
    """
    Update the name of a specific category.

    Args:
        category_id (int): The ID of the category to update.

    Returns:
        tuple: A JSON response with a success message and updated category or an error message.
    """
    logging.info(f'Received request to update category with ID {category_id}')
    data = request.get_json()
    new_name = data.get('name')

    if not new_name:
        logging.warning('New category name is required')
        return jsonify({'error': 'New category name is required'}), 400

    category = db.session.get(Category, category_id)

    if not category:
        logging.warning('New category name is required')
        return jsonify({'error': 'Category not found'}), 404

    category.name = new_name
    db.session.commit()

    logging.info(f'Category with ID {category_id} updated successfully')
    return jsonify(
        {'message': 'Category updated successfully',
         'category': {'category_id': category.id, 'name': category.name}}), 200


@main.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id: int) -> tuple:
    """
    Delete a specific category.

    Args:
        category_id (int): The ID of the category to delete.

    Returns:
        tuple: A JSON response with a success message and updated list of categories, or an error message.
    """
    logging.info(f'Received request to delete category with ID {category_id}')
    category = db.session.get(Category, category_id)

    if not category:
        logging.error('Category not found')
        return jsonify({'error': 'Category not found'}), 404

    if category.transactions:  # `category.transactions` uses the backref from the relationship in the models
        return jsonify({
            'error': 'Category cannot be deleted because it has associated transactions.'
        }), 400

    db.session.delete(category)
    db.session.commit()

    categories = Category.query.all()
    category_list = [{'id': cat.id, 'name': cat.name} for cat in categories]
    return jsonify({'message': 'Category deleted successfully', 'categories': category_list}), 200


@main.route('/transactions', methods=['POST'])
def create_transaction() -> Union[Response, tuple]:
    """
    Create a new transaction.

    Expects:
        JSON or form data with 'date', 'amount', 'category_id', and optionally 'notes'.

    Returns:
        Union[Response, tuple]: A JSON response or rendered template with success information.
    """
    data = request.get_json() if request.is_json else request.form

    date_str = data.get('date')
    amount = data.get('amount')
    category_id = data.get('category_id')
    notes = data.get('notes', '')

    if not date_str or not amount or not category_id:
        return jsonify({'error': 'Date, amount, and category_id are required fields'}), 400

    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    if not db.session.get(Category, category_id):
        return jsonify({'error': 'Category not found'}), 404

    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError('Amount must be positive')
    except ValueError:
        return jsonify({'error': 'Invalid amount. Must be a positive number'}), 400

    new_transaction = Transaction(date=date, amount=amount, category_id=category_id, notes=notes)
    db.session.add(new_transaction)
    db.session.commit()

    if request.is_json:
        return jsonify({
            'message': 'Transaction created successfully',
            'transaction': {
                'id': new_transaction.id,
                'date': new_transaction.date.isoformat(),
                'amount': new_transaction.amount,
                'category_id': new_transaction.category_id,
                'notes': new_transaction.notes
            }
        }), 201
    else:
        return render_template('transaction_result.html', transaction=new_transaction), 200


@main.route('/transactions', methods=['GET'])
def get_transactions() -> tuple:
    """
    Retrieve all transactions.

    Returns:
        tuple: A JSON response with a list of all transactions.
    """
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)
    transactions = Transaction.query.offset(offset).limit(limit).all()
    transaction_list = [
        {
            'id': txn.id,
            'date': txn.date.isoformat(),
            'amount': txn.amount,
            'category': txn.category.name,
            'notes': txn.notes
        }
        for txn in transactions
    ]
    return jsonify({'transactions': transaction_list}), 200


@main.route('/transactions/<int:transaction_id>', methods=['PUT'])
def update_transaction(transaction_id: int) -> tuple:
    """
    Update a specific transaction.

    Args:
        transaction_id (int): The ID of the transaction to update.

    Returns:
        tuple: A JSON response with a success message, or an error message if the transaction or category is not found.
    """
    data = request.get_json()
    transaction = db.session.get(Transaction, transaction_id)

    if not transaction:
        return jsonify({'error': 'Transaction not found'}), 404

    if 'date' in data:
        try:
            transaction.date = datetime.strptime(data['date'], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400
    transaction.amount = data.get('amount', transaction.amount)
    transaction.category_id = data.get('category_id', transaction.category_id)
    transaction.notes = data.get('notes', transaction.notes)

    if data.get('category_id') and not db.session.get(Category, transaction.category_id):
        return jsonify({'error': 'Category not found'}), 404

    db.session.commit()

    return jsonify({'message': 'Transaction updated successfully'}), 200


@main.route('/transactions/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id: int) -> tuple:
    """
    Delete a specific transaction.

    Args:
        transaction_id (int): The ID of the transaction to delete.

    Returns:
        tuple: A JSON response with a success message, or an error message if the transaction is not found.
    """
    transaction = db.session.get(Transaction, transaction_id)

    if not transaction:
        return jsonify({'error': 'Transaction not found'}), 404

    db.session.delete(transaction)
    db.session.commit()

    return jsonify({'message': 'Transaction deleted successfully'}), 200


@main.route('/summary', methods=['GET'])
def get_summary():
    summary = db.session.query(
        Category.name,
        db.func.sum(Transaction.amount).label('total_spent')
    ).join(Transaction).group_by(Category.name).all()

    summary_data = [{'category': item[0], 'total_spent': item[1]} for item in summary]
    return jsonify({'summary': summary_data}), 200


@main.route('/categories-page', methods=['GET'])
def get_categories_page():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)


@main.route('/transactions-page', methods=['GET'])
def get_transactions_page():
    categories = Category.query.all()
    transactions = Transaction.query.all()
    return render_template('transactions.html', categories=categories, transactions=transactions)


@main.route('/')
def home():
    """
    Render the homepage or redirect to categories page.

    Returns:
        Response: A rendered template or redirect.
    """
    # Option 1: Redirect to categories page
    return render_template('index.html')  # Or use redirect(url_for('main.get_categories_page'))


@main.route('/transactions', methods=['GET'])
def get_transactions() -> tuple:
    """
    Retrieve all transactions with optional search and filtering.

    Query Parameters:
        category_id (int, optional): Filter by category ID.
        start_date (str, optional): Filter transactions from this date (format: YYYY-MM-DD).
        end_date (str, optional): Filter transactions up to this date (format: YYYY-MM-DD).
        min_amount (float, optional): Minimum amount for filtering.
        max_amount (float, optional): Maximum amount for filtering.

    Returns:
        tuple: A JSON response with a list of filtered transactions.
    """
    category_id = request.args.get('category_id', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    min_amount = request.args.get('min_amount', type=float)
    max_amount = request.args.get('max_amount', type=float)

    query = Transaction.query

    if category_id:
        query = query.filter_by(category_id=category_id)
    if start_date:
        query = query.filter(Transaction.date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query = query.filter(Transaction.date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    if min_amount is not None:
        query = query.filter(Transaction.amount >= min_amount)
    if max_amount is not None:
        query = query.filter(Transaction.amount <= max_amount)

    transactions = query.all()
    transaction_list = [
        {
            'id': txn.id,
            'date': txn.date.isoformat(),
            'amount': txn.amount,
            'category': txn.category.name,
            'notes': txn.notes
        }
        for txn in transactions
    ]
    return jsonify({'transactions': transaction_list}), 200
