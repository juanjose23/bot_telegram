@echo off

rem Cambiar al directorio de tu aplicación Flask (ajusta la ruta según tu estructura)
cd C:\Users\jrios\OneDrive\Escritorio\Detection-and-count-CBB\yolov5

rem Activar el entorno virtual
call env\Scripts\activate
rem Instalar los requisitos
pip install -r requirements.txt
rem Ejecutar Flask
python detect.py --weights ./runs/train/exp15/weights/CBB_yolov5s.pt --img 3456 --conf 0.58 --source ../Broca2000/examp --save-txt
python detect.py --weights ./runs/train/exp15/weights/CBB_yolov5m.pt --img 3456 --conf 0.73 --source ../Broca2000/examp --save-txt

rem Desactivar el entorno virtual al finalizar
deactivate
