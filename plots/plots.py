import matplotlib.pyplot as plt

def show_sensitivity_call_price_to_stock_price(stock_prices: list,
                                               call_prices: list,
                                               call_intrinsic_values: list):
    plt.figure(figsize=(8, 5))
    plt.plot(stock_prices, call_prices, 'b^-', label="BS Option Price")
    plt.plot(stock_prices, call_intrinsic_values, 'ms-', label="Intrinsic Value")

    plt.xlabel("Stock price", fontsize=12)
    plt.ylabel("Value", fontsize=12)
    plt.title("Comparing the BS Option Price to the Option Intrinsic Value", fontsize=14)
    plt.grid(True)
    plt.legend()
    plt.show()