import tkinter as tk
import random

# Caras del dado en Unicode
CARAS = {1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"}

def lanzar_dado():
    """Anima el lanzamiento y muestra el resultado final."""
    boton.config(state="disabled")
    animar(10)

def animar(veces):
    """Muestra caras aleatorias rápidamente para simular el giro."""
    if veces > 0:
        numero = random.randint(1, 6)
        etiqueta_dado.config(text=CARAS[numero])
        etiqueta_resultado.config(text="Lanzando...")
        ventana.after(80, animar, veces - 1)
    else:
        resultado = random.randint(1, 6)
        etiqueta_dado.config(text=CARAS[resultado])
        etiqueta_resultado.config(text=f"¡Salió el {resultado}!")
        boton.config(state="normal")

# Ventana principal
ventana = tk.Tk()
ventana.title("Lanzar Dado")
ventana.geometry("300x320")
ventana.resizable(False, False)
ventana.config(bg="#2c3e50")

# Cara del dado
etiqueta_dado = tk.Label(
    ventana, text="⚀", font=("Arial", 120),
    bg="#2c3e50", fg="white"
)
etiqueta_dado.pack(pady=10)

# Texto del resultado
etiqueta_resultado = tk.Label(
    ventana, text="Presiona el botón",
    font=("Arial", 14), bg="#2c3e50", fg="#ecf0f1"
)
etiqueta_resultado.pack()

# Botón de lanzar
boton = tk.Button(
    ventana, text="🎲 Lanzar", font=("Arial", 14, "bold"),
    command=lanzar_dado, bg="#e74c3c", fg="white",
    activebackground="#c0392b", padx=20, pady=8
)
boton.pack(pady=20)

ventana.mainloop()