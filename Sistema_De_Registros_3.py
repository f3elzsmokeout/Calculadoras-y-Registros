import tkinter as tk
from tkinter import ttk, messagebox
import json
from pathlib import Path

APP_DIR = Path.home() / ".sistema_registro_estudiantes"
APP_DIR.mkdir(exist_ok=True)
DATA_FILE = APP_DIR / "datos.json"

def cargar():
    try:
        if DATA_FILE.exists():
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except:
        pass
    return []

def guardar_archivo():
    DATA_FILE.write_text(
        json.dumps(datos, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

def mostrar(nombre):
    for frame in (inicio, registro, listado):
        frame.pack_forget()

    vistas = {
        "inicio": inicio,
        "registro": registro,
        "listado": listado
    }

    vistas[nombre].pack(fill="both", expand=True)
    refrescar()

def guardar():
    nombre = e_nombre.get().strip()
    curso = e_curso.get().strip()
    telefono = e_telefono.get().strip()
    nota = e_nota.get().strip()

    if not nombre:
        messagebox.showwarning(
            "Falta información",
            "Ingresa el nombre del estudiante."
        )
        return

    datos.append({
        "nombre": nombre,
        "curso": curso,
        "telefono": telefono,
        "nota": nota
    })

    guardar_archivo()

    for entry in (e_nombre, e_curso, e_telefono, e_nota):
        entry.delete(0, tk.END)

    mostrar("listado")

def eliminar_seleccionado():
    seleccion = tabla.selection()

    if not seleccion:
        messagebox.showinfo(
            "Sin selección",
            "Selecciona un estudiante de la lista."
        )
        return

    if not messagebox.askyesno(
        "Eliminar registro",
        "¿Deseas eliminar el registro seleccionado?"
    ):
        return

    indice = tabla.index(seleccion[0])
    datos.pop(indice)
    guardar_archivo()
    refrescar()

def vaciar_lista():
    if not datos:
        messagebox.showinfo(
            "Lista vacía",
            "No hay registros para eliminar."
        )
        return

    if not messagebox.askyesno(
        "Vaciar lista",
        "¿Seguro que deseas eliminar todos los registros?"
    ):
        return

    datos.clear()
    guardar_archivo()
    refrescar()

def refrescar():
    lbl_total.config(text=str(len(datos)))

    for item in tabla.get_children():
        tabla.delete(item)

    for d in datos:
        tabla.insert(
            "",
            "end",
            values=(
                d.get("nombre", ""),
                d.get("curso", ""),
                d.get("telefono", ""),
                d.get("nota", "")
            )
        )

root = tk.Tk()
root.title("Sistema de Registro de Estudiantes")
root.geometry("1040x610")
root.minsize(880, 530)

BG = "#08090d"
PANEL = "#12141b"
PANEL_2 = "#181b24"
PURPLE = "#8b5cf6"
PURPLE_DARK = "#6d3fdb"
PURPLE_SOFT = "#241a3a"
CYAN = "#59d8ff"
CYAN_SOFT = "#15303a"
TEXT = "#f5f7fb"
MUTED = "#8e97a8"
BORDER = "#59d8ff"

root.configure(bg=BG)

style = ttk.Style(root)
style.theme_use("clam")

style.configure(
    "Treeview",
    background=PANEL_2,
    fieldbackground=PANEL_2,
    foreground=TEXT,
    rowheight=31,
    borderwidth=0,
    font=("Segoe UI", 10)
)

style.configure(
    "Treeview.Heading",
    background=PURPLE_DARK,
    foreground="white",
    font=("Segoe UI", 10, "bold"),
    relief="flat"
)

style.map(
    "Treeview",
    background=[("selected", PURPLE_DARK)],
    foreground=[("selected", "white")]
)

style.map(
    "Treeview.Heading",
    background=[("active", PURPLE)]
)

style.configure(
    "Purple.TButton",
    background=PURPLE,
    foreground="white",
    padding=9,
    font=("Segoe UI", 10, "bold")
)

style.map(
    "Purple.TButton",
    background=[("active", PURPLE_DARK)]
)

style.configure(
    "Cyan.TButton",
    background=CYAN_SOFT,
    foreground=CYAN,
    padding=9,
    font=("Segoe UI", 10, "bold")
)

style.map(
    "Cyan.TButton",
    background=[("active", "#1c4452")]
)

# Barra lateral
side = tk.Frame(
    root,
    bg=PANEL,
    width=250,
    highlightbackground=CYAN,
    highlightthickness=1
)
side.pack(side="left", fill="y")
side.pack_propagate(False)

tk.Label(
    side,
    text="Sistema de Registro\nde Estudiantes",
    bg=PANEL,
    fg=TEXT,
    font=("Segoe UI", 17, "bold"),
    justify="left"
).pack(anchor="w", padx=20, pady=(25, 6))

tk.Label(
    side,
    text="Menú principal",
    bg=PANEL,
    fg=CYAN,
    font=("Segoe UI", 9, "bold")
).pack(anchor="w", padx=21, pady=(0, 18))

def boton_menu(texto, comando):
    return tk.Button(
        side,
        text=texto,
        command=comando,
        bg=PANEL_2,
        fg=TEXT,
        activebackground=PURPLE_SOFT,
        activeforeground=CYAN,
        bd=0,
        highlightbackground=CYAN,
        highlightthickness=1,
        anchor="w",
        padx=16,
        pady=11,
        font=("Segoe UI", 10, "bold"),
        cursor="hand2"
    )

boton_menu("Inicio            Alt+1", lambda: mostrar("inicio")).pack(fill="x", padx=16, pady=5)
boton_menu("Nuevo registro   Alt+2", lambda: mostrar("registro")).pack(fill="x", padx=16, pady=5)
boton_menu("Listado          Alt+3", lambda: mostrar("listado")).pack(fill="x", padx=16, pady=5)

tk.Label(
    side,
    text="Enrique Rojas",
    bg=PANEL,
    fg=MUTED,
    font=("Segoe UI", 8)
).pack(side="bottom", pady=16)

# Contenido
content = tk.Frame(root, bg=BG)
content.pack(side="left", fill="both", expand=True)

def crear_panel():
    exterior = tk.Frame(content, bg=BG)
    tarjeta = tk.Frame(
        exterior,
        bg=PANEL,
        highlightbackground=CYAN,
        highlightthickness=1
    )
    tarjeta.pack(fill="both", expand=True, padx=26, pady=26)
    return exterior, tarjeta

inicio, inicio_card = crear_panel()
registro, registro_card = crear_panel()
listado, listado_card = crear_panel()

# Inicio
tk.Label(
    inicio_card,
    text="Panel principal",
    bg=PANEL,
    fg=TEXT,
    font=("Segoe UI", 23, "bold")
).pack(anchor="w", padx=28, pady=(28, 6))

tk.Label(
    inicio_card,
    text="Administra los registros de estudiantes desde un solo lugar.",
    bg=PANEL,
    fg=MUTED,
    font=("Segoe UI", 10)
).pack(anchor="w", padx=28)

resumen = tk.Frame(
    inicio_card,
    bg=PURPLE_SOFT,
    highlightbackground=CYAN,
    highlightthickness=1
)
resumen.pack(anchor="w", padx=28, pady=28, ipadx=18, ipady=14)

tk.Label(
    resumen,
    text="TOTAL DE REGISTROS",
    bg=PURPLE_SOFT,
    fg=CYAN,
    font=("Segoe UI", 9, "bold")
).pack(anchor="w")

lbl_total = tk.Label(
    resumen,
    text="0",
    bg=PURPLE_SOFT,
    fg=PURPLE,
    font=("Segoe UI", 26, "bold")
)
lbl_total.pack(anchor="w", pady=(4, 0))

# Registro
tk.Label(
    registro_card,
    text="Registrar estudiante",
    bg=PANEL,
    fg=TEXT,
    font=("Segoe UI", 23, "bold")
).pack(anchor="w", padx=28, pady=(28, 16))

form = tk.Frame(registro_card, bg=PANEL)
form.pack(anchor="w", padx=28)

def campo(label):
    tk.Label(
        form,
        text=label,
        bg=PANEL,
        fg=CYAN,
        font=("Segoe UI", 10, "bold")
    ).pack(anchor="w", pady=(9, 3))

    entry = ttk.Entry(form, width=54, font=("Segoe UI", 10))
    entry.pack(anchor="w")
    return entry

e_nombre = campo("Nombre completo")
e_curso = campo("Curso")
e_telefono = campo("Teléfono")
e_nota = campo("Nota")

ttk.Button(
    form,
    text="Guardar estudiante",
    style="Purple.TButton",
    command=guardar
).pack(anchor="w", pady=22)

# Listado
top_list = tk.Frame(listado_card, bg=PANEL)
top_list.pack(fill="x", padx=28, pady=(28, 10))

tk.Label(
    top_list,
    text="Listado de estudiantes",
    bg=PANEL,
    fg=TEXT,
    font=("Segoe UI", 23, "bold")
).pack(side="left")

acciones = tk.Frame(top_list, bg=PANEL)
acciones.pack(side="right")

ttk.Button(
    acciones,
    text="Eliminar seleccionado",
    style="Cyan.TButton",
    command=eliminar_seleccionado
).pack(side="left", padx=5)

ttk.Button(
    acciones,
    text="Vaciar lista",
    style="Purple.TButton",
    command=vaciar_lista
).pack(side="left", padx=5)

table_frame = tk.Frame(
    listado_card,
    bg=PANEL_2,
    highlightbackground=CYAN,
    highlightthickness=1
)
table_frame.pack(fill="both", expand=True, padx=28, pady=(6, 28))

tabla = ttk.Treeview(
    table_frame,
    columns=("Nombre", "Curso", "Teléfono", "Nota"),
    show="headings",
    selectmode="browse"
)

for col, width in [
    ("Nombre", 270),
    ("Curso", 180),
    ("Teléfono", 180),
    ("Nota", 100)
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

root.bind("<Alt-Key-1>", lambda e: mostrar("inicio"))
root.bind("<Alt-Key-2>", lambda e: mostrar("registro"))
root.bind("<Alt-Key-3>", lambda e: mostrar("listado"))
root.bind("<Delete>", lambda e: eliminar_seleccionado())

datos = cargar()
mostrar("inicio")
root.mainloop()
