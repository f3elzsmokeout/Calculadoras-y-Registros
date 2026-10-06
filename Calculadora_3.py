import tkinter as tk
import math

expr = ""

def update():
    display_var.set(expr if expr else "0")

def add(value):
    global expr
    if expr == "Error":
        expr = ""
    expr += value
    update()

def clear():
    global expr
    expr = ""
    update()

def back():
    global expr
    expr = expr[:-1]
    update()

def safe_eval():
    allowed = {
        "pi": math.pi,
        "e": math.e
    }
    return eval(expr, {"__builtins__": {}}, allowed)

def calculate():
    global expr
    try:
        expr = str(safe_eval())
    except:
        expr = "Error"
    update()

def scientific(name):
    global expr
    try:
        x = float(safe_eval())

        if name == "sqrt":
            result = math.sqrt(x)
        elif name == "square":
            result = x ** 2
        elif name == "cube":
            result = x ** 3
        elif name == "sin":
            result = math.sin(math.radians(x))
        elif name == "cos":
            result = math.cos(math.radians(x))
        elif name == "tan":
            result = math.tan(math.radians(x))
        elif name == "log":
            result = math.log10(x)
        elif name == "ln":
            result = math.log(x)
        elif name == "inv":
            result = 1 / x
        elif name == "abs":
            result = abs(x)
        else:
            return

        expr = str(result)
    except:
        expr = "Error"

    update()

def toggle_mode(event=None):
    global scientific_mode
    scientific_mode = not scientific_mode

    if scientific_mode:
        sci_frame.pack(fill="x", pady=(10, 0))
        mode_label.config(text="Modo científico")
        mode_button.config(text="Modo básico  ·  F2")
    else:
        sci_frame.pack_forget()
        mode_label.config(text="Modo básico")
        mode_button.config(text="Modo científico  ·  F2")

root = tk.Tk()
root.title("Calculadora Multifunción")
root.geometry("430x650")
root.resizable(False, False)
root.configure(bg="#090909")

PINK = "#ff4fa3"
PINK_DARK = "#d93687"
PINK_SOFT = "#2a1220"
BLACK = "#090909"
PANEL = "#151515"
BUTTON = "#222222"
TEXT = "#ffffff"
MUTED = "#9b7d8b"

container = tk.Frame(root, bg=BLACK, padx=18, pady=18)
container.pack(fill="both", expand=True)

title_row = tk.Frame(container, bg=BLACK)
title_row.pack(fill="x")

tk.Label(
    title_row,
    text="Calculadora Multifunción",
    bg=BLACK,
    fg=TEXT,
    font=("Segoe UI", 18, "bold")
).pack(side="left")

mode_label = tk.Label(
    title_row,
    text="Modo básico",
    bg=BLACK,
    fg=PINK,
    font=("Segoe UI", 9, "bold")
)
mode_label.pack(side="right")

display_frame = tk.Frame(
    container,
    bg=PANEL,
    highlightbackground=PINK_DARK,
    highlightthickness=1
)
display_frame.pack(fill="x", pady=(16, 10))

display_var = tk.StringVar(value="0")

tk.Label(
    display_frame,
    textvariable=display_var,
    bg=PANEL,
    fg=TEXT,
    anchor="e",
    justify="right",
    font=("Segoe UI", 28),
    padx=14,
    pady=18
).pack(fill="x")

mode_button = tk.Button(
    container,
    text="Modo científico  ·  F2",
    command=toggle_mode,
    bg=PINK_SOFT,
    fg=PINK,
    activebackground="#3a1729",
    activeforeground=TEXT,
    bd=0,
    font=("Segoe UI", 10, "bold"),
    padx=12,
    pady=8,
    cursor="hand2"
)
mode_button.pack(fill="x")

sci_frame = tk.Frame(container, bg=BLACK)

scientific_buttons = [
    ("√", lambda: scientific("sqrt")),
    ("x²", lambda: scientific("square")),
    ("x³", lambda: scientific("cube")),
    ("1/x", lambda: scientific("inv")),
    ("sin", lambda: scientific("sin")),
    ("cos", lambda: scientific("cos")),
    ("tan", lambda: scientific("tan")),
    ("log", lambda: scientific("log")),
    ("ln", lambda: scientific("ln")),
    ("|x|", lambda: scientific("abs")),
]

for i, (text, command) in enumerate(scientific_buttons):
    btn = tk.Button(
        sci_frame,
        text=text,
        command=command,
        bg=PINK_SOFT,
        fg=PINK,
        activebackground=PINK_DARK,
        activeforeground="white",
        bd=0,
        font=("Segoe UI", 10, "bold"),
        cursor="hand2"
    )
    btn.grid(
        row=i // 5,
        column=i % 5,
        sticky="nsew",
        padx=3,
        pady=3,
        ipady=8
    )

for c in range(5):
    sci_frame.columnconfigure(c, weight=1)

keys_frame = tk.Frame(container, bg=BLACK)
keys_frame.pack(fill="both", expand=True, pady=(10, 0))

buttons = [
    ("AC", clear, "special"),
    ("⌫", back, "special"),
    ("(", lambda: add("("), "special"),
    (")", lambda: add(")"), "special"),
    ("÷", lambda: add("/"), "op"),

    ("7", lambda: add("7"), "num"),
    ("8", lambda: add("8"), "num"),
    ("9", lambda: add("9"), "num"),
    ("π", lambda: add("pi"), "special"),
    ("×", lambda: add("*"), "op"),

    ("4", lambda: add("4"), "num"),
    ("5", lambda: add("5"), "num"),
    ("6", lambda: add("6"), "num"),
    ("e", lambda: add("e"), "special"),
    ("−", lambda: add("-"), "op"),

    ("1", lambda: add("1"), "num"),
    ("2", lambda: add("2"), "num"),
    ("3", lambda: add("3"), "num"),
    ("%", lambda: add("%"), "special"),
    ("+", lambda: add("+"), "op"),

    ("0", lambda: add("0"), "num"),
    ("00", lambda: add("00"), "num"),
    (".", lambda: add("."), "num"),
    ("^", lambda: add("**"), "special"),
    ("=", calculate, "equal")
]

for i, (text, command, kind) in enumerate(buttons):
    if kind == "num":
        bg = BUTTON
        fg = TEXT
    elif kind == "op":
        bg = PINK_DARK
        fg = "white"
    elif kind == "equal":
        bg = PINK
        fg = "#16000b"
    else:
        bg = PINK_SOFT
        fg = PINK

    btn = tk.Button(
        keys_frame,
        text=text,
        command=command,
        bg=bg,
        fg=fg,
        activebackground=PINK,
        activeforeground="white",
        bd=0,
        font=("Segoe UI", 13, "bold"),
        cursor="hand2"
    )
    btn.grid(
        row=i // 5,
        column=i % 5,
        sticky="nsew",
        padx=4,
        pady=4
    )

for r in range(5):
    keys_frame.rowconfigure(r, weight=1)
for c in range(5):
    keys_frame.columnconfigure(c, weight=1)

tk.Label(
    container,
    text="Enrique Rojas",
    bg=BLACK,
    fg=MUTED,
    font=("Segoe UI", 8)
).pack(pady=(8, 0))

scientific_mode = False
root.bind("<F2>", toggle_mode)

root.mainloop()
