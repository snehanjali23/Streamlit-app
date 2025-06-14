import sqlite3

def connect_db():
    return sqlite3.connect("hr.db")

def print_all_employees():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Department: {row[2]}, Designation: {row[3]}, Salary: ${row[4]}, Location: {row[5]}, Hire Date: {row[6]}")
    conn.close()

def print_avg_salary_by_department(department):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(salary) FROM employees WHERE department=?", (department,))
    avg_salary = cursor.fetchone()[0]
    print(f"Average Salary in {department}: ${avg_salary:.2f}")
    conn.close()

def print_highest_salary_and_employees(department):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(salary) FROM employees WHERE department=?", (department,))
    max_salary = cursor.fetchone()[0]
    cursor.execute("SELECT name FROM employees WHERE department=? AND salary=?", (department, max_salary))
    top_earners = cursor.fetchall()
    print(f"Highest Salary in {department}: ${max_salary}")
    print("Top Earning Employee(s):")
    for employee in top_earners:
        print(f"- {employee[0]} (${max_salary})")
    conn.close()

if __name__ == "__main__":
    print_all_employees()
    print()
    print_avg_salary_by_department("HR")
    print_highest_salary_and_employees("HR")
