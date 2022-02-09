from app import app
from flask import render_template, request, redirect, url_for, flash
import messages, users, topics, chains, validate

@app.route("/")
def index():
    list = topics.get_list()
    return render_template("index.html", topics=list, get_latest=messages.get_latest_message)

@app.route("/newtopic")
def newtopic():
    return render_template("newtopic.html")

@app.route("/newmessage/<int:id>")
def newmessage(id):
    return render_template("newmessage.html", chain_id=id)

@app.route("/newchain/<int:id>")
def newchain(id):
    return render_template("newchain.html", topic_id=id)

@app.route("/updatechain/<int:id>")
def updatechain(id):
    topic_id = topics.topic_id()
    return render_template("updatechain.html", id=id, t_id=topic_id)

@app.route("/updatemsg/<int:id>")
def updatemsg(id):
    c_id = chains.chain_id()
    return render_template("updatemsg.html", id=id, c_id=c_id)

@app.route("/topicarea/<int:id>")
def topicarea(id):
    topics.set_topic_id(id)
    header = topics.get_topic_name()
    list = chains.get_list()
    return render_template("topicarea.html", count = len(list), chains=list, header=header, topic_id=id)

@app.route("/chainarea/<int:id>")
def chainarea(id):
    chains.set_chain_id(id)
    header = chains.get_chain_name()
    topic_id = topics.topic_id()
    list = messages.get_list()
    return render_template("chainarea.html", count = len(list), messages=list, t_id=topic_id, header=header, chain_id=id)

@app.route("/sendtopic", methods=["POST"])
def sentopic():
    name = request.form["topicname"]
    if topics.create_topic(name):
        return redirect("/")
    flash("Aiheen luonti epäonnistui")
    return redirect("/newtopic")

@app.route("/sendchain", methods=["POST"])
def sendchain():
    topic_id = topics.topic_id()
    name = request.form["chainname"]
    content = request.form["msg"]
    if not validate.chain(name) or validate.msg(content): #täytyy tarkistaa jo tässä, ettei luo toista databaseen jos toinen ei ollekkaan validi
        flash("Otsikko tai aloitusviesti virheellinen")
        return redirect(url_for("newchain", id=topic_id))
    if chains.create_chain(name):
        if messages.send(content):
            return redirect(url_for("topicarea", id=topic_id))
    flash("Ketjun luonti epäonnistui")
    return redirect(url_for("newchain", id=topic_id))

@app.route("/sendmessage", methods=["POST"])
def sendmessage():
    chain_id = chains.chain_id()
    content = request.form["content"]
    if messages.send(content):
        return redirect(url_for("chainarea", id=chain_id))
    flash("Viestin lähetys epäonnistui")
    return redirect(url_for("newmessage", id=chain_id))

@app.route("/setupdatechain/<int:id>", methods=["POST"])
def setupdatechain(id):
    topic_id = topics.topic_id()
    chainname = request.form["chainname"]
    if chains.updatechain(chainname, id):
        flash("Ketjun muokkaaminen onnistui")
        return redirect(url_for("topicarea", id=topic_id))
    flash("Ketjun muokkaaminen epäonnistui")
    return redirect(url_for("updatechain", id=id))

@app.route("/setupdatemsg/<int:id>", methods=["POST"])
def setupdatemsg(id):
    chain_id = chains.chain_id()
    content = request.form["content"]
    if messages.updatemsg(content, id):
        flash("Viestin muokkaaminen onnistui")
        return redirect(url_for("chainarea", id=chain_id))
    flash("Viestin muokkaaminen epäonnistui")
    return redirect(url_for("updatechain", id=id))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        flash("Väärä tunnus tai salasana")
        return redirect("login")

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
        usernames = users.get_usernames()
        print(usernames)
        if password1 != password2:
            flash("Salasanat eroavat")
            return redirect("register")
        if username in usernames:
            flash("Käyttäjänimi on jo käytössä")
            return redirect("register")
        if users.register(username, password1):
            return redirect("/")
        flash("Rekisteröinti ei onnistunut")
        return redirect("register")