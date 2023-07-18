from flask import Flask,render_template
import sqlite3


app = Flask (__name__)


#Home Route
@app.route('/')
def home():
    return render_template("home.html",title = "Home")

@app.route('/drivers')
def drivers():
    conn =sqlite3.connect("F1.db")
    cursor =conn.cursor()
    cursor.execute("SELECT * FROM Drivers")
    drivers = cursor.fetchall()
    return render_template("drivers.html", title = "Drivers", drivers = drivers)











if __name__ == "__main__":
    app.run(debug =True)