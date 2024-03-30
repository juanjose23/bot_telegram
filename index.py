import telebot
from telebot import types
import requests
from datetime import datetime
import uuid
import os
import subprocess
#Conexion con nuestro BOT
TOKEN = '7183470855:AAGgo_eXb2POEsx6RjIRzCQI6bkwmvUOSFU'
bot = telebot.TeleBot(TOKEN)
PHOTOS_FOLDER = r"C:\Users\jrios\OneDrive\Escritorio\Detection-and-count-CBB\Broca2000\examp"
ruta_bat = r'C:\Users\jrios\OneDrive\Escritorio\Bot_telegram\run_app.bat'
TEXT_FOLDER = r'C:\Users\jrios\OneDrive\Escritorio\Detection-and-count-CBB\yolov5\runs\detect'

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
        bot.reply_to(message, "Se ha recibido con éxito:")
     

    except Exception as e:
        print(e)
        bot.reply_to(message, "¡Ha ocurrido un error al guardar o procesar la imagen.")


@bot.message_handler(func=lambda message: True)
def handle_other(message):
    bot.reply_to(message, "Lo siento, no entendí ese comando. Por favor, usa el comando /start para comenzar.")


if __name__ == "__main__":
    bot.polling(none_stop=True)