"""Tkinter desktop GUI for the Grocery Store Management System."""
import tkinter as tk
from tkinter import messagebox
import store_backend as store

root = tk.Tk()
root.title("Grocery Store Management System | Python Project")
root.geometry("1050x730")
root.minsize(800, 600)
root.configure(bg="#eaf0f7")

header = tk.Frame(root, bg="#15345b", pady=14)
header.pack(fill="x")
tk.Label(header, text="GROCERY STORE MANAGEMENT SYSTEM", font=("Arial", 20, "bold"), fg="white", bg="#15345b").pack()
tk.Label(header, text="Python + Tkinter  |  Inventory  •  Cart  •  Billing  •  Stock", fg="#b9d9fa", bg="#15345b").pack()

body = tk.Frame(root, bg="#eaf0f7", padx=16, pady=15)
body.pack(fill="both", expand=True)
left = tk.LabelFrame(body, text="Inventory and Controls", bg="white", padx=12, pady=12, font=("Arial", 11, "bold"))
left.pack(side="left", fill="both", expand=True, padx=(0, 8))
right = tk.LabelFrame(body, text="Shopping Cart and Bill", bg="white", padx=12, pady=12, font=("Arial", 11, "bold"))
right.pack(side="right", fill="both", expand=True, padx=(8, 0))

inventory_text = tk.Text(left, height=15, width=46, font=("Consolas", 10), bg="#f5f8fc")
inventory_text.pack(fill="both", expand=True)

fields = tk.Frame(left, bg="white", pady=8)
fields.pack(fill="x")
tk.Label(fields, text="Product name:", bg="white").grid(row=0, column=0, sticky="w", pady=5)
product_entry = tk.Entry(fields, width=26)
product_entry.grid(row=0, column=1, padx=6)
tk.Label(fields, text="Quantity:", bg="white").grid(row=1, column=0, sticky="w", pady=5)
quantity_entry = tk.Entry(fields, width=26)
quantity_entry.grid(row=1, column=1, padx=6)

status = tk.StringVar(value="Ready. Select a product and enter a quantity.")
cart_text = tk.Text(right, height=13, font=("Consolas", 10), bg="#f5f8fc")
cart_text.pack(fill="both", expand=True)
tk.Label(right, text="Bill / Transaction Result", bg="white", font=("Arial", 11, "bold")).pack(anchor="w", pady=(12, 4))
bill_text = tk.Text(right, height=13, font=("Consolas", 10), bg="#f5f8fc")
bill_text.pack(fill="both", expand=True)


def show_text(widget, content):
    widget.config(state="normal")
    widget.delete("1.0", tk.END)
    widget.insert(tk.END, content)
    widget.config(state="disabled")


def refresh():
    inventory_display = "PRODUCT                 PRICE      STOCK\n" + "-" * 45 + "\n"
    for name, price, quantity in store.get_inventory_data():
        inventory_display += name.ljust(23) + ("Rs." + format(price, ".2f")).ljust(11) + str(quantity) + "\n"
    show_text(inventory_text, inventory_display)
    cart_display = "PRODUCT              QTY       AMOUNT\n" + "-" * 42 + "\n"
    for name, price, quantity, total in store.get_cart_data():
        cart_display += name.ljust(21) + str(quantity).ljust(10) + "Rs." + format(total, ".2f") + "\n"
    if len(store.get_cart_data()) == 0:
        cart_display += "Cart is empty.\n"
    show_text(cart_text, cart_display)


def read_inputs():
    name = product_entry.get().strip()
    quantity_string = quantity_entry.get().strip()
    if name == "":
        status.set("Enter a product name.")
        return None
    # isdecimal avoids try/except while accepting whole-number input.
    if not quantity_string.isdecimal():
        status.set("Enter a valid non-negative whole-number quantity.")
        return None
    return (name, int(quantity_string))


def add_item():
    values = read_inputs()
    if values is not None:
        status.set(store.add_to_cart(values[0], values[1]))
        refresh()


def add_inventory():
    values = read_inputs()
    if values is not None:
        status.set(store.add_stock(values[0], values[1]))
        refresh()


def set_inventory():
    values = read_inputs()
    if values is not None:
        status.set(store.update_stock(values[0], values[1]))
        refresh()


def show_bill():
    show_text(bill_text, store.generate_bill())
    status.set("Bill preview generated. Checkout to complete purchase.")


def do_checkout():
    if len(store.get_cart_data()) == 0:
        status.set("Cart is empty; add products first.")
        return
    show_text(bill_text, store.checkout())
    status.set("Purchase completed. Stock updated.")
    refresh()


def reset_cart():
    status.set(store.clear_cart())
    refresh()

buttons = tk.Frame(left, bg="white")
buttons.pack(fill="x", pady=8)
for label, action in (("Add to Cart", add_item), ("Add Stock", add_inventory), ("Set Stock", set_inventory)):
    tk.Button(buttons, text=label, command=action, bg="#1b6bb3", fg="white", font=("Arial", 10, "bold"), padx=10, pady=8).pack(side="left", padx=3, fill="x", expand=True)
cart_buttons = tk.Frame(right, bg="white")
cart_buttons.pack(fill="x", pady=8)
for label, action in (("Preview Bill", show_bill), ("Checkout", do_checkout), ("Clear Cart", reset_cart)):
    tk.Button(cart_buttons, text=label, command=action, bg="#147d69", fg="white", font=("Arial", 10, "bold"), padx=8, pady=8).pack(side="left", padx=3, fill="x", expand=True)

menu = tk.Menu(root)
actions = tk.Menu(menu, tearoff=0)
actions.add_command(label="Refresh Inventory", command=refresh)
actions.add_command(label="Preview Bill", command=show_bill)
actions.add_separator()
actions.add_command(label="Exit", command=root.destroy)
menu.add_cascade(label="Actions", menu=actions)
root.config(menu=menu)

tk.Label(root, textvariable=status, bg="#d9e8f8", fg="#173c61", anchor="w", padx=14, pady=10).pack(fill="x")
refresh()
root.mainloop()
