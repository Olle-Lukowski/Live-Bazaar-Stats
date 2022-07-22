

class BazaarBrain:
    def __init__(self, data, requester):
        timestamp = ""
        for key, value in data.items():
            timestamp = key
        print(timestamp)
        if timestamp == "":
            self.data = requester.get().json()
        else:
            self.data = data[timestamp]
        self.products = self.data["products"]

    def get_best_profit_product_percentage(self):
        profits_per_minute = {"one": -1000000, "two": -1000000, "three": -1000000, "four": -1000000, "five": -1000000, "six": -1000000, "seven": -1000000, "eight": -1000000, "nine": -1000000, "ten": -1000000}
        best_profit_products = {"one": None, "two": None, "three": None, "four": None, "five": None, "six": None, "seven": None, "eight": None, "nine": None, "ten": None}
        best_profits = {"one": -1000000, "two": -1000000, "three": -1000000, "four": -1000000, "five": -1000000, "six": -1000000, "seven": -1000000, "eight": -1000000, "nine": -1000000, "ten": -1000000}
        avg_buy_movement_minutes = {"one": -1000000, "two": -1000000, "three": -1000000, "four": -1000000, "five": -1000000, "six": -1000000, "seven": -1000000, "eight": -1000000, "nine": -1000000, "ten": -1000000}
        avg_sell_movement_minutes = {"one": -1000000, "two": -1000000, "three": -1000000, "four": -1000000, "five": -1000000, "six": -1000000, "seven": -1000000, "eight": -1000000, "nine": -1000000, "ten": -1000000}
        for key, product in self.products.items():
            product_buy_summary = product["buy_summary"]
            product_sell_summary = product["sell_summary"]
            product_quick_status = product["quick_status"]
            if len(product_buy_summary) > 0 and len(product_sell_summary) > 0:
                buy_price = product_buy_summary[0]["pricePerUnit"]
                sell_price = product_sell_summary[0]["pricePerUnit"]
                buy_movement_minutes = product_quick_status["buyMovingWeek"] / 7 / 24 / 60
                sell_movement_minutes = product_quick_status["sellMovingWeek"] / 7 / 24 / 60

                if buy_price == 0 or sell_price == 0:
                    continue
                profit_percentage = (buy_price - (sell_price*0.9875)) / (sell_price * 0.9875) * 100
                profit_per_minute = ((buy_price*0.9875) * min(sell_movement_minutes, buy_movement_minutes)) - (sell_price * min(sell_movement_minutes, buy_movement_minutes))
                print("Profit: " + str(profit_per_minute))
                # check if the profit is better than the current lowest profit in the best_profits list
                if profit_per_minute > profits_per_minute["ten"]:
                    for key2, value in profits_per_minute.items():
                        if profit_per_minute > value:
                            best_profit_products[key2] = product
                            best_profits[key2] = profit_percentage
                            avg_buy_movement_minutes[key2] = buy_movement_minutes
                            avg_sell_movement_minutes[key2] = sell_movement_minutes
                            profits_per_minute[key2] = profit_per_minute
                            break
        return profits_per_minute, best_profit_products, best_profits, avg_buy_movement_minutes, avg_sell_movement_minutes

    def update_data(self, data):
        timestamp = ""
        for key, value in data.items():
            timestamp = key
        print(timestamp)
        self.data = data[timestamp]
        self.products = self.data["products"]