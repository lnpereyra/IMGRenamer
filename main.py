import os
import re
from pyunpack import Archive
import os.path
from tkinter import filedialog as fd
from tkinter import *
import shutil

# Carpeta contenedora del Keynote
root1 = Tk()
root1.directory = fd.askdirectory(
    parent=root1,
    initialdir=os.getcwd(),
    title="Seleccionar la carpeta contenedora del Keynote:",
)
directorio_original = root1.directory
# Busca solo el Keynote
for file in os.listdir(directorio_original):
    if file.endswith(".key"):
        nombre_keynote = os.path.join(directorio_original, file)
# Extrae el contenido a al directorio principal
Archive(nombre_keynote).extractall(directorio_original)

# Directorio con carpetas de idiomas
root = Tk()
root.directory = fd.askdirectory(
    parent=root,
    initialdir=os.getcwd(),
    title="Seleccionar carpeta contenedora de Targets:",
)
a = root.directory
# Tomo TODOS los targets
for root, dirs, files in os.walk(a):
    directorio_traducido = root + "/"
    # Generar lista de archivos de ambos directorios
    originales = os.listdir(directorio_original + "/data")
    traducidos = os.listdir(directorio_traducido)
    # Por cada foto traducida ver la lista de todas las originales
    for foto_traducida in traducidos:
        for foto_original in originales:
            # Filtramos el nombre del archivo y quitamos todo lo que viene luego de -12345
            # Ejemplo de japon-12345.jpg solo nos quedaria 'japon', esto ayuda a hacer una
            # comparacion literal y evitar nombres problematicos
            original_sin_numero = re.sub(r"-\d{5}\S*", "", foto_original)
            # Aca hacemos el split para agarrar el nombre de archivo nomas.
            # De 'japon.jpg' nos quedaria solo 'japon'
            # Si el nombre filtrado es igual al de la foto traducida, renombrarlo
            foto_sinext = os.path.splitext(foto_traducida)[0][0:]
            if foto_sinext == original_sin_numero:
                os.rename(
                    directorio_traducido + foto_traducida,
                    directorio_traducido + foto_original,
                )
# Borro Carpetas y Archivos que ya no me sirven
for root, dirs, files in os.walk(directorio_original):
    for name in dirs:
        if name == "VILT":
            continue
        else:
            shutil.rmtree(os.path.join(root, name))
    for name in files:
        if name.endswith(".key") or name.endswith(".pages"):
            continue
        else:
            print(directorio_original)
            print(root)
            print(os.path.join(root, name))
            os.remove(os.path.join(directorio_original, name))

# asi funciona pero tengo que evitar que tire el error al final,
# no encuentra las imagenes que se guardaron en "name"
# porque yo vuelvo al directorio_original , tengo que hacer que las saltee.
