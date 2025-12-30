import sqlite3
import csv
import datetime
import matplotlib.pyplot as plt

con = sqlite3.connect("Expense.db")
cur = con.cursor()

cur.execute(""" CREATE TABLE IF NOT EXISTS expense (date TEXT, category TEXT, note TEXT, amount INTEGER) """)


def add_expense(date=None, category="General", note="Usual", amount=0):
    if date is None or date.strip() == "":
        date = datetime.date.today()

    ADD_QUERY = "INSERT INTO expense (date, category, note, amount) VALUES (?, ?, ?, ?)"
    cur.execute(ADD_QUERY, (date.isoformat(), category, note, amount))
    con.commit()
    print(f"Expense Added! \n Date is {date} \n Category is {category} \n Note is {note} \n Amount is {amount}")

def show_summary():
    SUMMARY_QUERY = "SELECT category, SUM(amount) FROM expense GROUP BY category"
    cur.execute(SUMMARY_QUERY)
    rows = cur.fetchall()
    print("\n--- Expense Summary by Category ---")
    for row in rows:
        print(f"Category: {row[0]} Total Amount: {row[1]}/")


def max_expense_category():
    print("\n Most money spent on:")
    MAX_QUERY = "SELECT category, SUM(amount) as total From expense GROUP BY category ORDER BY total DESC LIMIT 1"
    cur.execute(MAX_QUERY)
    max_row = cur.fetchone()
    if max_row:
        print(f"Category: {max_row[0]} Amount: {max_row[1]}/")

def monthly_expense_report(year, month):
    REPORT_QUERY = "SELECT date, category, note, amount FROM expense WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ?"
    cur.execute(REPORT_QUERY, (str(year), f"{month:02d}"))
    rows = cur.fetchall()
    print(f"\n--- Expense Report for {year}-{month:02d} ---")
    for row in rows:
        print(f"Date: {row[0]} Category: {row[1]} Note: {row[2]} Amount: {row[3]}/")

def show_chart(cur):
    category_totals = {}
    CHART_QUERY = "SELECT category, amount FROM expense"
    cur.execute(CHART_QUERY)
    rows = cur.fetchall()

    for row in rows:
        category = row[0]
        amount = row[1] 
        
        category_totals[category] = category_totals.get(category, 0) + amount

    if not category_totals:
        print("No expenses to show chart!")
        return
    
    labels = list(category_totals.keys())
    sizes = list(category_totals.values())

    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title("Expenses by Category")
    plt.axis('equal')  
    plt.show()

def menu():
    while True:
        print("\n--- Expense Tracker ---")
        print("1. Add Expense")
        print("2. Show Summary")
        print("3. Show Chart")
        print("4. Monthly Expense Report")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            category = input("Enter category: ").lower()
            amount = int(input("Enter amount: "))
            datetime = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
            note = input("Enter note: ")
            add_expense(date=datetime, category=category, note=note, amount=amount)

        elif choice == "2":
            show_summary()
            max_expense_category()

        elif choice == "3":
            show_chart(cur=cur)

        elif choice == "4":
            year = int(input("Enter Year (YYYY): "))
            month = int(input("Enter Month (1-12): "))
            monthly_expense_report(year=year, month=month)

        elif choice == "5":
            print("Goodbye!")
            break
            cur.close()

        else:
            print("Invalid choice, try again.")
            

menu()