import csv
from typing import List, Dict, Tuple
from bussinese import Ingredient,PizzaRecipe,PizzaMenuItem, RecipeManagement,SideItem,SideCategory

class IngredientRepository:


    def save_ingredients(ingredients, filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Quantity", "Unit", "Reorder Level"])
            for ingredient in ingredients:
                row = [ingredient.name, ingredient.quantity, ingredient.unit, ingredient.reorder_level]
                writer.writerow(row)


    def load_ingredients(filename):
        ingredients = []
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # skip header row
            for row in reader:
                name, quantity, unit, reorder_level = row
                ingredient = Ingredient(name, float(quantity), unit, int(reorder_level))
                ingredients.append(ingredient)
        return ingredients
 
class PizzaRecipeRepository:
    def save_recipes(self, recipes: List[PizzaRecipe], filename: str):
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['recipe_name', 'ingredient_name', 'amount']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for recipe in recipes:
                for ingredient_name, amount in recipe.ingredients.items():
                    writer.writerow({
                        'recipe_name': recipe.name,
                        'ingredient_name': ingredient_name,
                        'amount': amount
                    })

    def load_pizza_recipes(self, filename: str) -> List[PizzaRecipe]:
        with open(filename, newline='') as csvfile:        
            reader = csv.DictReader(csvfile)
            recipes_dict = {}
            for row in reader:
                if row['recipe_name'] in recipes_dict:
                    recipes_dict[row['recipe_name']].ingredients[row['ingredient_name']] = float(row['amount'])
                else:
                    recipes_dict[row['recipe_name']] = PizzaRecipe(row['recipe_name'], {row['ingredient_name']: float(row['amount'])})
            return list(recipes_dict.values())
    
class PizzaMenuRepository:
    def save_menu_items(self, menu_items: List[PizzaMenuItem], filename: str):
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['name', 'description', 'size', 'price', 'category', 'recipe_name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for item in menu_items:
                writer.writerow({
                    'name': item.name,
                    'description': item.description,
                    'size': item.size,
                    'price': item.price,
                    'category': item.category,
                    'recipe_name': item.recipe.name
                })

    def load_menu_items(self, filename: str, recipe_mgt: RecipeManagement) -> List[PizzaMenuItem]:
        menu_items = []
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                recipe_name = row['recipe_name']
                recipe = recipe_mgt.get_recipe_by_name(recipe_name)
                if not recipe:
                    print(f"Recipe '{recipe_name}' not found. Skipping menu item '{row['name']}'.")
                    continue
                menu_item = PizzaMenuItem(
                    name=row['name'],
                    description=row['description'],
                    size=row['size'],
                    price=float(row['price']),
                    category=row['category'],
                    recipe=recipe
                )
                menu_items.append(menu_item)
        return menu_items



class SideDishRepository:
    def save_side_dishes(self, side_dishes: List[SideItem], filename: str) -> None:
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['name', 'price', 'category']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for side_dish in side_dishes:
                writer.writerow({
                    'name': side_dish.name,
                    'price': side_dish.price,
                    'category': side_dish.category  # No .value, as category is a string
                })

    def load_side_dishes(self, filename: str) -> List[SideItem]:
        side_dishes = []
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                side_dishes.append(SideItem(
                    name=row['name'],
                    price=float(row['price']),
                    category=SideCategory(row['category'])  # Convert string back to enum
                ))
        return side_dishes
