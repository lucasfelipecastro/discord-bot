# Discord Music Bot

This project is a Discord bot developed in Python using the `discord.py` library. The bot allows users to play music directly in their Discord servers, offering commands to play, pause, resume, and stop music, as well as to join and leave voice channels.

## Features

- Play music from provided URLs.
- Pause, resume, and stop music playback.
- Automatically join and leave voice channels as needed.

## Prerequisites

Ensure you have the following installed in your environment:

- Python 3.6 or higher.
- A Discord account and a server where you have permissions to add bots.
- [FFmpeg](https://ffmpeg.org/download.html) installed and available in the system PATH.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/lucasfelipecastro/discord-bot
    cd discord-bot
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use venv\Scripts\activate
    ```

3. **Install the dependencies:**

    ```bash
    pip install discord.py python-dotenv yt-dlp
    ```

4. **Configure the Bot Token:**

    Create a `.env` file in the project's root directory and add your bot's token:

    ```env
    DISCORD_TOKEN=your_token_here
    ```

    *Note:* To obtain your bot's token, you need to create an application in the [Discord Developer Portal](https://discord.com/developers/applications) and add a bot to your application.

5. **Install FFmpeg:**

    The bot uses FFmpeg for audio handling. Ensure that FFmpeg is installed and available in the system PATH. You can download it from:

    - [FFmpeg.org](https://ffmpeg.org/download.html)

## Usage

After completing the installation steps, start the bot with the following command:

```bash
python your_script.py
```

Replace your_script.py with the name of the file containing the bot's code.


## Commands

In Discord, you can interact with the bot using the following commands:
- `.play <URL>`: The bot will play the audio from the provided URL.
- `.pause`: Pauses the current playback.
- `.resume`: Resumes paused playback.
- `.stop`: Stops audio playback.
- `.join`: The bot will join your current voice channel.
- `.leave`: The bot will leave the voice channel.


*Note: Ensure that the bot has the appropriate permissions on the server and that you are in a voice channel when using audio-related commands.

## Contributing
Contributions are welcome! Feel free to open issues and pull requests for improvements or fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
