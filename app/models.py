# models.py
from datetime import datetime
from . import db


class Category(db.Model):
    """
    Model representing a spending category.

    Attributes:
        id (int): Primary key, unique identifier for the category.
        name (str): Name of the category, must be unique and not nullable.
    """
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


class Transaction(db.Model):
    """
    Model representing a financial transaction.

    Attributes:
        id (int): Primary key, unique identifier for the transaction.
        date (datetime.date): Date of the transaction, defaults to current date.
        amount (float): Amount spent in the transaction, cannot be null.
        category_id (int): Foreign key linking to the category of the transaction.
        notes (str): Additional notes about the transaction (optional).
        category (Category): Relationship to the Category model.
    """
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    notes = db.Column(db.String(200))

    # Relationship with Category model
    category = db.relationship('Category', backref=db.backref('transactions', lazy=True))
