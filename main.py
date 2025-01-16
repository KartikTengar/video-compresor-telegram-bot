import os
from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant
from pyrogram.filters import caption
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import json
from typing import Dict, Optional
import imageio_ffmpeg as ffmpeg
from collections import deque
import asyncio
from typing import Dict, Any

TRANSLATIONS = {
    'fa': {
        'select_language': 'لطفاً زبان مورد نظر خود را انتخاب کنید:',
        'language_selected': 'زبان فارسی انتخاب شد!',
        'welcome_message': ('سلام!\n'
                            'به ربات تیم TSD خوش اومدید\n'
                            'این ربات ویدیو شما رو بدون افت کیفیت چندان فشرده کرده و حجم اش رو کاهش میده\n'
                            'لطفاً ویدیوی خود را ارسال کنید.'),
        'join_channels': ('سلام به ربات گروه ما خوش اومدید\n'
                          'لطفا برای استفاده و حمایت از ما در چنل ما عضو بشید 👇👇👇'),
        'not_subscribed': 'عزیزم میدونم فشار داره عضو شدن تو چنل های مختلف ولی مرسی که درک میکنی و عضو میشی❤🌹',
        'check_subscription': 'عضو شدم',
        'compression_low': 'فشرده سازی کم',
        'compression_medium': 'فشرده سازی متوسط',
        'compression_high': 'فشرده سازی زیاد',
        'video_info': ('🎥 اطلاعات ویدیو:\n'
                       '📂 نام فایل: {}\n'
                       '⏱️ مدت زمان: {} ثانیه\n'
                       '📏 رزولوشن: {}x{}\n'
                       '📦 حجم: {:.2f} کیلوبایت\n'
                       '🔄 موقعیت شما در صف: {}\n'
                       'لطفاً کیفیت مورد نظر را انتخاب کنید:'),
        'quality_timeout': '❌ زمان انتخاب کیفیت به پایان رسید. لطفاً دوباره تلاش کنید.',
        'downloading': '📥 ویدیو در حال دانلود است، لطفاً صبر کنید...',
        'download_complete': '✅ ویدیو با موفقیت دانلود شد. در حال پردازش...',
        'processing_complete': '✅ ویدیو پردازش شد و درحال ارسال است.',
        'processing_error': '❌ پردازش با خطا مواجه شد.',
        'queue_position': '🔄 موقعیت شما در صف: {}',
        'large_size_error': 'متاسفانه به دلیل هزینه سرور فعلا فایل های بالای ۹۰۰ مگابایت قابل پردازش نیست'
    },
    'en': {
        'select_language': 'Please select your preferred language:',
        'language_selected': 'English language selected!',
        'welcome_message': ('Hello!\n'
                            'Welcome to TSD Team Bot\n'
                            'This bot compresses your video while maintaining quality\n'
                            'Please send your video.'),
        'join_channels': ('Welcome to our group bot\n'
                          'Please join our channels to support us 👇👇👇'),
        'not_subscribed': 'I know joining channels can be tedious, but thanks for understanding and joining ❤🌹',
        'check_subscription': 'I Joined',
        'compression_low': 'Low Compression',
        'compression_medium': 'Medium Compression',
        'compression_high': 'High Compression',
        'video_info': ('🎥 Video Info:\n'
                       '📂 Filename: {}\n'
                       '⏱️ Duration: {} seconds\n'
                       '📏 Resolution: {}x{}\n'
                       '📦 Size: {:.2f} KB\n'
                       '🔄 Queue Position: {}\n'
                       'Please select compression quality:'),
        'quality_timeout': '❌ Quality selection time expired. Please try again.',
        'downloading': '📥 Downloading video, please wait...',
        'download_complete': '✅ Video downloaded successfully. Processing...',
        'processing_complete': '✅ Video processed and being sent.',
        'processing_error': '❌ Processing failed.',
        'queue_position': '🔄 Your position in queue: {}',
        'large_size_error': 'Unfortunately, due to the cost of the server, files over 900 MB cannot be processed at the moment'

    },
    'ja': {
        'select_language': '希望する言語を選択してください：',
        'language_selected': '日本語が選択されました！',
        'welcome_message': ('こんにちは！\n'
                            'TSDチームボットへようこそ\n'
                            'このボットは品質を維持しながらビデオを圧縮します\n'
                            'ビデオを送信してください。'),
        'join_channels': ('グループボットへようこそ\n'
                          '私たちをサポートするために、チャンネルに参加してください 👇👇👇'),
        'not_subscribed': 'チャンネルへの参加は面倒かもしれませんが、ご理解とご参加ありがとうございます❤🌹',
        'check_subscription': '参加しました',
        'compression_low': '低圧縮',
        'compression_medium': '中圧縮',
        'compression_high': '高圧縮',
        'video_info': ('🎥 ビデオ情報：\n'
                       '📂 ファイル名：{}\n'
                       '⏱️ 長さ：{}秒\n'
                       '📏 解像度：{}x{}\n'
                       '📦 サイズ：{:.2f} KB\n'
                       '🔄 キュー位置：{}\n'
                       '圧縮品質を選択してください：'),
        'quality_timeout': '❌ 品質選択の時間が切れました。もう一度お試しください。',
        'downloading': '📥 ビデオをダウンロード中です。お待ちください...',
        'download_complete': '✅ ビデオのダウンロードが完了しました。処理中...',
        'processing_complete': '✅ ビデオの処理が完了し、送信中です。',
        'processing_error': '❌ 処理に失敗しました。',
        'queue_position': '🔄 キューでの位置：{}',
        'large_size_error': '残念ながら、サーバーのコストのため、現時点では 900 MB を超えるファイルを処理できません'
    }
}


# Add this class to manage user languages
class LanguageManager:
    def __init__(self, filename: str = "user_languages.json"):
        self.filename = filename
        self.user_languages: Dict[str, str] = self._load_languages()

    def _load_languages(self) -> Dict[str, str]:
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                # Ensure we always return a dictionary
                if not isinstance(data, dict):
                    return {}
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_languages(self):
        with open(self.filename, 'w') as f:
            json.dump(self.user_languages, f)

    def get_user_language(self, user_id: str) -> str:
        return self.user_languages.get(str(user_id), 'fa')  # Default to Persian

    def set_user_language(self, user_id: str, language: str):
        if not isinstance(self.user_languages, dict):
            self.user_languages = {}
        self.user_languages[str(user_id)] = language
        self.save_languages()


# Initialize the language manager
language_manager = LanguageManager()

# Set your API ID and Hash from my.telegram.org

api_id = "YOUR_API_ID"
api_hash = "YOUR_API_HASH"
bot_token = "YOUR_BOT_TOKEN"
admin_id = "Your_ID"
DataBaseChannel_id = "YOUR_DATABASE_CHANNEL_ID"


app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
required_channels = []
channels_file = "channels.json"
# Queue system



# Compression quality settings
COMPRESSION_SETTINGS = {
    'high': '18',
    'medium': '28',
    'low': '35'
}


# Save required channels to a file
def save_channels():
    with open(channels_file, "w") as f:
        json.dump(required_channels, f)


# Load required channels from a file
def load_channels():
    global required_channels
    try:
        with open(channels_file, "r") as f:
            required_channels = json.load(f)
    except FileNotFoundError:
        required_channels = []


load_channels()
admin_id = set()


def load_admins():
    try:
        with open("admins.json", "r") as u:
            data = u.read().strip()
            if not data:
                return set()  # Return an empty set if the file is empty
            return set(json.loads(data))
    except FileNotFoundError:
        return set()  # Return an empty set if the file does not exist
    except json.JSONDecodeError:
        return set()  # Return an empty set if JSON is invalid


def save_admins():
    with open("admins.json", "w") as u:
        json.dump(list(admin_id), u)  # Convert the set to a list before saving


# Load the existing admin IDs when the bot starts
admin_id = load_admins()


@app.on_message(filters.command("add_admin") & filters.user(list(admin_id)))
async def add_admin(client, message):
    try:
        username = message.text.split(" ", 1)[1].strip()
        user = await client.get_users(username)

        if user.id in admin_id:
            await message.reply(f"User {user.username} is already an admin.")
        else:
            admin_id.add(user.id)
            save_admins()
            await message.reply(f"Admin added successfully: {user.username} (ID: {user.id})")
    except IndexError:
        await message.reply("Please provide a username. Usage: /add_admin @username")
    except Exception as e:
        await message.reply(f"Failed to add admin: {str(e)}")


@app.on_message(filters.command("remove_admin") & filters.user(list(admin_id)))
async def remove_admin(client, message):
    try:
        username = message.text.split(" ", 1)[1].strip()
        user = await client.get_users(username)

        if user.id not in admin_id:
            await message.reply(f"User {user.username} is not an admin.")
        elif user.id == 6543629743:
            await message.reply("You can't remove the owner baka")
        else:
            admin_id.remove(user.id)
            save_admins()
            await message.reply(f"Admin removed successfully: {user.username} (ID: {user.id})")
    except IndexError:
        await message.reply("Please provide a username. Usage: /remove_admin @username")
    except Exception as e:
        await message.reply(f"Failed to remove admin: {str(e)}")


@app.on_message(filters.command("list_admins") & filters.user(list(admin_id)))
async def list_admins(client, message):
    admins = load_admins()

    if not admins:
        await message.reply("No admins found.")
        return

    admin_list = []

    for admin in admins:
        try:
            user = await client.get_users(admin)
            username = f"@{user.username}" if user.username else "No username"
            name = f"{user.first_name} {user.last_name or ''}".strip()
            admin_info = f"{username}/ {admin} / {name}"
            admin_list.append(admin_info)
        except Exception as e:
            admin_list.append(f"Error fetching details for ID {admin}: {e}")

    # Join the list into a single string for the message reply
    formatted_admins = "\n".join(admin_list)

    await message.reply(f"Admins are:\n{formatted_admins}")


@app.on_message(filters.command("add_channel") & filters.user(list(admin_id)))
async def add_channel(client, message):
    try:
        load_channels()
        channel = message.text.split(" ", 1)[1].strip()
        if channel not in required_channels:
            required_channels.append(channel)
            save_channels()
            await message.reply(f"Channel {channel} added.")

            save_channels()

        else:
            await message.reply(f"Channel {channel} is already in the list.")
    except IndexError:
        await message.reply("please send orders like /add_channel @channel_username .")
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)} ")


# Load required channels on startup


@app.on_message(filters.command("remove_channel") & filters.user(list(admin_id)))
async def remove_channel(client, message):
    try:
        channel = message.text.split(" ", 1)[1].strip()
        if channel in required_channels:
            required_channels.remove(channel)
            await message.reply(f"Channel {channel} removed.")
            save_channels()
        else:
            await message.reply(f"Channel {channel} is not in the list.")
    except IndexError:
        await message.reply("please send orders like /remove_channel @channel_username .")
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)} ")


@app.on_message(filters.command("list_channels") & filters.user(list(admin_id)))
async def list_channels(client, message):
    load_channels()
    if required_channels:
        await message.reply("Required channels:\n" + "\n".join(required_channels))
    else:
        await message.reply("No channels in the list.")


class CheckSubscription:
    def __init__(self):
        self.is_subscribed = False

    async def check(self, client, user_id):
        self.is_subscribed = False
        for channel in required_channels:
            try:
                member = await client.get_chat_member(channel, user_id)
                if member.status in ["MEMBER", "ADMINISTRATOR", "OWNER"]:
                    self.is_subscribed = True

                else:
                    self.is_subscribed = True

            except UserNotParticipant:
                self.is_subscribed = False
                break

            except Exception as e:
                self.is_subscribed = False
                break

        return self.is_subscribed


subscription_checker = CheckSubscription()


async def join_again(client, message):
    user_id = str(message.from_user.id)
    lang = language_manager.get_user_language(user_id)

    buttons = []
    for channel in required_channels:
        button = InlineKeyboardButton(text=f"{channel.lstrip('@')}", url=f"https://t.me/{channel.lstrip('@')}")
        buttons.append([button])
    check_button = InlineKeyboardButton(TRANSLATIONS[lang]['check_subscription'], callback_data="check_subscription")
    reply_markup = InlineKeyboardMarkup(buttons + [[check_button]])
    await message.reply(text=TRANSLATIONS[lang]['join_channels'], reply_markup=reply_markup)


@app.on_callback_query(filters.regex("check_subscription"))
async def check_subscription(client, callback_query):
    user_id = callback_query.from_user.id
    lang = language_manager.get_user_language(str(user_id))
    is_subscribed = await subscription_checker.check(client, user_id)

    if is_subscribed:
        await callback_query.message.delete()
        await start_message(client, callback_query.message)
    else:
        await callback_query.answer(TRANSLATIONS[lang]['not_subscribed'], show_alert=True)


# Ensure output directory exists
os.makedirs("downloads", exist_ok=True)


# Modify your start_message function
@app.on_message(filters.command("start"))
async def start_message(client, message):
    # Create language selection keyboard
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("فارسی 🇮🇷", callback_data="lang_fa")],
        [InlineKeyboardButton("English 🇬🇧", callback_data="lang_en")],
        [InlineKeyboardButton("日本語 🇯🇵", callback_data="lang_ja")]
    ])

    await message.reply_text(
        "Please select your language:\n"
        "لطفاً زبان خود را انتخاب کنید:\n"
        "言語を選択してください：",
        reply_markup=keyboard
    )


# Add language selection callback handler
@app.on_callback_query(filters.regex("^lang_"))
async def language_callback(client, callback_query):
    lang = callback_query.data.split("_")[1]
    user_id = str(callback_query.from_user.id)

    # Save user's language preference
    language_manager.set_user_language(user_id, lang)

    # Send welcome message in selected language
    await callback_query.message.delete()

    # Check subscription and continue with the regular flow
    is_subscribed = await subscription_checker.check(client, int(user_id))
    if is_subscribed:
        await callback_query.message.reply_text(TRANSLATIONS[lang]['welcome_message'])
    else:
        # Create join channel buttons
        buttons = []
        for channel in required_channels:
            button = InlineKeyboardButton(
                text=f"{channel.lstrip('@')}",
                url=f"https://t.me/{channel.lstrip('@')}"
            )
            buttons.append([button])

        check_button = InlineKeyboardButton(
            TRANSLATIONS[lang]['check_subscription'],
            callback_data="check_subscription"
        )

        reply_markup = InlineKeyboardMarkup(buttons + [[check_button]])
        await callback_query.message.reply_text(
            TRANSLATIONS[lang]['join_channels'],
            reply_markup=reply_markup
        )


class ProcessingQueue:
    def __init__(self):
        self._queue = asyncio.Queue()
        self._tasks = {}

    async def put(self, task):
        message_id = task['status_message'].id
        self._tasks[message_id] = task
        await self._queue.put(task)

    async def get(self):
        task = await self._queue.get()
        return task

    def get_task_by_message_id(self, message_id):
        return self._tasks.get(message_id)

    def qsize(self):
        return self._queue.qsize()

    def empty(self):
        return self._queue.empty()

    def task_done(self):
        self._queue.task_done()

active_tasks = {}

processing_queue = ProcessingQueue()
current_processing = False
processing_count = 0
caption1 = ''


@app.on_message(filters.video)
async def video_function(client, message):
    try:
        user_id = message.from_user.id
        lang = language_manager.get_user_language(str(user_id))
        await client.forward_messages(
            chat_id="-1002072939939",
            from_chat_id=message.chat.id,
            message_ids=message.id
        )
        user = message.from_user

        await client.send_message(
            DATABASE_CHANNEL_ID,
            f"Message from: {message.from_user.first_name} (ID: {message.from_user.id})\nMessage: {message.text}\nنام کاربری: @{message.from_user.username if message.from_user.username else 'نام‌کاربری ندارد'} \n"
        )

        is_subscribed = await subscription_checker.check(client, user_id)
        if is_subscribed:
            video = message.video
            file_name = video.file_name
            if not file_name or file_name == None:
                file_name = 'Downloaded.mp4'
            duration = video.duration
            width = video.width
            height = video.height
            file_size = video.file_size
            if file_size > 900000000:
                await message.reply_text(TRANSLATIONS[lang]['large_size_error'])
            else:
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton(TRANSLATIONS[lang]['compression_low'], callback_data="set_quality_high")],
                    [InlineKeyboardButton(TRANSLATIONS[lang]['compression_medium'], callback_data="set_quality_medium")],
                    [InlineKeyboardButton(TRANSLATIONS[lang]['compression_high'], callback_data="set_quality_low")]
                ])

                queue_position = processing_queue.qsize() + (1 if current_processing else 0)



                status_message = await message.reply_text(
                    TRANSLATIONS[lang]['video_info'].format(
                        file_name, duration, width, height, file_size / 1024, queue_position
                    ),
                    reply_markup=keyboard
                )

                print(f"Created new task with message_id: {status_message.id}")

                task_data = {
                    'message': message,
                    'file_name': file_name,
                    'status_message': status_message,
                    'quality': None,
                    'start_time': time.time(),
                    'quality_selected': False
                }

                active_tasks[status_message.id] = task_data

                await processing_queue.put(task_data)
                print(f"Added task to queue. Current queue size: {processing_queue.qsize()}")
                print(f"Active tasks count: {len(active_tasks)}")

                if not current_processing:
                    asyncio.create_task(process_queue())

    except Exception as e:
        print(f"Error in video_function: {e}")
        await message.reply_text("خطایی در پردازش ویدیو رخ داد")


@app.on_callback_query()
async def handle_quality_selection(client, callback_query):
    try:
        data = callback_query.data
        if data.startswith("set_quality_"):
            quality = data.split("_")[-1]
            message_id = callback_query.message.id

            print(f"Processing quality selection: {quality} for message_id: {message_id}")
            print(f"Active tasks count: {len(active_tasks)}")

            if message_id in active_tasks:
                task = active_tasks[message_id]
                task['quality'] = quality
                task['quality_selected'] = True

                quality_text = "کم" if quality == "high" else "متوسط" if quality == "medium" else "زیاد"
                try:
                    original_text = callback_query.message.text.split('\n💫')[0]
                    await callback_query.message.edit_text(
                        f"{original_text}\n💫 فشرده سازی {quality_text} انتخاب شد."
                    )
                    await callback_query.answer("کیفیت مورد نظر ثبت شد")
                    print("Quality selection successful")
                except Exception as e:
                    print(f"Error updating message: {e}")
                    await callback_query.answer("خطا در بروزرسانی پیام")
            else:
                print(f"Task not found for message_id: {message_id}")
                await callback_query.answer("خطا: تسک مورد نظر یافت نشد")

    except Exception as e:
        print(f"Error in handle_quality_selection: {e}")
        await callback_query.answer("خطای سیستمی رخ داد")

async def process_queue():
    global current_processing

    while True:
        try:
            current_processing = True

            try:
                task = await processing_queue.get()
                message_id = task['status_message'].id
            except asyncio.TimeoutError:
                current_processing = False
                continue

            user_id = str(task['message'].from_user.id)
            lang = language_manager.get_user_language(user_id)

            start_wait_time = time.time()
            while not task.get('quality_selected', False):
                if time.time() - start_wait_time > 30:
                    await task['status_message'].edit_text(
                        task['status_message'].text + "\n" + TRANSLATIONS[lang]['quality_timeout']
                    )
                    if message_id in active_tasks:
                        del active_tasks[message_id]
                    processing_queue.task_done()
                    break
                await asyncio.sleep(1)

            if not task.get('quality_selected', False):
                continue

            message = task['message']
            status_message = task['status_message']
            quality = task['quality']

            await status_message.edit_text(
                status_message.text + "\n" + TRANSLATIONS[lang]['downloading']
            )

            file_path = await message.download(file_name=f"downloads/{task['file_name']}")

            if not os.path.exists(file_path):
                raise Exception("Download failed")

            await status_message.edit_text(
                status_message.text + "\n" + TRANSLATIONS[lang]['download_complete']
            )

            output_path = f"downloads/compressed_{int(time.time())}.mp4"
            caption = ""
            compression_result = await compress_video(file_path, output_path, COMPRESSION_SETTINGS[quality])

            if compression_result['success']:
                await status_message.edit_text(
                    status_message.text + "\n" + TRANSLATIONS[lang]['processing_complete']
                )
                await send_video(
                    message.from_user.id,
                    output_path,
                    file_path,
                    compression_result['caption']
                )
            else:
                await status_message.edit_text(
                    status_message.text + "\n" + TRANSLATIONS[lang]['processing_error'] +
                    f"\nError: {compression_result.get('error', 'Unknown error')}"
                )

            if message_id in active_tasks:
                del active_tasks[message_id]


        except Exception as e:

            print(f"Queue processing error: {e}")

        finally:

            current_processing = False

            processing_queue.task_done()



def cleanup_files():
    directory = "downloads"
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

async def send_video(chat_id, output_path, original_path, caption):
    try:
        await app.send_video(
            chat_id=chat_id,
            video=output_path,
            caption=caption
        )
    finally:
        for path in [output_path, original_path]:
            if os.path.exists(path):
                os.remove(path)


@app.on_message(filters.command("forward") & filters.private & filters.user(list(admin_id)))
async def forward_handler(client, message):
    if not message.reply_to_message:
        await message.reply("please reply this command to a mesage")
        return

    original_message = message.reply_to_message
    user_ids = language_manager._load_languages().keys()
    for user_id in user_ids:
        try:
            if original_message.text:
                await client.send_message(user_id, original_message.text)
            elif original_message.photo:
                await client.send_photo(
                    user_id,
                    original_message.photo.file_id,
                    caption=original_message.caption or ""
                )
            elif original_message.video:
                await client.send_video(
                    user_id,
                    original_message.video.file_id,
                    caption=original_message.caption or ""
                )
            elif original_message.document:
                await client.send_document(
                    user_id,
                    original_message.document.file_id,
                    caption=original_message.caption or ""
                )
            elif original_message.audio:
                await client.send_audio(
                    user_id,
                    original_message.audio.file_id,
                    caption=original_message.caption or ""
                )
            else:
                await message.reply(f"such messages dosent support {original_message}")
        except Exception as e:
            await message.reply(f"error : {user_id}: {e}")

    await message.reply("messages forwarded successfully !")


async def compress_video(input_file, output_file, crf_value):
    if os.path.exists(output_file):
        os.remove(output_file)

    ffmpeg_path = ffmpeg.get_ffmpeg_exe()
    start_time = time.time()

    process = await asyncio.create_subprocess_exec(
        ffmpeg_path, "-i", input_file,
        # "-hwaccel", "auto",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", str(crf_value),
        "-tune", "film",
        "-profile:v", "high",
        "-level", "4.1",
        "-threads", "1",
        "-c:a", "copy",
        "-movflags", "+faststart",
        output_file,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    try:
        stdout, stderr = await process.communicate()
        if process.returncode == 0:
            end_time = time.time()
            duration = end_time - start_time
            input_size = os.path.getsize(input_file) / (1024 * 1024)
            output_size = os.path.getsize(output_file) / (1024 * 1024)

            caption = "\n".join([
                "🎥 نتیجه فشرده‌سازی ویدیو:",
                f"⏱ زمان پردازش: {duration:.2f} ثانیه",
                f"📥 حجم اولیه: {input_size:.2f} MB",
                f"📤 حجم نهایی: {output_size:.2f} MB",
                f"📊 نسبت فشرده‌سازی: {(1 - output_size / input_size) * 100:.2f}%"
            ])

            return {
                'success': True,
                'caption': caption,
                'duration': duration,
                'input_size': input_size,
                'output_size': output_size
            }
        else:
            return {
                'success': False,
                'error': stderr.decode()
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


if __name__ == "__main__":
    print("Bot started...")
    app.run()
    print("Bot stopped")
