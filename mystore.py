import streamlit as st
import pandas as pd
from datetime import date

# File Paths for CSV Files
PRODUCTS_FILE = "record.csv"
SALES_FILE = "Sales.csv"

# Initialize CSV Files
def initialize_files():
    for file, columns in [
        (PRODUCTS_FILE, ["ProductID", "ProductName", "Quantity", "PerUnitPrice", "FullPrice"]),
        (SALES_FILE, ["SaleID", "ProductID", "QuantitySold", "ProductLeft", "SaleDate"])
    ]:
        try:
            pd.read_csv(file)
        except FileNotFoundError:
            pd.DataFrame(columns=columns).to_csv(file, index=False)

# Add Product
def add_product(product_id, product_name, product_quantity, product_perunit_price):
    products = pd.read_csv(PRODUCTS_FILE)
    full_price = product_quantity * product_perunit_price
    new_product = {
        "ProductID": product_id,
        "ProductName": product_name,
        "Quantity": product_quantity,
        "PerUnitPrice": product_perunit_price,
        "FullPrice": full_price
    }
    products = pd.concat([products, pd.DataFrame([new_product])], ignore_index=True)
    products.to_csv(PRODUCTS_FILE, index=False)
    st.success(f"Product '{product_name}' added successfully!")

# Record Sale
def record_sale(product_id, quantity_sold):
    products = pd.read_csv(PRODUCTS_FILE)
    sales = pd.read_csv(SALES_FILE)

    if product_id not in products["ProductID"].values:
        st.error("Error: Product ID not found.")
        return

    product = products.loc[products["ProductID"] == product_id]
    available_quantity = product["Quantity"].values[0]

    if available_quantity < quantity_sold:
        st.error("Error: Insufficient stock.")
        return

    # Update stock in products
    products.loc[products["ProductID"] == product_id, "Quantity"] -= quantity_sold
    product_left = products.loc[products["ProductID"] == product_id, "Quantity"].values[0]
    products.to_csv(PRODUCTS_FILE, index=False)

    # Record sale in sales
    sale_id = sales["SaleID"].max() + 1 if not sales.empty else 1
    new_sale = {
        "SaleID": sale_id,
        "ProductID": product_id,
        "QuantitySold": quantity_sold,
        "ProductLeft": product_left,
        "SaleDate": date.today()
    }
    sales = pd.concat([sales, pd.DataFrame([new_sale])], ignore_index=True)
    sales.to_csv(SALES_FILE, index=False)
    st.success(f"Sale recorded successfully! ProductID: {product_id}, Quantity Sold: {quantity_sold}")

# View Products
def view_products():
    products = pd.read_csv(PRODUCTS_FILE)
    if not products.empty:
        st.write(products)
    else:
        st.write("No products available.")

# View Sales
def view_sales():
    sales = pd.read_csv(SALES_FILE)
    if not sales.empty:
        st.write(sales)
    else:
        st.write("No sales records available.")

# Streamlit Interface
def main():
    st.title("Store Record System")

    # Initialize files
    initialize_files()

    # Sidebar menu
    menu = ["Add Product", "Record Sale", "View Products", "View Sales"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Product":
        st.subheader("Add a New Product")
        product_id = st.number_input("Enter Product ID", min_value=1, step=1)
        product_name = st.text_input("Enter Product Name")
        product_quantity = st.number_input("Enter Product Quantity", min_value=1, step=1)
        product_perunit_price = st.number_input("Enter Product Per Unit Price", min_value=0.0, step=0.01)
        if st.button("Add Product"):
            add_product(product_id, product_name, product_quantity, product_perunit_price)

    elif choice == "Record Sale":
        st.subheader("Record a Sale")
        product_id = st.number_input("Enter Product ID", min_value=1, step=1)
        quantity_sold = st.number_input("Enter Quantity Sold", min_value=1, step=1)
        if st.button("Record Sale"):
            record_sale(product_id, quantity_sold)

    elif choice == "View Products":
        st.subheader("Product List")
        view_products()

    elif choice == "View Sales":
        st.subheader("Sales Records")
        view_sales()

if __name__ == "__main__":
    main()
