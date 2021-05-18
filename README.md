# MyCookNoteBook

![Home page](/static/images/screen_home.png)
![Recipe page](/static/images/screen_recipes.png)

[View the live project here]
## Application for food lovers, who want to store and manage their recipes in one place
# Project description
“MyCookNoteBook” is a project that will allow food lovers and those who enjoy frequent cooking to create, update and store recipes with the help of the Application, which is a kind of storage or notebook for recipes for the user. 
The purpose of the application is to allow food loving users (if they saw, heard, read the recipe somewhere) write down the recipe with quick notes as well as upload an image illustrating a certain recipe, so after some time they can return to it and use it. Users have the ability to store, modify the recipe, and delete it if it is no longer needed.
In order to attract users to start using the Application, the page with posted recipes is available even for non-logged-in/non-registered users.
There are 5 categories of Users:
1.  Generic Users
2.  Admin (the Application Owner)
3.  Logged-in Users
4.  Non-logged-in Users
5.  Non-registered Users

Thus, the Application will help to:
- Quickly write down favorite recipes.
- Manage recipes records: store, read, update, delete.
- Create categories and allocate recipes.
- Manage categories: store, update, delete.
- Search for recipes/categories by keywords.

# User Stories

## Users who want to create and manage recipes 

## Generic Users
-	As a generic user, I want to easily understand the main purpose of the application due to the clear layout.
-	As a generic user, I want to be able to intuitively navigate through the application.
-	As a generic user, I want the application be responsive on all devices.
-	As a generic user, I want to be able to use the application on any device .
-	As a generic user, I want to be able to navigate the application from any kind of devices. 

## Non logged-in Users
-	As a non-logged-in user, who is a food or cook lover, I want to easily understand the main purpose of the applcation, which is providing the possibility to write down favorite recipes with quick notes as well as to manage recipes: create, update, delete. (The information will be placed on the Home Page).
-	As a non-logged-in user, I want to easily understand how i can start using the application. (By SignUp/SignIn function on the home page).  
-	As a non-logged-in user I want to have a quick access to the recipe page.
-	As a non-logged-in user I want to be able to use the search option in order to find a recipe i want.

## Non-registered Users
-	As a non-registered user, who is a food or cook lover, I want to easily understand the main purpose of the applcation, which is providing the possibility to write down favorite recipes with quick notes as well as to manage recipes: create, update, delete. (The information will be placed on the Home Page).
-	As a non-registered user I want to easily understand how the page with posted recipes looks like (page Recipes on the navbar)
-	As a non-registered user I want to be able to read the description of recipes and get inspired of the content.
-	As a non-registered user, I want to easily understand how i can start using the application. (By SignUp/SignIn function on the home page).   
-	As a non-registered user, I want to easily sign up in order to start using the application.

## Logged-in Users
-	As a logged-in user I want to be redirected to my Profile page where i am greeted as a User and from where I can create new recipes or search for recipes. (My page, where the User can find all these options)
-	As a logged-in user, I want to easily find out how i can put quick notes of a new recipe. (Through navbar Create new recipe or after signing in with the button “Create your recipe” on My page). 
-	As a logged-in user, I want to easily get any recipe or category by search option.
-	As a logged-in user, I want to easily find out what kind of the recipe information I can write down (The form will intuitively guide by its fileds: Name, Description, Ingredients).
-	As a logged-in user, I want to create a recipe record in the easiest way (form with drop down categories ). 
-	As a logged-in user, I want to easily cancel adding the Recipe (The button cancel below the Create recipe form).
-	As a logged-in user, I want to upload a recipe image to remember how it looks like (form with the field for the link – source from the Internet). 
-	As a logged-in user, I want to easily find out how to edit or delete the Recipe.
-	As a logged-in user, I want to easily cancel editing the Recipe (The button cancel below the Edit recipe form).
-	As a logged-in user, I want to have basic food categories to where i can allocate my recipes.

## Admin
-	As an Admin, I want to easily sign-in to the website.
-	As an Admin, I want to have access for editing/deleting any created recipe of any user. 
-	As an Admin, I want to to have access to the recipes categories with the possibility to manage them (add, edit, delete).
-	As an Admin, I want the recipes Authors to be able to manage only their own recipes (by buttons “edit”, “delete”)
-	As an Admin I want to showcase all the created recipes to all users (to logged- or non-logged in users) 

# Database Model

## Collections:
1.	![recipes](/static/images/recipes_collection.png)

2.	![recipes_categories](/static/images/categories_collection.png)

3.	![users](/static/images/users_collection.png)

