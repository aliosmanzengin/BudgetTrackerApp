# app/routes.py
from datetime import datetime
from flask import Blueprint, request, jsonify
from .models import Category, Transaction
from . import db  # Import db from __init__.py

# Create a Blueprint instance
main = Blueprint('main', __name__)


# Route to create a new category
@main.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    name = data.get('name')

    # Check if 'name' is provided in the JSON data
    if not name:
        return jsonify({'error': 'Category name is required'}), 400  # Return 400 Bad Request if name is missing

    # Check if the category already exists
    if Category.query.filter_by(name=name).first():
        return jsonify({'error': 'Category already exists'}), 400

    # Create a new category and add it to the database
    new_category = Category(name=name)
    db.session.add(new_category)
    db.session.commit()

    # Return the updated category list
    categories = Category.query.all()
    category_list = [{'id': cat.id, 'name': cat.name} for cat in categories]
    return jsonify({'message': 'Category created successfully', 'categories': category_list}), 201


# Route to retrieve all categories
@main.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    category_list = [{'id': cat.id, 'name': cat.name} for cat in categories]
    return jsonify({'categories': category_list}), 200


@main.route('/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    # Get the new category name from the request data
    data = request.get_json()
    new_name = data.get('name')

    # Check if 'name' is provided in the JSON data
    if not new_name:
        return jsonify({'error': 'New category name is required'}), 400  # Return 400 if name is missing

    # Find the category by ID
    category = Category.query.get(category_id)

    # If category not found, return an error
    if not category:
        return jsonify({'error': 'Category not found'}), 404

    # Update the category name
    category.name = new_name
    db.session.commit()

    return jsonify(
        {'message': 'Category updated successfully',
         'category': {'category_id': category.id, 'name': category.name}}), 200


@main.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    # Find the category by ID
    category = Category.query.get(category_id)

    # If category not found, return an error
    if not category:
        return jsonify({'error': 'Category not found'}), 404

    # Delete the category from the database
    db.session.delete(category)
    db.session.commit()

    categories = Category.query.all()
    category_list = [{'id': cat.id, 'name': cat.name} for cat in categories]
    return jsonify({'message': 'Category deleted successfully', 'categories': category_list}), 200


@main.route('/transactions', methods=['POST'])
def create_transaction():
    # Get JSON data from the request
    data = request.get_json()
    date_str = data.get('date')
    amount = data.get('amount')
    category_id = data.get('category_id')
    notes = data.get('notes', '')  # Optional field with default empty string

    # Validate required fields
    if not date_str or not amount or not category_id:
        return jsonify({'error': 'Date, amount, and category_id are required fields'}), 400

    # Convert the date string to a Python date object
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()  # Convert to a date object
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    # Check if the category exists
    if not Category.query.get(category_id):
        return jsonify({'error': 'Category not found'}), 404

    # Create the new transaction
    new_transaction = Transaction(date=date, amount=amount, category_id=category_id, notes=notes)
    db.session.add(new_transaction)
    db.session.commit()

    # Return the created transaction
    return jsonify({
        'message': 'Transaction created successfully',
        'transaction': {
            'id': new_transaction.id,
            'date': new_transaction.date,
            'amount': new_transaction.amount,
            'category_id': new_transaction.category_id,
            'notes': new_transaction.notes
        }
    }), 201


@main.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    transaction_list = [
        {
            'id': txn.id,
            'date': txn.date,
            'amount': txn.amount,
            'category': txn.category.name,  # Accessing related category name
            'notes': txn.notes
        }
        for txn in transactions
    ]
    return jsonify({'transactions': transaction_list}), 200


@main.route('/transactions/<int:transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    # Get JSON data from the request
    data = request.get_json()
    transaction = Transaction.query.get(transaction_id)

    # If transaction not found, return an error
    if not transaction:
        return jsonify({'error': 'Transaction not found'}), 404

    # Update fields if provided in the request data
    transaction.date = data.get('date', transaction.date)
    transaction.amount = data.get('amount', transaction.amount)
    transaction.category_id = data.get('category_id', transaction.category_id)
    transaction.notes = data.get('notes', transaction.notes)

    # Validate category if category_id was updated
    if data.get('category_id') and not Category.query.get(transaction.category_id):
        return jsonify({'error': 'Category not found'}), 404

    db.session.commit()

    return jsonify({'message': 'Transaction updated successfully'}), 200


@main.route('/transactions/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    transaction = Transaction.query.get(transaction_id)

    # If transaction not found, return an error
    if not transaction:
        return jsonify({'error': 'Transaction not found'}), 404

    # Delete the transaction from the database
    db.session.delete(transaction)
    db.session.commit()

    return jsonify({'message': 'Transaction deleted successfully'}), 200
