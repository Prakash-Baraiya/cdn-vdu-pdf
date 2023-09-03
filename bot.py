import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Replace 'YOUR_BOT_TOKEN' with your actual bot token obtained from BotFather on Telegram
bot_token = '6598445027:AAHOiQ5_P-SV_x0aPH1iuUku6SOboIiMvys'

def start(update, context):
    update.message.reply_text("Please send a .txt file containing name:url pairs.")

def process_txt_file(update, context):
    file = update.message.document.get_file()
    file.download('input.txt')
    with open('input.txt', 'r') as infile:
        lines = infile.readlines()

    # Filter lines to keep only those containing 'cdn-vidu'
    filtered_lines = [line for line in lines if 'cdn-vidu' in line]

    # Prepare the corrected content
    corrected_content = '\n'.join(filtered_lines)

    # Write the corrected content to a new file
    with open('output.txt', 'w') as outfile:
        outfile.write(corrected_content)

    # Send the corrected file to the user
    context.bot.send_document(chat_id=update.effective_chat.id, document=open('output.txt', 'rb'))
    os.remove('input.txt')
    os.remove('output.txt')

def main():
    updater = Updater(bot_token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.document.file_extension('txt'), process_txt_file))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
