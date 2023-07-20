
from flask import Flask,render_template
#Importing sqlite3
import sqlite3


app = Flask (__name__)


#Home Route
@app.route('/')
def home():
    return render_template("home.html",title = "Home")


#Drivers Route
@app.route('/drivers')
def drivers():
    conn =sqlite3.connect("F1.db")
    cursor =conn.cursor()
    cursor.execute("SELECT * FROM Drivers")
    drivers = cursor.fetchall()
    return render_template("drivers.html", title = "Drivers", drivers = drivers)
#Teams Route
@app.route('/teams')
def teams():
    conn =sqlite3.connect("F1.db")
    cursor =conn.cursor()
    cursor.execute("SELECT * FROM Teams")
    teams = cursor.fetchall()
    return render_template("teams.html",title = "Teams", teams=teams)
#Seats Route
@app.route('/seats')
def seats():
    conn=sqlite3.connect("F1.db")
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM Seat")
    seat = cursor.fetchall()
    return render_template("seats.html",title = "Seats", seat=seat)












if __name__ == "__main__":
    app.run(debug =True)