#!/bin/bash

# Abrir una nueva terminal y ejecutar los comandos en ella
gnome-terminal -- bash -c '
# Cambiar a la ruta de la carpeta
cd /home/juan/Escritorio/Detection-and-count-CBB/yolov5/

# Activar el entorno virtual
source env/bin/activate

# Instalar los requisitos
pip install -r requirements.txt

# Ejecutar el programa
python3 detect.py --weights ./weights/CBB_yolov5m.pt --img 224 --conf 0.6 --source ./data/Broca2000/images --save-txt --save-conf --exist-ok  --agnostic-nms --augmen

# Cerrar la terminal
sleep infinity
'
