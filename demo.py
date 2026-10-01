from food_delivery import Customer, DeliveryPartner, Restaurant, MenuItem

# =========================================================
# 1. Register customer Priya
# =========================================================
priya = Customer(
    name="Priya",
    phone="9876543210",
    address="Bangalore"
)

print("\n===== CUSTOMER CREATED =====")
priya.display_profile()


# =========================================================
# 2. Register delivery partner Rajesh
# =========================================================
# DeliveryPartner class requires a phone number, so a demo
# phone number is used here because the task only specifies
# Rajesh's name and vehicle.
rajesh = DeliveryPartner(
    name="Rajesh",
    phone="9999999999",
    vehicle="Bike"
)

print("\n===== DELIVERY PARTNER CREATED =====")
rajesh.display_profile()


# =========================================================
# 3. Create Bawarchi restaurant and add items
# =========================================================
bawarchi = Restaurant(
    name="Bawarchi",
    location="MG Road"
)

biryani = MenuItem(
    name="Biryani",
    price=250,
    is_veg=False
)

kebab = MenuItem(
    name="Kebab",
    price=200,
    is_veg=False
)

bawarchi.add_item(biryani)
bawarchi.add_item(kebab)

print("\n===== RESTAURANT MENU =====")
print("Restaurant:", bawarchi.name)
print("Location:", bawarchi.location)

for item in bawarchi.get_menu():
    print(item.name, "- ₹", item.price)


# =========================================================
# 4. Top up wallet by 500, then attempt -100
# =========================================================
print("\n===== WALLET =====")

priya.add_to_wallet(500)
print("After adding ₹500:", priya._wallet_balance)

priya.add_to_wallet(-100)
print("After attempting to add -₹100:", priya._wallet_balance)


# =========================================================
# 5. Priya places an order for Biryani and Kebab
# =========================================================
order = priya.place_order(
    bawarchi,
    [biryani, kebab]
)

# The Order class generates a random OTP.
# For this demo, we set it to 1234 so the requested
# OTP-delivery demonstration can be performed.
order._otp = 1234

print("\n===== ORDER CREATED =====")
print("Order ID:", order._order_id)
print("Status:", order._status)


# =========================================================
# 6. Print bill details and estimated delivery time
# =========================================================
subtotal = sum(item.price for item in order._items)
gst = subtotal * 0.05
packaging_fee = 20
total = order.calculate_bill()

print("\n===== BILL DETAILS =====")
print("Subtotal: ₹", subtotal)
print("GST (5%): ₹", gst)
print("Packaging Fee: ₹", packaging_fee)
print("Total: ₹", total)
print("Estimated Delivery Time:", order.estimated_time(), "minutes")


# =========================================================
# 7. Rajesh accepts order, wrong OTP, then correct OTP
# =========================================================
print("\n===== DELIVERY =====")

rajesh.accept_order(order)
print("Order status after acceptance:", order._status)

print("\nTrying wrong OTP: 9999")
rajesh.deliver(order, 9999)
print("Order status after wrong OTP:", order._status)

print("\nTrying correct OTP: 1234")
rajesh.deliver(order, 1234)
print("Order status after correct OTP:", order._status)


# =========================================================
# 8. Notify Priya and Rajesh
# =========================================================
print("\n===== NOTIFICATIONS =====")

priya.notify("Order delivered")
rajesh.notify("Order delivered")
