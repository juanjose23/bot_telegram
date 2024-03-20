library(httr)

# Definir la URL base de la API de Telegram y el token de tu bot
base_url <- "https://api.telegram.org/bot"
token <- "7183470855:AAGgo_eXb2POEsx6RjIRzCQI6bkwmvUOSFU"
api_url <- paste0(base_url, token)

# Función para enviar un mensaje al bot
send_message <- function(chat_id, text) {
  url <- paste0(api_url, "/sendMessage")
  body <- list(chat_id = chat_id, text = text)
  POST(url, body = body)
}

# Manejar el comando /start
handle_start_command <- function(message) {
  chat_id <- message$message$chat$id
  text <- "¡Hola! 👋\n\n¡Bienvenido a nuestro bot de imágenes! 🌟\n\n¿Quieres compartir una imagen con nosotros? Simplemente presiona el botón 📷 Enviar Imagen."
  send_message(chat_id, text)
}

# Manejar los mensajes que contienen el texto "📷 Enviar Imagen"
handle_image_request <- function(message) {
  chat_id <- message$message$chat$id
  text <- "Por favor, envía una imagen."
  send_message(chat_id, text)
}

# Manejar los mensajes que contienen una imagen
save_photo <- function(message) {
  tryCatch({
    chat_id <- message$message$chat$id
    file_id <- message$message$photo[[length(message$message$photo)]]$file_id
    url <- paste0(api_url, "/getFile?file_id=", file_id)
    file_info <- content(GET(url), "parsed")
    file_path <- file_info$result$file_path
    file_url <- paste0("https://api.telegram.org/file/bot", token, "/", file_path)
    downloaded_file <- GET(file_url)
    file_path <- paste0("ruta_de_guardado/", file_id, ".jpg")  # Especifica la ruta de guardado
    writeBin(content(downloaded_file), file_path)
    send_message(chat_id, "¡Imagen guardada con éxito!")
  }, error = function(e) {
    send_message(chat_id, "¡Ha ocurrido un error al guardar la imagen.")
  })
}

# Función principal para manejar los mensajes
handle_message <- function(message) {
  text <- message$message$text
  if (text == "/start") {
    handle_start_command(message)
  } else if (text == "📷 Enviar Imagen") {
    handle_image_request(message)
  } else if (startsWith(text, "/image")) {
    save_photo(message)
  } else {
    chat_id <- message$message$chat$id
    send_message(chat_id, "Lo siento, no entendí ese comando. Por favor, usa el comando /start para comenzar.")
  }
}

# Función para obtener actualizaciones del bot
get_updates <- function(offset) {
  url <- paste0(api_url, "/getUpdates?offset=", offset)
  response <- GET(url)
  content(response, "parsed")
}

# Función principal para ejecutar el bot
run_bot <- function() {
  offset <- 0
  
  while (TRUE) {
    updates <- get_updates(offset)
    if (length(updates$result) > 0) {
      for (update in updates$result) {
        handle_message(update)
        offset <- update$update_id + 1
      }
    }
  }
}

# Ejecutar el bot
run_bot()
