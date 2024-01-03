from io import StringIO
from typing import List, Dict, Tuple
from typing import Optional
import csv

class PizzaSize:
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'

class PizzaCategory:
    VEGETARIAN = 'vegetarian'
    MEAT = 'meat'
    SPECIALTY = 'specialty'

class Ingredient:
    def __init__(self, name: str, quantity: float, unit: str, reorder_level: int):
        self._name = name
        self._quantity = quantity
        self._unit = unit
        self._reorder_level = reorder_level

    @property
    def name(self) -> str:
        return self._name

    @property
    def quantity(self) -> float:
        return self._quantity

    @quantity.setter
    def quantity(self, quantity: float) -> None:
        self._quantity = quantity

    @property
    def unit(self) -> str:
        return self._unit

    @property
    def reorder_level(self) -> int:
        return self._reorder_level

class PizzaRecipe:
    def __init__(self, name: str, ingredients: dict):
        self._name = name
        self._ingredients = ingredients

    @property
    def name(self) -> str:
        return self._name

    @property
    def ingredients(self) -> dict:
        return self._ingredients

    @ingredients.setter
    def ingredients(self, ingredients: dict) -> None:
        self._ingredients = ingredients

class PizzaMenuItem:
    def __init__(self, name: str, description: str, size: 'PizzaSize', price: float, category: 'PizzaCategory', recipe: 'PizzaRecipe'):
        self._name = name
        self._description = description
        self._size = size
        self._price = price
        self._category = category
        self._recipe = recipe

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def size(self) -> 'PizzaSize':
        return self._size

    @property
    def price(self) -> float:
        return self._price

    @property
    def category(self) -> 'PizzaCategory':
        return self._category

    @property
    def recipe(self) -> 'PizzaRecipe':
        return self._recipe

class RecipeManagement:
    def __init__(self):
        self._recipes = []

    def add_recipe(self, recipe: 'PizzaRecipe') -> None:
        self._recipes.append(recipe)

    def remove_recipe(self, recipe_name: str) -> None:
        self._recipes = [recipe for recipe in self._recipes if recipe.name != recipe_name]

    def update_recipe(self, recipe_name: str, new_ingredients: dict) -> bool:
        for recipe in self._recipes:
            if recipe.name == recipe_name:
                recipe.ingredients = new_ingredients
                return True
        return False

    def get_recipe_by_name(self, recipe_name: str) -> Optional['PizzaRecipe']:
        for recipe in self._recipes:
            if recipe.name == recipe_name:
                return recipe
        return None

    def list_recipes(self) -> List['PizzaRecipe']:
        return self._recipes

    def list_recipes_by_category(self, category: 'PizzaCategory') -> List['PizzaRecipe']:
        return [recipe for recipe in self._recipes if recipe.category == category]

    def search_recipes(self, keyword: str) -> List['PizzaRecipe']:
        keyword = keyword.lower()
        return [recipe for recipe in self._recipes if keyword in recipe.name.lower() or 
                any(keyword in ingredient.lower() for ingredient in recipe.ingredients.keys())]
    

class InventoryManager:
    def __init__(self, filename='ingredients.csv'):
        self._ingredients = []  # Private attribute
        self._filename = filename
        self.load_inventory()

    @property
    def ingredients(self):
        return self._ingredients

    @property
    def filename(self) -> str:
        return self._filename
    def load_inventory(self):
        try:
            with open(self.filename, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                self._ingredients = [Ingredient(row['name'], float(row['quantity']), row['unit'], int(row['reorder_level'])) for row in reader]
        except FileNotFoundError:
            print(f"File {self.filename} not found. Starting with an empty inventory.")
            self._ingredients = []

    def save_inventory(self):
        with open(self.filename, 'w', newline='') as csvfile:
            fieldnames = ['name', 'quantity', 'unit', 'reorder_level']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for ingredient in self._ingredients:
                writer.writerow({
                    'name': ingredient.name,
                    'quantity': ingredient.quantity,
                    'unit': ingredient.unit,
                    'reorder_level': ingredient.reorder_level
                })
  
        
    def add_ingredient(self):
        name = input("Enter ingredient name: ")
        quantity = float(input("Enter quantity: "))
        unit = input("Enter unit: ")
        reorder_level = int(input("Enter reorder level: "))
        ingredient = Ingredient(name, quantity, unit, reorder_level)
        self.load_inventory()
        if ingredient.name not in [i.name for i in self._ingredients]:
            self._ingredients.append(ingredient)
            self.save_inventory()
            
    def remove_ingredient_ui(self):
        name = input("Enter ingredient name to remove: ")
        quantity = float(input("Enter quantity to remove: "))
        self.load_inventory()
        for ingredient in self._ingredients:
            if ingredient.name == name:
                if quantity >= ingredient.quantity:
                    self._ingredients.remove(ingredient)
                else:
                    ingredient.quantity -= quantity
                self.save_inventory()
                break
        else:
            print(f"Ingredient with name '{name}' not found.")

            
    def use_ingredient_ui(self):
        recipe_ingredients = {}
        while True:
            name = input("Enter ingredient name used in the recipe (or 'done' to finish): ")
            if name.lower() == 'done':
                break

            quantity_used = float(input(f"Enter quantity of {name} used in the recipe: "))
            recipe_ingredients[name] = quantity_used

        self.use_ingredient(recipe_ingredients)

    def use_ingredient(self, recipe_ingredients):
        self.load_inventory()
        for ingredient_name, quantity_used in recipe_ingredients.items():
            for ingredient in self._ingredients:
                if ingredient.name == ingredient_name:
                    if quantity_used >= ingredient.quantity:
                        self._ingredients.remove(ingredient)
                    else:
                        ingredient.quantity -= quantity_used
                    self.save_inventory()

    def check_reorder_levels(self):
        self.load_inventory()
        reorder_list = []
        for ingredient in self._ingredients:
            if ingredient.quantity <= ingredient.reorder_level:
                reorder_list.append(ingredient.name)
        if reorder_list:
            print("Reorder the following ingredients:")
            for ingredient_name in reorder_list:
                print(ingredient_name)
        else:
            print("No ingredients need to be reordered.")

            return reorder_list


    def print_inventory(self):
        self.load_inventory()
        for ingredient in self._ingredients:
            print(f"Name: {ingredient.name}")
            print(f"Quantity: {ingredient.quantity} {ingredient.unit}")
            print(f"Reorder Level: {ingredient.reorder_level}")
            print("\n")

class MenuManagement:
    def __init__(self):
        self.menu_items = [] 

    def add_menu_item(self, menu_item: PizzaMenuItem):
        self.menu_items.append(menu_item)

    def remove_menu_item(self, name: str):
        self.menu_items = [item for item in self.menu_items if item.name != name]

    def update_menu_item(self, name: str, new_menu_item: PizzaMenuItem):
        updated = False
        for i, item in enumerate(self.menu_items):
            if item.name == name:
                self.menu_items[i] = new_menu_item
                updated = True
                break
        if not updated:
            print(f"Menu item with name '{name}' not found. No update made.")
    def display_menu(self):
        for item in self.menu_mgt.list_menu_items():
            print(f"Name: {item.name}")
            print(f"Description: {item.description}")
            print(f"Price: ${item.price}")
            print("Ingredients:")
            for ingredient, amount in item.recipe.ingredients.items():
                print(f"  - {ingredient}: {amount}")
            print()  
    def get_menu_items_by_category(self, category: PizzaCategory) -> List[PizzaMenuItem]:
        return [item for item in self.menu_items if item.category == category]
    
    def get_menu_items_by_size(self, size: PizzaSize) -> List[PizzaMenuItem]:
        return [item for item in self.menu_items if item.size == size]
    def get_menu_item_by_name(self, name: str) -> Optional[PizzaMenuItem]:
        for item in self.menu_items:
            if item.name.lower() == name.lower():
                return item
        return None
    def list_menu_items(self) -> List[PizzaMenuItem]:
        return self.menu_items

    def display_menu_item_details(self):
        for item in self.menu_items:
            print(f"Name: {item.name}\nDescription: {item.description}\nPrice: ${item.price}\nSize: {item.size}\nCategory: {item.category}\n")

class CustomerInfo:
    def __init__(self, name: str, phone: str, email: str, company: str = None, delivery_date: str = '', delivery_time: str = ''):
        self.name = name
        self.phone = phone
        self.email = email
        self.company = company
        self.delivery_date = delivery_date
        self.delivery_time = delivery_time
        self.orders = []  
    def place_order(self, order):
        self.orders.append(order)

class CustomPizzaOrder:
    def create_custom_pizza(self):
        print("\n--- Build Your Own Pizza ---")
        base_price = 14.00

        # Options for bases, sauces, toppings, and additional ingredients
        bases = {"Thin Crust": 2.00, "Thick Crust": 2.50}
        sauces = {"Tomato": 1.00, "BBQ": 1.50, "White Garlic": 1.25}
        toppings = {"Pepperoni": 1.75, "Ham": 1.75, "Bacon": 1.75,
                    "Mushrooms": 1.75, "Onion": 1.75, "Black Olives": 1.75,
                    "Tomato Slices": 1.75, "Extra Cheese": 1.75, "Pineapple": 1.75}
        additional_ingredients = {"Chicken": 2.00, "Beef": 2.25, "Cheddar": 1.75}

        # Let the customer select and customize
        print("Select a base:")
        for base, price in bases.items():
            print(f"{base} (${price})")
        selected_base = input("Your choice: ")
        base_quantity = int(input("Enter quantity: "))

        print("\nSelect a sauce:")
        for sauce, price in sauces.items():
            print(f"{sauce} (${price})")
        selected_sauce = input("Your choice: ")
        sauce_quantity = int(input("Enter quantity: "))

        selected_toppings = {}
        print("\nSelect toppings:")
        for topping, price in toppings.items():
            choice = input(f"Add {topping} (${price}) (yes/no)? ")
            if choice.lower() == "yes":
                quantity = int(input(f"Quantity for {topping}: "))
                selected_toppings[topping] = (price, quantity)

        selected_additional_ingredients = {}
        print("\nSelect additional ingredients:")
        for ingredient, price in additional_ingredients.items():
            choice = input(f"Add {ingredient} (${price}) (yes/no)? ")
            if choice.lower() == "yes":
                quantity = int(input(f"Quantity for {ingredient}: "))
                selected_additional_ingredients[ingredient] = (price, quantity)

        # Calculate total price
        total_price = base_price
        total_price += bases.get(selected_base, 0) * base_quantity
        total_price += sauces.get(selected_sauce, 0) * sauce_quantity
        total_price += sum(price * qty for price, qty in selected_toppings.values())
        total_price += sum(price * qty for price, qty in selected_additional_ingredients.values())

        # Display the total price
        print(f"\nTotal price for your custom pizza: ${total_price:.2f}")

        # Create a custom PizzaRecipe and PizzaMenuItem for the order
        custom_ingredients = {selected_base: base_quantity, selected_sauce: sauce_quantity}
        custom_ingredients.update({topping: qty for topping, (_, qty) in selected_toppings.items()})
        custom_ingredients.update({ingredient: qty for ingredient, (_, qty) in selected_additional_ingredients.items()})
        custom_pizza_recipe = PizzaRecipe("Custom Pizza", custom_ingredients)
        custom_pizza_item = PizzaMenuItem("Custom Pizza", "Your personalized pizza", PizzaSize.LARGE, total_price, PizzaCategory.SPECIALTY, custom_pizza_recipe)

        # Return the custom pizza item for ordering
        return custom_pizza_item

class SideCategory:
    APPETIZERS = 'Appetizers'
    DESSERTS = 'Desserts'
    BEVERAGES = 'Beverages'

class SideItem:
    def __init__(self, name: str, price: float, category: SideCategory):
        self.name = name
        self.price = price
        self.category = category

class SideMenuManagement:
    def __init__(self, side_dish_repo):
        self.side_items = []
        self.side_dish_repo = side_dish_repo

    def add_side_item(self, side_item):
        self.side_items.append(side_item)
        self.side_dish_repo.save_side_dishes(self.side_items, 'side_dish.csv')

    def remove_side_item(self, name):
        self.side_items = [item for item in self.side_items if item.name != name]

    def update_side_item(self, name, new_side_item):
        updated = False
        for i, item in enumerate(self.side_items):
            if item.name == name:
                self.side_items[i] = new_side_item
                updated = True
                break
        if not updated:
            print(f"Side dish with name '{name}' not found. No update made.")

    def list_side_items(self):
        return self.side_items

    def list_side_items_by_category(self, category):
        return [item for item in self.side_items if item.category == category]
 
    def get_side_item_by_name(self, name: str):
        # Search for a side item by its name and return it
        for item in self.side_items:
            if item.name.lower() == name.lower():
                return item
        return None
    
    def display_side_dish(self, side_dish):
        # Display side dish information
        print(f"Name: {side_dish.name}")
        print(f"Description: {side_dish.description}")
        print(f"Price: {side_dish.price}")
        print(f"Category: {side_dish.category}")    




class Order:
    def __init__(self, customer_info, delivery_date: str, delivery_time: str, pizzas: List[PizzaMenuItem], sides: List[SideItem]):
        self.customer_info = customer_info  # Assuming CustomerInfo type, define if not already
        self.delivery_date = delivery_date
        self.delivery_time = delivery_time
        self.pizzas = pizzas  
        self.sides = sides  

        



    def add_pizza(self, pizza: PizzaMenuItem) -> None:
        self.pizzas.append(pizza)

    def add_side_dish(self, side_dish: SideItem) -> None:
        self.sides.append(side_dish)

    def generate_order_slip(self) -> str:
        order_slip = "Order Slip:\n"

        # Pizzas
        if self.pizzas:
            order_slip += "Pizzas:\n"
            for pizza in self.pizzas:
                order_slip += f"- {pizza.name}\n"
                order_slip += f"  Ingredients: {', '.join([ingredient for ingredient, amount in pizza.recipe.ingredients.items()])}\n"

        # Side Dishes
        if self.sides:
            order_slip += "Side Dishes:\n"
            for side_dish in self.sides:
                order_slip += f"- {side_dish.name}\n"
                order_slip += f"  Description: {side_dish.description}\n"

        return order_slip

    def get_side_item_by_name(self, name: str) -> Optional[SideItem]:
        for item in self.menu_mgt.list_side_items():
            if item.name.lower() == name.lower():
                return item
        return None

    def create_order(self) -> 'Order':
        order = Order(self.customer_info, self.delivery_date, self.delivery_time, self.pizzas, self.sides)
        return order

    def add_pizza_to_order(self, order: 'Order', pizza: PizzaMenuItem) -> None:
        order.add_pizza(pizza)

    def add_side_dish_to_order(self, order: 'Order', side_dish: SideItem) -> None:
        order.add_side_dish(side_dish)

