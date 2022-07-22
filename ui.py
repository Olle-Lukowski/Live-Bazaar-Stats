import tkinter as tk
from requester import Requester
from brain import BazaarBrain
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from saver import DataSaver
import datetime
from functools import partial


class TrackerInterface:
    def __init__(self, data_requester: Requester, data_saver: DataSaver):
        self.api_key = None
        self.canvas = None
        self.canvas2 = None
        self.brain = None
        self.data = None
        self.product_name = None
        self.product_profit = None
        self.product_profit_percentage = []
        self.product_buy_movement = []
        self.product_sell_movement = []
        self.data_saver = data_saver
        self.data_requester = data_requester
        self.root = tk.Tk()
        self.root.title("Live Bazaar Stats")
        self.product_names = []
        self.product_profits = []
        self.info_buttons = []

        self.product_name_text = tk.StringVar()
        self.product_profit_text = tk.StringVar()

        self.main_header = tk.Label(self.root, text="Live Bazaar Stats", font=("Arial", 30))
        self.main_header.config(padx=10, pady=10)
        self.main_header.grid(row=0, column=0)

        tk.Label(self.root, text="Please enter your API key below for the tracker to work", font=("Arial", 16)).grid(row=1, column=0)
        self.api_key_input = tk.Entry(self.root, width=30)
        self.api_key_input.grid(row=2, column=0)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit_button_clicked)
        self.submit_button.grid(row=3, column=0)

        self.root.mainloop()

    def submit_button_clicked(self):
        self.api_key = self.api_key_input.get()
        print(self.api_key)
        self.root.destroy()
        self.main()

    def main(self):
        self.root = tk.Tk()
        self.root.title("Live Bazaar Stats")

        self.main_header = tk.Label(self.root, text="Live Bazaar Stats", font=("Arial", 30))
        self.main_header.config(padx=10, pady=10)
        self.main_header.grid(row=0, column=0)

        self.data = self.data_requester.get({"Api-Key": self.api_key})
        print(self.data.json()["success"])
        self.brain = BazaarBrain(self.data_saver.load(), self.data_requester)
        response = self.brain.get_best_profit_product_percentage()
        profits, products, profit_percentages, buy_movements, sell_movements = response
        name_text = []
        profit_text = []
        profit_percentage_text = []
        buy_movement_text = []
        sell_movement_text = []
        for key, value in products.items():
            name_text.append(f"{key}: {value['product_id']}")
        for key, value in profits.items():
            profit_text.append(f"{key}: {value} coins per minute (avg)")
        for key, value in profit_percentages.items():
            profit_percentage_text.append(f"{key}: {value}%")
        for key, value in buy_movements.items():
            buy_movement_text.append(f"{key}: {value} instant buys per minute (avg)")
        for key, value in sell_movements.items():
            sell_movement_text.append(f"{key}: {value} instant sells per minute (avg)")
        self.root.update()
        print(name_text)

        index = 0
        for name in name_text:
            text_object = tk.Label(self.root, text=name, font=("Arial", 16))
            text_object.grid(row=index+1, column=0)
            self.product_names.append(text_object)
            index += 1
        index = 0
        for profit in profit_text:
            text_object = tk.Label(self.root, text=profit, font=("Arial", 16))
            text_object.grid(row=index+1, column=1)
            self.product_profits.append(text_object)
            index += 1
        index = 0
        for profit_percentage in profit_percentage_text:
            text_object = tk.Label(self.root, text=profit_percentage, font=("Arial", 16))
            text_object.grid(row=index+1, column=3)
            self.product_profit_percentage.append(text_object)
            index += 1
        index = 0
        for buy_movement in buy_movement_text:
            text_object = tk.Label(self.root, text=buy_movement, font=("Arial", 16))
            text_object.grid(row=index+11, column=0)
            self.product_buy_movement.append(text_object)
            index += 1
        index = 0
        for sell_movement in sell_movement_text:
            text_object = tk.Label(self.root, text=sell_movement, font=("Arial", 16))
            text_object.grid(row=index+11, column=1)
            self.product_sell_movement.append(text_object)
            info_button = tk.Button(self.root, text="Info",
                                    command=partial(self.info_button_clicked, index, name_text[index].split(" ")[1]))
            info_button.grid(row=index + 11, column=2)
            self.info_buttons.append(info_button)
            index += 1

        self.data_saver.save(self.data.json())

        self.refresh()

    def refresh(self):
        for text in self.product_names:
            text.destroy()
        for text in self.product_profits:
            text.destroy()
        for text in self.product_profit_percentage:
            text.destroy()
        for text in self.product_buy_movement:
            text.destroy()
        for text in self.product_sell_movement:
            text.destroy()
        for button in self.info_buttons:
            button.destroy()
        print("Refreshing")
        self.data = self.data_requester.get({"Api-Key": self.api_key})
        self.data_saver.save(self.data.json())
        self.brain.update_data(self.data_saver.load())
        response = self.brain.get_best_profit_product_percentage()
        profits, products, profit_percentages, buy_movements, sell_movements = response
        name_text = []
        profit_text = []
        profit_percentage_text = []
        buy_movement_text = []
        sell_movement_text = []
        self.info_buttons = []
        self.product_names = []
        self.product_profits = []
        self.product_profit_percentage = []
        self.product_buy_movement = []
        self.product_sell_movement = []
        for key, value in products.items():
            print(key, value)
            name_text.append(f"{key}: {value['product_id']}")
        for key, value in profits.items():
            print(key, value)
            profit_text.append(f"{key}: {value} coins per minute (avg)")
        for key, value in profit_percentages.items():
            print(key, value)
            profit_percentage_text.append(f"{key}: {value}%")
        for key, value in buy_movements.items():
            print(key, value)
            buy_movement_text.append(f"{key}: {value} instant buys per minute (avg)")
        for key, value in sell_movements.items():
            print(key, value)
            sell_movement_text.append(f"{key}: {value} instant sells per minute (avg)")
        self.root.update()

        index = 0
        for name in name_text:
            self.product_names.append(tk.Label(self.root, text=name, font=("Arial", 16)))
            self.product_names[index].grid(row=index+1, column=0)
            index += 1
        index = 0
        for profit in profit_text:
            self.product_profits.append(tk.Label(self.root, text=profit, font=("Arial", 16)))
            self.product_profits[index].grid(row=index+1, column=1)
            index += 1
        index = 0
        for profit_percentage in profit_percentage_text:
            self.product_profit_percentage.append(tk.Label(self.root, text=profit_percentage, font=("Arial", 16)))
            self.product_profit_percentage[index].grid(row=index+1, column=3)
            index += 1
        index = 0
        for buy_movement in buy_movement_text:
            self.product_buy_movement.append(tk.Label(self.root, text=buy_movement, font=("Arial", 16)))
            self.product_buy_movement[index].grid(row=index+11, column=0)
            index += 1
        index = 0
        for sell_movement in sell_movement_text:
            self.product_sell_movement.append(tk.Label(self.root, text=sell_movement, font=("Arial", 16)))
            self.product_sell_movement[index].grid(row=index+11, column=1)
            info_button = tk.Button(self.root, text="Info",
                                    command=partial(self.info_button_clicked, index, name_text[index].split(" ")[1]))
            info_button.grid(row=index + 11, column=2)
            self.info_buttons.append(info_button)
            index += 1
        self.root.update()
        self.root.after(60000, self.refresh)

    def info_button_clicked(self, index, product_id):
        win = tk.Toplevel()
        win.title("Product Info")
        win.geometry("1000x1000")
        win.resizable(False, False)
        win.config(padx=10, pady=10)
        print(f"Info button clicked for {index}")
        fig = Figure(figsize=(5,5), dpi=100)
        fig.tight_layout(pad=1.0)
        a = fig.add_subplot(221)
        data = self.data_saver.load()
        timestamps = [x for x in data]
        prices = []
        for i in range(len(timestamps)):
            price = data[timestamps[i]]["products"][product_id]["buy_summary"][0]["pricePerUnit"]
            prices.append(price)
        dates = []
        for i in range(len(timestamps)):
            date = datetime.datetime.fromtimestamp(float(timestamps[i])).strftime('%Y-%m-%d %H:%M:%S')
            dates.append(date)
        a.plot(dates, prices)
        a.xaxis.set_visible(False)
        a.set_xlabel('Date')
        a.set_ylabel('Price')
        a.set_title(f"{product_id}\nBuy Data")
        self.canvas = FigureCanvasTkAgg(fig, win)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0)

        fig2 = Figure(figsize=(5,5), dpi=100)
        fig2.tight_layout(pad=1.0)
        a2 = fig2.add_subplot(221)
        prices = []
        for i in range(len(timestamps)):
            price = data[timestamps[i]]["products"][product_id]["sell_summary"][0]["pricePerUnit"]
            prices.append(price)
        dates = []
        for i in range(len(timestamps)):
            date = datetime.datetime.fromtimestamp(float(timestamps[i])).strftime('%Y-%m-%d %H:%M:%S')
            dates.append(date)
        a2.plot(dates, prices)
        a2.xaxis.set_visible(False)
        a2.set_xlabel('Date')
        a2.set_ylabel('Price')
        a2.set_title(f"{product_id}\nSell Data")
        self.canvas2 = FigureCanvasTkAgg(fig2, win)
        self.canvas2.draw()
        self.canvas2.get_tk_widget().grid(row=0, column=1)

        fig3 = Figure(figsize=(5,5), dpi=100)
        fig3.tight_layout(pad=1.0)
        a3 = fig3.add_subplot(221)

        movement = []
        for i in range(len(timestamps)):
            move = data[timestamps[i]]["products"][product_id]["quick_status"]["buyMovingWeek"] / 7
            movement.append(move)
        dates = []
        for i in range(len(timestamps)):
            date = datetime.datetime.fromtimestamp(float(timestamps[i])).strftime('%Y-%m-%d %H:%M:%S')
            dates.append(date)
        a3.plot(dates, movement)
        a3.xaxis.set_visible(False)
        a3.set_xlabel('Date')
        a3.set_ylabel('Volume')
        a3.set_title(f"{product_id}\nBuy Movement 24h (avg from week)")
        self.canvas3 = FigureCanvasTkAgg(fig3, win)
        self.canvas3.draw()
        self.canvas3.get_tk_widget().grid(row=1, column=0)

        fig4 = Figure(figsize=(5,5), dpi=100)
        a4 = fig4.add_subplot(221)

        movement = []
        for i in range(len(timestamps)):
            move = data[timestamps[i]]["products"][product_id]["quick_status"]["sellMovingWeek"] / 7
            movement.append(move)
        dates = []
        for i in range(len(timestamps)):
            date = datetime.datetime.fromtimestamp(float(timestamps[i])).strftime('%Y-%m-%d %H:%M:%S')
            dates.append(date)
        a4.plot(dates, movement)
        a4.xaxis.set_visible(False)
        a4.set_xlabel('Date')
        a4.set_ylabel('Movement')
        a4.set_title(f"{product_id}\nSell Movement 24h (avg from week)")
        self.canvas4 = FigureCanvasTkAgg(fig4, win)
        self.canvas4.draw()
        self.canvas4.get_tk_widget().grid(row=1, column=1)

