import json
from config import TAX_RATE

with open("data/prices.json") as f:
    PRICES = json.load(f)

def calculate(cart):
    subtotal = sum(PRICES.get(name, 0.00) for name in cart.values())
    tax = subtotal * TAX_RATE
    total = subtotal + tax
    return subtotal, tax, total