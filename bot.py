from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from telegram.ext.filters import *
import time

user_tasks = {}
# /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('👋 Привет! Этот бот поможет вам управлять задачами. Используйте /help, чтобы увидеть доступные команды.')

# /help
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('➼ /add - добавить задачу\n➼ /list - показать список задач\n➼ /remove - удалить задачу\n➼ /clear - очистить список задач\n➼ /done - отметить задачу выполненной\n➼ /help - показать список команд')

# /add
def add_task(update: Update, context: CallbackContext) -> None:
    task_text = ' '.join(context.args)
    if task_text:
        user_id = update.message.from_user.id
        if user_id not in user_tasks:
            user_tasks[user_id] = []
        user_tasks[user_id].append(task_text)
        update.message.reply_text(f'ℹ Задача "{task_text}" добавлена.')
    else:
        update.message.reply_text('⚠ Используйте /add [текст задачи] для добавления новой задачи. ⚠')

# /list
def list_tasks(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    tasks = user_tasks.get(user_id, [])
    if tasks:
        task_list = '\n'.join([f'💠 {index + 1}. {task}' for index, task in enumerate(tasks)])
        update.message.reply_text(f'⁋ Список задач: ¶\n{task_list}')
    else:
        update.message.reply_text('♻ Список задач пуст. ♻')

# /remove
def remove_task(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    tasks = user_tasks.get(user_id, [])
    if tasks:
        try:
            index = int(context.args[0]) - 1
            if 0 <= index < len(tasks):
                removed_task = tasks.pop(index)
                update.message.reply_text(f'❌ Задача "{removed_task}" удалена.')
            else:
                update.message.reply_text('⚠ Указан некорректный номер задачи. ⚠')
        except ValueError:
            update.message.reply_text('⚠ Используйте /remove [номер задачи] для удаления задачи. ⚠')
    else:
        update.message.reply_text('♻ Список задач пуст. ♻')

# /clear
def clear_tasks(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id in user_tasks:
        user_tasks[user_id] = []
        update.message.reply_text('♻ Список задач очищен. ♻')
    else:
        update.message.reply_text('♻ Список задач уже пуст. ♻')

# /done
def mark_done(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    tasks = user_tasks.get(user_id, [])
    if tasks:
        try:
            index = int(context.args[0]) - 1
            if 0 <= index < len(tasks):
                marked_task = tasks.pop(index)
                update.message.reply_text(f'✅ Задача "{marked_task}" выполнена.')
                if len(tasks) == 0:
                    update.message.reply_text('🌠 Все задачи выполнены! Отлично! 🌠')
            else:
                update.message.reply_text('⚠ Указан некорректный номер задачи. ⚠')
        except ValueError:
            update.message.reply_text('⚠ Используйте /done [номер задачи] для отметки задачи как выполненной. ⚠')
    else:
        update.message.reply_text('Список задач пуст.')

def main() -> None:
    updater = Updater('6489434816:AAHfnKgo2F4nAiH8lvAubYmVAIgkCRFUgnA')
    bot = updater.bot
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("add", add_task))
    dp.add_handler(CommandHandler("list", list_tasks))
    dp.add_handler(CommandHandler("remove", remove_task))
    dp.add_handler(CommandHandler("clear", clear_tasks))
    dp.add_handler(CommandHandler("done", mark_done))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
