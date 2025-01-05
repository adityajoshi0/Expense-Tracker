from flask import Flask, render_template, request, redirect, url_for
from collections import defaultdict
import datetime

app = Flask(__name__)

# In-memory expense storage using a list for ordered expenses
expenses = []

# Dictionary to categorize expenses
expenses_by_category = defaultdict(list)

@app.route('/')
def index():
    return render_template('index.html', expenses=expenses)

@app.route('/add', methods=['POST'])
def add_expense():
    category = request.form['category']
    amount = float(request.form['amount'])
    date = request.form['date']
    description = request.form['description']
    
    # Create an expense entry
    expense = {
        'category': category,
        'amount': amount,
        'date': datetime.datetime.strptime(date, "%Y-%m-%d").date(),
        'description': description
    }
    
    # Add to list of expenses
    expenses.append(expense)
    
    # Categorize the expense using a dictionary
    expenses_by_category[category].append(expense)

    return redirect(url_for('index'))

@app.route('/report')
def report():
    # Sort expenses by date for reporting
    sorted_expenses = sorted(expenses, key=lambda x: x['date'])
    
    # Calculate total spent per category
    total_spent_by_category = {cat: sum(exp['amount'] for exp in exp_list) 
                                for cat, exp_list in expenses_by_category.items()}
    
    return render_template('report.html', sorted_expenses=sorted_expenses, 
                           total_spent_by_category=total_spent_by_category)

if __name__ == '__main__':
    app.run(debug=True)
