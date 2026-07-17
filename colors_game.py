"""
Juego de Colores con Tkinter
----------------------------
En pantalla aparece el NOMBRE de un color, pero escrito con un color
de letra diferente. Tienes que escribir el COLOR DE LA LETRA (no la
palabra) antes de que se acabe el tiempo. ¡Cada acierto suma un punto!
"""

import tkinter as tk
import random

# Colores disponibles (nombre en español -> color de tkinter)
COLORES = {
    "rojo": "red",
    "azul": "blue",
    "verde": "green",
    "amarillo": "yellow",
    "naranja": "orange",
    "morado": "purple",
    "rosa": "pink",
    "negro": "black",
    "marron": "brown",
    "gris": "gray",
}

TIEMPO_JUEGO = 30  # segundos por partida


class JuegoColores:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Juego de Colores")
        self.ventana.geometry("480x320")
        self.ventana.resizable(False, False)

        self.puntaje = 0
        self.tiempo_restante = TIEMPO_JUEGO
        self.jugando = False
        self.color_correcto = ""

        # --- Widgets ---
        self.etiqueta_instrucciones = tk.Label(
            ventana,
            text="Escribe el COLOR de la letra, ¡no la palabra!",
            font=("Helvetica", 12),
        )
        self.etiqueta_instrucciones.pack(pady=10)

        self.etiqueta_tiempo = tk.Label(
            ventana, text=f"Tiempo: {TIEMPO_JUEGO}", font=("Helvetica", 12)
        )
        self.etiqueta_tiempo.pack()

        self.etiqueta_puntaje = tk.Label(
            ventana, text="Puntaje: 0", font=("Helvetica", 12)
        )
        self.etiqueta_puntaje.pack()

        self.etiqueta_palabra = tk.Label(
            ventana, text="Presiona ENTER para empezar", font=("Helvetica", 40, "bold")
        )
        self.etiqueta_palabra.pack(pady=20)

        self.entrada = tk.Entry(ventana, font=("Helvetica", 14), justify="center")
        self.entrada.pack(pady=5)
        self.entrada.focus_set()

        # Enter inicia el juego o comprueba la respuesta
        self.ventana.bind("<Return>", self.manejar_enter)

    def manejar_enter(self, evento):
        if not self.jugando:
            self.iniciar_juego()
        else:
            self.comprobar_respuesta()

    def iniciar_juego(self):
        self.jugando = True
        self.puntaje = 0
        self.tiempo_restante = TIEMPO_JUEGO
        self.etiqueta_puntaje.config(text="Puntaje: 0")
        self.entrada.delete(0, tk.END)
        self.siguiente_palabra()
        self.cuenta_regresiva()

    def cuenta_regresiva(self):
        if self.tiempo_restante > 0:
            self.tiempo_restante -= 1
            self.etiqueta_tiempo.config(text=f"Tiempo: {self.tiempo_restante}")
            self.ventana.after(1000, self.cuenta_regresiva)
        else:
            self.terminar_juego()

    def siguiente_palabra(self):
        palabra = random.choice(list(COLORES.keys()))
        # Elegir un color de letra distinto a la palabra para hacerlo difícil
        nombre_color = random.choice([c for c in COLORES if c != palabra])
        self.color_correcto = nombre_color
        self.etiqueta_palabra.config(text=palabra.upper(), fg=COLORES[nombre_color])

    def comprobar_respuesta(self):
        respuesta = self.entrada.get().strip().lower()
        if respuesta == self.color_correcto:
            self.puntaje += 1
            self.etiqueta_puntaje.config(text=f"Puntaje: {self.puntaje}")
        self.entrada.delete(0, tk.END)
        self.siguiente_palabra()

    def terminar_juego(self):
        self.jugando = False
        self.etiqueta_palabra.config(
            text=f"¡Fin! Puntaje: {self.puntaje}", fg="black"
        )
        self.etiqueta_tiempo.config(text="Presiona ENTER para jugar otra vez")
        self.entrada.delete(0, tk.END)


if __name__ == "__main__":
    ventana = tk.Tk()
    juego = JuegoColores(ventana)
    ventana.mainloop()