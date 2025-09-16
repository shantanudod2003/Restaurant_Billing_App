def calculate_totals(subtotal):
    gst = subtotal * 0.05
    discount = subtotal * 0.10
    total = subtotal + gst - discount
    return gst, discount, total
