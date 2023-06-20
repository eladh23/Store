from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import sqlite3

con = sqlite3.connect("Store.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS Product(Id, Name, Category, Price, Stock)")
con.commit()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Store.db'
db = SQLAlchemy(app)
CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
    app.run(port=9000, debug=True)
