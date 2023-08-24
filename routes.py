# Importing flask, and render template
from flask import Flask, render_template
# Importing sqlite3
import sqlite3

app = Flask(__name__)


def seat_sort(seat):
    return seat[2]


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
    # Initial sort
    seats.sort(key=seat_sort)
    # Sorts the information again and checks for when the driver has left and come back to a new team on the same year
    if len(seats) >= 2:
        last_num = seats[0][2]
        for i in range(1, len(seats)):
            if last_num == seats[i][2]:
                if seats[i-1][3] is None:
                    seats[i], seats[i-1] = seats[i-1], seats[i]
            last_num = seats[i][2]
    # Merges both the name and image of the associated team into the associated tuple of seats
    for i in range(len(seats)):
        team = connect_database_id("SELECT name, Image FROM Teams WHERE id =?", (seats[i][1],))
        seats[i] += (team[0][0], team[0][1])
    print(seats)
    return render_template("driver.html", title="Driver", driver=driver, seats=seats)


# Teams route, gets a specific team's entry with the given id, then renders teams.html
@app.route('/teams/<int:id>')
def team(id):
    teams = connect_database_id("SELECT * FROM Teams WHERE id =?", (id,))
    return render_template("team.html", title="Team", teams=teams)


if __name__ == "__main__":
    app.run(debug=True)