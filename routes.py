from flask import Flask,render_template
# Importing sqlite3
import sqlite3

def connect_database(statement):
    conn = sqlite3.connect("F1.db")
    cursor = conn.cursor()
    cursor.execute(statement)
    results = cursor.fetchall()
    conn.close()
    return results

app = Flask(__name__)


# Home Route
@app.route('/')
def home():
    return render_template("home.html", title="Home")


# Drivers Route
@app.route('/all_drivers')
def all_drivers():
    conn = sqlite3.connect("F1.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM Drivers")
    drivers = connect_database("SELECT id, name FROM Drivers")
    return render_template("all_drivers.html", title="Drivers", drivers=drivers)


# Teams Route
@app.route('/teams')
def teams():
    conn = sqlite3.connect("F1.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Teams")
    teams = cursor.fetchall()
    return render_template("teams.html", title="Teams", teams=teams)
# Seats Route


@app.route('/seats')
def seats():
    conn = sqlite3.connect("F1.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Seat")
    seat = cursor.fetchall()
    return render_template("seats.html", title="Seats", seat=seat)


@app.route('/drivers/<int:id>')
def drivers(id):
    conn = sqlite3.connect("F1.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Drivers WHERE id =?", (id,))
    driver = cursor.fetchall()
    return render_template("driver.html", title="Driver", driver=driver)
    
@app.route('/teams/<int:id>')
def team(id):
    teams = connect_database(("SELECT * FROM Teams WHERE id =?", (id,)))
    return render_template("team.html", title="Team", teams=teams)

if __name__ == "__main__":
    app.run(debug=True)