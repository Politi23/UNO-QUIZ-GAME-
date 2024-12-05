import tkinter as tk
from tkinter import messagebox
import random  # Importa la libreria random para mezclar las cartas

# Constantes para los colores de las cartas
ROJO = "Rojo"
AZUL = "Azul"
VERDE = "Verde"
AMARILLO = "Amarillo"

# Tipo de cartas especiales que pueden aparecer en el juego
TIPO_CARTAS_ESPECIALES = {
    "+2": "+2",  # Carta de +2 cartas
    "salta": "salta",  # Carta que salta el turno del siguiente jugador
    "reversa": "reversa",  # Carta que invierte el orden de los turnos
    "cambio_color": "cambio_color",  # Carta que cambia el color del juego
    "+4": "+4"  # Carta que hace que el siguiente jugador robe 4 cartas
}

class Carta:
    def __init__(self, color, tipo, numero=None):
        """
        Constructor de la clase Carta.
        :param color: El color de la carta (Rojo, Azul, Verde, Amarillo, o Negro)
        :param tipo: El tipo de la carta (normal o especial)
        :param numero: El numero de la carta si es una carta normal (de 0 a 9)
        """
        self.color = color
        self.tipo = tipo  # El tipo puede ser "normal" o uno de los tipos especiales
        self.numero = numero

    def __str__(self):
        """
        Representacion en forma de texto de la carta.
        Si la carta es normal, devuelve el color y el numero.
        Si es una carta especial, devuelve el color y el tipo de carta especial.
        """
        if self.tipo == "normal":
            return f"{self.color} {self.numero}"
        else:
            return f"{self.color} {self.tipo}"

class JuegoUNO:
    def __init__(self, root, menu_ventana):
        """
        Constructor del juego UNO.
        :param root: La ventana principal de la interfaz grafica.
        :param menu_ventana: La ventana del menu principal para cerrarla al iniciar el juego.
        """
        self.root = root
        self.menu_ventana = menu_ventana  # Guardar la referencia a la ventana del menu
        self.root.title("Juego de UNO")  # Titulo de la ventana
        self.root.geometry("800x600")  # Tamano de la ventana
        self.root.config(bg="#006400")  # Fondo verde de la ventana

        # Preguntas y respuestas sobre Permutaciones y Combinaciones
        self.preguntas = [
            {"pregunta": "¿Para 5 objetos distintos, existen 5! formas de ordenarlos?", "respuesta": "si"},
            {"pregunta": "¿Una combinacion de 5 elementos tomados 3 a la vez es mayor que una permutacion de los mismos elementos?", "respuesta": "no"},
            {"pregunta": "¿Para un conjunto de 4 elementos, hay mas permutaciones que combinaciones?", "respuesta": "si"},
            {"pregunta": "¿P(5,2) representa el numero de formas de seleccionar 2 elementos de 5, sin importar el orden?", "respuesta": "no"},
            {"pregunta": "¿Para calcular combinaciones, el orden no importa?", "respuesta": "si"},
            {"pregunta": "¿Las permutaciones consideran el orden de los elementos?", "respuesta": "si"},
            {"pregunta": "¿El numero de formas de organizar 3 elementos de un conjunto de 5 es igual a C(5,3)?", "respuesta": "no"},
            {"pregunta": "¿C(n,r) representa combinaciones de n elementos tomados r a la vez?", "respuesta": "si"},
            {"pregunta": "¿Para 3 elementos en un conjunto, hay exactamente 3! formas de ordenarlos?", "respuesta": "si"},
            {"pregunta": "¿Una combinacion es siempre mayor que una permutacion para el mismo conjunto de elementos?", "respuesta": "no"},
            {"pregunta": "¿Es posible organizar las letras de la palabra 'PERMUTACIONES' de mas de 5,000 maneras?", "respuesta": "si"},
            {"pregunta": "¿Si hay 15 participantes y se premian los primeros 3 lugares, las asignaciones son una permutacion?", "respuesta": "si"},
            {"pregunta": "¿Si se tienen 8 bolas de diferentes colores, se pueden seleccionar 4 bolas de exactamente 70 formas diferentes?", "respuesta": "no"},
            {"pregunta": "¿Es posible elegir 2 preguntas de un conjunto de 12 preguntas de mas de una manera?", "respuesta": "si"},
            {"pregunta": "¿Es posible formar un equipo de 3 personas a partir de un grupo de 9 sin importar el orden?", "respuesta": "si"},
            {"pregunta": "¿Si se tienen 7 personas, es posible organizar una fila con 3 personas en el centro de solo una manera?", "respuesta": "no"},
            {"pregunta": "¿En un comite de 5 personas formado de un grupo de 12, el orden en que se seleccionan no importa?", "respuesta": "si"},
            {"pregunta": "¿Es posible ordenar 4 libros de manera unica si 2 de ellos son identicos?", "respuesta": "no"},
            {"pregunta": "¿Si hay 3 bolsillos y 6 objetos, es posible distribuir los objetos de mas de una manera?", "respuesta": "si"},
            {"pregunta": "¿Si seleccionamos 3 cartas de una baraja de 52 cartas y deben ser de diferentes palos, las combinaciones posibles son limitadas?", "respuesta": "si"}
        ]

        # Colores disponibles para las cartas
        self.colores = [ROJO, AZUL, VERDE, AMARILLO]
        
        # Crear la baraja de cartas
        self.crear_baraja()

        # Datos iniciales de los jugadores (mano y puntos)
        self.jugador1 = {"mano": [], "puntos": 0}
        self.jugador2 = {"mano": [], "puntos": 0}
        
        # Repartir 7 cartas a cada jugador al inicio
        self.repartir_cartas()

        # Configurar la carta actual en la pila de juego
        self.carta_actual = self.baraja.pop()

        # Definir el turno (0 para jugador 1, 1 para jugador 2)
        self.turno = 0

        # Configurar la interfaz grafica (UI)
        self.configurar_ui()

    def crear_baraja(self):
        """
        Crea la baraja de cartas. Incluye cartas normales y especiales.
        """
        self.baraja = []
        
        # Agregar cartas normales (0-9) y especiales
        for color in self.colores:
            for numero in range(0, 10):
                self.baraja.append(Carta(color, "normal", numero))  # Cartas normales
            for tipo_especial in TIPO_CARTAS_ESPECIALES.values():
                self.baraja.append(Carta(color, tipo_especial))  # Cartas especiales

        # Agregar cartas especiales de cambio de color y +4
        for _ in range(4):
            self.baraja.append(Carta("Negro", "cambio_color"))
            self.baraja.append(Carta("Negro", "+4"))

        # Mezclar la baraja de manera aleatoria
        random.shuffle(self.baraja)

    def repartir_cartas(self):
        """
        Reparte 7 cartas a cada jugador al inicio del juego.
        """
        for _ in range(7):
            self.jugador1["mano"].append(self.baraja.pop())
            self.jugador2["mano"].append(self.baraja.pop())

    def configurar_ui(self):
        """
        Configura la interfaz grafica del juego (UI).
        Incluye la informacion del turno, carta actual, y botones para jugar.
        """
        # Frame para mostrar informacion del turno y carta actual
        self.info_frame = tk.Frame(self.root, bg="#008000")
        self.info_frame.pack(pady=20)

        # Etiqueta para mostrar el turno actual
        self.turno_label = tk.Label(self.info_frame, text="Turno de Jugador 1", font=("Arial", 20, "bold"), bg="#008000", fg="white")
        self.turno_label.pack()

        # Etiqueta para mostrar la carta actual en la pila
        self.carta_actual_label = tk.Label(self.info_frame, text=f"Carta en la pila: {self.carta_actual}", font=("Arial", 20), bg="#008000", fg="white")
        self.carta_actual_label.pack()

        # Boton para robar una carta
        self.robar_carta_button = tk.Button(self.info_frame, text="Robar Carta", font=("Arial", 14), bg="yellow", fg="black", command=self.robar_carta)
        self.robar_carta_button.pack(pady=10)

        # Etiqueta para mostrar el puntaje de ambos jugadores
        self.puntaje_label = tk.Label(self.info_frame, text=self.obtener_puntajes(), font=("Arial", 16), bg="#008000", fg="white")
        self.puntaje_label.pack()

        # Boton de Cerrar Juego
        self.cerrar_juego_button = tk.Button(self.root, text="Cerrar Juego", font=("Arial", 16), bg="#ff0000", fg="white", command=self.cerrar_juego)
        self.cerrar_juego_button.pack(pady=20)

        # Frame para mostrar las cartas de los jugadores
        self.jugador1_frame = tk.Frame(self.root, bg="#ADD8E6")
        self.jugador1_frame.pack(pady=20)
        self.jugador2_frame = tk.Frame(self.root, bg="#FFB6C1")
        self.jugador2_frame.pack(pady=20)

        # Mostrar las cartas de ambos jugadores
        self.mostrar_cartas()

    def mostrar_cartas(self):
        """
        Muestra las cartas de los jugadores en la interfaz grafica.
        Cada carta se representa como un boton que, al ser presionado, se juega.
        """
        # Limpiar las cartas anteriores antes de mostrar nuevas
        for widget in self.jugador1_frame.winfo_children():
            widget.destroy()
        for widget in self.jugador2_frame.winfo_children():
            widget.destroy()

        # Mostrar las cartas del Jugador 1
        tk.Label(self.jugador1_frame, text="Jugador 1", font=("Arial", 12), bg="#ADD8E6").pack()
        for carta in self.jugador1["mano"]:
            boton_carta = tk.Button(self.jugador1_frame, text=str(carta), command=lambda c=carta: self.jugar_carta(c, 0))
            boton_carta.pack(side="left")

        # Mostrar las cartas del Jugador 2
        tk.Label(self.jugador2_frame, text="Jugador 2", font=("Arial", 12), bg="#FFB6C1").pack()
        for carta in self.jugador2["mano"]:
            boton_carta = tk.Button(self.jugador2_frame, text=str(carta), command=lambda c=carta: self.jugar_carta(c, 1))
            boton_carta.pack(side="left")

    def jugar_carta(self, carta, jugador):
        """
        Funcion para jugar una carta. Verifica que sea el turno correcto
        y que la carta sea valida (coincida en color o numero).
        """
        # Verificar que sea el turno del jugador correspondiente
        if (self.turno == 0 and jugador == 0) or (self.turno == 1 and jugador == 1):
            # Verificar si la carta es valida (coincide en color, numero o es una carta especial)
            if carta.color == self.carta_actual.color or (carta.tipo == "normal" and carta.numero == self.carta_actual.numero) or carta.color == "Negro":
                # El jugador juega la carta y se elimina de su mano
                if jugador == 0:
                    self.jugador1["mano"].remove(carta)
                else:
                    self.jugador2["mano"].remove(carta)

                # Actualizar la carta actual en la pila
                self.carta_actual = carta
                self.carta_actual_label.config(text=f"Carta en la pila: {self.carta_actual}")

                # Aplicar efectos especiales si es necesario
                if carta.tipo == "+2":
                    self.aplicar_efecto_especial(2, 1 - self.turno)
                elif carta.tipo == "+4":
                    self.aplicar_efecto_especial(4, 1 - self.turno)
                elif carta.tipo == "salta":
                    self.turno = 1 - self.turno  # Salta el turno del siguiente jugador
                elif carta.tipo == "reversa":
                    return  # El turno no cambia, el jugador juega nuevamente
                elif carta.tipo == "cambio_color":
                    nuevo_color = random.choice(self.colores)
                    self.carta_actual.color = nuevo_color
                    messagebox.showinfo("Cambio de color", f"El jugador {self.turno + 1} ha cambiado el color a {nuevo_color}.")

                # Comprobar si algun jugador ha ganado
                if not self.jugador1["mano"]:
                    self.fin_del_juego("Jugador 1")
                    return
                elif not self.jugador2["mano"]:
                    self.fin_del_juego("Jugador 2")
                    return

                # Cambiar el turno al siguiente jugador
                self.turno = 1 - self.turno
                self.turno_label.config(text=f"Turno de Jugador {self.turno + 1}")
                self.mostrar_cartas()
            else:
                # Mostrar mensaje si la carta no es valida
                messagebox.showinfo("Movimiento invalido", "Debes jugar una carta que coincida en color o numero.")
        else:
            # Mostrar mensaje si el jugador intenta jugar en el turno incorrecto
            messagebox.showinfo("Error de turno", f"Es el turno del Jugador {self.turno + 1}")

    def aplicar_efecto_especial(self, cantidad, jugador):
        """
        Aplica el efecto de cartas especiales como +2 y +4, preguntando al jugador
        sobre permutaciones y combinaciones, y actualizando su puntaje segun su respuesta.
        """
        pregunta = random.choice(self.preguntas)
        respuesta_usuario = messagebox.askquestion("Pregunta", pregunta["pregunta"])

        # Asegurarse de que las respuestas sean correctas
        if respuesta_usuario == "yes":
            respuesta_usuario = "si"
        elif respuesta_usuario == "no":
            respuesta_usuario = "no"

        if respuesta_usuario.strip().lower() == pregunta["respuesta"].lower():
            # Si la respuesta es correcta, el jugador gana puntos
            if jugador == 0:
                self.jugador1["puntos"] += 10
            else:
                self.jugador2["puntos"] += 10
            messagebox.showinfo("¡Respuesta correcta!", f"¡El jugador {jugador + 1} evito recibir las cartas y gano 10 puntos!")
        else:
            # Si la respuesta es incorrecta, el jugador pierde puntos y recibe cartas
            if jugador == 0:
                self.jugador1["puntos"] -= 10
            else:
                self.jugador2["puntos"] -= 10
            messagebox.showinfo("Respuesta incorrecta", f"El jugador {jugador + 1} recibira {cantidad} cartas y perdio 10 puntos.")

        # Actualizar puntajes
        self.actualizar_puntajes()

    def robar_carta(self):
        """
        Permite a un jugador robar una carta si la baraja no esta vacia.
        """
        if not self.baraja:
            self.fin_del_juego_por_mazo_vacio()
            return

        carta_robada = self.baraja.pop()
        if self.turno == 0:
            self.jugador1["mano"].append(carta_robada)
        else:
            self.jugador2["mano"].append(carta_robada)

        messagebox.showinfo("Carta robada", f"Jugador {self.turno + 1} ha robado una carta.")
        self.mostrar_cartas()

    def fin_del_juego_por_mazo_vacio(self):
        """
        Termina el juego si la baraja se queda sin cartas. El ganador se determina por puntos.
        """
        if self.jugador1["puntos"] > self.jugador2["puntos"]:
            self.fin_del_juego("Jugador 1")
        elif self.jugador2["puntos"] > self.jugador1["puntos"]:
            self.fin_del_juego("Jugador 2")
        else:
            self.fin_del_juego("Nadie")

    def fin_del_juego(self, ganador):
        """
        Termina el juego y muestra el ganador.
        """
        messagebox.showinfo("Fin del Juego", f"¡{ganador} ha ganado!")
        self.root.destroy()

    def obtener_puntajes(self):
        """
        Devuelve los puntajes de ambos jugadores como un string.
        """
        return f"Jugador 1: {self.jugador1['puntos']} puntos | Jugador 2: {self.jugador2['puntos']} puntos"

    def actualizar_puntajes(self):
        """
        Actualiza la visualizacion de los puntajes en la interfaz grafica.
        """
        self.puntaje_label.config(text=self.obtener_puntajes())

    def cerrar_juego(self):
        """
        Cierra la ventana del juego.
        """
        self.root.destroy()

# Funcion que se abrira al presionar el boton de INSTRUCCIONES
def mostrar_instrucciones():
    # Leer el contenido del archivo de instrucciones
    with open('Instrucciones UNO QUIZ.txt', 'r') as file:
        instrucciones = file.read()
    
    # Crear una nueva ventana con las instrucciones
    instrucciones_window = tk.Toplevel()
    instrucciones_window.title("Instrucciones - UNO QUIZ")
    instrucciones_window.geometry("600x400")
    
    # Mostrar las instrucciones en un widget Text
    text_widget = tk.Text(instrucciones_window, wrap=tk.WORD, height=15, width=70)
    text_widget.insert(tk.END, instrucciones)
    text_widget.config(state=tk.DISABLED)  # Hacer el texto no editable
    text_widget.pack(pady=20)

    # Boton de Cerrar Instrucciones
    cerrar_instrucciones_button = tk.Button(instrucciones_window, text="Cerrar", font=("Arial", 14), bg="#ff0000", fg="white", command=instrucciones_window.destroy)
    cerrar_instrucciones_button.pack(pady=20)

# Funcion que se abrira al presionar el boton de JUGAR
def iniciar_juego():
    # Cerrar el menu principal
    ventana.destroy()
    # Iniciar el juego
    root = tk.Tk()
    juego = JuegoUNO(root, ventana)
    root.mainloop()

# Crear la ventana principal del menu
ventana = tk.Tk()
ventana.title("UNO QUIZ")
ventana.geometry("800x600")
ventana.config(bg="#ff4f00")  # Color de fondo similar al de UNO (rojo)

# Titulo grande en el centro
titulo = tk.Label(ventana, text="UNO QUIZ", font=("Helvetica", 36, "bold"), bg="#ff4f00", fg="white")
titulo.pack(pady=40)

# Boton de INSTRUCCIONES
boton_instrucciones = tk.Button(ventana, text="INSTRUCCIONES", font=("Helvetica", 16), bg="#0095ff", fg="white", command=mostrar_instrucciones)
boton_instrucciones.pack(pady=20)

# Boton de JUGAR
boton_jugar = tk.Button(ventana, text="JUGAR", font=("Helvetica", 16), bg="#00c853", fg="white", command=iniciar_juego)
boton_jugar.pack(pady=20)

# Boton de Cerrar Juego
boton_cerrar = tk.Button(ventana, text="Cerrar Juego", font=("Helvetica", 16), bg="#ff0000", fg="white", command=ventana.quit)
boton_cerrar.pack(pady=20)

# Iniciar el bucle principal de la interfaz grafica
ventana.mainloop()
