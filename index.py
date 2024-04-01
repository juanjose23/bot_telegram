from telebot import types
import telebot
import requests
from datetime import datetime
import uuid
import os
import subprocess
import glob
import time
#Conexion con nuestro BOT
TOKEN = '7183470855:AAGgo_eXb2POEsx6RjIRzCQI6bkwmvUOSFU'
bot = telebot.TeleBot(TOKEN)

PHOTOS_FOLDER = "C:\\Users\\jrios\\Desktop\\Detection-and-count-CBB\\yolov5\\data\\Broca2000\\images"
ruta_bat = r"C:\\Users\\jrios\\Desktop\\bot_telegram\\run_app.bat"
directoriotxt = "C:\\Users\\jrios\\Desktop\\Detection-and-count-CBB\\yolov5\\runs\\detect\\exp\\labels"
directorio= "C:\\Users\\jrios\\Desktop\\Detection-and-count-CBB\\yolov5\\runs\\detect\\exp"

def buscar_archivos(nombre_directorio, nombre_archivo):
    # Cambiar al directorio especificado
    os.chdir(nombre_directorio)
    
    # Buscar archivos con el nombre especificado
    archivos_encontrados = glob.glob(nombre_archivo + ".*")
    
    # Devolver la lista de rutas absolutas de archivos encontrados
    return archivos_encontrados
def contartxt(nombre_directorio, nombre_archivo):
    # Cambiar al directorio especificado
    os.chdir(nombre_directorio)
    
    # Buscar archivos con el nombre especificado
    archivos_encontrados = glob.glob(nombre_archivo + ".txt")
    
    # Contar las líneas del primer archivo encontrado
    if archivos_encontrados:
        with open(archivos_encontrados[0], 'r') as archivo:
            lineas = sum(1 for linea in archivo)
        return lineas
    else:
        return None, 0
# Manejar el comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Crear un teclado personalizado con un botón para enviar una imagen
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button = types.KeyboardButton("📷 Enviar Imagen")
    keyboard.add(button)
    
    # Mensaje de bienvenida con formato en negrita y emoticones
    welcome_message = (
        "¡Hola! 👋\n\n"
        "¡Bienvenido a nuestro bot de imágenes! 🌟\n\n"
        "¿Quieres compartir una imagen con nosotros? Simplemente presiona el botón 📷 Enviar Imagen."
    )
    
    # Enviar el mensaje de bienvenida con el teclado personalizado
    bot.reply_to(message, welcome_message, parse_mode="Markdown", reply_markup=keyboard)

# Manejar los mensajes que contienen imágenes
@bot.message_handler(func=lambda message: message.text == "📷 Enviar Imagen")
def handle_image_request(message):
    bot.reply_to(message, "Por favor, envía una imagen.")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, 'Puedes interactuar conmigo usando comandos. Por ahora, solo respondo a /start y /help')

# Manejador para el comando /imagen
@bot.message_handler(commands=['image'])
def send_image_help(message):
    bot.reply_to(message, 'Por favor, envía una foto.')

@bot.message_handler(content_types=['photo'])
def save_photo(message):
    try:
        # Obtener información de la imagen
        file_info = bot.get_file(message.photo[-1].file_id)
        # Descargar la imagen
        downloaded_file = bot.download_file(file_info.file_path)
        # Guardar la imagen en la carpeta especificada
       
        file_path = os.path.join(PHOTOS_FOLDER, f"{message.photo[-1].file_id}.jpg")
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        subprocess.run(ruta_bat, shell=True)

         # Enviar el contenido del archivo de texto como mensaje
        bot.reply_to(message, "Se ha recibido con éxito, en un momento se le enviara los resultados")
        # Directorio en el que quieres buscar
       
        # Nombre del archivo que estás buscando (sin la extensión)
        nombre_archivo =  message.photo[-1].file_id
       
        # Llamar a la función para buscar archivos
        numeros = []
        archivos_encontrados = []
        enviado_mensaje = False

        while not enviado_mensaje:
            while not numeros:
                numeros = contartxt(directoriotxt, nombre_archivo)
                if not numeros:
                    bot.reply_to(message, f"Esperando a que se encuentren insectos...")
                    time.sleep(1)

            while not archivos_encontrados:
                archivos_encontrados = buscar_archivos(directorio, nombre_archivo)
                if not archivos_encontrados:
                    bot.reply_to(message, "Esperando a que se encuentren archivos...")
                    time.sleep(1)

            bot.reply_to(message, f"Se han encontrado {numeros} insectos.")
            rutas_completas = f"{directorio}\\{archivos_encontrados[0]}"
           # bot.reply_to(message, f"Se han encontrado {archivos_encontrados} insectos.")
            bot.send_photo(chat_id=message.chat.id, photo=open(rutas_completas, 'rb'), caption='Aquí tienes tu imagen')
          
            enviado_mensaje = True

                
                
    except Exception as e:
        print(e)
        bot.reply_to(message, "¡Ha ocurrido un error al guardar o procesar la imagen.")


@bot.message_handler(func=lambda message: True)
def handle_other(message):

    bot.reply_to(message, "Lo siento, no entendí ese comando. Por favor, usa el comando /start para comenzar.")


if __name__ == "__main__":
    bot.polling(none_stop=True)