from flask import Flask, jsonify, redirect, render_template, request, session, url_for, g
import sqlite3



app = Flask(__name__)

app.config["SECRET_KEY"] = "7sl0Hs1ETuodotD9yv9TAIwYAdICiH"

def connect_db():
   sql = sqlite3.connect("data.db")
   #convert return data in tuples to dict
   sql.row_factory = sqlite3.Row
   return sql

def get_db():
    if not hasattr(g, "sqlite_db"):
        g.sqlite_db = connect_db()
        return g.sqlite_db
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "sqlite_db"):
        g.sqlite_db.close()

@app.route("/")
def index():
    # put application's code here
    session.pop("name", None)
    return "<h1>Hello World!</h1>"


# <name> should be the same as value passed to the function
@app.route("/home", methods=["POST", "GET"], defaults={"name": "Default"})
@app.route("/home/<string:name>", methods=["GET", "POST"])
def home(name):
    session["name"] = name

    db = get_db()
    cursor = db.execute('select id, name, location from users')
    results = cursor.fetchall()

    return render_template(
        "home.html",
        name=name,
        display=True,
        food=["jollof", "pizza", "banku"],
        listofdictionaries=[{"name": "John"}, {"name": "jane"}],results=results
    )


@app.route("/query")
def query():
    name: str | None = request.args.get("name")
    location: str | None = request.args.get("location")
    return "<h1>Hi {},You are from {}. You are on the query page </h1>".format(
        name, location
    )


@app.route("/theform", methods=["POST", "GET"])
def theform():

    if request.method == "GET":
        return render_template("form.html")
    else:
        name: str | None = request.form["name"]
        location: str | None = request.form["location"]

        db = get_db()
        db.execute('insert into users (name, location) values (?, ?)', (name, location))
        db.commit()

        return "Hello {}, You are from {}. You have successfully submitted the form </h1>".format(
            name, location
        )


# @app.route("/process", methods=["POST"])
# def process():
#     name: str | None = request.form["name"]
#     location: str | None = request.form["location"]
#     return 'Hello {}, You are from {}. You have successfully submitted the form </h1>'.format(name, location)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return """
        <form method="POST" action="/login">
            <input type="text" name="username">
            <input type="password" name="password">
            <input type="submit" value="Submit" />
        </form>
        """
    else:
        name: str | None = request.form["username"]
        return redirect(url_for("home", name=name))


@app.route("/processjson", methods=["POST"])
def processjson():
    # get json from request
    data = request.get_json()

    name = data["name"]
    location = data["location"]
    randomList = data["randomlist"]

    return jsonify(
        {
            "result": "success",
            "name": name,
            "location": location,
            "randomkeyinlist": randomList[1],
        }
    )

@app.route('/viewresults')
def viewresults():
    db = get_db()
    cursor = db.execute('select id, name, location from users')
    results = cursor.fetchall()
    return  "<h1>The id is {}, The name is {}, The location is {}</h1>".format(results[1]['id'], results[1]["name"], results[1]["location"])


@app.route("/json")
def json():
    if "name" in session:
        name = session["name"]
    else:
        name = "Not in session"
    return jsonify({"key": "value", "listkey": [1, 2, 3, 4], "name": name})


if __name__ == "__main__":
    app.run()
