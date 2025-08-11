#!/usr/bin/env python3
"""
Main entry point for the Telegram Music Bot
"""

import asyncio
import logging
from bot import MusicBot

def main():
    """Main function to start the bot"""
    # Configure logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    
    # Create and run the bot
    bot = MusicBot()
    
    try:
        bot.run()
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
    except Exception as e:
        logging.error(f"Bot crashed with error: {e}")

if __name__ == "__main__":
    main()
