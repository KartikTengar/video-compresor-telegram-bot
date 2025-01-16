# Video Compressor Bot  
[![Pyrogram](https://img.shields.io/badge/Pyrogram-2.0-blue?style=for-the-badge&logo=python)](https://docs.pyrogram.org/)  [![FFmpeg](https://img.shields.io/badge/FFmpeg-5.1-green?style=for-the-badge&logo=ffmpeg)](https://www.ffmpeg.org/)  [![Python](https://img.shields.io/badge/Python-3.9+-yellow?style=for-the-badge&logo=python)](https://www.python.org/)  



## 🎥 Introduction  
### **Video Compressor Bot** is an advanced Telegram bot designed to compress videos while maintaining high quality. It is optimized for restricted environments and offers a wide range of features for seamless user interaction.  
#### Here is my bot link  [Video compressor](https://t.me/video_compressorxbot?start=_tgr_3QQJAbE5MjE0), I hope the bot still running on the server when you read this .
---

## ⚡ Key Features  
- **Multi-Language Support:** Supports Persian, English, and Japanese for diverse user interactions.  
- **Queue Management:** Efficiently handles multiple video requests in real-time.  
- **Compression Quality Options:** Low, medium, and high compression settings for custom output.  
- **Forced Channel Join:** Users must join predefined channels before accessing the bot.  
- **Admin Management:** Add, remove, and list bot administrators dynamically.  
- **Channel Management:** Add or remove mandatory channels for user subscription, stored in a JSON file.  
- **User Language Preferences:** Maintains a dictionary of users and their selected languages, saved in JSON format.  
- **Forward Announcements:** Send notifications or announcements to all users with a single command.  
- **Restricted FFmpeg Usage:** Utilizes FFmpeg binary for environments without `sudo` access.  

---

## 🛠 How It Works  
1. **User Interaction:**  
   - Users send a video to the bot.  
   - The bot processes and compresses the video based on the selected quality level.  

2. **Queue System:**  
   - Requests are added to a queue and processed sequentially to ensure fairness.  

3. **Forced Channel Join:**  
   - The bot checks if the user has joined mandatory channels before providing its services.  

4. **Language Preferences:**  
   - Each user's preferred language is saved and used in all bot interactions.  

---

## 🧰 Technologies Used  
- **[Pyrogram](https://docs.pyrogram.org/) 2.0:** A modern Telegram API wrapper for Python.  
- **[FFmpeg](https://ffmpeg.org/):** Industry-standard multimedia processing tool.  
- **Python 3.9+:** Core logic and functionality.  
- **JSON Storage:** Used for storing admin data, channels, and user preferences persistently.  

---

## 🚀 Quick Start  

### 1. Prerequisites  
- Python 3.9+  
- Install required packages:  
```bash
pip install -r requirements.txt
```
### 2. Download FFmpeg Binary  
Download the FFmpeg binary suitable for your operating system from the official website:  
[FFmpeg Official Site](https://ffmpeg.org/download.html)  

- Place the downloaded binary in your project folder.  
- Alternatively, ensure the binary is added to your system's PATH for global access.  
#### or you can use  [imageio[ffmpeg]](https://imageio.readthedocs.io/en/v2.11.0/reference/_backends/imageio.plugins.ffmpeg.html)
```bash
 pip install imageio[ffmpeg]
```

### 3. Configure the Bot  
Update the following values in `main.py`:  
- `api_id`  
- `api_hash`  
- `bot_token`  

These credentials can be obtained from the [Telegram BotFather](https://core.telegram.org/bots).  

### 4. Run the Bot  
```bash
python main.py
```  
#### Great way to run on hosts like Cpanel
```bash
nohup python main.py
```
### 5. Optimize FFmpeg Threads (Optional)  
Run the `ThreadOptimizer` script to identify the optimal thread count for your server:  
```bash
python ThreadOptimizer.py
```  

---

## 📝 Commands and Functionalities  

### **Admin Commands**  
1. `/add_admin @username`  
   Add a new administrator by username.  
2. `/remove_admin @username`  
   Remove an existing administrator.  
3. `/list_admins`  
   List all current administrators.  

### **Channel Commands**  
1. `/add_channel @channel_username`  
   Add a mandatory channel for user subscription.  
2. `/remove_channel @channel_username`  
   Remove a channel from the mandatory list.  
3. `/list_channels`  
   Display the list of mandatory channels.  

### **User Management**  
- Automatically stores user IDs and their preferred languages in a JSON file for personalized interactions.  

### **Forward Announcements**  
- Reply to a message with `/forward` to broadcast it to all registered users.  

---

## 📂 Additional Utility: `ThreadOptimizer`  
This script helps identify the optimal thread count for FFmpeg compression on your server.  
- Tests compression speed and performance for different thread counts.  
- Outputs the best configuration for efficient processing.  

---

## ❓ FAQ  

### Q: Why does the bot use FFmpeg binary instead of the default installation?  
A: The bot is designed for environments where `sudo` access is unavailable. The binary ensures compatibility in such restricted setups.  

### Q: How does the forced channel join work?  
A: Users must join specified channels before using the bot. The bot verifies their membership using the Telegram API.  

---

## 📜 License  
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.  

---

## 🤝 Contributions  
Contributions are welcome! Feel free to fork the repository, enhance features, and submit a pull request.  

---

## 📧 Contact  
For questions, suggestions, or bug reports, please open an issue on GitHub.

---
## Powered by Shinigami_110
You can [contact me on Telegram](https://t.me/shinigami_110) using this link.

