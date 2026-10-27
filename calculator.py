import tkinter as tk
from tkinter import messagebox
import hashlib
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
USERS = os.path.join(BASE, "users.json")
SESSION = os.path.join(BASE, "session.json")

BG = "#1e1e1e"
FG = "#ffffff"
GRAY = "#888888"
NUM = "#333333"
OP = "#f39c12"
EQ = "#2ecc71"
CLR = "#e74c3c"
EXTRA = "#555555"


def load_users():
    if os.path.exists(USERS):
        with open(USERS, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_users(users):
    with open(USERS, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def clear_session():
    if os.path.exists(SESSION):
        os.remove(SESSION)


def save_session(user, history):
    with open(SESSION, "w", encoding="utf-8") as f:
        json.dump({"user": user, "history": history}, f, ensure_ascii=False)


def fmt(x):
    if x == int(x) and abs(x) < 1e15:
        return str(int(x))
    return str(round(x, 10))


class Auth(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Калькулятор — вход")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.user = None
        tk.Label(self, text="Авторизация", bg=BG, fg=FG, font=("Segoe UI", 18, "bold")).pack(pady=(20, 10))
        tk.Label(self, text="Логин", bg=BG, fg=GRAY, font=("Segoe UI", 11)).pack(anchor="w", padx=30)
        self.login = tk.Entry(self, font=("Segoe UI", 13), bg=NUM, fg=FG, insertbackground=FG, relief="flat")
        self.login.pack(padx=30, fill="x", ipady=5)
        tk.Label(self, text="Пароль", bg=BG, fg=GRAY, font=("Segoe UI", 11)).pack(anchor="w", padx=30, pady=(10, 0))
        self.password = tk.Entry(self, show="•", font=("Segoe UI", 13), bg=NUM, fg=FG, insertbackground=FG, relief="flat")
        self.password.pack(padx=30, fill="x", ipady=5)
        tk.Button(self, text="Войти", command=self.sign_in, bg=EQ, fg=FG, font=("Segoe UI", 12, "bold"),
                  relief="flat", activebackground=EQ, activeforeground=FG).pack(padx=30, pady=(20, 5), fill="x", ipady=4)
        tk.Button(self, text="Регистрация", command=self.sign_up, bg=OP, fg=FG, font=("Segoe UI", 12, "bold"),
                  relief="flat", activebackground=OP, activeforeground=FG).pack(padx=30, pady=(0, 25), fill="x", ipady=4)
        self.geometry("320x340")
        self.bind("<Return>", lambda e: self.sign_in())
        self.login.focus()

    def fields(self):
        login = self.login.get().strip()
        password = self.password.get()
        if not login or not password:
            messagebox.showerror("Ошибка", "Введите логин и пароль")
            return None, None
        return login, password

    def sign_in(self):
        login, password = self.fields()
        if not login:
            return
        users = load_users()
        if users.get(login) != hash_password(password):
            messagebox.showerror("Ошибка", "Неверный логин или пароль")
            return
        self.user = login
        self.destroy()

    def sign_up(self):
        login, password = self.fields()
        if not login:
            return
        if len(password) < 4:
            messagebox.showerror("Ошибка", "Пароль должен быть не короче 4 символов")
            return
        users = load_users()
        if login in users:
            messagebox.showerror("Ошибка", "Пользователь уже существует")
            return
        users[login] = hash_password(password)
        save_users(users)
        messagebox.showinfo("Готово", "Регистрация успешна")
        self.user = login
        self.destroy()


class Calculator(tk.Tk):
    def __init__(self, user):
        super().__init__()
        self.title("Калькулятор")
        self.configure(bg=BG)
        self.geometry("340x500")
        self.minsize(300, 440)
        self.user = user
        self.log = []
        self.cur = "0"
        self.prev = None
        self.op = None
        self.reset = False

        self.top = tk.Label(self, text="", anchor="e", bg=BG, fg=GRAY, font=("Segoe UI", 14))
        self.top.pack(fill="x", padx=15, pady=(15, 0))
        self.main = tk.Label(self, text="0", anchor="e", bg=BG, fg=FG, font=("Segoe UI", 36, "bold"))
        self.main.pack(fill="x", padx=15, pady=(0, 10))

        grid = tk.Frame(self, bg=BG)
        grid.pack(fill="both", expand=True, padx=8, pady=8)
        rows = [
            [("C", CLR), ("±", EXTRA), ("%", EXTRA), ("⌫", EXTRA)],
            [("7", NUM), ("8", NUM), ("9", NUM), ("÷", OP)],
            [("4", NUM), ("5", NUM), ("6", NUM), ("×", OP)],
            [("1", NUM), ("2", NUM), ("3", NUM), ("−", OP)],
            [("0", NUM), (".", NUM), ("=", EQ), ("+", OP)],
        ]
        for r, row in enumerate(rows):
            grid.rowconfigure(r, weight=1)
            for c, (t, color) in enumerate(row):
                grid.columnconfigure(c, weight=1)
                tk.Button(grid, text=t, bg=color, fg=FG, activebackground=color, activeforeground=FG,
                          font=("Segoe UI", 18, "bold"), relief="flat", bd=0,
                          command=lambda t=t: self.press(t)).grid(row=r, column=c, sticky="nsew", padx=4, pady=4)

        self.bind("<Key>", self.key)

    def key(self, e):
        keys = {"*": "×", "/": "÷", "-": "−", "+": "+", "=": "=", "%": "%", ".": ".", ",": "."}
        if e.char.isdigit():
            self.press(e.char)
        elif e.char in keys:
            self.press(keys[e.char])
        elif e.keysym in ("Return", "KP_Enter"):
            self.press("=")
        elif e.keysym == "BackSpace":
            self.press("⌫")
        elif e.keysym in ("Escape", "Delete"):
            self.press("C")
        elif e.keysym == "F9":
            self.press("±")

    def press(self, t):
        if self.cur == "Ошибка" and t != "C":
            self.clear()
        if t.isdigit():
            if self.reset or self.cur == "0":
                self.cur = t
                self.reset = False
            elif self.cur == "-0":
                self.cur = "-" + t
            else:
                self.cur += t
        elif t == ".":
            if self.reset:
                self.cur = "0."
                self.reset = False
            elif "." not in self.cur:
                self.cur += "."
        elif t in "+−×÷":
            if self.op and not self.reset:
                self.calc()
                if self.cur == "Ошибка":
                    return self.show()
            self.prev = float(self.cur)
            self.op = t
            self.top.config(text=f"{fmt(self.prev)} {t}")
            self.reset = True
        elif t == "=":
            if self.op:
                a, b, o = self.prev, float(self.cur), self.op
                self.calc()
                line = f"{fmt(a)} {o} {fmt(b)} ="
                self.top.config(text=line)
                self.log.append(f"{line} {self.cur}")
                save_session(self.user, self.log)
                self.op = None
                self.reset = True
        elif t == "C":
            self.clear()
        elif t == "⌫":
            if self.reset and self.op:
                self.op = None
                self.cur = fmt(self.prev)
                self.top.config(text="")
                self.reset = False
            elif not self.reset:
                self.cur = self.cur[:-1]
                if self.cur in ("", "-"):
                    self.cur = "0"
        elif t == "±":
            self.cur = self.cur[1:] if self.cur.startswith("-") else "-" + self.cur
            self.reset = False
        elif t == "%":
            self.cur = fmt(float(self.cur) / 100)
        self.show()

    def calc(self):
        a, b = self.prev, float(self.cur)
        if self.op == "+":
            r = a + b
        elif self.op == "−":
            r = a - b
        elif self.op == "×":
            r = a * b
        else:
            if b == 0:
                self.cur = "Ошибка"
                self.op = None
                self.reset = True
                return
            r = a / b
        self.cur = fmt(r)

    def clear(self):
        self.cur = "0"
        self.prev = None
        self.op = None
        self.reset = False
        self.top.config(text="")

    def show(self):
        self.main.config(text=self.cur)


if __name__ == "__main__":
    clear_session()
    auth = Auth()
    auth.mainloop()
    if auth.user:
        Calculator(auth.user).mainloop()
