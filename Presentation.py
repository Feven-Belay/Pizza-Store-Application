import csv
from io import StringIO
from typing import List, Dict, Tuple
from bussinese import PizzaSize, PizzaCategory,Ingredient,PizzaRecipe,PizzaMenuItem, RecipeManagement,InventoryManager,MenuManagement,CustomerInfo,CustomPizzaOrder,SideCategory,SideItem,SideMenuManagement,Order
from Datalayer import IngredientRepository,PizzaRecipeRepository,PizzaMenuRepository,SideDishRepository


class PizzaStore:
    def __init__(self):
        self.actions = []  # List to store actions performed
        self.inventory_mgr = InventoryManager()
        self.recipe_mgt = RecipeManagement()
        self.menu_mgt = MenuManagement()   
        side_dish_repo = SideDishRepository()
        self.side_menu_mgt = SideMenuManagement(side_dish_repo)
        CustomPizzaOrder()


    def print_menu(self, menu_title, options):
        print(f"\n{menu_title}")
        for key, value in options.items():
            print(f"{key}: {value}")
        return input("Please select an option: ")

    def handle_csv_input(self, prompt):
        print(prompt)
        ingredients_csv = input()
        ingredients_file_like = StringIO(ingredients_csv)
        reader = csv.reader(ingredients_file_like, skipinitialspace=True)

        ingredients = {}
        for rows in reader:
            if len(rows) != 2 or not rows[1].replace('.', '', 1).isdigit():
                print("Invalid format. Enter in 'ingredient_name,amount' format.")
                return None
            ingredients[rows[0]] = float(rows[1])
        return ingredients
    def show_inventory_menu(self):
        self.inventory_mgr.print_inventory()

    def show_recipe_menu(self):
        for recipe in self.recipe_mgt.list_recipes():
            print(f"Recipe Name: {recipe.name}")
            print(f"Ingredients: {recipe.ingredients}")

    def show_menu_item_menu(self):
        for menu_item in self.menu_mgt.list_menu_items():
            print(f"Menu Item: {menu_item.name}, Price: {menu_item.price}")

    def take_order(self):
        customer_info = self.capture_customer_info()
        pizzas = self.select_pizzas()
        sides = self.select_sides()
        delivery_date = input("Delivery Date: ")
        delivery_time = input("Delivery Time: ")
        return Order(customer_info, delivery_date, delivery_time, pizzas, sides)


    def process_recipe_menu(self):
            recipe_repo = PizzaRecipeRepository()  # Initialize the repository

            while True:
                print("\nRecipe Management Menu:")
                print("1: Add Recipe")
                print("2: Remove Recipe")
                print("3: Update Recipe")
                print("4: Return to Main Menu")
                selection = input("Please select an option: ")

                if selection == "1":
                    name = input("Enter the recipe name: ")
                    ingredients = self.handle_csv_input("Enter ingredients in CSV format (ingredient_name,amount):")
                    if ingredients:
                        recipe = PizzaRecipe(name, ingredients)
                        self.recipe_mgt.add_recipe(recipe)
                        print(f"Recipe '{name}' added.")
                        recipe_repo.save_recipes(self.recipe_mgt.list_recipes(), 'recipes.csv')
                    else:
                        print("No valid ingredients provided.")

                elif selection == "2":
                    name = input("Enter the recipe name to remove: ")
                    self.recipe_mgt.remove_recipe(name)
                    print(f"Recipe '{name}' removed.")
                    recipe_repo.save_recipes(self.recipe_mgt.list_recipes(), 'recipes.csv')

                elif selection == "3":
                    name = input("Enter the recipe name to update: ")
                    new_ingredients = self._handle_csv_input("Enter new ingredients in CSV format (ingredient_name,amount):")
                    if new_ingredients:
                        updated = self.recipe_mgt.update_recipe(name, new_ingredients)
                        if updated:
                            print(f"Recipe '{name}' updated.")
                            recipe_repo.save_recipes(self.recipe_mgt.list_recipes(), 'recipes.csv')
                        else:
                            print(f"Recipe '{name}' not found.")
                    else:
                        print("No valid ingredients provided.")

                elif selection == "4":
                    break
                else:
                    print("Invalid option. Please try again.")


    def process_inventory_menu(self):
                # Create an InventoryManager instance
        inventory_manager = InventoryManager()

        # Print the initial inventory

        # User interface menu
        while True:
            print("\n=== Inventory Management Menu ===")
            # print("1. View Inventory")
            print("1. Add Ingredient")
            print("2. Remove Ingredient")
            print("3. Use Ingredient in Recipe")
            print("4. Check Reorder Levels")
            print("5. Exit")

            choice = input("Enter your choice (1-5): ")
            # if choice == '1':
       
            #     self.inventory_mgr.print_inventory()
            if choice == '1':
                inventory_manager.add_ingredient()
            elif choice == '2':
                inventory_manager.remove_ingredient_ui()
            elif choice == '3':
                inventory_manager.use_ingredient_ui()
            elif choice == '4':
                inventory_manager.check_reorder_levels()
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")

        # Print the updated inventory
        inventory_manager.print_inventory()
    def process_menu_item_menu(self):
        menu_repo = PizzaMenuRepository()  # Initialize the repository

        while True:
            print("\nMenu Item Management Menu:")
            print("1: Add Menu Item")
            print("2: Remove Menu Item")
            print("3: Update Menu Item")
            print("4: Return to Main Menu")
            selection = input("Please select an option: ")

            if selection == "1":
                name = input("Enter the menu item name: ")
                description = input("Enter the description: ")
                size = input("Enter the size (small, medium, large): ")
                price = float(input("Enter the price: "))
                category = input("Enter the category (vegetarian, meat, specialty): ")
                recipe_name = input("Enter the name of the associated recipe: ")
                recipe = self.recipe_mgt.get_recipe_by_name(recipe_name)
                if recipe:
                    menu_item = PizzaMenuItem(name, description, size, price, category, recipe)
                    self.menu_mgt.add_menu_item(menu_item)
                    print(f"Menu item '{name}' added.")
                    menu_repo.save_menu_items(self.menu_mgt.list_menu_items(), 'menu_items.csv')
                else:
                    print("Recipe does not exist.")

            elif selection == "2":
                name = input("Enter the menu item name to remove: ")
                self.menu_mgt.remove_menu_item(name)
                print(f"Menu item '{name}' removed.")
                menu_repo.save_menu_items(self.menu_mgt.list_menu_items(), 'menu_items.csv')

            elif selection == "3":
                name = input("Enter the menu item name to update: ")
                existing_item = self.menu_mgt.get_menu_item_by_name(name)
                if existing_item:
                    new_description = input("Enter the new description (or press Enter to keep current): ") or existing_item.description
                    new_size = input("Enter the new size (small, medium, large) (or press Enter to keep current): ") or existing_item.size
                    new_price = float(input("Enter the new price (or press Enter to keep current): ") or existing_item.price)
                    new_category = input("Enter the new category (vegetarian, meat, specialty) (or press Enter to keep current): ") or existing_item.category
                    new_recipe_name = input("Enter the new recipe name (or press Enter to keep current): ") or existing_item.recipe.name
                    new_recipe = self.recipe_mgt.get_recipe_by_name(new_recipe_name) or existing_item.recipe

                    updated_menu_item = PizzaMenuItem(name, new_description, new_size, new_price, new_category, new_recipe)
                    self.menu_mgt.update_menu_item(name, updated_menu_item)
                    print(f"Menu item '{name}' updated.")
                    menu_repo.save_menu_items(self.menu_mgt.list_menu_items(), 'menu_items.csv')
                else:
                    print(f"Menu item '{name}' not found.")

            elif selection == "4":
                break
            else:
                print("Invalid option. Please try again.")



    def capture_customer_info(self):
        print("Please enter customer information.")
        name = input("Customer name: ")
        company = input("Company (optional): ")
        phone = input("Phone number: ")
        email = input("Email address: ")
        customer_info = CustomerInfo(name=name, phone=phone, email=email, company=company)
        return customer_info
    

    
    def create_standard_pizza(self):
        print("\n--- Standard Pizzas ---")
        for item in self.menu_mgt.list_menu_items():
            print(f"{item.name} - {item.description} - ${item.price}")
        pizza_name = input("Enter the name of the pizza you want to add: ")
        quantity = int(input("Enter the quantity: "))
        selected_pizza = next((item for item in self.menu_mgt.list_menu_items() if item.name.lower() == pizza_name.lower()), None)
        return [(selected_pizza, quantity)] if selected_pizza else []


    def populate_standard_pizzas(pizza_store):
        # Predefined list of standard pizzas
        standard_pizzas = [
            ("Pepperoni", "Pepperoni pizza", PizzaSize.LARGE, 15.50, PizzaCategory.MEAT, {"Pepperoni": 1}),
            ("Hawaiian", "Ham and pineapple pizza", PizzaSize.LARGE, 18.50, PizzaCategory.MEAT, {"Ham": 1, "Pineapple": 1}),
            ("Deluxe", "Pepperoni, Bacon, Mushrooms, Olives, Peppers, Onion", PizzaSize.LARGE, 19.50, PizzaCategory.SPECIALTY, {"Pepperoni": 1, "Bacon": 1, "Mushrooms": 1, "Olives": 1, "Peppers": 1, "Onion": 1}),
            ("Meat Lovers", "Pepperoni, Ham, Bacon", PizzaSize.LARGE, 18.50, PizzaCategory.MEAT, {"Pepperoni": 1, "Ham": 1, "Bacon": 1}),
            ("Vegetarian", "Mushrooms, Olives, Onion, Peppers, Tomato", PizzaSize.LARGE, 19.50, PizzaCategory.VEGETARIAN, {"Mushrooms": 1, "Olives": 1, "Onion": 1, "Peppers": 1, "Tomato": 1}),
            ("BBQ Chicken", "Chicken, Red Onion, BBQ Sauce, Cheddar", PizzaSize.LARGE, 19.50, PizzaCategory.MEAT, {"Chicken": 1, "Red Onion": 1, "BBQ Sauce": 1, "Cheddar": 1})
        ]
        
        for name, description, size, price, category, ingredients in standard_pizzas:
            recipe = PizzaRecipe(name, ingredients)
            pizza_store.recipe_mgt.add_recipe(recipe)
            menu_item = PizzaMenuItem(name, description, size, price, category, recipe)
            pizza_store.menu_mgt.add_menu_item(menu_item)


    def populate_side_dishes(pizza_store):
        # Predefined list of side dishes
        side_dishes = [
            SideItem("Caesar Salad", 2.29, SideCategory.APPETIZERS),
            SideItem("Tossed Salad", 2.29, SideCategory.APPETIZERS),
            SideItem("Assorted Pop", 1.35, SideCategory.BEVERAGES),
            SideItem("Assorted Juices", 1.45, SideCategory.BEVERAGES),
            SideItem("Water", 1.00, SideCategory.BEVERAGES),
            SideItem("Cookies", 1.00, SideCategory.DESSERTS),
        ]
            
        for side_item in side_dishes:
            pizza_store.side_menu_mgt.add_side_item(side_item)

    def select_pizzas(self):
        pizzas = []
        print("\n--- Standard Pizzas ---")
        for menu_item in self.menu_mgt.list_menu_items():
            print(f"{menu_item.name} - ${menu_item.price}")

        while True:
            pizza_choice = input("Would you like to add a pizza to your order (yes/no)? ").lower()
            if pizza_choice != 'yes':
                break

            pizza_name = input("Enter the name of the pizza you want to add: ").strip()
            selected_pizza = None
            for item in self.menu_mgt.list_menu_items():
                if item.name.lower() == pizza_name.lower():
                    selected_pizza = item
                    break

            if selected_pizza:
                try:
                    quantity = int(input(f"How many of the {selected_pizza.name} pizza would you like to add? "))
                    pizzas.append((selected_pizza, quantity))
                except ValueError:
                    print("Please enter a valid number.")
            else:
                print(f"Pizza '{pizza_name}' not found.")

        return pizzas


    def select_sides(self):
        sides = []
        print("--- Side Dishes ---")
        for side_item in self.side_menu_mgt.list_side_items():  # Use self to access attributes of the class
            print(f"{side_item.name} - ${side_item.price}")        
        while True:
            side_choice = input("Would you like to add sides to your order (yes/no)? ").lower()
            if side_choice != 'yes':
                break

            side_name = input("Enter the name of the side you want to add: ")
            side = self.side_menu_mgt.get_side_item_by_name(side_name)  # Retrieve the side item by name
            if side:
                try:
                    quantity = int(input(f"How many of the {side_name} would you like to add? "))
                    sides.append((side, quantity))
                except ValueError:
                    print("Please enter a valid number.")
            else:
                print(f"Side item '{side_name}' not found.")
        return sides
    def process_side_dish_menu(self):
        side_dish_repo = SideDishRepository()  # Initialize the repository

        while True:
            print("\nSide Dish Management Menu:")
            print("1: Add Side Dish")
            print("2: Remove Side Dish")
            print("3: Update Side Dish")
            print("4: Return to Main Menu")
            selection = input("Please select an option: ")

            if selection == "1":
                name = input("Enter the side dish name: ")
                price = float(input("Enter the price: "))
                category = input("Enter the category (Appetizers, Desserts, Beverages): ")
                side_dish = SideItem(name, price, SideCategory[category.upper()])
                self.side_menu_mgt.add_side_item(side_dish)
                print(f"Side dish '{name}' added.")
                side_dish_repo.save_side_dishes(self.side_menu_mgt.list_side_items(), 'side_dishes.csv')

            elif selection == "2":
                name = input("Enter the side dish name to remove: ")
                self.side_menu_mgt.remove_side_item(name)
                print(f"Side dish '{name}' removed.")
                side_dish_repo.save_side_dishes(self.side_menu_mgt.list_side_items(), 'side_dishes.csv')

            elif selection == "3":
                name = input("Enter the side dish name to update: ")
                existing_item = self.side_menu_mgt.get_side_item_by_name(name)
                if existing_item:
                    new_price = float(input("Enter the new price (or press Enter to keep current): ") or existing_item.price)
                    new_category = input("Enter the new category (Appetizers, Desserts, Beverages) (or press Enter to keep current): ") or existing_item.category.name
                    updated_side_item = SideItem(name, new_price, SideCategory[new_category.upper()])
                    self.side_menu_mgt.update_side_item(name, updated_side_item)
                    print(f"Side dish '{name}' updated.")
                    side_dish_repo.save_side_dishes(self.side_menu_mgt.list_side_items(), 'side_dishes.csv')
                else:
                    print(f"Side dish '{name}' not found.")

            elif selection == "4":
                break
            else:
                print("Invalid option. Please try again.")

    def build_custom_pizza(self):
        self.actions.append("Built a custom pizza.")       
        custom_pizza_order = CustomPizzaOrder()

        
        custom_pizza = custom_pizza_order.create_custom_pizza()
        return custom_pizza

    def create_order(self):
        customer_info = self.capture_customer_info()
        pizzas = self.select_pizzas()
        sides = self.select_sides()
        delivery_date = input("Delivery Date: ")
        delivery_time = input("Delivery Time: ")
        return Order(customer_info, delivery_date, delivery_time, pizzas, sides)  
    def take_and_print_order(pizza_store):
        # Take an order and print its summary
        order = pizza_store.take_order()

    def print_order_summary(self,order):
        print("\nOrder Summary:")
        print(f"Customer: {order.customer_info.name}")
        if order.customer_info.company:
            print(f"Company: {order.customer_info.company}")
        print(f"Phone: {order.customer_info.phone}")
        print(f"Email: {order.customer_info.email}")
        print(f"Delivery Date: {order.delivery_date}")
        print(f"Delivery Time: {order.delivery_time}")

        print("\nPizzas:")
        for pizza, quantity in order.pizzas:
            print(f"  - {pizza.name} x{quantity}")

        print("Sides:")
        for side, quantity in order.sides:
            print(f"  - {side.name} x{quantity}")


        print("\nActions Performed:")
        for action in self.actions:
            print(f"  - {action}")    

       
def load_data(pizza_store):
    # ingredient_repo = IngredientRepository()
    recipe_repo = PizzaRecipeRepository()
    menu_repo = PizzaMenuRepository()
    side_dish_repo = SideDishRepository()
    side_menu_mgmt = SideMenuManagement(side_dish_repo)

    # pizza_store.inventory_mgr.ingredients = ingredient_repo.load_ingredients('ingredients.csv')
    inventory_manager = InventoryManager()

    # Print the initial inventory
    inventory_manager.print_inventory()
    pizza_store.recipe_mgt.recipes = recipe_repo.load_pizza_recipes('recipes.csv')
    pizza_store.menu_mgt.menu_items = menu_repo.load_menu_items('menu_items.csv', pizza_store.recipe_mgt)


def print_header():
    print("        HELLO DEAR CUSTOMER, HERE IS THE ORDER FROM FOR OUR PIZZA STORE")      
    print()          
    print("                 Choose your pizza(s), call, fax or bring this order to")
    print("                           SFBU Voice or FAX 510-555-7777")
    print("                         MINIMUM SUGGESTED NOTICE 48 HOURS")
    print('----------------------------------------------------------------------------------')
    print("Delivery Date                     Delivery Time")
    print('----------------------------------------------------------------------------------')
    print("                      DeliWorks Feature Combinations")
    print()
    print("Qty    16\" Extra large, 12 Slices- all start with sauce and Mozzarella     @" )
    print("__   Pepperoni     Pepperoni                                             $15.50")
    print("__   Hawaiian      Ham, Red Onion, Pineapple                             $18.50")
    print("__   Deluxe        Pepperoni/Bacon/Mushrooms/Olives/Peppers/Onion        $19.50")
    print("__   Meat Lovers   Pepperoni, Ham, Bacon                                 $18.50")
    print("__   Vegetarian    Mushrooms, Olives, Onion, Peppers, Tomato             $19.50")
    print("__   BBQ Chicken   Chicken, Red Onion, BBQ Sauce, Cheddar                $19.50")
    print('----------------------------------------------------------------------------------')    
    print("BUILD YOUR OWN OPTIONS             EX. Large 16\" ,  12 Slices")
    print('----------------------------------------------------------------------------------')     
    print("    Basic with Sauce and Mozzarella $14.00        each item add $1.75")
    print()
    print("       Pizza 1                Pizza 2             Pizza 3")
    print(" ___   Pepperoni          ___ Pepperoni         __Pepperoni")
    print(" ___   Ham                ___ Ham               __Ham")
    print(" ___   Bacon              ___ Bacon             __Bacon")
    print(" ___   Mushrooms          ___ Mushrooms         __Mushrooms")
    print(" ___   Onion              ___ Onion             __Onion")
    print(" ___   Black Olives       ___ Black Olives      __Black Olives")
    print(" ___   Tomato Slices      ___ Tomato Slices     __Tomato Slices")
    print(" ___   Extra Cheese       ___ Extra Cheese      __Extra Cheese")
    print(" ___   Pineapple          ___ Pineapple         __Pineapple")
    print()
    print()
    print("Qty  SIDES             @      |    Name" )
    print("__   Caesar Salad     $2.29   |    __________________")
    print("__   Tossed Salad     $2.29   |    Company")
    print("__   Assorted Pop     $1.35   |    __________________")
    print("__   Assorted Juices  $1.45   |    Phone")
    print("__   Water            $1.00   |    __________________")
    print("__   Cookies          $1.00   |    Email")
    print("                              |    ___________________")
    print()
    print()        



def main(): 
    pizza_store = PizzaStore()
    print_header()    
    # load_data(pizza_store)
    pizza_store.populate_standard_pizzas()
    pizza_store.populate_side_dishes()

    order = None
    selected_pizzas = []  # Initialize list for selected pizzas
    selected_sides = []     
    while True:
       
        print("\nMain Menu:")
        print("1: Inventory Management")
        print("2: Recipe Management")
        print("3: Menu Item Management")
        print("4: Choose Standard Pizzas")
        print("5: Build Your Own Pizza")
        print("6: Add Side Dish")
        print("7: Enter Customer Information")
        print("8: Display Order Details")
        print("9: Exit")

        selection = input("Please select an option: ")
        if selection == "1":
            pizza_store.process_inventory_menu()
        elif selection == "2":
            pizza_store.process_recipe_menu()
        elif selection == "3":
            pizza_store.process_menu_item_menu()
        if selection == "4":
            selected_pizzas = pizza_store.select_pizzas()
        elif selection == "5":
            # Build custom pizza
            custom_pizza = pizza_store.build_custom_pizza()
        elif selection == "6":
            # Add side dish
            selected_sides = pizza_store.select_sides()
        elif selection == "7":
            # Enter customer information
            customer_info = pizza_store.capture_customer_info()
            # Ask for delivery date and time
            delivery_date = input("Enter Delivery Date (e.g., 2023-01-30): ")
            delivery_time = input("Enter Delivery Time (e.g., 18:30): ")
            # Create an order with the selected items and customer info
            order = Order(customer_info, delivery_date, delivery_time, selected_pizzas, selected_sides)
        elif selection == "8":
            # Display order details
            if order:
                pizza_store.print_order_summary(order)
            else:
                print("No order has been created yet.")
        elif selection == "9":
            # Exiting the program
            print("Exiting the program.")
            break
        else:
            print("Invalid option. Please try again.")    
if __name__ == "__main__":
    main()


