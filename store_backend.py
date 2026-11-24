"""Grocery Store Management System - Term 1 concepts only."""

# Inventory: nested lists [product name, price per unit, available quantity].
inventory = [
    ["Rice", 60.0, 40],
    ["Wheat Flour", 45.0, 30],
    ["Sugar", 42.0, 25],
    ["Milk", 30.0, 50],
    ["Cooking Oil", 150.0, 20],
    ["Salt", 20.0, 35],
    ["Tea Powder", 120.0, 15],
    ["Biscuits", 25.0, 60],
]

# Cart: list of tuples (name, price, quantity, line total).
cart = []
GST_RATE = 0.05  # Classroom example; actual GST varies by product.
line_total = lambda price, quantity: round(price * quantity, 2)


def get_inventory_data():
    result = []
    for product in inventory:
        result.append((product[0], product[1], product[2]))
    return result


def get_cart_data():
    return cart[:]


def find_product(name):
    for product in inventory:
        if product[0].lower() == name.strip().lower():
            return product
    return None


def add_to_cart(name, quantity):
    product = find_product(name)
    if product is None:
        return "Product not found."
    if quantity <= 0:
        return "Quantity must be a positive whole number."
    if quantity > product[2]:
        return "Not enough stock. Available: " + str(product[2])
    # Reserve the units now, preventing multiple cart additions from overselling.
    product[2] -= quantity
    for index in range(len(cart)):
        item = cart[index]
        if item[0] == product[0]:
            new_quantity = item[2] + quantity
            cart[index] = (item[0], item[1], new_quantity, line_total(item[1], new_quantity))
            return "Added to cart: " + product[0]
    cart.append((product[0], product[1], quantity, line_total(product[1], quantity)))
    return "Added to cart: " + product[0]


def add_stock(name, quantity):
    product = find_product(name)
    if product is None:
        return "Product not found."
    if quantity <= 0:
        return "Stock quantity must be positive."
    product[2] += quantity
    return "Stock updated: " + product[0] + " (" + str(product[2]) + " available)"


def update_stock(name, quantity):
    product = find_product(name)
    if product is None:
        return "Product not found."
    if quantity < 0:
        return "Stock cannot be negative."
    product[2] = quantity
    return "Stock set to " + str(quantity) + " for " + product[0]


def calculate_cart_total_recursive(items, index=0):
    if index >= len(items):
        return 0.0
    return items[index][3] + calculate_cart_total_recursive(items, index + 1)


def generate_bill():
    if len(cart) == 0:
        return "Cart is empty. Add products before generating a bill."
    subtotal = round(calculate_cart_total_recursive(cart), 2)
    gst = round(subtotal * GST_RATE, 2)
    total = round(subtotal + gst, 2)
    bill = "=" * 45 + "\n"
    bill += "             GROCERY STORE BILL\n"
    bill += "=" * 45 + "\n"
    for name, price, quantity, amount in cart:
        bill += name + " | Rs." + format(price, ".2f") + " x " + str(quantity) + " = Rs." + format(amount, ".2f") + "\n"
    bill += "-" * 45 + "\n"
    bill += "Subtotal: Rs." + format(subtotal, ".2f") + "\n"
    bill += "Demo GST (5%): Rs." + format(gst, ".2f") + "\n"
    bill += "TOTAL: Rs." + format(total, ".2f") + "\n"
    bill += "=" * 45 + "\n"
    bill += "Thank you for shopping!\n"
    return bill


def clear_cart():
    for name, price, quantity, amount in cart:
        product = find_product(name)
        if product is not None:
            product[2] += quantity
    cart.clear()
    return "Cart cleared; reserved quantities returned to stock."


def checkout():
    if len(cart) == 0:
        return "Cart is empty."
    bill = generate_bill()
    # Reserved stock stays deducted after checkout.
    cart.clear()
    return bill
