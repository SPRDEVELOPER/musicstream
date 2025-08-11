# Telegram Music Bot

A Python-based Telegram bot that can play music in voice chats using YouTube as the source. The bot supports command-based controls for playing, pausing, resuming, and managing a music queue.

## Features

### Core Functionality
- **YouTube Integration**: Search and download music from YouTube using yt-dlp
- **Queue Management**: Add songs to a queue, skip tracks, and view upcoming songs
- **Playback Controls**: Play, pause, resume, and stop music
- **Voice Chat Support**: Join Telegram voice chats to stream audio (simulation mode)
- **Multi-Chat Support**: Handle multiple voice chats simultaneously

### Available Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `/start` | Show welcome message and available commands | `/start` |
| `/help` | Display help information | `/help` |
| `/play <song_name>` | Search and play music from YouTube | `/play bohemian rhapsody` |
| `/pause` | Pause the current song | `/pause` |
| `/resume` | Resume playback | `/resume` |
| `/stop` | Stop music and leave voice chat | `/stop` |
| `/queue` | Show the current queue | `/queue` |
| `/skip` | Skip the current song | `/skip` |

## Setup Instructions

### Prerequisites
1. Python 3.8+ installed
2. A Telegram Bot Token from [@BotFather](https://t.me/BotFather)
3. FFmpeg installed (for audio processing)

### Installation Steps

1. **Create a Telegram Bot**:
   - Open Telegram and search for `@BotFather`
   - Send `/newbot` command
   - Choose a name and username for your bot
   - Save the bot token provided

2. **Configure Environment Variables**:
   ```bash
   export BOT_TOKEN="your_telegram_bot_token_here"
   ```

3. **Install Dependencies**:
   ```bash
   pip install python-telegram-bot yt-dlp
   ```

4. **Run the Bot**:
   ```bash
   python main.py
   ```

## Project Structure

```
├── main.py              # Entry point for the bot
├── bot.py               # Main bot class with command handlers
├── config.py            # Configuration management
├── music_player.py      # Music playback functionality
├── youtube_downloader.py # YouTube search and download
├── queue_manager.py     # Queue management for multiple chats
├── downloads/           # Downloaded audio files (created automatically)
└── README.md           # This file
```

## Configuration Options

The bot can be configured using environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `BOT_TOKEN` | Required | Telegram Bot API token |
| `DOWNLOAD_DIR` | `./downloads` | Directory for downloaded audio files |
| `MAX_DOWNLOAD_SIZE` | `104857600` | Maximum file size (100MB) |
| `AUDIO_BITRATE` | `128k` | Audio quality for downloads |
| `AUDIO_FORMAT` | `mp3` | Audio format for downloads |
| `MAX_QUEUE_SIZE` | `20` | Maximum songs per queue |
| `FFMPEG_PATH` | `ffmpeg` | Path to FFmpeg executable |

## Usage Examples

### Basic Usage
1. Add the bot to your Telegram group
2. Start a voice chat in the group
3. Use commands to control music:
   ```
   /play never gonna give you up
   /pause
   /resume
   /queue
   /skip
   /stop
   ```

### Queue Management
- Songs are automatically queued when multiple `/play` commands are used
- Use `/queue` to see upcoming songs
- Use `/skip` to move to the next song
- Use `/stop` to clear the queue and stop playback

## Technical Details

### Architecture
- **Modular Design**: Separate components for bot logic, music player, YouTube integration, and queue management
- **Asynchronous Processing**: Uses asyncio for non-blocking operations
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Resource Management**: Automatic cleanup of temporary files and streams

### Voice Chat Integration
The current implementation includes a simulation mode for voice chat functionality. For production use with actual Telegram voice chats, additional setup would be required:

- Telegram API credentials (API_ID and API_HASH)
- Working voice chat library integration
- User session management

### Audio Processing
- Downloads audio from YouTube using yt-dlp
- Converts audio to specified format using FFmpeg
- Manages file storage with configurable size limits
- Automatic cleanup of old downloaded files

## Troubleshooting

### Common Issues

1. **Bot Token Error**:
   - Ensure BOT_TOKEN environment variable is set
   - Verify the token is correct from @BotFather

2. **YouTube Download Failures**:
   - Check internet connection
   - Ensure yt-dlp is installed and updated
   - Verify FFmpeg is available in PATH

3. **Permission Issues**:
   - Ensure the bot has necessary permissions in the group
   - Check file system permissions for download directory

### Logs
The bot provides detailed logging for troubleshooting:
- Startup and initialization messages
- Command processing logs
- Download progress and errors
- Playback status updates

## Development

### Adding New Features
The modular architecture makes it easy to extend functionality:

1. **New Commands**: Add handlers in `bot.py`
2. **Playback Features**: Extend `music_player.py`
3. **Audio Sources**: Modify `youtube_downloader.py`
4. **Queue Features**: Update `queue_manager.py`

### Testing
- Use demo mode when yt-dlp is not available
- Simulation mode for voice chat testing
- Comprehensive error handling for edge cases

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Disclaimer

This bot is for educational and personal use. Ensure you comply with YouTube's Terms of Service and applicable copyright laws when downloading content.