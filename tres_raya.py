"""
=====================================================
   TRES EN RAYA (Tic-Tac-Toe) - Python + Tkinter
=====================================================
Características:
  - Modo 1 Jugador (vs CPU con IA Minimax imbatible
    en dificultad "Difícil", y aleatoria en "Fácil")
  - Modo 2 Jugadores locales
  - Marcador persistente durante la sesión
  - Resaltado de la línea ganadora
  - Interfaz moderna con efectos hover
Ejecutar:  python tres_en_raya.py
"""

import tkinter as tk
from tkinter import font as tkfont
import random

# ----------------- Paleta de colores -----------------
COL_FONDO      = "#1e1e2e"
COL_TABLERO    = "#2a2a3d"
COL_CELDA      = "#313145"
COL_CELDA_HOV  = "#3d3d55"
COL_X          = "#89b4fa"   # azul
COL_O          = "#f38ba8"   # rosa
COL_TEXTO      = "#cdd6f4"
COL_GANADOR    = "#a6e3a1"   # verde
COL_EMPATE     = "#f9e2af"   # amarillo
COL_BOTON      = "#45475a"
COL_BOTON_HOV  = "#585b70"

LINEAS_GANADORAS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),   # filas
    (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columnas
    (0, 4, 8), (2, 4, 6),              # diagonales
]


class TresEnRaya(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tres en Raya")
        self.configure(bg=COL_FONDO)
        self.resizable(False, False)

        # Fuentes
        self.f_titulo = tkfont.Font(family="Helvetica", size=22, weight="bold")
        self.f_celda  = tkfont.Font(family="Helvetica", size=36, weight="bold")
        self.f_estado = tkfont.Font(family="Helvetica", size=14)
        self.f_boton  = tkfont.Font(family="Helvetica", size=11, weight="bold")
        self.f_score  = tkfont.Font(family="Helvetica", size=12, weight="bold")

        # Estado del juego
        self.tablero = [""] * 9
        self.turno = "X"
        self.juego_activo = True
        self.modo_cpu = True          # True = vs CPU, False = 2 jugadores
        self.dificultad = "dificil"   # "facil" | "dificil"
        self.marcador = {"X": 0, "O": 0, "Empates": 0}

        self._construir_ui()
        self._nueva_partida()

    # ==================== INTERFAZ ====================
    def _construir_ui(self):
        tk.Label(self, text="TRES EN RAYA", font=self.f_titulo,
                 bg=COL_FONDO, fg=COL_TEXTO).pack(pady=(15, 5))

        # --- Selector de modo ---
        marco_modo = tk.Frame(self, bg=COL_FONDO)
        marco_modo.pack(pady=5)
        self.btn_1j = self._crear_boton(marco_modo, "1 Jugador (vs CPU)",
                                        lambda: self._cambiar_modo(True))
        self.btn_1j.pack(side="left", padx=5)
        self.btn_2j = self._crear_boton(marco_modo, "2 Jugadores",
                                        lambda: self._cambiar_modo(False))
        self.btn_2j.pack(side="left", padx=5)

        # --- Selector de dificultad ---
        self.marco_dif = tk.Frame(self, bg=COL_FONDO)
        self.marco_dif.pack(pady=3)
        tk.Label(self.marco_dif, text="Dificultad:", font=self.f_boton,
                 bg=COL_FONDO, fg=COL_TEXTO).pack(side="left", padx=(0, 5))
        self.btn_facil = self._crear_boton(self.marco_dif, "Fácil",
                                           lambda: self._cambiar_dificultad("facil"))
        self.btn_facil.pack(side="left", padx=3)
        self.btn_dificil = self._crear_boton(self.marco_dif, "Difícil",
                                             lambda: self._cambiar_dificultad("dificil"))
        self.btn_dificil.pack(side="left", padx=3)

        # --- Marcador ---
        self.lbl_marcador = tk.Label(self, font=self.f_score,
                                     bg=COL_FONDO, fg=COL_EMPATE)
        self.lbl_marcador.pack(pady=5)

        # --- Tablero ---
        marco_tablero = tk.Frame(self, bg=COL_TABLERO, padx=8, pady=8)
        marco_tablero.pack(padx=20, pady=5)
        self.celdas = []
        for i in range(9):
            btn = tk.Button(marco_tablero, text="", font=self.f_celda,
                            width=3, height=1, bd=0, relief="flat",
                            bg=COL_CELDA, fg=COL_TEXTO,
                            activebackground=COL_CELDA_HOV,
                            disabledforeground=COL_TEXTO,
                            cursor="hand2",
                            command=lambda i=i: self._click_celda(i))
            btn.grid(row=i // 3, column=i % 3, padx=4, pady=4)
            btn.bind("<Enter>", lambda e, b=btn: self._hover(b, True))
            btn.bind("<Leave>", lambda e, b=btn: self._hover(b, False))
            self.celdas.append(btn)

        # --- Etiqueta de estado ---
        self.lbl_estado = tk.Label(self, font=self.f_estado,
                                   bg=COL_FONDO, fg=COL_TEXTO)
        self.lbl_estado.pack(pady=8)

        # --- Botones de acción ---
        marco_acciones = tk.Frame(self, bg=COL_FONDO)
        marco_acciones.pack(pady=(0, 15))
        self._crear_boton(marco_acciones, "Nueva partida",
                          self._nueva_partida).pack(side="left", padx=5)
        self._crear_boton(marco_acciones, "Reiniciar marcador",
                          self._reiniciar_marcador).pack(side="left", padx=5)

        self._actualizar_botones_modo()

    def _crear_boton(self, padre, texto, comando):
        btn = tk.Button(padre, text=texto, font=self.f_boton, bd=0,
                        bg=COL_BOTON, fg=COL_TEXTO,
                        activebackground=COL_BOTON_HOV,
                        activeforeground=COL_TEXTO,
                        padx=10, pady=5, cursor="hand2", command=comando)
        btn.bind("<Enter>", lambda e: btn.config(bg=COL_BOTON_HOV))
        btn.bind("<Leave>", lambda e: self._restaurar_color_boton(btn))
        return btn

    def _restaurar_color_boton(self, btn):
        # Mantiene resaltados los botones de modo/dificultad activos
        activos = []
        if self.modo_cpu:
            activos.append(self.btn_1j)
            activos.append(self.btn_facil if self.dificultad == "facil"
                           else self.btn_dificil)
        else:
            activos.append(self.btn_2j)
        btn.config(bg=COL_BOTON_HOV if btn in activos else COL_BOTON)

    def _hover(self, btn, entrando):
        if btn["text"] == "" and self.juego_activo:
            btn.config(bg=COL_CELDA_HOV if entrando else COL_CELDA)

    # ==================== LÓGICA ====================
    def _cambiar_modo(self, vs_cpu):
        self.modo_cpu = vs_cpu
        self._actualizar_botones_modo()
        self._reiniciar_marcador()
        self._nueva_partida()

    def _cambiar_dificultad(self, dif):
        self.dificultad = dif
        self._actualizar_botones_modo()
        self._nueva_partida()

    def _actualizar_botones_modo(self):
        for b in (self.btn_1j, self.btn_2j, self.btn_facil, self.btn_dificil):
            self._restaurar_color_boton(b)
        if self.modo_cpu:
            self.marco_dif.pack(pady=3, after=self.btn_1j.master)
        else:
            self.marco_dif.pack_forget()

    def _nueva_partida(self):
        self.tablero = [""] * 9
        self.turno = "X"
        self.juego_activo = True
        for btn in self.celdas:
            btn.config(text="", bg=COL_CELDA, state="normal", fg=COL_TEXTO)
        self._actualizar_estado()
        self._actualizar_marcador()

    def _reiniciar_marcador(self):
        self.marcador = {"X": 0, "O": 0, "Empates": 0}
        self._actualizar_marcador()

    def _actualizar_marcador(self):
        nombre_o = "CPU (O)" if self.modo_cpu else "Jugador O"
        self.lbl_marcador.config(
            text=f"Jugador X: {self.marcador['X']}   |   "
                 f"{nombre_o}: {self.marcador['O']}   |   "
                 f"Empates: {self.marcador['Empates']}")

    def _actualizar_estado(self, texto=None, color=COL_TEXTO):
        if texto is None:
            if self.modo_cpu:
                texto = "Tu turno (X)" if self.turno == "X" else "Turno de la CPU..."
            else:
                texto = f"Turno del jugador {self.turno}"
            color = COL_X if self.turno == "X" else COL_O
        self.lbl_estado.config(text=texto, fg=color)

    def _click_celda(self, i):
        if not self.juego_activo or self.tablero[i] != "":
            return
        if self.modo_cpu and self.turno == "O":
            return  # esperando a la CPU
        self._marcar(i)
        if self.juego_activo and self.modo_cpu and self.turno == "O":
            self.after(400, self._jugada_cpu)  # pequeña pausa para naturalidad

    def _marcar(self, i):
        self.tablero[i] = self.turno
        color = COL_X if self.turno == "X" else COL_O
        self.celdas[i].config(text=self.turno, fg=color,
                              bg=COL_CELDA, state="disabled")
        ganador, linea = self._verificar_ganador()
        if ganador:
            self._fin_partida(ganador, linea)
        elif "" not in self.tablero:
            self._fin_partida(None, None)
        else:
            self.turno = "O" if self.turno == "X" else "X"
            self._actualizar_estado()

    def _verificar_ganador(self):
        for linea in LINEAS_GANADORAS:
            a, b, c = linea
            if self.tablero[a] != "" and \
               self.tablero[a] == self.tablero[b] == self.tablero[c]:
                return self.tablero[a], linea
        return None, None

    def _fin_partida(self, ganador, linea):
        self.juego_activo = False
        for btn in self.celdas:
            btn.config(state="disabled")
        if ganador:
            for i in linea:
                self.celdas[i].config(bg=COL_GANADOR, fg=COL_FONDO)
            self.marcador[ganador] += 1
            if self.modo_cpu:
                msg = "¡Ganaste! 🎉" if ganador == "X" else "La CPU gana 🤖"
            else:
                msg = f"¡Gana el jugador {ganador}! 🎉"
            self._actualizar_estado(msg, COL_GANADOR)
        else:
            self.marcador["Empates"] += 1
            for btn in self.celdas:
                btn.config(bg=COL_EMPATE, fg=COL_FONDO)
            self._actualizar_estado("¡Empate! 🤝", COL_EMPATE)
        self._actualizar_marcador()

    # ==================== IA (CPU) ====================
    def _jugada_cpu(self):
        if not self.juego_activo:
            return
        if self.dificultad == "facil":
            # 70% aleatorio, 30% óptimo → se puede ganar
            if random.random() < 0.7:
                i = random.choice([j for j in range(9) if self.tablero[j] == ""])
            else:
                i = self._mejor_jugada()
        else:
            i = self._mejor_jugada()
        self._marcar(i)

    def _mejor_jugada(self):
        mejor_valor = -float("inf")
        mejor_indice = None
        for i in range(9):
            if self.tablero[i] == "":
                self.tablero[i] = "O"
                valor = self._minimax(False, 0, -float("inf"), float("inf"))
                self.tablero[i] = ""
                if valor > mejor_valor:
                    mejor_valor = valor
                    mejor_indice = i
        return mejor_indice

    def _minimax(self, maximizando, profundidad, alfa, beta):
        ganador, _ = self._verificar_ganador()
        if ganador == "O":
            return 10 - profundidad      # gana la CPU: mejor cuanto antes
        if ganador == "X":
            return profundidad - 10      # gana el humano: peor escenario
        if "" not in self.tablero:
            return 0                     # empate

        if maximizando:  # turno de la CPU (O)
            mejor = -float("inf")
            for i in range(9):
                if self.tablero[i] == "":
                    self.tablero[i] = "O"
                    mejor = max(mejor, self._minimax(False, profundidad + 1, alfa, beta))
                    self.tablero[i] = ""
                    alfa = max(alfa, mejor)
                    if beta <= alfa:
                        break  # poda alfa-beta
            return mejor
        else:            # turno del humano (X)
            peor = float("inf")
            for i in range(9):
                if self.tablero[i] == "":
                    self.tablero[i] = "X"
                    peor = min(peor, self._minimax(True, profundidad + 1, alfa, beta))
                    self.tablero[i] = ""
                    beta = min(beta, peor)
                    if beta <= alfa:
                        break  # poda alfa-beta
            return peor


if __name__ == "__main__":
    app = TresEnRaya()
    app.mainloop()