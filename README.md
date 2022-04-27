# Taller Fotografía 3º GTDM

Trabajo académico realizado por Pau Pérez Manzaneda y Diego Vicente Villagrasa para la asignatura de Talleres de Tecnologías Emergentes del grado de Tecnología Digital y Multimedia impartido en la UPV.


# Índice 
  * [Introducción](#introducción)
  * [Panoramicas](#panorámicas)
  * [Focus Stacking](#focus-stacking)
  * [Main](#main)

# Introducción

El código desarrollado consiste en un programa capaz de realizar técnicas fotográficas tales como panorámicas y focus stacking. También cuenta con una interfaz gráfica básica, que permite al usuario utilizar fácilmente el programa. 

Al iniciar el código, se abrirá la ventana principal, donde se encuentran dos botones que abren las diferentes ventanas del programa, una para realizar fotografías panorámicas, y otra para realizar focus stacking.


# Panorámicas

Las fotografías panorámicas se realizan a través del programa [panoramic.py](https://github.com/PauSuerte/Taller-Fotografia-3-GTDM/blob/main/Archivos/panoramic.py). Para ello, necesitará dos o más fotografías, la carpeta donde se quiera guardar el archivo final, y el nombre con la extensión de dicho archivo. 

Para el funcionamiento del script, son necesarias cuatro funciones:  `progPaneo`, `pan`, `warpImages` y `crop`.

La función `progPaneo` es la que se encarga de coordinar todas las demás. Esta recibe las imágenes desde la función [main.py](https://github.com/PauSuerte/Taller-Fotografia-3-GTDM/blob/main/Archivos/main.py) y posteriormente las manda a la función `pan`.

Esta se encarga de encontrar puntos en común entre las imágenes, para posteriormente unirlas con la función `warpImages`.

Por último, la función `crop` se encarga de encontrar automáticamente los espacios negros de la imagen panorámica creada por las funciones anteriores, y recortarlos, dejando una imagen limpia.


# Focus Stacking

En este apartado, en el archivo [fs.py](https://github.com/PauSuerte/Taller-Fotografia-3-GTDM/blob/main/Archivos/fs.py) se ha desarrollado un programa de apilamiento de enfoque, esto es, una técnica de procesamiento digital en la cual se agrupar múltiples imágenes de un mismo objeto que han sido tomadas enfocando en distintos puntos o tienen diversas profundidades de campo con el fin de crear una imagen final con más profundidad de campo que las imágenes iniciales.

Respecto al funcionamiento del programa se encontrará en primer lugar una función llamada `load_images(images)` en la cual el argumento de entrada será las imágenes que se quieran tratar con el programa. Esta función lo que hará será marcar el orden de las capas de color en el que se encuentran ya que cv2 trabaja en BGR (blue-green-red) y las imágenes en su mayoria se trabajan en RGB (red-green-blue).

A continuación, se halla la _primera_ función (de dos) de alineamiento de imágenes (`align(im1, im2)`). Como parámetros de entrada se introducen las imágenes que se quieren alinear. Primero se pasarán a blanco y negro para que el módulo de cv2 trabaje de manera más eficiente. y tras ello la función se encargará de, según el tamaño de la primera imagen introducida mantener dicho tamaño y alinear la siguiente sobre la misma.

A esta función le sigue pues la _segunda_ función de alineamiento `align_images(images)` y que empleará la anterior para alinear toda la lista que se le ha de introducir. Así pues extraerá una lista nueva con las imagenes alineadas.

Seguidamente, se encuentra la función `doLap(image)`. Esta calculará el gradient map de la imagen mediante un filtro de blur gaussiano y una laplaciana.

Finalmente, se sitúan dos funciones complementarias `focus_stack(unimages)` y `main(nameSalida,imagenes,dirname)`. `focus_stack(unimages)` empleará las funciones anteriores para alinear las imagenes y con ellas comenzará almacenarlas todas en la misma imagen final. En esta función se asegura que las imagenes introducidas se encuentran en blanco y negro y tras ello genera el output vacío en el que almacenará el mismo y tras ello lo generará.
En `main(nameSalida,imagenes,dirname)`, por otro lado, llamará a todas las funciones necesarias para que el código de la interfaz pueda ejecutar sin errores las funciones y conseguir generar la imagen deseada.


# Main

El programa [main.py](https://github.com/PauSuerte/Taller-Fotografia-3-GTDM/blob/main/Archivos/main.py) se encarga de coordinar los dos otros programas y toda la interfaz gráfica. Este cuenta con cuatro funciones, más 16 líneas que se encargan de la ventana del GUI principal.

La primera función, `getDataPan`, se encarga de recibir los datos introducidos por el usuario a través de la GUI. Estos datos son el nombre del archivo y la extensión. Aparte se introduce el _frame_ donde se mostrará la foto final. La función se encarga de preguntar al usuario a través de la GUI, que imágenes quiere utilizar para el efecto, y donde quiere que se deje el resultado final. Después de esto, se leen las imágenes con cv2, y se introducen a un diccionario, para entonces ejecutar el programa `progPaneo`, que se encarga de realizar la panorámica. Tras terminar, se mostrará la imagen por pantalla.

La segunda función, `getDataFs`, es prácticamente idéntica a la anterior, con la diferencia que ahora al final de esta, se ejecuta la función encargada de realizar el Focus Stacking [fs.py](https://github.com/PauSuerte/Taller-Fotografia-3-GTDM/blob/main/Archivos/fs.py). 

Posteriormente se encuentra la función `close_window`, encargada de cerrar las ventanas cuando se pulse el botón de cerrar, y posteriormente abrir la ventana principal.

Después se encuentra la función `openNewWindow`, encargada de abrir la ventana elegida por el usuario, y todos los elementos necesarios, como botones o cajas de texto.
Esta función está separada en dos condiciones if, una para la ventana de la panorámica, y otra para la ventana del focus stacking. Ambos funcionan de la misma manera, primero se esconde la ventana principal, para mostrar la nueva con los nuevos elementos, entre los que encontramos botones tipo radio para seleccionar la extensión del archivo, cajas de texto para escribir el nombre del archivo final, y un botón para realizar el efecto, entre otros elementos.

Por último, encontramos unas líneas encargadas de mantener la ventana principal, y el mainloop, encargado de que toda la GUI funcione.
