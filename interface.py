import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

import ph2
from calculator import Auth

BG = "#1e1e1e"
FG = "#ffffff"
GRAY = "#888888"
NUM = "#333333"
OP = "#f39c12"
EQ = "#2ecc71"


class Interface(tk.Tk):
    def __init__(self, user):
        super().__init__()
        self.title("Калькулятор наработки I-131")
        self.configure(bg=BG)
        self.geometry("520x600")
        self.user = user

        tk.Label(self, text=f"Вы вошли как: {user}", bg=BG, fg=GRAY,
                 font=("Segoe UI", 10)).pack(anchor="e", padx=15, pady=(10, 0))
        tk.Label(self, text="Наработка Йода-131", bg=BG, fg=FG,
                 font=("Segoe UI", 18, "bold")).pack(pady=(5, 15))

        self.entries = {}
        self.add_field("Масса теллура (г)", "1")
        self.add_field("Время облучения (сут)", "7")
        self.add_field("Потери в пути (%)", "20")

        tk.Button(self, text="Рассчитать", command=self.calc, bg=EQ, fg=FG,
                  font=("Segoe UI", 12, "bold"), relief="flat",
                  activebackground=EQ, activeforeground=FG).pack(padx=30, pady=(15, 5), fill="x", ipady=5)
        tk.Button(self, text="График A(t)", command=self.graph, bg=OP, fg=FG,
                  font=("Segoe UI", 12, "bold"), relief="flat",
                  activebackground=OP, activeforeground=FG).pack(padx=30, pady=(0, 10), fill="x", ipady=5)

        self.out = tk.Text(self, bg=NUM, fg=FG, font=("Consolas", 11), relief="flat",
                           height=11, wrap="word", bd=0)
        self.out.pack(padx=15, pady=10, fill="both", expand=True)

    def add_field(self, name, default):
        f = tk.Frame(self, bg=BG)
        f.pack(fill="x", padx=30, pady=4)
        tk.Label(f, text=name, bg=BG, fg=GRAY, font=("Segoe UI", 11),
                 width=20, anchor="w").pack(side="left")
        e = tk.Entry(f, font=("Segoe UI", 12), bg=NUM, fg=FG, insertbackground=FG, relief="flat")
        e.insert(0, default)
        e.pack(side="right", fill="x", expand=True, ipady=3)
        self.entries[name] = e

    def read_inputs(self):
        try:
            m = float(self.entries["Масса теллура (г)"].get().replace(",", "."))
            days = float(self.entries["Время облучения (сут)"].get().replace(",", "."))
            poteri = float(self.entries["Потери в пути (%)"].get().replace(",", ".")) / 100
        except ValueError:
            messagebox.showerror("Ошибка", "Введите числа во все поля")
            return None
        if m <= 0 or days < 0 or not (0 <= poteri < 1):
            messagebox.showerror("Ошибка", "Проверьте значения (масса > 0, потери 0..99%)")
            return None
        return m, days, poteri

    def calc(self):
        data = self.read_inputs()
        if not data:
            return
        m, days, poteri = data
        N = ph2.find_amount_te_core(m)
        R = ph2.find_rad_zahvata(ph2.F, N)
        A = ph2.find_A(R, days * ph2.DAY)
        A_ki = ph2.perevod_v_ki(A)
        A_dost = ph2.find_dostavka(A, poteri)
        patients = ph2.find_patients(A_dost)
        emkost = ph2.find_emkost()

        text = (
            f"1) Ядра-мишени N      = {N:.3e} шт\n"
            f"2) Скорость захвата R = {R:.3e} Бк (насыщение)\n\n"
            f"3) Активность за {days:g} сут:\n"
            f"     A = {A:.3e} Бк = {A / 10**9:.2f} ГБк\n\n"
            f"4) Перевод: {A_ki:.4f} Ки ({A_ki * 1000:.1f} мКи)\n\n"
            f"5) Доставка и нужды:\n"
            f"     после 48ч + {poteri * 100:.0f}% потерь: {A_dost / 10**9:.2f} ГБк\n"
            f"     пациентов с {m:g} г: {patients:.2f}\n"
            f"     нужно на 80 центров: {emkost / 10**12:.1f} ТБк\n"
        )
        self.out.delete("1.0", "end")
        self.out.insert("1.0", text)

    def graph(self):
        data = self.read_inputs()
        if not data:
            return
        m, days, poteri = data
        N = ph2.find_amount_te_core(m)
        R = ph2.find_rad_zahvata(ph2.F, N)
        end = max(days, 1) * ph2.DAY
        x1 = [i / ph2.DAY for i in range(0, int(end) + 1, 3600)]
        y1 = [ph2.find_A(R, i) / 10**9 for i in range(0, int(end) + 1, 3600)]
        A_end = ph2.find_A(R, days * ph2.DAY) / 10**9

        plt.figure()
        plt.plot(x1, y1, label="A(t)")
        plt.axhline(R / 10**9, ls="--", color="gray", label="насыщение")
        plt.scatter([days], [A_end], color="red", zorder=5)
        plt.annotate(f"{A_end:.2f} ГБк", (days, A_end),
                     textcoords="offset points", xytext=(-10, 10), color="red")
        plt.xlabel("T (сут)")
        plt.ylabel("A (ГБк)")
        plt.title(f"{m:g} г теллура, {days:g} сут облучения")
        plt.legend()
        plt.show()


if __name__ == "__main__":
    auth = Auth()
    auth.mainloop()
    if auth.user:
        Interface(auth.user).mainloop()
