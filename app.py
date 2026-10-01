
import streamlit as st
from food_delivery import Customer, Restaurant, MenuItem, DeliveryPartner

st.set_page_config(page_title="Food Delivery System", page_icon="🍔", layout="wide")

st.title("🍔 Food Delivery System")
st.caption("Simple Streamlit interface for the OOP food delivery project")

# -----------------------------
# Session state
# -----------------------------
if "customer" not in st.session_state:
    st.session_state.customer = None

if "restaurant" not in st.session_state:
    restaurant = Restaurant("Tasty Bites", "Chhatrapati Sambhajinagar")
    restaurant.add_item(MenuItem("Pizza", 250, True))
    restaurant.add_item(MenuItem("Burger", 150, True))
    restaurant.add_item(MenuItem("Pasta", 180, True))
    restaurant.add_item(MenuItem("Biryani", 220, False))
    st.session_state.restaurant = restaurant

if "delivery_partner" not in st.session_state:
    st.session_state.delivery_partner = None

if "order" not in st.session_state:
    st.session_state.order = None

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("📌 Navigation")

section = st.sidebar.radio(
    "Choose a section",
    [
        "1. Create Customer",
        "2. Add Wallet Balance",
        "3. Restaurant Menu",
        "4. Place Order",
        "5. Create Delivery Partner",
        "6. Accept Order",
        "7. Complete Delivery",
    ],
)

customer = st.session_state.customer
restaurant = st.session_state.restaurant
partner = st.session_state.delivery_partner
order = st.session_state.order


# =========================================================
# 1. CREATE CUSTOMER
# =========================================================
if section == "1. Create Customer":
    st.header("👤 Create Customer")

    name = st.text_input("Customer Name")
    phone = st.text_input("Phone Number")
    address = st.text_input("Delivery Address")

    if st.button("Create Customer", type="primary"):
        if name and phone and address:
            st.session_state.customer = Customer(name, phone, address)
            st.success(f"Customer '{name}' created successfully!")
        else:
            st.warning("Please enter name, phone number, and address.")

    if customer:
        st.subheader("Customer Details")
        st.write(f"**Name:** {customer._name}")
        st.write(f"**Phone:** {customer._phone}")
        st.write(f"**Address:** {customer.address}")
        st.write(f"**Wallet Balance:** ₹{customer._wallet_balance:.2f}")


# =========================================================
# 2. ADD WALLET BALANCE
# =========================================================
elif section == "2. Add Wallet Balance":
    st.header("💰 Add Wallet Balance")

    if customer is None:
        st.warning("Please create a customer first.")
    else:
        st.write(f"Current wallet balance: **₹{customer._wallet_balance:.2f}**")

        amount = st.number_input(
            "Enter amount",
            min_value=0.0,
            step=100.0,
            format="%.2f"
        )

        if st.button("Add Money", type="primary"):
            if amount > 0:
                customer.add_to_wallet(amount)
                st.success(f"₹{amount:.2f} added to wallet!")
                st.write(
                    f"New wallet balance: **₹{customer._wallet_balance:.2f}**"
                )
            else:
                st.warning("Enter an amount greater than 0.")


# =========================================================
# 3. RESTAURANT MENU
# =========================================================
elif section == "3. Restaurant Menu":
    st.header("🍽️ Restaurant Menu")

    st.subheader(f"{restaurant.name}")
    st.write(f"📍 Location: {restaurant.location}")
    st.write(f"🟢 Open: {restaurant.is_open()}")

    menu = restaurant.get_menu()

    for i, item in enumerate(menu, start=1):
        veg_text = "🟢 Veg" if item.is_veg else "🔴 Non-Veg"

        col1, col2, col3 = st.columns([3, 2, 2])
        with col1:
            st.write(f"**{i}. {item.name}**")
        with col2:
            st.write(f"₹{item.price:.2f}")
        with col3:
            st.write(veg_text)

    st.info("GST: 5% + Packaging Fee: ₹20")


# =========================================================
# 4. PLACE ORDER
# =========================================================
elif section == "4. Place Order":
    st.header("🛒 Place an Order")

    if customer is None:
        st.warning("Please create a customer first.")
    else:
        menu = restaurant.get_menu()

        item_names = [item.name for item in menu]

        selected_names = st.multiselect(
            "Select food items",
            item_names
        )

        if selected_names:
            selected_items = [
                item for item in menu if item.name in selected_names
            ]

            st.subheader("Selected Items")

            subtotal = 0
            for item in selected_items:
                st.write(f"- {item.name}: ₹{item.price:.2f}")
                subtotal += item.price

            gst = subtotal * 0.05
            packaging = 20
            total = subtotal + gst + packaging

            st.write(f"**Subtotal:** ₹{subtotal:.2f}")
            st.write(f"**GST (5%):** ₹{gst:.2f}")
            st.write(f"**Packaging:** ₹{packaging:.2f}")
            st.write(f"### Total: ₹{total:.2f}")

            if st.button("Place Order", type="primary"):
                # The provided Order class calculates the bill but does not
                # deduct wallet money, so this interface only creates the order.
                st.session_state.order = customer.place_order(
                    restaurant,
                    selected_items
                )

                st.success(
                    f"Order #{st.session_state.order._order_id} placed successfully!"
                )

                st.warning(
                    f"Your OTP is: **{st.session_state.order._otp}**"
                )
        else:
            st.info("Select at least one food item.")

        if order:
            st.divider()
            st.subheader("Current Order")
            st.write(f"**Order ID:** {order._order_id}")
            st.write(f"**Status:** {order._status}")
            st.write(f"**Bill:** ₹{order.calculate_bill():.2f}")
            st.write(f"**Estimated Time:** {order.estimated_time()} minutes")


# =========================================================
# 5. CREATE DELIVERY PARTNER
# =========================================================
elif section == "5. Create Delivery Partner":
    st.header("🛵 Create Delivery Partner")

    name = st.text_input("Partner Name")
    phone = st.text_input("Partner Phone")
    vehicle = st.selectbox(
        "Vehicle",
        ["Bike", "Scooter", "Cycle"]
    )

    if st.button("Create Delivery Partner", type="primary"):
        if name and phone:
            st.session_state.delivery_partner = DeliveryPartner(
                name,
                phone,
                vehicle
            )
            st.success(f"Delivery partner '{name}' created successfully!")
        else:
            st.warning("Please enter partner name and phone.")

    if partner:
        st.subheader("Delivery Partner Details")
        st.write(f"**Name:** {partner._name}")
        st.write(f"**Phone:** {partner._phone}")
        st.write(f"**Vehicle:** {partner.vehicle}")
        st.write(f"**Available:** {partner.is_available}")


# =========================================================
# 6. ACCEPT ORDER
# =========================================================
elif section == "6. Accept Order":
    st.header("📦 Accept Order")

    if order is None:
        st.warning("Please place an order first.")
    elif partner is None:
        st.warning("Please create a delivery partner first.")
    else:
        st.write(f"**Order ID:** {order._order_id}")
        st.write(f"**Current Status:** {order._status}")
        st.write(f"**Delivery Partner:** {partner._name}")
        st.write(f"**Partner Available:** {partner.is_available}")

        if order._status == "Placed" and partner.is_available:
            if st.button("Accept Order", type="primary"):
                partner.accept_order(order)
                st.success("Order accepted by delivery partner!")
                st.write(f"**New Status:** {order._status}")
        elif order._status == "Accepted":
            st.info("This order has already been accepted.")
        else:
            st.warning("Order cannot be accepted in its current state.")


# =========================================================
# 7. COMPLETE DELIVERY
# =========================================================
elif section == "7. Complete Delivery":
    st.header("🔐 Complete Delivery")

    if order is None:
        st.warning("Please place an order first.")
    elif partner is None:
        st.warning("Please create a delivery partner first.")
    elif order._status != "Accepted":
        st.warning(
            f"Order must be in 'Accepted' status. Current status: {order._status}"
        )
    else:
        st.write(f"**Order ID:** {order._order_id}")
        st.write(f"**Delivery Partner:** {partner._name}")
        st.write(f"**Current Status:** {order._status}")

        otp = st.text_input(
            "Enter customer OTP",
            max_chars=4,
            type="password"
        )

        if st.button("Verify OTP & Complete Delivery", type="primary"):
            if otp.isdigit() and len(otp) == 4:
                partner.deliver(order, int(otp))

                if order._status == "Delivered":
                    st.success("✅ OTP verified. Delivery completed!")
                    st.write(f"**Final Status:** {order._status}")
                    st.write(
                        f"**Delivery Partner Available:** "
                        f"{partner.is_available}"
                    )
                else:
                    st.error("❌ Incorrect OTP. Delivery is not completed.")
            else:
                st.warning("Please enter a valid 4-digit OTP.")


# -----------------------------
# Current order status
# -----------------------------
st.sidebar.divider()
st.sidebar.subheader("📋 Current Status")

if customer:
    st.sidebar.write(f"👤 Customer: {customer._name}")
else:
    st.sidebar.write("👤 Customer: Not created")

if order:
    st.sidebar.write(f"🧾 Order: #{order._order_id}")
    st.sidebar.write(f"📌 Status: {order._status}")
else:
    st.sidebar.write("🧾 Order: Not placed")

if partner:
    st.sidebar.write(f"🛵 Partner: {partner._name}")
else:
    st.sidebar.write("🛵 Partner: Not created")
