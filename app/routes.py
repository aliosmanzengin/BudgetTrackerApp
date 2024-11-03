from datetime import datetime
from flask import Blueprint, request, jsonify
from .models import Category, Transaction
from . import db

# Create a Blueprint instance
main = Blueprint('main', __name__)


@main.route('/categories', methods=['POST'])
def create_category() -> tuple:
    """
    Create a new spending category.

    Expects:
        JSON data with a 'name' field for the category name.

    Returns:
        tuple: A JSON response with a success message and list of categories, or an error message.
    """
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({'error': 'Category name is required'}), 400

    if Category.query.filter_by(name=name).first():
        return jsonify({'error': 'Category already exists'}), 400

    new_category = Category(name=name)
    db.session.add(new_category)
    db.session.commit()

    categories = Category.query.all()
    category_list = [{'id': cat.id, 'name': cat.name} for cat in categories]
    return jsonify({'message': 'Category created successfully', 'categories': category_list}), 201


@main.route('/categories', methods=['GET'])
def get_categories() -> tuple:
    """
    Retrieve all spending categories.

    Returns:
        tuple: A JSON response with a list of all categories.
    """
    categories = Category.query.all()
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
    data = request.get_json()
    new_name = data.get('name')

    if not new_name:
        return jsonify({'error': 'New category name is required'}), 400

    category = db.session.get(Category, category_id)

    if not category:
        return jsonify({'error': 'Category not found'}), 404

    category.name = new_name
    db.session.commit()

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
    category = db.session.get(Category, category_id)

    if not category:
        return jsonify({'error': 'Category not found'}), 404

    db.session.delete(category)
    db.session.commit()

    categories = Category.query.all()
    category_list = [{'id': cat.id, 'name': cat.name} for cat in categories]
    return jsonify({'message': 'Category deleted successfully', 'categories': category_list}), 200


@main.route('/transactions', methods=['POST'])
def create_transaction() -> tuple:
    """
    Create a new transaction.

    Expects:
        JSON data with 'date', 'amount', 'category_id', and optionally 'notes'.

    Returns:
        tuple: A JSON response with a success message and created transaction, or an error message.
    """
    data = request.get_json()
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

    new_transaction = Transaction(date=date, amount=amount, category_id=category_id, notes=notes)
    db.session.add(new_transaction)
    db.session.commit()

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


@main.route('/transactions', methods=['GET'])
def get_transactions() -> tuple:
    """
    Retrieve all transactions.

    Returns:
        tuple: A JSON response with a list of all transactions.
    """
    transactions = Transaction.query.all()
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
