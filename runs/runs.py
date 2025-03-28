from options.option import Options
from plots.plots import show_sensitivity_call_price_to_stock_price

if __name__ == "__main__":
    stock_prices = list(range(65, 141, 5))
    exercise_prices = [90]*len(stock_prices)

    options = Options(
        stock_prices,
        exercise_prices,
        182.5,
        4,
        35
    )

    call_prices = options.call_prices()
    call_price_intrinsic_value = options.call_intrinsic_values()
    for i in range(0, len(stock_prices)):
        print(f"Stock price: {stock_prices[i]} | BS call price {call_prices[i]} | Option intrinsic value: {call_price_intrinsic_value[i]}")

    show_sensitivity_call_price_to_stock_price(stock_prices, options.call_prices(), options.call_intrinsic_values())


