import tkinter as tk
from tkinter import ANCHOR, NW, Label, filedialog, Frame, Toplevel, mainloop, Button
import panoramic as pm
import fs as fs
import cv2
from PIL import Image, ImageTk

def getDataPan(nameBox,extension,frame): # Funcion para obtener datos y ejecutar la funcion de paneo
    global pan_window 
    global imRepre # Declaracion global obligatoria de la representacion de la panoramica en ventana
    imagenes = {} # Diccionario que guarda las imagenes seleccionadas por el usuario
    nameSalida = nameBox.get() + extension.get() # Obtener el nombre de la salida seleccionado por el usuario de la caja de input y añadir la extension
    dirname = filedialog.askdirectory() #Seleccion de carpeta donde se dejaran los resultados a traves del buscador

    panFiles = filedialog.askopenfilenames(title = "Elige las fotos a panear", filetypes=(("png files", "*.png"),("jpg files","*.jpg")))
    numFotos = len(panFiles) # Obtener el numero de fotos seleccionadas

    for i in range(numFotos): # Bucle for, en rango de 0 al numero de fotos total anteriormente seleccionado. El usuario seleccionara a traves del buscador las imagenes a panear.
        imagenes[str(i)] = cv2.imread(panFiles[i]) # Se guarda el path de las imagenes en el diccionario
    
    flag = pm.progPaneo(nameSalida,numFotos,imagenes,dirname) # Ejecutamos la funcion de paneo, junto a los datos necesarios anteriormente obtenidos
    if flag:
        imRepre = ImageTk.PhotoImage(Image.open(dirname+'/'+nameSalida)) # Mostrar imagen en ventana
        labelIm = Label(frame, image=imRepre) ; labelIm.pack() # Label necesario para que se muestre la imagen 

def getDataFS(nameBox,extension,frame): # Funcion para obtener datos y ejecutar la funcion de paneo
    global fs_window 
    global imRepre # Declaracion global obligatoria de la representacion de la imagen final en ventana
    imagenes = {} # Diccionario que guarda las imagenes seleccionadas por el usuario
    nameSalida = nameBox.get() + extension.get() # Obtener el nombre de la salida seleccionado por el usuario de la caja de input y añadir la extension
    dirname = filedialog.askdirectory() #Seleccion de carpeta donde se dejaran los resultados a traves del buscador

    fsFiles = filedialog.askopenfilenames(title = "Elige las fotos a panear", filetypes=(("png files", "*.png"),("jpg files","*.jpg")))
    numFotos = len(fsFiles) # Obtener el numero de fotos seleccionadas

    for i in range(numFotos): # Bucle for, en rango de 0 al numero de fotos total anteriormente seleccionado. El usuario seleccionara a traves del buscador las imagenes a panear.
        imagenes[str(i)] = cv2.imread(fsFiles[i]) # Se guarda el path de las imagenes en el diccionario
    
    flag = fs.main(nameSalida,imagenes,dirname) # Ejecutamos la funcion de paneo, junto a los datos necesarios anteriormente obtenidos
    if flag:
        print('PASO')
        imRepre = ImageTk.PhotoImage(Image.open(dirname+'/'+nameSalida)) # Mostrar imagen en ventana
        print(dirname+'/'+nameSalida)
        labelIm = Label(frame, image=imRepre) ; labelIm.pack() # Label necesario para que se muestre la imagen 


def close_window(wd): # Funcion para esconder la ventana actual y posteriormente mostrar de nuevo la master

    if wd == 'pan':
        pan_window.withdraw()

    if wd == 'fs':
        fs_window.withdraw()

    if wd == 'edit':
        edit_window.withdraw()

    master.deiconify() # Reaparece la ventana master 

def openNewWindow(ventana):
    global pan_window 
    global fs_window
    global edit_window

    if ventana == 'pan':
        ### PANORAMIC ###
        master.withdraw() # Se esconde la ventana principal

        pan_window = Toplevel(master) ; pan_window.geometry("800x600") # Creacion de ventana principal ; Tamaño inicial de la ventana

        pan_window.protocol("WM_DELETE_WINDOW", lambda: close_window('pan')) # Al cerrar la ventana, se recuperara la ventana principal

        title = tk.Label(pan_window, text = "Focus Staking") ; title.pack() # Creacion de etiqueta ; colocado de etiqueta

        title_nameSalida = tk.Label(pan_window, text = "Introduzca el nombre del resultado (con extension)") ; title_nameSalida.pack() 

        nameBox = tk.Entry(pan_window) ; nameBox.pack() # Caja de introduccion de nombre del resultado

        title_extensions = tk.Label(pan_window, text = "Seleccione la extension deseada") ; title_extensions.pack()

        extension = tk.StringVar() # Variable que guardara el resultado de los radio buttons (extensiones)

        rPng = tk.Radiobutton(pan_window, text='.png', variable=extension, value='.png') ; rPng.pack()

        rJpg = tk.Radiobutton(pan_window, text='jpg', variable=extension, value='.jpg') ; rJpg.pack()

        panBtn = tk.Button(pan_window , text = "Realizar focus staking" , command= lambda: getDataPan(nameBox,extension,frame)) ; panBtn.pack() # Realizar panoramica

        frame = Frame(pan_window, width=200, height=100) ; frame.pack() 
    
    if ventana == 'fs':
        master.withdraw() # Se esconde la ventana principal

        fs_window = Toplevel(master) ; fs_window.geometry("800x600") # Creacion de ventana principal ; Tamaño inicial de la ventana

        fs_window.protocol("WM_DELETE_WINDOW", lambda: close_window('fs')) # Al cerrar la ventana, se recuperara la ventana principal

        titleFs = tk.Label(fs_window, text = "Focus Stacking") ; titleFs.pack() # Creacion de etiqueta ; colocado de etiqueta

        title_nameSalida = tk.Label(fs_window, text = "Introduzca el nombre del resultado (con extension)") ; title_nameSalida.pack() 

        nameBox = tk.Entry(fs_window) ; nameBox.pack() # Caja de introduccion de nombre del resultado

        title_extensions = tk.Label(fs_window, text = "Seleccione la extension deseada") ; title_extensions.pack()

        extension = tk.StringVar() # Variable que guardara el resultado de los radio buttons (extensiones)

        rPng = tk.Radiobutton(fs_window, text='.png', variable=extension, value='.png') ; rPng.pack()

        rJpg = tk.Radiobutton(fs_window, text='jpg', variable=extension, value='.jpg') ; rJpg.pack()

        panBtn = tk.Button(fs_window , text = "Realizar panoramica" , command= lambda: getDataFS(nameBox,extension,frame)) ; panBtn.pack() # Realizar panoramica

        frame = Frame(fs_window, width=200, height=100) ; frame.pack() 

    if ventana == 'edit':
        master.withdraw() # Se esconde la ventana principal

        edit_window = Toplevel(master) ; edit_window.geometry("800x600") # Creacion de ventana principal ; Tamaño inicial de la ventana

        edit_window.protocol("WM_DELETE_WINDOW", lambda: close_window('edit')) # Al cerrar la ventana, se recuperara la ventana principal

        titleEd = tk.Label(edit_window, text = "Edicion de fotografias") ; titleEd.pack() # Creacion de etiqueta ; colocado de etiqueta




### MAIN ###

master = tk.Tk() ; master.geometry("800x600") # Creacion de la ventana master

btnPan = Button(master,
             text ="Pan",
             command = lambda: openNewWindow('pan')) # Boton para abrir ventana de paneo
btnPan.pack(pady = 10)

btnFS = Button(master,
             text ="Focus Stacking",
             command = lambda: openNewWindow('fs')) # Boton para abrir ventana focus stacking
btnFS.pack(pady = 10)

btnEd = Button(master,
             text ="Edit ",
             command = lambda: openNewWindow('edit')) # Boton para abrir ventana de edicion
btnEd.pack(pady = 10)


mainloop() # Registro obligatorio para funcionamiento de las ventanas