import tempfile
import os
import sys
import logging
from telegram import Update, Poll
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def start(update: Update, context: CallbackContext) -> None:
    # Initialize the list of message IDs
    try:
        with open(r'R:\RawandChatBoat\Stored message ID\message_ids.txt', 'r') as f:
            context.bot_data['message_ids'] = [int(line.strip()) for line in f]
    except FileNotFoundError:
        context.bot_data['message_ids'] = []

    # Send the start message and save its message ID
    message = update.message.reply_text('Bot restarted. Hello! Send me a message with the poll details to create a quiz poll.')
    context.bot_data['message_ids'].append(message.message_id)
    with open(r'R:\RawandChatBoat\Stored message ID\message_ids.txt', 'a') as f:
        f.write(f'{message.message_id}\n')

def help(update: Update, context: CallbackContext) -> None:
    # Send the help message and save its message ID
    message = update.message.reply_text('Available commands:\n/start - Start the bot\n/help - Show this help message\n/poll - Create a quiz poll\n/stop - Stop the bot\n/restart - Restart the bot')
    context.bot_data['message_ids'].append(message.message_id)
    with open(r'R:\RawandChatBoat\Stored message ID\message_ids.txt', 'a') as f:
        f.write(f'{message.message_id}\n')

def stop(update: Update, context: CallbackContext) -> None:
    if 'message_ids' not in context.bot_data:
        context.bot_data['message_ids'] = []
    # Send the stop message and save its message ID
    message = update.message.reply_text('Stopping the bot. Use /start to start the bot again.')
    context.bot_data['message_ids'].append(message.message_id)
    with open(r'R:\RawandChatBoat\Stored message ID\message_ids.txt', 'a') as f:
        f.write(f'{message.message_id}\n')
    context.bot_data['stopped'] = True

def restart(update: Update, context: CallbackContext) -> None:
    if 'message_ids' not in context.bot_data:
        context.bot_data['message_ids'] = []
    # Send the restart message and save its message ID
    message = update.message.reply_text('Restarting the bot...')
    context.bot_data['message_ids'].append(message.message_id)
    with open(r'R:\RawandChatBoat\Stored message ID\message_ids.txt', 'a') as f:
        f.write(f'{message.message_id}\n')
    os.execl(sys.executable, sys.executable, *sys.argv)

def poll(update: Update, context: CallbackContext) -> None:
    if 'message_ids' not in context.bot_data:
        context.bot_data['message_ids'] = []
    # Check if the bot is stopped
    if context.bot_data.get('stopped'):
        return

    # Save the message ID of the incoming message
    context.bot_data['message_ids'].append(update.message.message_id)
    with open(r'R:\RawandChatBoat\Stored message ID\message_ids.txt', 'a') as f:
        f.write(f'{update.message.message_id}\n')

    # Split the message into separate questions
    questions = update.message.text.split('&')

    # Extract the comment from the last question
    comment = questions[-1].split('#')[-1].strip()
    questions[-1] = questions[-1].split('#')[0].strip()

    # Create a poll for each question
    for question_text in questions:
        # Parse the poll details from the question text
        try:
            lines = question_text.strip().split('\n')
            question = lines[0].replace('$','')
            options = lines[1:]
            correct_option_index = len(options) - 1
            for idx,option in enumerate(options):
                if '$' in option:
                    correct_option_index = idx
                    options[idx] = option.replace('$','')
        except Exception as e:
            # Send an error message and save its message ID
            message = update.message.reply_text(f'Error: {e}\nPlease make sure the message is in the correct format.')
            context.bot_data['message_ids'].append(message.message_id)
            with open(r'R:\RawandChatBoat\Stored message ID\message_ids.txt', 'a') as f:
                f.write(f'{message.message_id}\n')
            return

          # Check the value of correct_option_index
        print(f'correct_option_index: {correct_option_index}')

        # Check the number of options
        print(f'options: {options}')
        if len(options) > 10:
            # Send an error message and save its message ID
            message = update.message.reply_text(f'Error: Poll can\'t have more than 10 options.')
            context.bot_data['message_ids'].append(message.message_id)
            with open(r'R:\RawandChatBoat\Stored message ID\message_ids.txt', 'a') as f:
                f.write(f'{message.message_id}\n')
            return

        # Send the quiz poll and save its message ID
        message = context.bot.send_poll(
            chat_id=update.effective_chat.id,
            question=question,
            options=options,
            type=Poll.QUIZ,
            correct_option_id=correct_option_index,
            explanation=comment
        )
        context.bot_data['message_ids'].append(message.message_id)
        with open(r'R:\RawandChatBoat\Stored message ID\message_ids.txt', 'a') as f:
            f.write(f'{message.message_id}\n')

def delete(update: Update, context: CallbackContext) -> None:
    if 'message_ids' not in context.bot_data:
        context.bot_data['message_ids'] = []
    # Check if the bot is stopped
    if context.bot_data.get('stopped'):
        return

    # Print the message_ids list
    print(f'message_ids: {context.bot_data.get("message_ids", [])}')

    # Delete all messages in the chat
    for message_id in context.bot_data.get('message_ids', []):
        try:
            context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message_id)
        except Exception as e:
            # Print any errors that occur
            print(f'Error deleting message: {e}')

    # Clear the list of message IDs
    context.bot_data['message_ids'] = []

    # Delete the message IDs from the message_ids.txt file
    with open(r'R:\RawandChatBoat\Stored message ID\message_ids.txt', 'w') as f:
        f.write('')

def export_message_ids(update: Update, context: CallbackContext) -> None:
    if 'message_ids' not in context.bot_data:
        context.bot_data['message_ids'] = []
    # Check if the bot is stopped
    if context.bot_data.get('stopped'):
        return

    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        # Write the message IDs to the temporary file
        for message_id in context.bot_data.get('message_ids', []):
            f.write(f'{message_id}\n')
        # Save the temporary file name
        temp_file_name = f.name

    # Send the temporary file as a document
    with open(temp_file_name, 'rb') as f:
        context.bot.send_document(chat_id=update.effective_chat.id, document=f)

    # Delete the temporary file
    os.unlink(temp_file_name)

def main():
    updater = Updater("Your_Token")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("stop", stop))
    dispatcher.add_handler(CommandHandler("restart", restart))
    dispatcher.add_handler(MessageHandler(filters.Filters.text & ~filters.Filters.command, poll))
    dispatcher.add_handler(CommandHandler("delete", delete))
    dispatcher.add_handler(CommandHandler("id", export_message_ids))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
