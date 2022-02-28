from app import app
from flask import jsonify, render_template, request, redirect, url_for, flash, abort
import messages, users, topics, chains, validate

@app.route("/")
def index():
    list = topics.get_list()
    secret_list = topics.get_secret_list()
    return render_template("index.html", topics=list, secret_topics=secret_list, get_latest=messages.get_latest_message,
    chain_count=topics.get_chain_count, message_count=topics.get_message_count)

@app.route("/validatemember/<int:id>", methods=["POST"])
def validatemember(id):
    if users.csrf_token() != request.form["csrf_token"]:
        abort(403)
    username = request.form["username"]
    if topics.add_member(username, id):
        flash("Käyttäjän lisääminen onnistui")
        return redirect(url_for("addmember", id=id))
    flash("Käyttäjän lisääminen epäonnistui")
    return redirect(url_for("addmember", id=id))

@app.route("/addmember/<int:id>")
def addmember(id):
    return render_template("addmember.html", topic_id=id)

@app.route("/deltopic/<int:id>")
def deltopic(id):
    topics.delete(id)
    return redirect("/")

@app.route("/delchain/<int:id>")
def delchain(id):
    chains.delete(id)
    return redirect(url_for("topicarea", id=topics.topic_id()))

@app.route("/delmsg/<int:id>")
def delmsg(id):
    messages.delete(id)
    return redirect(url_for("chainarea", id=chains.chain_id()))

@app.route("/like/<int:id>", methods=["POST"])
def like(id):
    if not messages.add_like(id):
        flash("Olet jo tykännyt kyseisestä viestistä")
    return redirect(url_for("chainarea", id=chains.chain_id()))

@app.route("/testlike", methods=["POST"])
def testlike():
    if request.method == "POST":
        print(request.get_json())
        messages.add_like(id)
        return jsonify({'status':'success'}, 201)

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/searchmessages", methods=["POST"])
def searchmessages():
    filter = request.form["filter"]
    list = messages.get_filtered_messages(filter)
    return render_template("filteredmessages.html", messages=list, count=len(list), get_likes=messages.get_likes)

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
    return render_template("updatechain.html", id=id, t_id=topics.topic_id())

@app.route("/updatemsg/<int:id>")
def updatemsg(id):
    return render_template("updatemsg.html", id=id, c_id=chains.chain_id())

@app.route("/topicarea/<int:id>")
def topicarea(id):
    topics.set_topic_id(id)
    list = chains.get_list()
    return render_template("topicarea.html", count = len(list), chains=list, header=topics.get_topic_name(), topic_id=id)

@app.route("/chainarea/<int:id>")
def chainarea(id):
    chains.set_chain_id(id)
    list = messages.get_list()
    return render_template("chainarea.html", count = len(list), messages=list, 
    t_id=topics.topic_id(), header=chains.get_chain_name(), chain_id=id, get_likes=messages.get_likes)

@app.route("/sendtopic", methods=["POST"])
def sentopic():
    if users.csrf_token() != request.form["csrf_token"]:
        abort(403)
    name = request.form["topicname"]
    secret = request.form["secret"]
    if secret == "false":
        if topics.create_topic(name, False):
            return redirect("/")
    else:
        if topics.create_topic(name, True):
            return redirect("/")
    flash("Aiheen luonti epäonnistui")
    return redirect("/newtopic")

@app.route("/sendchain", methods=["POST"])
def sendchain():
    if users.csrf_token() != request.form["csrf_token"]:
        abort(403)
    name = request.form["chainname"]
    content = request.form["msg"]
    if not validate.chain(name) or not validate.msg(content): #täytyy tarkistaa jo tässä, ettei luo toista databaseen jos toinen ei ollekkaan validi
        flash("Otsikko tai aloitusviesti virheellinen")
        return redirect(url_for("newchain", id=topics.topic_id()))
    if chains.create_chain(name):
        if messages.send(content):
            return redirect(url_for("topicarea", id=topics.topic_id()))
    flash("Ketjun luonti epäonnistui")
    return redirect(url_for("newchain", id=topics.topic_id()))

@app.route("/sendmessage", methods=["POST"])
def sendmessage():
    if users.csrf_token() != request.form["csrf_token"]:
        abort(403)
    content = request.form["content"]
    if messages.send(content):
        return redirect(url_for("chainarea", id=chains.chain_id()))
    flash("Viestin lähetys epäonnistui")
    return redirect(url_for("newmessage", id=chains.chain_id()))

@app.route("/setupdatechain/<int:id>", methods=["POST"])
def setupdatechain(id):
    if users.csrf_token() != request.form["csrf_token"]:
        abort(403)
    chainname = request.form["chainname"]
    if chains.updatechain(chainname, id):
        flash("Ketjun muokkaaminen onnistui")
        return redirect(url_for("topicarea", id=topics.topic_id()))
    flash("Ketjun muokkaaminen epäonnistui")
    return redirect(url_for("updatechain", id=id))

@app.route("/setupdatemsg/<int:id>", methods=["POST"])
def setupdatemsg(id):
    if users.csrf_token() != request.form["csrf_token"]:
        abort(403)
    content = request.form["content"]
    if messages.updatemsg(content, id):
        flash("Viestin muokkaaminen onnistui")
        return redirect(url_for("chainarea", id=chains.chain_id()))
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
        if password1 != password2:
            flash("Salasanat eroavat")
            return redirect("register")
        if users.username_taken(username):
            flash("Käyttäjänimi on jo käytössä")
            return redirect("register")
        if users.register(username, password1):
            return redirect("/")
        flash("Rekisteröinti ei onnistunut")
        return redirect("register")