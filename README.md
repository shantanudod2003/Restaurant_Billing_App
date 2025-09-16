# 🍽️ Restaurant Billing App

A simple Restaurant Billing Software built using **Python Tkinter** and **SQLite**.

## ✨ Features
- Select menu items with quantity
- Automatic calculation of Subtotal, GST (5%), Discount (10%)
- Generates and displays final bill
- Saves order history into SQLite database

## 🚀 How to Run
1. Install requirements:
   ```bash
   pip install pandas
## Run the app
python app.py

## 📂 Project Structure

app.py → Main entry point (runs the app)

main_ui.py → Tkinter user interface

calculator.py → Billing calculations

db_utils.py → Database operations

menu.csv → Menu items

restaurant.db → SQLite database file
