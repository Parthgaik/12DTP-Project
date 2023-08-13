from flask import Flask,render_template
# Importing sqlite3
import sqlite3

# Connect database (F1.db), get cursor, execute cursor with statement and id, fetchall() results and return results
def connect_database_id(statement, id):
    conn = sqlite3.connect("F1.db")
    cursor = conn.cursor()
    cursor.execute(statement, id)
    results = cursor.fetchall()
    conn.close()
    return results

#
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
    cursor.execute("SELECT id, name, Image FROM Drivers")
    drivers = connect_database("SELECT id, name, Image FROM Drivers")
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
    driver = connect_database_id("SELECT * FROM Drivers WHERE id =?", (id,))
    return render_template("driver.html", title="Driver", driver=driver)
    

@app.route('/teams/<int:id>')
def team(id):
    teams = connect_database_id("SELECT * FROM Teams WHERE id =?", (id,))
    return render_template("team.html", title="Team", teams=teams)


@app.route('/signup')
def signup():
    return render_template("Signup.html", title="Sign up")


if __name__ == "__main__":
    app.run(debug=True)