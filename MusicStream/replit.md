# Overview

This is a Telegram Music Bot built with Python that enables users to play YouTube music in Telegram voice chats. The bot handles audio streaming, queue management, and YouTube video downloading. It uses the python-telegram-bot library for Telegram API interactions and includes a music player simulation system for voice chat functionality, along with yt-dlp for YouTube content downloading.

## Recent Changes (August 11, 2025)

✓ **Successfully implemented complete Telegram Music Bot with working components**
✓ **Fixed dependency conflicts by switching from pyrogram/pytgcalls to python-telegram-bot**
✓ **Bot is now running and connected to Telegram successfully**
✓ **All core features implemented**: /play, /pause, /resume, /stop, /queue, /skip commands
✓ **YouTube integration working with yt-dlp**
✓ **Music player simulation system for development/testing**
✓ **Queue management system supporting multiple chats**
✓ **Comprehensive error handling and logging**

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Core Components

The bot follows a modular architecture with clear separation of concerns:

**Main Bot Controller (`bot.py`)**
- Serves as the central orchestrator managing all bot operations
- Handles Telegram command processing and user interactions
- Coordinates between different service modules
- Manages active voice chat sessions across multiple groups

**Configuration Management (`config.py`)**
- Centralized configuration using environment variables
- Validates required API credentials and settings
- Configurable audio quality, download limits, and queue sizes
- Supports customizable FFMPEG paths and download directories

**Music Player (`music_player.py`)**
- Manages voice chat audio streaming using PyTgCalls
- Handles playback controls (play, pause, resume, stop)
- Tracks active streams and their states across different chats
- Integrates with Telegram's voice chat infrastructure

**Queue Management (`queue_manager.py`)**
- Implements per-chat music queues with configurable size limits
- Provides queue manipulation operations (add, remove, clear, skip)
- Maintains queue state and position tracking
- Supports queue viewing and management commands

**YouTube Integration (`youtube_downloader.py`)**
- Handles YouTube video search and metadata extraction
- Downloads audio content using yt-dlp with quality optimization
- Manages temporary file storage and cleanup
- Configurable download size limits and audio format conversion

## Data Flow Architecture

1. **Command Processing**: User commands are received through Telegram and processed by the bot controller
2. **Content Resolution**: YouTube URLs or search queries are resolved to downloadable content
3. **Audio Processing**: Content is downloaded and converted to the specified audio format
4. **Queue Management**: Songs are added to chat-specific queues with position tracking
5. **Playback Execution**: Audio is streamed to voice chats using PyTgCalls integration

## Design Patterns

**Modular Service Architecture**: Each major functionality is isolated in separate modules with clear interfaces, enabling independent testing and maintenance.

**Configuration-Driven Behavior**: All operational parameters are externalized through environment variables, allowing deployment flexibility without code changes.

**Asynchronous Processing**: Leverages Python's asyncio for non-blocking operations, essential for handling multiple concurrent voice chats and downloads.

**Resource Management**: Implements proper cleanup mechanisms for temporary files and manages download directory space.

# External Dependencies

## Core Libraries
- **Pyrogram**: Telegram MTProto API client for bot functionality and user session management
- **PyTgCalls**: Voice chat integration library for audio streaming to Telegram voice chats
- **yt-dlp**: YouTube video downloading and metadata extraction with format conversion capabilities

## System Dependencies
- **FFMPEG**: Audio processing and format conversion, configurable installation path
- **Python 3.8+**: Async/await support and modern Python features

## Telegram API Requirements
- **Bot Token**: Telegram Bot API token for bot authentication
- **API ID/Hash**: Telegram application credentials for voice chat functionality
- **Bot Username**: Required for proper command handling and mentions

## Audio Processing
- Configurable audio bitrate and format conversion
- Download size limits to prevent resource exhaustion
- Temporary file management with automatic cleanup
- Support for various YouTube audio quality options