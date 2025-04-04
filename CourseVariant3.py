import tkinter as tk
from tkinter import messagebox

class BankCard:
    def __init__(self, pin, balance, card_type):
        self.pin = pin
        self.balance = balance
        self.card_type = card_type
        self.history = []

class CreditCard(BankCard):
    def __init__(self, pin, balance, card_type='credit', peni=0):
        super().__init__(pin, balance, card_type)
        self.peni = peni

    def if_negative(self):
        if self.balance < 0:
            self.peni += -(int(self.balance)) * 25.9
        return self.peni

class DebitCard(BankCard):
    def __init__(self, pin, balance, card_type='debit'):
        super().__init__(pin, balance, card_type)

class ATM:
    def __init__(self):
        self.card_inserted = False
        self.current_card = None
        self.root = tk.Tk()
        self.root.title("Банкомат")
        self.current_frame = None
        self.attempts = 0
        self.show_welcome_frame()

    def show_welcome_frame(self):
        self.clear_frame()
        tk.Label(self.root, text="Добро пожаловать в банкомат!", font=('Arial', 14)).pack(pady=20)
        tk.Button(self.root, text="Вставить карту", command=self.insert_card).pack(pady=10)
        tk.Button(self.root, text="Отмена", command=self.root.destroy).pack()

    def create_pin_frame(self):
        self.clear_frame()
        tk.Label(self.root, text="Введите PIN-код:", font=('Arial', 12)).pack(pady=10)
        self.pin_entry = tk.Entry(self.root, show='*', font=('Arial', 12))
        self.pin_entry.pack()
        tk.Button(self.root, text="Подтвердить", command=self.check_pin).pack(pady=10)
        tk.Button(self.root, text="Отмена", command=self.reset_atm).pack()

    def create_main_menu(self):
        self.clear_frame()
        tk.Label(self.root, text="Главное меню", font=('Arial', 14)).pack(pady=20)
        tk.Button(self.root, text="Снять деньги", command=self.withdraw_money).pack(pady=5)
        tk.Button(self.root, text="Перевести деньги", command=self.transfer_money).pack(pady=5)
        tk.Button(self.root, text="Проверить баланс", command=self.print_balance).pack(pady=5)
        tk.Button(self.root, text="История операций", command=self.print_history).pack(pady=5)
        tk.Button(self.root, text="Возврат карты", command=self.reset_atm).pack(pady=10)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def insert_card(self):
        self.clear_frame()
        tk.Label(self.root, text="Чтение карточки...").pack(pady=20)
        self.root.after(2000, self.create_pin_frame)
        self.card_inserted = True

    def check_pin(self):
        pin_input = self.pin_entry.get()
        if pin_input == self.current_card.pin:
            self.attempts = 0
            self.create_main_menu()
        else:
            self.attempts += 1
            if self.attempts < 3:
                messagebox.showerror("Ошибка", "Неправильный PIN-код")
                self.pin_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Ошибка", "Превышено число попыток входа, карта блокируется")
                self.root.destroy()

    def withdraw_money(self):
        self.clear_frame()
        tk.Label(self.root, text="Снять деньги").pack(pady=10)
        tk.Label(self.root, text="Введите сумму:").pack()
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack()
        tk.Button(self.root, text="Подтвердить", command=self.process_withdraw).pack(pady=10)
        tk.Button(self.root, text="Назад", command=self.create_main_menu).pack()

    def transfer_money(self):
        self.clear_frame()
        tk.Label(self.root, text="Перевести деньги").pack(pady=10)
        tk.Label(self.root, text="Введите сумму:").pack()
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack()
        tk.Button(self.root, text="Подтвердить", command=self.process_transfer).pack(pady=10)
        tk.Button(self.root, text="Назад", command=self.create_main_menu).pack()

    def process_withdraw(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= self.current_card.balance:
                self.current_card.balance -= amount
                self.current_card.history.append(f"Снято {amount}")
                messagebox.showinfo("Успешно", f"Сумма {amount} снята. Баланс: {self.current_card.balance}")
                self.create_main_menu()
            elif amount > self.current_card.balance and self.current_card.card_type == 'credit':
                self.current_card.balance -= amount
                self.current_card.history.append(f"Снято {amount} (кредит)")
                messagebox.showinfo("Успешно", f"Сумма {amount} снята. Баланс: {self.current_card.balance}, пени: {self.current_card.if_negative()}")
                self.create_main_menu()
            else:
                messagebox.showerror("Ошибка", "Недостаточно средств")
                self.create_main_menu()
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректная сумма")
            self.create_main_menu()

    def process_transfer(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= self.current_card.balance:
                self.current_card.balance -= amount
                self.current_card.history.append(f"Переведено {amount}")
                messagebox.showinfo("Успешно", f"Сумма {amount} переведена. Баланс: {self.current_card.balance}")
                self.create_main_menu()
            elif amount > self.current_card.balance and self.current_card.card_type == 'credit':
                self.current_card.balance -= amount
                self.current_card.history.append(f"Переведено {amount} (кредит)")
                messagebox.showinfo("Успешно", f"Сумма {amount} переведена. Баланс: {self.current_card.balance}, пени: {self.current_card.if_negative()}")
                self.create_main_menu()
            else:
                messagebox.showerror("Ошибка", "Недостаточно средств")
                self.create_main_menu()
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректная сумма")
            self.create_main_menu()

    def print_balance(self):
        balance_text = f"Баланс: {self.current_card.balance}"
        if self.current_card.card_type == 'credit' and self.current_card.balance < 0:
            balance_text += f", пени: {self.current_card.if_negative()}"
        messagebox.showinfo("Баланс", balance_text)
        self.create_main_menu()

    def print_history(self):
        history_text = "История операций:\n"
        for i, op in enumerate(self.current_card.history, 1):
            history_text += f"{i}. {op}\n"
        messagebox.showinfo("История", history_text)
        self.create_main_menu()

    def reset_atm(self):
        self.card_inserted = False
        self.attempts = 0
        self.show_welcome_frame()

    def run(self):
        self.root.mainloop()

atm = ATM()
card = CreditCard('1234', 1000)
atm.current_card = card
atm.run()