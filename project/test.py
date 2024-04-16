from flask import Flask, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'decentralized'
print(app.config)
# Initialize MySQL
mysql = MySQL(app)
print(mysql.connection)
@app.route('/')
def index():
    try:
        cursor = mysql.connection.cursor()
        # Example query: select all rows from a table
        query = "SELECT * FROM election"
        cursor.execute(query)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append(row)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500
    # finally:
    #     if cursor:
    #         cursor.close()

if __name__ == '__main__':
    app.run(debug=True)
