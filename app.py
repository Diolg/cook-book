import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)



@app.route("/")
@app.route("/get_recipes")
def get_recipes():
    recipes = mongo.db.recipes.find()
    return render_template("recipes.html", recipes=recipes)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Sorry, this login is already taken!")
            return redirect(url_for("signup"))

        signup = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(signup)
        

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Welcome! You can start using this app!")
        return redirect(url_for("mypage", username=session["user"]))

    return render_template("signup.html")


@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                        session["user"] = request.form.get("username").lower()
                        flash("Welcome back, {}!".format(
                            request.form.get("username")))
                        return redirect(url_for(
                            "mypage", username=session["user"]))
            else:
                # invalid password match
                flash("Sorry, check your Username and/or Password!")
                return redirect(url_for("signin"))

        else:
            # username doesn't exist
            flash("Sorry, the Username and/or Password are incorrect!")
            return redirect(url_for("signin"))
   
    return render_template("signin.html")


@app.route("/mypage/<username>", methods=["GET", "POST"])
def mypage(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("mypage.html", username=username)

    return redirect(url_for("signin"))
        


@app.route("/signout")
def signout():
    # remove user from session cookie
    flash("See you soon!")
    session.pop("user")
    return redirect(url_for("signin"))


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        recipe = {
            "category_name": request.form.get("category_name"),
            "recipe_name": request.form.get("recipe_name"),
            "recipe_description": request.form.get("recipe_description"),
            "cooking_time": request.form.get("cooking_time"),
            "ingredients": request.form.get("ingredients"),
            "link_website": request.form.get("link_website"),
            "created_by": session["user"]
        }
        mongo.db.recipes.insert_one(recipe)
        flash("Your recipe is added to the CookBook!")
        return redirect(url_for("get_recipes"))

    recipes_categories = mongo.db.recipes_categories.find().sort("category_name", 1)
    return render_template("add_recipe.html", recipes_categories = recipes_categories)

@app.route("/edit_recipe/<recipe_id>", methods=["GET","POST"])
def edit_recipe(recipe_id):
    recipe = mongo.db.tasks.find_one({"id_": ObjectId(recipe_id)})

    recipes_categories = mongo.db.recipes_categories.find().sort("category_name", 1)
    return render_template("edit_recipe.html", recipe=recipe, recipes_categories = recipes_categories)




if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
