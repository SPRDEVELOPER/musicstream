"""
Configuration file for the Telegram Music Bot
"""

import os
from typing import Optional

class Config:
    """Configuration class for bot settings"""
    
    # Telegram Bot Token (required)
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "8414407217:AAExvbwiJ-LVcWRWija8rzNGZElwdLH-FM8")
    
    # Telegram API credentials for voice chat functionality
    API_ID: int = int(os.getenv("API_ID", "10210894"))
    API_HASH: str = os.getenv("API_HASH", "431fb206f0c1daad9eef06fa1d6a998f")
    
    # Bot username (without @)
    BOT_USERNAME: str = os.getenv("BOT_USERNAME", "@SPR_COMRADE_BOT")
    
    # Download settings
    DOWNLOAD_DIR: str = os.getenv("DOWNLOAD_DIR", "./downloads")
    MAX_DOWNLOAD_SIZE: int = int(os.getenv("MAX_DOWNLOAD_SIZE", "104857600"))  # 100MB
    
    # Audio settings
    AUDIO_BITRATE: str = os.getenv("AUDIO_BITRATE", "128k")
    AUDIO_FORMAT: str = os.getenv("AUDIO_FORMAT", "mp3")
    
    # Queue settings
    MAX_QUEUE_SIZE: int = int(os.getenv("MAX_QUEUE_SIZE", "20"))
    
    # FFMPEG path
    FFMPEG_PATH: str = os.getenv("FFMPEG_PATH", "ffmpeg")
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration"""
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN is required")
        # Note: API_ID, API_HASH, and BOT_USERNAME are optional for basic functionality
        # They would be required for actual voice chat integration
        return True
