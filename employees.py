import sqlite3

def query_employees():
    # Connect to the database file
    conn = sqlite3.connect('hr.db')
    cursor = conn.cursor()

    # Write your SQL query
    query = "SELECT id, name, department, designation, salary, location, hire_date FROM employees"

    try:
        cursor.execute(query)  # Execute the query
        rows = cursor.fetchall()  # Fetch all results

        # Print the results row by row
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Department: {row[2]}, Designation: {row[3]}, Salary: ${row[4]}, Location: {row[5]}, Hire Date: {row[6]}")

    except Exception as e:
        print("Error querying database:", e)

    finally:
        conn.close()  # Close the connection

if __name__ == "__main__":
    query_employees()
