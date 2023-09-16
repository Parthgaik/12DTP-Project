# # Importing flask, render template and abort
# from flask import Flask, render_template, abort
# # Importing sqlite3
# import sqlite3

# app = Flask(__name__)


# # Error Function
# @app.errorhandler(404)
# def not_found(e):
#     # Defining function
#     return render_template("404.html", title="Error"), 404


# # Getting the 'joined' information from seats table to use in driver route to
# # display when the driver joined the team.
# #hello
# def seat_sort(seat):
#     return seat[2]


# # Connect database (F1.db), get cursor, execute cursor with statement and id,
# # fetchall() results and return results
# def connect_database(statement, id=None):
#     # Connects my F1 Database with sqlite3 and stores as name conn
#     conn = sqlite3.connect("F1.db")
#     # Connection creates cursor, and stored as name cursor
#     cursor = conn.cursor()

#     # If the function recieves an id execute (statement, id), else execute (statement)
#     # This if function is here when we are trying to find one thing or many things,
#     # for example when clicking drivers, it doesnt take a specific id whereas when clicking on a driver it does
#     if id is not None:
#         cursor.execute(statement, id)
#     else:
#         cursor.execute(statement)
#     # Get every result, then close connection
#     results = cursor.fetchall()
#     conn.close()
#     return results


# # # Connects the databse and then executes the statement, fetches all the results, closes the connection and then returns the values from the results.
# # def connect_database(statement):
# #     conn = sqlite3.connect("F1.db")
# #     cursor = conn.cursor()
# #     cursor.execute(statement)
# #     results = cursor.fetchall()
# #     conn.close()
# #     return results

# # NANDINI IS CUTE

# # Home Route, takes the user to the home page
# @app.route('/')
# def home():
#     return render_template("home.html", title="Home", pagename="homepage")


# # Drivers Route, gets the id, name and image from drivers and delivers it to the all_drivers.html
# @app.route('/all_drivers')
# def all_drivers():
#     drivers = connect_database("SELECT id, name, Image FROM Drivers")
#     return render_template("all_drivers.html", title="Drivers", drivers=drivers, pagename = "all_drivers_page")


# # Teams Route, gets everything from teams and then delivers it to the teams.html
# @app.route('/all_teams')
# def teams():
#     all_teams = connect_database("SELECT * FROM Teams")
#     print("hi")
#     return render_template("teams.html", title="Teams", all_teams=all_teams, pagename="all_teams")


# # Seats Route, gets all everythig from seats and then delivers it to the seats html
# @app.route('/seats')
# def seats():
#     seat = connect_database("SELECT * FROM Seat")
#     return render_template("seats.html", title="Seats", seat=seat)


# # Driver route, gets a specific driver's entry with the given id, then renders driver.html
# @app.route('/drivers/<int:id>')
# def driver(id):
#     seats = connect_database("SELECT * FROM Seat WHERE did = ?", (id,))
#     driver = connect_database("SELECT * FROM Drivers WHERE id =?", (id,))
#     if driver and seats:
#         # Initial sort
#         seats.sort(key=seat_sort)

#         # Sorts the information again and checks for when the driver has left and come back to a new team on the same year
#         if len(seats) >= 2:
#             last_num = seats[0][2]
#             for i in range(1, len(seats)):
#                 if last_num == seats[i][2]:
#                     if seats[i-1][3] is None:
#                         seats[i], seats[i-1] = seats[i-1], seats[i]
#                 last_num = seats[i][2]
#         # Merges both the name and image of the associated team into the associated tuple of seats
#         for i in range(len(seats)):
#             team = connect_database("SELECT name, Image FROM Teams WHERE id =?", (seats[i][1],))
#             seats[i] += (team[0][0], team[0][1])
#         print(seats)
#         return render_template("driver.html", title="Driver", driver=driver, seats=seats)
#     else:
#         abort(404)


# # Teams route, gets a specific team's entry with the given id, then renders teams.html
# @app.route('/teams/<int:id>')
# def team(id):
#     if team:
#         teams = connect_database("SELECT * FROM Teams WHERE id =?", (id,))
#         return render_template("team.html", title="Team", teams=teams, pagename="team_single_image")
#     else:
#         abort(404)


# if __name__ == "__main__":
#     app.run(debug=True)






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