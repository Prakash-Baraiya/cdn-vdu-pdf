import os
import logging
from telegram import Update, Document
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# States for the conversation
SELECT_FILE = 1

# Global variable to store the selected file content
file_content = ""

# Function to start the bot and ask for a file
def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Welcome to the bot! Please send a .txt file containing name:url with 'cdn-vidu'.")

    return SELECT_FILE

# Function to handle received documents
def receive_file(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    document = update.message.document

    # Check if the file is a .txt file
    if document.mime_type == "text/plain":
        file = context.bot.get_file(document.file_id)
        file.download("input.txt")
        
        with open("input.txt", "r") as txt_file:
            global file_content
            file_content = txt_file.read()

        # Process the file content (remove lines with "cdn-vidu")
        processed_content = "\n".join(line for line in file_content.split("\n") if "cdn-vidu" in line)

        # Save the processed content to a new file
        with open("output.txt", "w") as output_file:
            output_file.write(processed_content)

        # Send the processed file to the user
        context.bot.send_document(update.message.chat_id, document=open("output.txt", "rb"))
        return ConversationHandler.END
    else:
        update.message.reply_text("Please send a .txt file.")
        return SELECT_FILE

# Function to handle the cancel command
def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END

def main() -> None:
    # Initialize the Telegram bot
    updater = Updater(token="YOUR_BOT_TOKEN", use_context=True)
    dp = updater.dispatcher

    # Define the conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={SELECT_FILE: [MessageHandler(Filters.document.mime("text/plain"), receive_file)]},
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    dp.add_handler(conv_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
