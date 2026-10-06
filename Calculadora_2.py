import tkinter as tk
import math

expr = ""

def update():
    display_var.set(expr if expr else "0")

def put(value):
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
    return eval(expr, {"__builtins__": {}}, {"pi": math.pi, "e": math.e})

def calc():
    global expr
    try:
        expr = str(safe_eval())
    except:
        expr = "Error"
    update()
    if expr == "Error":
        expr = ""

def fn(name):
    global expr
    try:
        x = float(safe_eval())

        if name == "sqrt":
            y = math.sqrt(x)
        elif name == "square":
            y = x ** 2
        elif name == "sin":
            y = math.sin(math.radians(x))
        elif name == "cos":
            y = math.cos(math.radians(x))
        elif name == "tan":
            y = math.tan(math.radians(x))
        elif name == "log":
            y = math.log10(x)
        elif name == "ln":
            y = math.log(x)
        elif name == "inv":
            y = 1 / x
        else:
            return

        expr = str(y)
    except:
        expr = "Error"

    update()

root = tk.Tk()
root.title("Calculadora Científica")
root.geometry("470x610")
root.resizable(False, False)

WHITE = "#ffffff"
BG = "#f8f7fc"
PURPLE = "#7c3aed"
PURPLE_DARK = "#5b21b6"
PURPLE_SOFT = "#ede9fe"
PURPLE_BORDER = "#c4b5fd"
TEXT = "#2a2233"
MUTED = "#8b7c99"
BTN = "#ffffff"

root.configure(bg=BG)

container = tk.Frame(root, bg=BG, padx=18, pady=18)
container.pack(fill="both", expand=True)

header = tk.Frame(container, bg=BG)
header.pack(fill="x")

tk.Label(
    header,
    text="Calculadora Científica",
    bg=BG,
    fg=TEXT,
    font=("Segoe UI", 19, "bold")
).pack(side="left")

tk.Label(
    header,
    text="SCI",
    bg=PURPLE_SOFT,
    fg=PURPLE_DARK,
    font=("Segoe UI", 9, "bold"),
    padx=10,
    pady=4
).pack(side="right")

display_box = tk.Frame(
    container,
    bg=WHITE,
    highlightbackground=PURPLE_BORDER,
    highlightthickness=2
)
display_box.pack(fill="x", pady=(16, 14))

display_var = tk.StringVar(value="0")

tk.Label(
    display_box,
    textvariable=display_var,
    bg=WHITE,
    fg=TEXT,
    anchor="e",
    justify="right",
    font=("Segoe UI", 29),
    padx=16,
    pady=20
).pack(fill="x")

# Fila científica superior
science = tk.Frame(container, bg=BG)
science.pack(fill="x", pady=(0, 8))

scientific_buttons = [
    ("sin", lambda: fn("sin")),
    ("cos", lambda: fn("cos")),
    ("tan", lambda: fn("tan")),
    ("log", lambda: fn("log")),
    ("ln", lambda: fn("ln")),
    ("√", lambda: fn("sqrt")),
    ("x²", lambda: fn("square")),
    ("1/x", lambda: fn("inv")),
]

for i, (text, command) in enumerate(scientific_buttons):
    b = tk.Button(
        science,
        text=text,
        command=command,
        bg=PURPLE_SOFT,
        fg=PURPLE_DARK,
        activebackground=PURPLE,
        activeforeground="white",
        bd=0,
        highlightbackground=PURPLE_BORDER,
        highlightthickness=1,
        font=("Segoe UI", 10, "bold"),
        cursor="hand2"
    )
    b.grid(row=i//4, column=i%4, sticky="nsew", padx=4, pady=4, ipady=8)

for c in range(4):
    science.columnconfigure(c, weight=1)

# Teclado principal
grid = tk.Frame(container, bg=BG)
grid.pack(fill="both", expand=True)

buttons = [
    ("AC", clear, "special"),
    ("⌫", back, "special"),
    ("(", lambda: put("("), "special"),
    (")", lambda: put(")"), "special"),
    ("÷", lambda: put("/"), "op"),

    ("7", lambda: put("7"), "num"),
    ("8", lambda: put("8"), "num"),
    ("9", lambda: put("9"), "num"),
    ("π", lambda: put("pi"), "special"),
    ("×", lambda: put("*"), "op"),

    ("4", lambda: put("4"), "num"),
    ("5", lambda: put("5"), "num"),
    ("6", lambda: put("6"), "num"),
    ("e", lambda: put("e"), "special"),
    ("−", lambda: put("-"), "op"),

    ("1", lambda: put("1"), "num"),
    ("2", lambda: put("2"), "num"),
    ("3", lambda: put("3"), "num"),
    ("%", lambda: put("%"), "special"),
    ("+", lambda: put("+"), "op"),

    ("0", lambda: put("0"), "num"),
    ("00", lambda: put("00"), "num"),
    (".", lambda: put("."), "num"),
    ("^", lambda: put("**"), "special"),
    ("=", calc, "equal")
]

for i, (text, command, kind) in enumerate(buttons):
    if kind == "num":
        bg = BTN
        fg = TEXT
        border = "#ddd6fe"
    elif kind == "op":
        bg = PURPLE
        fg = "white"
        border = PURPLE_DARK
    elif kind == "equal":
        bg = PURPLE_DARK
        fg = "white"
        border = PURPLE_DARK
    else:
        bg = "#f5f3ff"
        fg = PURPLE_DARK
        border = PURPLE_BORDER

    b = tk.Button(
        grid,
        text=text,
        command=command,
        bg=bg,
        fg=fg,
        activebackground=PURPLE_SOFT if kind == "num" else PURPLE_DARK,
        activeforeground=TEXT if kind == "num" else "white",
        bd=0,
        highlightbackground=border,
        highlightthickness=1,
        font=("Segoe UI", 13, "bold"),
        cursor="hand2"
    )
    b.grid(
        row=i//5,
        column=i%5,
        sticky="nsew",
        padx=4,
        pady=4
    )

for r in range(5):
    grid.rowconfigure(r, weight=1)
for c in range(5):
    grid.columnconfigure(c, weight=1)

tk.Label(
    container,
    text="Enrique Rojas",
    bg=BG,
    fg=MUTED,
    font=("Segoe UI", 8)
).pack(pady=(10, 0))

root.mainloop()
