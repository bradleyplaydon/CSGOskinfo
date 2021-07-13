import os
from flask import (Flask, render_template, 
    request, redirect, url_for, flash, session)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)

skinColl = mongo.db.skins
skins = skinColl.find()

@app.route('/')
def index():
    return render_template("pages/index.html", page_title="Latest Skins", skins=skins)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        if request.form.get("password") != request.form.get("confirmpassword"):
            flash("Passwords doesn't match") 
            return redirect(url_for("register"))

        register = {
            "first_name": request.form.get("firstName").capitalize(),
            "last_name": request.form.get("lastName").capitalize(),
            "username": request.form.get("username").lower(),
            "email_address": request.form.get("email"),
            "password": generate_password_hash(request.form.get("password")),
            "is_admin": "false",
            "skins_liked": list(),
            "skins_disliked": list()
        }    

        mongo.db.users.insert_one(register)

        session["user"] = request.form.get("username").lower()
        flash("Registration Succesful")
        return redirect(url_for("account", username=session["user"]))

    return render_template("pages/signup.html", login=False, page_title="Sign Up")

@app.route('/add/skin', methods=["GET", "POST"])
def add_skin():
    skinColl.insert_one(request.form.to_dict())
    return render_template("components/add-skin.html", page_title="Latest Skins")

if __name__ == '__main__':
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True
    )  