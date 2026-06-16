from flask import Flask, render_template, request
import json

app = Flask(__name__)

with open("data/recipes.json", "r", encoding="utf-8") as file:
    recipes = json.load(file)

# Generate ingredient catalog automatically
ingredient_catalog = {}

for recipe in recipes:
    cuisine = recipe["cuisine"]

    if cuisine not in ingredient_catalog:
        ingredient_catalog[cuisine] = set()

    for ingredient in recipe["ingredients"]:
        ingredient_catalog[cuisine].add(ingredient)

for cuisine in ingredient_catalog:
    ingredient_catalog[cuisine] = sorted(
        list(ingredient_catalog[cuisine])
    )


@app.route("/", methods=["GET", "POST"])
def home():

    results = []

    selected_cuisine = "Indian"

    if request.method == "POST":

        ingredients = request.form.get("ingredients", "")
        selected_cuisine = request.form.get("cuisine", "")

        user_ingredients = [
            item.strip().lower()
            for item in ingredients.split(",")
            if item.strip()
        ]

        for recipe in recipes:

            if recipe["cuisine"].lower() != selected_cuisine.lower():
                continue

            recipe_ingredients = [
                item.lower()
                for item in recipe["ingredients"]
            ]

            matched = []
            missing = []

            for ingredient in recipe_ingredients:

                if ingredient in user_ingredients:
                    matched.append(ingredient)
                else:
                    missing.append(ingredient)

            if len(matched) > 0:

                score = round(
                    (len(matched) / len(recipe_ingredients)) * 100,
                    2
                )

                results.append({
                    "name": recipe["name"],
                    "cuisine": recipe["cuisine"],
                    "score": score,
                    "matched": matched,
                    "missing": missing,
                    "time": recipe["time"],
                    "difficulty": recipe["difficulty"],
                    "description": recipe["description"],
                    "steps": recipe["steps"],
                    "substitutions": recipe["substitutions"]
                })

        results.sort(
            key=lambda x: x["score"],
            reverse=True
        )

    return render_template(
        "index.html",
        results=results,
        ingredient_catalog=ingredient_catalog,
        selected_cuisine=selected_cuisine
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)