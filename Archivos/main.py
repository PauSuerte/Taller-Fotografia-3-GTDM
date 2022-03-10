import tkinter as tk
from tkinter import Label, filedialog, Frame
import panoramic as pm
import cv2
from PIL import Image, ImageTk

def getData(): # Funcion para obtener datos y ejecutar la funcion de paneo
    global imRepre # Declaracion global obligatoria de la representacion de la panoramica en ventana
    imagenes = {} # Diccionario que guarda las imagenes seleccionadas por el usuario
    numFotos = int(numBox.get()) # Obtener el numero de fotos seleccionado por el usuario de la caja de input
    nameSalida = nameBox.get() # Obtener el nombre de la salida seleccionado por el usuario de la caja de input
    
    dirname = filedialog.askdirectory() #Seleccion de carpeta donde se dejaran los resultados a traves del buscador

    for i in range(numFotos): # Bucle for, en rango de 0 al numero de fotos total anteriormente seleccionado. El usuario seleccionara a traves del buscador las imagenes a panear.
        pan_window.filename = filedialog.askopenfilename(title = "Elige la foto a panear", filetypes=(("png files", "*.png"),("jpg files","*.jpg")))
        imagenes[str(i)] = cv2.imread(pan_window.filename) # Se guarda el path de las imagenes en el diccionario
    
    flag = pm.progPaneo(nameSalida,numFotos,imagenes,dirname) # Ejecutamos la funcion de paneo, junto a los datos necesarios anteriormente obtenidos
    if flag:
        imRepre = ImageTk.PhotoImage(Image.open(dirname+'/'+nameSalida)) # Mostrar imagen en ventana
        labelIm = Label(frame, image=imRepre) ; labelIm.pack()

pan_window = tk.Tk() ; pan_window.geometry("800x600")   # Creacion de ventana principal ; Tamaño inicial de la ventana

title = tk.Label(pan_window, text = "Creacion de panoramicas") ; title.pack() # Creacion de etiqueta ; colocado de etiqueta

title_numFotos = tk.Label(pan_window, text = "Introduzca el numero de fotos") ; title_numFotos.pack() 

numBox = tk.Entry(pan_window) ; numBox.pack() # Caja de introduccion de numero de fotos para panear

title_nameSalida = tk.Label(pan_window, text = "Introduzca el nombre del resultado (con extension)") ; title_nameSalida.pack() 

nameBox = tk.Entry(pan_window) ; nameBox.pack() # Caja de introduccion de numero de fotos para panear

panBtn = tk.Button(pan_window , text = "Realizar panoramica" , command= getData) ; panBtn.pack() # Realizar panoramica

frame = Frame(pan_window, width=300, height=200) ; frame.pack()
# frame.place(anchor='center', relx=0.5, rely=0.5)

# imRepre = ImageTk.PhotoImage(Image.open("pan.jpg"))
# labelIm = Label(frame, image=imRepre) ; labelIm.pack() 

pan_window.mainloop() # Registro obligatorio para funcionamiento de la ventana
