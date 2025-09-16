import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from calculator import calculate_totals
from db_utils import load_menu, save_order

class RestaurantBillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mauli Restaurant Billing System")
        self.root.geometry("700x750")
        self.root.configure(bg="#f7f7f7")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TButton", font=("Arial", 12), padding=5)
        style.configure("TCombobox", font=("Arial", 12))
        style.configure("TFrame", background="#f7f7f7")

        # Title
        ttk.Label(root, text="🍽️ Mauli Restaurant", font=("Arial", 20, "bold")).pack(pady=10)

        # Order type + table number
        top_frame = ttk.Frame(root)
        top_frame.pack(pady=5)
        ttk.Label(top_frame, text="Order Type: ").grid(row=0, column=0, padx=5)
        self.mode_var = tk.StringVar(value="Dine-In")
        self.mode_combo = ttk.Combobox(top_frame, textvariable=self.mode_var, values=["Dine-In", "Takeaway"], width=12)
        self.mode_combo.grid(row=0, column=1)

        ttk.Label(top_frame, text="Table No: ").grid(row=0, column=2, padx=5)
        self.table_var = tk.StringVar()
        self.table_entry = ttk.Entry(top_frame, textvariable=self.table_var, width=10)
        self.table_entry.grid(row=0, column=3)

        # Menu section
        self.menu_frame = ttk.LabelFrame(root, text="Select Menu Items")
        self.menu_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.menu_items = load_menu()
        self.qty_vars = {}

        for i, (item, price) in enumerate(self.menu_items):
            row = i // 2
            col = (i % 2) * 2
            ttk.Label(self.menu_frame, text=f"{item} (₹{price})").grid(row=row, column=col, sticky="w", padx=5, pady=5)
            qty_var = tk.IntVar(value=0)
            spinbox = tk.Spinbox(self.menu_frame, from_=0, to=20, width=5, textvariable=qty_var)
            spinbox.grid(row=row, column=col+1, padx=5)
            self.qty_vars[item] = qty_var

        # Payment method
        bottom_frame = ttk.Frame(root)
        bottom_frame.pack(pady=10)
        ttk.Label(bottom_frame, text="Payment Method: ").grid(row=0, column=0, padx=5)
        self.payment_var = tk.StringVar(value="Cash")
        ttk.Combobox(bottom_frame, textvariable=self.payment_var, values=["Cash", "Card", "UPI"], width=15).grid(row=0, column=1)

        # Generate bill button
        ttk.Button(root, text="🧾 Generate & Save Bill", command=self.generate_bill).pack(pady=10)

        # Output area
        self.output_text = tk.Text(root, height=15, width=80, font=("Courier", 10))
        self.output_text.pack(padx=10, pady=5)

    # ------------------ Generate Bill ------------------
    def generate_bill(self):
        selected_items = []
        subtotal = 0
        for item, qty_var in self.qty_vars.items():
            qty = qty_var.get()
            if qty > 0:
                for i, (m_item, price) in enumerate(self.menu_items):
                    if m_item == item:
                        selected_items.append((item, qty, price))
                        subtotal += price * qty

        if not selected_items:
            messagebox.showerror("Error", "Please select at least one item.")
            return

        gst, discount, total = calculate_totals(subtotal)

        now = datetime.now()
        date_time = now.strftime('%Y-%m-%d %H:%M:%S')

        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "========== MAULI RESTAURANT ==========\n")
        self.output_text.insert(tk.END, f"Date: {date_time}\n")
        self.output_text.insert(tk.END, f"Mode: {self.mode_var.get()}\n")
        if self.table_var.get():
            self.output_text.insert(tk.END, f"Table No: {self.table_var.get()}\n")
        self.output_text.insert(tk.END, "--------------------------------------\n")
        self.output_text.insert(tk.END, "Item\tQty\tPrice\n")
        self.output_text.insert(tk.END, "--------------------------------------\n")

        for item, qty, price in selected_items:
            self.output_text.insert(tk.END, f"{item}\t{qty}\t₹{price * qty:.2f}\n")

        self.output_text.insert(tk.END, "--------------------------------------\n")
        self.output_text.insert(tk.END, f"Subtotal:\t\t₹{subtotal:.2f}\n")
        self.output_text.insert(tk.END, f"GST (5%):\t\t₹{gst:.2f}\n")
        self.output_text.insert(tk.END, f"Discount (10%):\t₹{discount:.2f}\n")
        self.output_text.insert(tk.END, f"TOTAL:\t\t₹{total:.2f}\n")
        self.output_text.insert(tk.END, f"Payment: {self.payment_var.get()}\n")
        self.output_text.insert(tk.END, "======================================\n")

        save_order(
            self.mode_var.get(),
            self.table_var.get(),
            selected_items,
            subtotal,
            gst,
            discount,
            total,
            self.payment_var.get()
        )

# ------------------ Run App ------------------
def run_app():
    root = tk.Tk()
    app = RestaurantBillingApp(root)
    root.mainloop()
