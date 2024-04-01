@echo off

rem Cambiar al directorio de tu aplicación Flask (ajusta la ruta según tu estructura)
cd C:\\Users\\jrios\\Desktop\\Detection-and-count-CBB\\yolov5

rem Activar el entorno virtual
call env\Scripts\activate
rem Instalar los requisitos
pip install -r requirements.txt
rem Ejecutar Flask
python detect.py --weights ./weights/CBB_yolov5m.pt --img 224 --conf 0.2 --source ./data/Broca2000/images --save-txt --save-conf --exist-ok  --agnostic-nms --augmen

rem Desactivar el entorno virtual al finalizar
deactivate
