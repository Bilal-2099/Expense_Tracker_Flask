from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import json

"""
Expense Tracker Flask app

Simple Flask application that stores expenses in a SQLite database using
SQLAlchemy. Routes:
 - `/` (GET, POST): add a new expense via form
 - `/show` (GET): show all expenses and a category breakdown
 - `/dashboard` (GET): alternate route to render the same dashboard view
 - `/clear` (POST): delete all expenses

The helper `add_expense_from_form` centralizes parsing and validation
of incoming form data before saving an Expense record.
"""

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Expense.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Expense(db.Model):
    """SQLAlchemy model representing a single expense entry.

    Fields:
    - id: primary key
    - category: short category name (e.g. Food)
    - amount: floating-point amount spent
    - date: expense date (stored as a Date)
    - note: optional free-text note
    """
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    note = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<Expense {self.category}>'


def add_expense_from_form(form):
    """Parse form data and create an Expense record.

    This helper converts strings to the correct types, provides
    sensible defaults for missing values, and commits the new
    record to the database. It returns the created `Expense`.
    """
    category = form.get('category')
    amount_str = form.get('amount')

    # Parse amount safely; default to 0.0 on missing/invalid input
    try:
        amount = float(amount_str) if amount_str else 0.0
    except ValueError:
        amount = 0.0

    # Parse date string into a date object; fallback to today
    date_str = form.get('date')
    if date_str:
        date_object = datetime.strptime(date_str, '%Y-%m-%d').date()
    else:
        date_object = datetime.utcnow().date()

    note = form.get('note')
    new_expense = Expense(category=category, amount=amount, date=date_object, note=note)
    db.session.add(new_expense)
    db.session.commit()
    return new_expense


@app.route('/', methods=['GET', 'POST'])
def home():
    """Home route: shows the add-expense form and handles submissions.

    On POST the form is processed by `add_expense_from_form` and the
    user is redirected to the `/show` page. On GET this returns the
    `index.html` template with the current list of expenses (used for
    any inline previews or counts if desired).
    """
    if request.method == 'POST':
        add_expense_from_form(request.form)
        return redirect(url_for('show'))

    # Provide all expenses to the template (not strictly necessary for
    # the add form but useful for small previews or testing).
    expenses = Expense.query.all()
    return render_template('index.html', new_expense=expenses)

@app.route('/show')
def show():
    """Show route: render expense history and category breakdown.

    Queries all expenses for the table and aggregates amounts by
    category for the chart. The aggregated lists (`labels_list` and
    `amounts_list`) are passed to the template where the chart is
    conditionally rendered only when data exists.
    """
    expenses = Expense.query.all()

    # Aggregate amounts by category for charting
    results = db.session.query(
        Expense.category,
        func.sum(Expense.amount)
    ).group_by(Expense.category).all()

    labels = [row[0] for row in results]
    amounts = [row[1] for row in results]

    return render_template('show.html',
                           new_expenses=expenses,
                           labels_list=labels,
                           amounts_list=amounts)

@app.route('/dashboard')
def dashboard():
    """Alternate dashboard route that renders the same template.

    This exists for direct navigation to `/dashboard` but serves the
    same `show.html` view populated with expenses and chart data.
    """
    expenses = Expense.query.all()

    # Aggregate amounts by category for charting
    results = db.session.query(
        Expense.category,
        func.sum(Expense.amount)
    ).group_by(Expense.category).all()

    labels = [row[0] for row in results]
    amounts = [row[1] for row in results]

    return render_template('show.html',
                           labels_list=labels,
                           amounts_list=amounts,
                           new_expenses=expenses)


@app.route('/clear', methods=['POST'])
def clear_expenses():
    """Delete all Expense records from the database.

    This route is triggered via a POST from the navbar button. It
    performs a bulk delete and commits the transaction. On error it
    rolls back and still redirects back to the `/show` page.
    """
    try:
        Expense.query.delete()
        db.session.commit()
    except Exception:
        db.session.rollback()
    return redirect(url_for('show'))

if __name__ == '__main__':
    app.run(debug=True)