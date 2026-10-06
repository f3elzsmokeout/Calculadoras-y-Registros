import tkinter as tk
from tkinter import ttk, messagebox
import json
from pathlib import Path

APP_DIR = Path.home() / ".inventario_enrique"
APP_DIR.mkdir(exist_ok=True)
DATA_FILE = APP_DIR / "inventario.json"

def cargar():
    try:
        if DATA_FILE.exists():
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except:
        pass
    return []

def guardar():
    DATA_FILE.write_text(
        json.dumps(inventario, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

def limpiar_campos():
    e_producto.delete(0, tk.END)
    e_cantidad.delete(0, tk.END)
    e_precio.delete(0, tk.END)

def agregar():
    producto = e_producto.get().strip()

    try:
        cantidad = int(e_cantidad.get())
        precio = float(e_precio.get())
    except:
        messagebox.showwarning(
            "Datos inválidos",
            "Cantidad y precio deben ser números."
        )
        return

    if not producto or cantidad <= 0 or precio < 0:
        messagebox.showwarning(
            "Datos inválidos",
            "Completa correctamente todos los campos."
        )
        return

    inventario.append({
        "producto": producto,
        "cantidad": cantidad,
        "precio": precio
    })

    guardar()
    limpiar_campos()
    refrescar()

def eliminar():
    sel = tabla.selection()

    if not sel:
        messagebox.showinfo(
            "Sin selección",
            "Selecciona un producto para eliminar."
        )
        return

    if not messagebox.askyesno(
        "Confirmar eliminación",
        "¿Deseas eliminar el producto seleccionado?"
    ):
        return

    indice = tabla.index(sel[0])
    inventario.pop(indice)
    guardar()
    refrescar()

def refrescar():
    for item in tabla.get_children():
        tabla.delete(item)

    total_valor = 0
    total_unidades = 0

    for x in inventario:
        subtotal = x["cantidad"] * x["precio"]
        total_valor += subtotal
        total_unidades += x["cantidad"]

        tabla.insert(
            "",
            "end",
            values=(
                x["producto"],
                x["cantidad"],
                f"Bs {x['precio']:.2f}",
                f"Bs {subtotal:.2f}"
            )
        )

    lbl_productos.config(text=str(len(inventario)))
    lbl_unidades.config(text=str(total_unidades))
    lbl_total.config(text=f"Bs {total_valor:.2f}")

root = tk.Tk()
root.title("Sistema de Registro de Inventario")
root.geometry("1020x620")
root.minsize(880, 540)

BG = "#f4fbff"
WHITE = "#ffffff"
BLUE = "#5cc8ff"
BLUE_DARK = "#218fca"
BLUE_SOFT = "#dff4ff"
LIME = "#b7f34a"
LIME_DARK = "#79b91d"
LIME_SOFT = "#efffd2"
TEXT = "#203040"
MUTED = "#718395"
BORDER = "#cbe7f3"

root.configure(bg=BG)

style = ttk.Style(root)
style.theme_use("clam")

style.configure(
    "Treeview",
    background=WHITE,
    fieldbackground=WHITE,
    foreground=TEXT,
    rowheight=32,
    borderwidth=0,
    font=("Segoe UI", 10)
)

style.configure(
    "Treeview.Heading",
    background=BLUE_DARK,
    foreground="white",
    font=("Segoe UI", 10, "bold"),
    relief="flat"
)

style.map(
    "Treeview.Heading",
    background=[("active", "#187bb0")]
)

style.configure(
    "Lime.TButton",
    background=LIME,
    foreground="#27410a",
    padding=10,
    font=("Segoe UI", 10, "bold")
)

style.map(
    "Lime.TButton",
    background=[("active", "#a6df3c")]
)

style.configure(
    "Blue.TButton",
    background=BLUE_SOFT,
    foreground=BLUE_DARK,
    padding=10,
    font=("Segoe UI", 10, "bold")
)

style.map(
    "Blue.TButton",
    background=[("active", "#caecff")]
)

# Barra superior
top = tk.Frame(root, bg=WHITE, height=82)
top.pack(fill="x")
top.pack_propagate(False)

tk.Label(
    top,
    text="Sistema de Registro de Inventario",
    bg=WHITE,
    fg=TEXT,
    font=("Segoe UI", 21, "bold")
).pack(side="left", padx=26)

badge = tk.Label(
    top,
    text="● ACTIVO",
    bg=LIME_SOFT,
    fg=LIME_DARK,
    font=("Segoe UI", 9, "bold"),
    padx=10,
    pady=5
)
badge.pack(side="right", padx=26)

# Contenido
body = tk.Frame(root, bg=BG)
body.pack(fill="both", expand=True, padx=22, pady=22)

# Columna izquierda
left = tk.Frame(
    body,
    bg=WHITE,
    highlightbackground=BORDER,
    highlightthickness=1
)
left.pack(side="left", fill="y", padx=(0, 16))

tk.Frame(left, bg=LIME, height=8).pack(fill="x")

tk.Label(
    left,
    text="Nuevo producto",
    bg=WHITE,
    fg=TEXT,
    font=("Segoe UI", 17, "bold")
).pack(anchor="w", padx=22, pady=(20, 4))

tk.Label(
    left,
    text="Agrega información al inventario.",
    bg=WHITE,
    fg=MUTED,
    font=("Segoe UI", 9)
).pack(anchor="w", padx=22, pady=(0, 16))

form = tk.Frame(left, bg=WHITE)
form.pack(fill="x", padx=22)

def campo(label):
    tk.Label(
        form,
        text=label,
        bg=WHITE,
        fg=TEXT,
        font=("Segoe UI", 10, "bold")
    ).pack(anchor="w", pady=(9, 3))

    entry = ttk.Entry(form, width=31, font=("Segoe UI", 10))
    entry.pack(fill="x")
    return entry

e_producto = campo("Producto")
e_cantidad = campo("Cantidad")
e_precio = campo("Precio unitario")

ttk.Button(
    form,
    text="+ Agregar producto",
    style="Lime.TButton",
    command=agregar
).pack(fill="x", pady=(22, 8))

ttk.Button(
    form,
    text="Eliminar seleccionado",
    style="Blue.TButton",
    command=eliminar
).pack(fill="x")

tk.Label(
    left,
    text="Enrique Rojas",
    bg=WHITE,
    fg="#a5b7c3",
    font=("Segoe UI", 8)
).pack(side="bottom", pady=14)

# Área derecha
right = tk.Frame(body, bg=BG)
right.pack(side="left", fill="both", expand=True)

# Tarjetas de resumen
cards = tk.Frame(right, bg=BG)
cards.pack(fill="x", pady=(0, 14))

def stat_card(parent, title, color):
    frame = tk.Frame(
        parent,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1,
        padx=16,
        pady=12
    )
    frame.pack(side="left", fill="x", expand=True, padx=5)

    tk.Label(
        frame,
        text=title,
        bg=WHITE,
        fg=MUTED,
        font=("Segoe UI", 9, "bold")
    ).pack(anchor="w")

    value = tk.Label(
        frame,
        text="0",
        bg=WHITE,
        fg=color,
        font=("Segoe UI", 20, "bold")
    )
    value.pack(anchor="w", pady=(4, 0))
    return value

lbl_productos = stat_card(cards, "PRODUCTOS", BLUE_DARK)
lbl_unidades = stat_card(cards, "UNIDADES", LIME_DARK)
lbl_total = stat_card(cards, "VALOR TOTAL", BLUE_DARK)

# Tabla
table_card = tk.Frame(
    right,
    bg=WHITE,
    highlightbackground=BORDER,
    highlightthickness=1
)
table_card.pack(fill="both", expand=True)

header = tk.Frame(table_card, bg=WHITE)
header.pack(fill="x", padx=20, pady=(18, 8))

tk.Label(
    header,
    text="Inventario actual",
    bg=WHITE,
    fg=TEXT,
    font=("Segoe UI", 17, "bold")
).pack(side="left")

tk.Label(
    header,
    text="Vista general",
    bg=BLUE_SOFT,
    fg=BLUE_DARK,
    font=("Segoe UI", 9, "bold"),
    padx=10,
    pady=4
).pack(side="right")

table_frame = tk.Frame(table_card, bg=WHITE)
table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

tabla = ttk.Treeview(
    table_frame,
    columns=("Producto", "Cantidad", "Precio", "Subtotal"),
    show="headings",
    selectmode="browse"
)

for col, width in [
    ("Producto", 260),
    ("Cantidad", 100),
    ("Precio", 120),
    ("Subtotal", 130)
]:
    tabla.heading(col, text=col)
    tabla.column(col, width=width, anchor="w")

scroll = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=tabla.yview
)

tabla.configure(yscrollcommand=scroll.set)

tabla.pack(side="left", fill="both", expand=True)
scroll.pack(side="right", fill="y")

root.bind("<Delete>", lambda e: eliminar())

inventario = cargar()
refrescar()
root.mainloop()
