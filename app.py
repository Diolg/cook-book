# Import files
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

# Configurations
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


# Home page
@app.route("/")
def home():
    return render_template("home.html")


# Page with recipes
@app.route("/get_recipes")
def get_recipes():
    if not session.get("user"):
         return render_template("error_recipes.html")
    query = request.args.get("query")
    if query:   
        recipes = list(mongo.db.recipes.find({"$text": {"$search": query}})).sort("_id", -1)
    else:
        recipes = mongo.db.recipes.find().sort("_id", -1)
    if not recipes:
        return render_template("error.html")
    return render_template("recipes.html", recipes=recipes)


# Search function in recipes
@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))
    if not recipes:
        return render_template("error.html")
    return render_template("recipes.html", recipes=recipes)


# Sign up function
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
        
       #put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Welcome! You can start using this app!")
        return redirect(url_for("mypage", username=session["user"]))

    return render_template("signup.html")


# Sign in function
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


# Opening User's profile function
@app.route("/mypage/<username>", methods=["GET", "POST"])
def mypage(username):
    if not session.get("user"):
        return render_template("error_recipes.html")

    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("mypage.html", username=username)

    return redirect(url_for("signin"))


# Sign out function
@app.route("/signout")
def signout():
    # remove user from session cookie
    flash("See you soon!")
    session.pop("user")
    return redirect(url_for("signin"))


# Add recipes function
@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if not session.get("user"):
        return render_template("error_recipes.html")

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


# Edit recipes function
@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    
    if not session.get("user"):
        return render_template("error_recipes.html")

    if request.method == "POST":
        submit = {
            "category_name": request.form.get("category_name"),
            "recipe_name": request.form.get("recipe_name"),
            "recipe_description": request.form.get("recipe_description"),
            "cooking_time": request.form.get("cooking_time"),
            "ingredients": request.form.get("ingredients"),
            "link_website": request.form.get("link_website"),
            "created_by": session["user"]
        }
        mongo.db.recipes.update({"_id": ObjectId(recipe_id)}, submit)
        flash("Your recipe now is updated!")
        return redirect(url_for("get_recipes"))

    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    recipes_categories = mongo.db.recipes_categories.find().sort("category_name", 1)
    return render_template(
        "edit_recipe.html", recipe=recipe, recipes_categories=recipes_categories)


# Delete recipes function
@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    if not session.get("user"):
        return render_template("error_recipes.html")

    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    flash("Recipe is Deleted")
    return redirect(url_for("get_recipes"))


# Open categories page for Admin function
@app.route("/get_categories")
def get_categories():
    if not session.get("user") =="admin":
        return render_template("error_permission.html")

    recipes_categories = list(mongo.db.recipes_categories.find().sort("category_name", 1))
    return render_template("categories.html", recipes_categories=recipes_categories)


# Add category function
@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if not session.get("user") =="admin":
        return render_template("error_permission.html")

    if request.method == "POST":
        recipe_category = {
            "category_name": request.form.get("category_name")
        }
        mongo.db.recipes_categories.insert_one(recipe_category)
        flash("You have created a new category!")
        return redirect(url_for("get_categories"))

    return render_template("add_category.html")


# Edit category function
@app.route("/edit_category, <recipes_category_id>", methods=["GET", "POST"])
def edit_category(recipes_category_id):
    if not session.get("user") =="admin":
        return render_template("error_permission.html")

    if request.method == "POST":
        submit = {
            "category_name": request.form.get("category_name")
        }
        mongo.db.recipes_categories.update({"_id":ObjectId(recipes_category_id)}, submit)
        flash("You have updated the Category")
        return redirect(url_for("get_categories"))

    recipes_category = mongo.db.recipes_categories.find_one({"_id": ObjectId(recipes_category_id)})
    return render_template("edit_category.html", recipes_category=recipes_category)


# Delete category function
@app.route("/delete_category, <recipes_category_id>")
def delete_category(recipes_category_id):
    if not session.get("user") =="admin":
        return render_template("error_permission.html")

    mongo.db.recipes_categories.remove({"_id":ObjectId(recipes_category_id)})
    flash("You removed the Category Successfully!")
    return redirect(url_for("get_categories"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=('DEBUGGING' in os.environ))
