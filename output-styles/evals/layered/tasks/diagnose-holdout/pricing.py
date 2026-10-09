def order_total(prices, discount_rate=0.0):
    subtotal = sum(prices)
    return subtotal * (1 - discount_rate)
