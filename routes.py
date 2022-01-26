
from app import app
from flask import render_template, request, redirect
import messages, users, topics

# @app.route("/")
# def index():
#     list = messages.get_list()
#     return render_template("index.html", count=len(list), messages=list)

@app.route("/")
def index():
    list = topics.get_list()
    return render_template("index.html", topics=list)

@app.route("/newtopic")
def newtopic():
    return render_template("newtopic.html")

@app.route("/newmessage")
def newmessage():
    return render_template("newmessage.html")

@app.route("/sendtopic", methods=["POST"])
def sentopic():
    name = request.form["topicname"]
    if topics.create_topic(name):
        return redirect("/")
    else:
        return render_template("error.html", message="Aiheen luonti epäonnistui")

@app.route("/sendmessage", methods=["POST"])
def sendmessage():
    content = request.form["content"]
    if messages.send(content):
        return redirect("/")
    else:
        return render_template("error.html", message="Viestin lähetys epäonnistui")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        admin = request.form["admin"]
        if admin == "False":
            admin = False
        else:
            admin = True
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.register(username, password1, admin):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")