# Importing flask, and render template
from flask import Flask, render_template
# Importing sqlite3
import sqlite3

app = Flask(__name__)


# Connect database (F1.db), get cursor, execute cursor with statement and id, fetchall() results and return results
def connect_database_id(statement, id):
    conn = sqlite3.connect("F1.db")
    cursor = conn.cursor()
    cursor.execute(statement, id)
    results = cursor.fetchall()
    conn.close()
    return results


# Connects the databse and then executes the statement, fetches all the results, closes the connection and then returns the values from the results.
def connect_database(statement):
    conn = sqlite3.connect("F1.db")
    cursor = conn.cursor()
    cursor.execute(statement)
    results = cursor.fetchall()
    conn.close()
    return results


# Home Route, takes the user to the home page
@app.route('/')
def home():
    return render_template("home.html", title="Home")


# Drivers Route, gets the id, name and image from drivers and delivers it to the all_drivers.html
@app.route('/all_drivers')
def all_drivers():
    drivers = connect_database("SELECT id, name, Image FROM Drivers")
    return render_template("all_drivers.html", title="Drivers", drivers=drivers)


# Teams Route, gets everything from teams and then delivers it to the teams.html
@app.route('/teams')
def teams():
    teams = connect_database("SELECT * FROM Teams")
    return render_template("teams.html", title="Teams", teams=teams)


# Seats Route, gets all everythig from seats and then delivers it to the seats html
@app.route('/seats')
def seats():
    seat = connect_database("SELECT * FROM Seat")
    return render_template("seats.html", title="Seats", seat=seat)


# Driver route, gets a specific driver's entry with the given id, then renders driver.html
@app.route('/drivers/<int:id>')
def driver(id):
    seats = connect_database_id("SELECT * FROM Seat WHERE did = ?", (id,))
    driver = connect_database_id("SELECT * FROM Drivers WHERE id =?", (id,))
    print(seats)
    ordered_entries = []
    for i in range(len(seats)):
        ordered_entries.append((int(seats[i][2])), i)
    ordered_entries.sort()
    print(ordered_entries)
    for i in seats:
        team = connect_database_id("SELECT * FROM Teams WHERE id =?", (i[1],))

    return render_template("driver.html", title="Driver", driver=driver)


# Teams route, gets a specific team's entry with the given id, then renders teams.html
@app.route('/teams/<int:id>')
def team(id):
    teams = connect_database_id("SELECT * FROM Teams WHERE id =?", (id,))
    return render_template("team.html", title="Team", teams=teams)


if __name__ == "__main__":
    app.run(debug=True)