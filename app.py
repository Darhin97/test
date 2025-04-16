from flask import Flask, jsonify, request, url_for, redirect, session, render_template

app = Flask(__name__)

app.config['SECRET_KEY'] = '7sl0Hs1ETuodotD9yv9TAIwYAdICiH'

@app.route("/")
def index():
    # put application's code here
    session.pop('name', None)
    return "<h1>Hello World!</h1>"


# <name> should be the same as value passed to the function
@app.route("/home", methods=["POST", "GET"], defaults={"name": "Default"})
@app.route("/home/<string:name>", methods=["GET", "POST"])
def home(name):
    session["name"] = name
    return "<h1>Hello {}, on the home page!</h1>".format(name)


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
        return render_template('form.html')
    else:
        name: str | None = request.form["name"]
        location: str | None = request.form["location"]
        return 'Hello {}, You are from {}. You have successfully submitted the form </h1>'.format(name, location)


# @app.route("/process", methods=["POST"])
# def process():
#     name: str | None = request.form["name"]
#     location: str | None = request.form["location"]
#     return 'Hello {}, You are from {}. You have successfully submitted the form </h1>'.format(name, location)

@app.route('/login', methods=["GET", 'POST'])
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
        return  redirect(url_for("home", name=name))


@app.route('/processjson', methods=['POST'])
def processjson():
    # get json from request
    data = request.get_json()

    name = data["name"]
    location = data["location"]
    randomList = data["randomlist"]

    return jsonify({"result": "success", "name": name, "location": location, "randomkeyinlist": randomList[1]})

@app.route("/json")
def json():
    if "name" in session:
        name = session["name"]
    else:
        name = "Not in session"
    return jsonify({"key": "value", "listkey": [1, 2, 3, 4], "name": name})


if __name__ == "__main__":
    app.run()
