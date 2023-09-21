# Importing Flask, render template and abort from flask
from flask import Flask, render_template, abort
# Importing sqlite3
import sqlite3

app = Flask(__name__)


# Error Function
@app.errorhandler(404)
def not_found(e):
    # Defining function, taking the user to the 404.html page with title "Error" when an error occurs
    return render_template("404.html", title="Error", pagename="error"), 404


# Getting the 'joined' information from seats table to use in driver route to
# display when the driver joined the team.
def seat_sort(seat):
    return seat[2]


# Connect database (F1.db), get cursor, execute cursor with statement and id,
# fetchall() results and return results
def connect_database(statement, id=None):
    # Connects my F1 Database with sqlite3 and stores as name conn
    conn = sqlite3.connect("F1.db")
    # Connection creates cursor, and stored as name cursor
    cursor = conn.cursor()

    # If the function recieves an id execute (statement, id), else execute (statement)
    # This if function is here when we are trying to find one thing or many things,
    # for example when clicking drivers, it doesnt take a specific id whereas when clicking on a driver it does
    if id is not None:
        cursor.execute(statement, id)
    else:
        cursor.execute(statement)
    # Get every result, then close connection
    results = cursor.fetchall()
    conn.close()
    return results


# # This function retrieves the maximum 'id' value from the "Drivers" table in the database.
# def get_max_driver_id(driver):
#     """Execute an SQL query to find the maximum 'id'
#     value in the "Drivers" table."""
#     query = "SELECT MAX(id) FROM Drivers"
#     result = connect_database(query)
#     # Check if a valid result was obtained.
#     if result and result[0][0] is not None:
#         # If a valid maximum 'id' value exists, return it.
#         return result[0][0]
#     else:
#         # If there are no records in the "Drivers" table, return 0.
#         return 0


# # This function is the same as above, the only difference is the table name and so i have not commented it.
# def get_max_teams_id(teams):
#     query = "SELECT MAX(id) FROM Teams"
#     result = connect_database(query)
#     if result and result[0][0] is not None:
#         return result[0][0]
#     else:
#         return 0

def get_max_id(table_name):
    """Execute an SQL query to find the maximum 'id'
    value in the "Drivers" table."""
    result = connect_database("SELECT MAX(id) FROM " + table_name)
    # Check if a valid result was obtained.
    if result and result[0][0] is not None:
        # If a valid maximum 'id' value exists, return it.
        return result[0][0]
    else:
        # If there are no records in the "Drivers" table, return 0.
        return 0

# # Connects the databse and then executes the statement, fetches all the results, closes the connection and then returns the values from the results.
# def connect_database(statement):
#     conn = sqlite3.connect("F1.db")
#     cursor = conn.cursor()
#     cursor.execute(statement)
#     results = cursor.fetchall()
#     conn.close()
#     return results


# Home Route, takes the user to the home page
@app.route('/')
def home():
    return render_template("home.html", title="Home", pagename="homepage")


# Drivers Route, gets the id, name and image from drivers and delivers it to the all_drivers.html
@app.route('/all_drivers')
def all_drivers():
    drivers = connect_database("SELECT id, name, Image FROM Drivers")
    print(drivers, drivers[0])
    return render_template("all_drivers.html", title="Drivers", drivers=drivers, pagename="background_image")


# Teams Route, gets everything from teams and then delivers it to the teams.html
@app.route('/all_teams')
def teams():
    all_teams = connect_database("SELECT * FROM Teams")
    return render_template("teams.html", title="Teams", all_teams=all_teams, pagename="background_image")


# Seats Route, gets all everythig from seats and then delivers it to the seats html
@app.route('/seats')
def seats():
    seat = connect_database("SELECT * FROM Seat")
    return render_template("seats.html", title="Seats", seat=seat)


# Driver route, gets a specific driver's entry with the given id, then renders driver.html
@app.route('/drivers/<int:id>')
def driver(id):
    max_id = get_max_id("Drivers")
    if id > max_id:
        abort(404)
    seats = connect_database("SELECT * FROM Seat WHERE did = ?", (id,))
    driver = connect_database("SELECT * FROM Drivers WHERE id =?", (id,))
    if driver and seats:
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
            team = connect_database("SELECT name, Image FROM Teams WHERE id =?", (seats[i][1],))
            seats[i] += (team[0][0], team[0][1])
        print(seats)
        return render_template("driver.html", title="Driver", driver=driver, seats=seats, pagename="background_image")
    else:
        abort(404)


# Teams route, gets a specific team's entry with the given id, then renders teams.html
@app.route('/teams/<int:id>')
def team(id):
    max_id = get_max_id("Teams")
    if id > max_id:
        abort(404)
    teams = connect_database("SELECT * FROM Teams WHERE id =?", (id,))
    if teams:
        return render_template("team.html", title="Team", teams=teams, pagename="background_image")
    else:
        abort(404)


if __name__ == "__main__":
    app.run(debug=True)
