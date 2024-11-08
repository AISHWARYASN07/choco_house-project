from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import traceback

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chocolate_house.db"
app.config["SECRET_KEY"] = "my_secrete_key@123*-"  
db = SQLAlchemy(app)

class SeasonalFlavor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    ingredients = db.Column(db.Text)

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Integer)

class CustomerSuggestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    suggestion = db.Column(db.Text, nullable=False)

class AllergyConcern(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    concern = db.Column(db.Text, nullable=False)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/seasonal-flavors", methods=["GET", "POST"])
def seasonal_flavors():
    if request.method == "POST":
        try:
            flavor = SeasonalFlavor(
                name=request.form["name"],
                description=request.form.get("description", ""),  # Default to empty string if not provided
                ingredients=request.form["ingredients"]
            )
            db.session.add(flavor)
            db.session.commit()
            flash("Seasonal flavor added successfully!", "success")
        except Exception as e:
            db.session.rollback()  # Rollback any changes in case of error
            print(f"Error adding flavor: {e}")
            print(traceback.format_exc())  # Print the stack trace for debugging
            flash("An error occurred while adding the flavor.", "danger")
    
    flavors = SeasonalFlavor.query.all()
    return render_template("seasonal_flavors.html", flavors=flavors)

@app.route("/edit-flavor/<int:id>", methods=["GET", "POST"])
def edit_flavor(id):
    flavor = SeasonalFlavor.query.get_or_404(id)
    if request.method == "POST":
        flavor.name = request.form["name"]
        flavor.description = request.form["description"]
        flavor.ingredients = request.form["ingredients"]
        db.session.commit()
        flash("Seasonal flavor updated successfully!", "success")
        return redirect(url_for("seasonal_flavors"))
    return render_template("edit_flavor.html", flavor=flavor)


@app.route("/delete-flavor/<int:id>", methods=["POST"])
def delete_flavor(id):
    flavor = SeasonalFlavor.query.get_or_404(id)
    db.session.delete(flavor)
    db.session.commit()
    flash("Seasonal flavor deleted successfully!", "success")
    return redirect(url_for("seasonal_flavors"))

@app.route("/ingredient-inventory", methods=["GET", "POST"])
def ingredient_inventory():
    if request.method == "POST":
        try:
            ingredient = Ingredient(name=request.form["name"], quantity=request.form["quantity"])
            db.session.add(ingredient)
            db.session.commit()
            flash("Ingredient added successfully!", "success")
        except Exception as e:
            db.session.rollback()
            print(f"Error adding ingredient: {e}")
            print(traceback.format_exc())
            flash("An error occurred while adding the ingredient.", "danger")
    
    ingredients = Ingredient.query.all()
    return render_template("ingredient_inventory.html", ingredients=ingredients)

@app.route("/edit_ingredient/<int:ingredient_id>", methods=["GET", "POST"])
def edit_ingredient(ingredient_id):
    ingredient = Ingredient.query.get_or_404(ingredient_id)
    if request.method == "POST":
        ingredient.name = request.form["name"]
        ingredient.quantity = request.form["quantity"]
        db.session.commit()
        flash("Ingredient updated successfully!", "success")
        return redirect(url_for('ingredient_inventory'))
    return render_template("edit_ingredient.html", ingredient=ingredient)

@app.route("/delete_ingredient/<int:ingredient_id>", methods=["POST"])
def delete_ingredient(ingredient_id):
    ingredient = Ingredient.query.get(ingredient_id)
    if ingredient:
        db.session.delete(ingredient)
        db.session.commit()
        flash("Ingredient deleted successfully!", "success")
    return redirect(url_for('ingredient_inventory'))

@app.route("/customer-suggestions", methods=["GET", "POST"])
def customer_suggestions():
    if request.method == "POST":
        suggestion = CustomerSuggestion(suggestion=request.form["suggestion"])
        db.session.add(suggestion)
        db.session.commit()
        flash("Suggestion added successfully!", "success")
    suggestions = CustomerSuggestion.query.all()
    return render_template("customer_suggestions.html", suggestions=suggestions)

@app.route("/allergy-concerns", methods=["GET", "POST"])
def allergy_concerns():
    if request.method == "POST":
        concern = request.form["concern"].strip().lower()  # Normalize input for matching
        new_concern = AllergyConcern(concern=concern)
        db.session.add(new_concern)
        db.session.commit()

        flavors_with_allergens = SeasonalFlavor.query.filter(
            SeasonalFlavor.ingredients.ilike(f"%{concern}%")
        ).all()

        print(f"Flavors with allergens related to '{concern}': {[flavor.name for flavor in flavors_with_allergens]}")

        return render_template("allergy_concerns.html", concerns=AllergyConcern.query.all(),
                               flavors=flavors_with_allergens, concern=concern)

    concerns = AllergyConcern.query.all()
    return render_template("allergy_concerns.html", concerns=concerns)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure tables are created
    app.run(debug=True)
