import json
from tkinter import *
from tkinter import messagebox

mod_x = None
mod_y = None

with open("aves.json", "r", encoding="utf-8") as archivo:
    aves = json.load(archivo)
        
def buscar(event=None):
    repeticiones = 0
    linea = f"-------------------------------------------"
    output.delete("1.0", END)
    nombre = searcher.get()
    resultado = [p for p in aves if p["nombre"].lower() == nombre.lower()]
    if resultado:
        texto = f"Se han encontrado {len(resultado)} resultado(s):"
        output.insert(END, "\n" + texto)
        for p in resultado:
            name = f"Ave vista: " + p["nombre"]
            date = f"Fecha: " + p["fecha"]
            note = f"Notas: " + p["notas"]
            output.insert(END, "\n" + str(name))
            output.insert(END, "\n" + str(date))
            output.insert(END, "\n" + str(note))
            repeticiones = repeticiones + 1
            if len(resultado) > repeticiones:
                output.insert(END, "\n" + linea)
    else:
        resultado = [p for p in aves if p["fecha"].lower() == nombre.lower()]
        if resultado:
            texto = f"Se han encontrado {len(resultado)} resultado(s):"
            output.insert(END, "\n" + texto)
            for p in resultado:
                name = f"Ave vista: " + p["nombre"]
                date = f"Fecha: " + p["fecha"]
                note = f"Notas: " + p["notas"]
                output.insert(END, "\n" + str(name))
                output.insert(END, "\n" + str(date))
                output.insert(END, "\n" + str(note))
                repeticiones = repeticiones + 1
                if len(resultado) > repeticiones:
                    output.insert(END, "\n" + linea)
        else:
            error = "Ninguna vista registrada coincide con la busqueda."
            output.insert(END, "\n" + str(error))
    searcher.delete(0, END)
    output.see(END)

def emerger_UP(event=None):
    global intro, bird, day, opinion

    intro = Toplevel()
    intro.title("Nuevo avistamiento")
    intro.configure(bg="#4D7C8A")

    bird_lb = Label(intro, text="Ave:")
    bird_lb.grid(row=0, column=0)

    bird = Entry(intro, width=20)
    bird.grid(row=1, column=0)
    
    day_lb = Label(intro, text="Fecha:")
    day_lb.grid(row=0, column=1)

    day = Entry(intro, width=20)
    day.grid(row=1, column=1)

    opinion_lb = Label(intro, text="Notas:")
    opinion_lb.grid(row=0, column=2)

    opinion = Entry(intro, width=20)
    opinion.grid(row=1, column=2)

    reg = Button(intro, text="Registrar", width=20, command=registrar)
    reg.grid(row=2, column=0, columnspan= 3)

    bird.focus()

def registrar():
    Nombre = bird.get()
    Fecha = day.get()
    Nota = opinion.get()

    if not Nombre or not Fecha:
        messagebox.showerror(title=None, message="Información faltante")
    else:
        nuevo = {
            "nombre": Nombre,
            "fecha": Fecha,
            "notas": Nota
        }
        aves.append(nuevo)

        with open("aves.json", "w", encoding="utf-8") as archivo:
            json.dump(aves, archivo, ensure_ascii=False, indent=4)
        
        intro.destroy()

def emerger_MO(event=None):
    global mod, mod_x, mod_y

    mod = Toplevel()
    mod.title("Modificar")
    mod.configure(bg="#4D7C8A")
    mod.resizable(0, 0)
    
    if mod_x != None and mod_y != None:
        mod.geometry(f"+{mod_x}+{mod_y}")

    filas = 0

    for index, vista in enumerate(aves):
        entrada = Label(mod, width="20")
        V_name = vista["nombre"]
        V_date = vista["fecha"]
        entrada.config(text=str(V_name)+" - "+str(V_date))
        entrada.grid(row=filas, column=0)
        borrar = Button(mod, width=5, text="Borrar", command=lambda i=index: eliminar(i, entrada, borrar))
        borrar.grid(row=filas, column=1)
        filas = filas + 1
    if len(aves) == 0:
        entrada = Label(mod, width="20")
        entrada.config(text="Sin avistamientos")
        entrada.grid(row=1, column=0)

def eliminar(index, entrada, borrar):
    global mod_x, mod_y
    aves.pop(index)
    entrada.destroy()
    borrar.destroy()

    mod_x = mod.winfo_x()
    mod_y = mod.winfo_y()
    mod.destroy()
    emerger_MO()

    with open("aves.json", "w", encoding="utf-8") as archivo:
        json.dump(aves, archivo, ensure_ascii=False, indent=4)

def centrar(ventana, ancho, alto):
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

#Interfaz
root = Tk()
root.title("Aviario")
centrar(root, 400, 445)
root.resizable(0, 0)
root.configure(bg="#4D7C8A")

output = Text(root, width=50, wrap="word")
output.grid(row=1, column=0, columnspan=4, pady=10)

searcher = Entry(root, width=30)
searcher.grid(row=2, column=0)
searcher.bind("<Return>", buscar)
searcher.bind("<Control-m>", emerger_MO)
searcher.bind("<Control-r>", emerger_UP)

search = Button(text="Buscar", command=buscar)
search.grid(row=2, column=1)

upload = Button(text="Registrar", command=emerger_UP)
upload.grid(row=2, column=2)

modify = Button(text="Modificar", command=emerger_MO)
modify.grid(row=2, column=3)

if __name__ == "__main__":
    searcher.focus()
    root.mainloop()