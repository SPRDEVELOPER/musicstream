"""
Main bot class with command handlers using python-telegram-bot
"""

import asyncio
import logging
import os
from typing import Dict, Optional

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from config import Config
from music_player import MusicPlayer
from youtube_downloader import YouTubeDownloader
from queue_manager import QueueManager

class MusicBot:
    """Main Telegram Music Bot class"""
    
    def __init__(self):
        """Initialize the bot"""
        # Validate configuration
        Config.validate()
        
        # Initialize application
        self.application = Application.builder().token(Config.BOT_TOKEN).build()
        
        # Initialize components
        self.music_player = MusicPlayer()
        self.youtube_downloader = YouTubeDownloader()
        self.queue_manager = QueueManager()
        
        # Track active voice chats
        self.active_chats: Dict[int, bool] = {}
        
        # Setup handlers
        self._setup_handlers()
        
        # Create download directory
        os.makedirs(Config.DOWNLOAD_DIR, exist_ok=True)
        
        logging.info("Music bot initialized successfully")
    
    def _setup_handlers(self):
        """Setup command handlers"""
        
        async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            """Handle /start command"""
            welcome_text = (
                "🎵 **Welcome to the Music Bot!** 🎵\n\n"
                "**Available Commands:**\n"
                "• `/play <song_name>` - Search and play music from YouTube\n"
                "• `/pause` - Pause the current song\n"
                "• `/resume` - Resume playback\n"
                "• `/stop` - Stop music and leave voice chat\n"
                "• `/queue` - Show the current queue\n"
                "• `/skip` - Skip the current song\n"
                "• `/help` - Show this help message\n\n"
                "**Note:** Add me to a group and use these commands in voice chat!"
            )
            await update.message.reply_text(welcome_text, parse_mode='Markdown')
        
        async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            """Handle /help command"""
            await start_command(update, context)
        
        async def play_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            """Handle /play command"""
            chat_id = update.effective_chat.id
            
            try:
                # Extract song name from command
                if not context.args:
                    await update.message.reply_text("❌ Please provide a song name!\nUsage: `/play <song_name>`")
                    return
                
                song_name = " ".join(context.args)
                
                # Send searching message
                search_msg = await update.message.reply_text(f"🔍 Searching for: **{song_name}**...", parse_mode='Markdown')
                
                # Search and download from YouTube
                result = await self.youtube_downloader.search_and_download(song_name)
                
                if not result:
                    await search_msg.edit_text("❌ No results found for your search!")
                    return
                
                # Add to queue
                queue_position = self.queue_manager.add_to_queue(chat_id, result)
                
                if queue_position == 1:
                    # Start playing immediately
                    await search_msg.edit_text(f"🎵 **Now Playing:** {result['title']}", parse_mode='Markdown')
                    success = await self.music_player.play_audio(chat_id, result['file_path'])
                    
                    if not success:
                        await update.message.reply_text("❌ Failed to join voice chat! Make sure the bot has permission to join voice chats.")
                        self.queue_manager.remove_from_queue(chat_id, result)
                else:
                    await search_msg.edit_text(f"✅ **Added to queue (#{queue_position}):** {result['title']}", parse_mode='Markdown')
                
            except Exception as e:
                logging.error(f"Error in play command: {e}")
                await update.message.reply_text("❌ An error occurred while processing your request!")
        
        async def pause_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            """Handle /pause command"""
            chat_id = update.effective_chat.id
            
            if await self.music_player.pause_audio(chat_id):
                await update.message.reply_text("⏸️ **Paused** the current song", parse_mode='Markdown')
            else:
                await update.message.reply_text("❌ No active playback to pause!")
        
        async def resume_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            """Handle /resume command"""
            chat_id = update.effective_chat.id
            
            if await self.music_player.resume_audio(chat_id):
                await update.message.reply_text("▶️ **Resumed** playback", parse_mode='Markdown')
            else:
                await update.message.reply_text("❌ No paused playback to resume!")
        
        async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            """Handle /stop command"""
            chat_id = update.effective_chat.id
            
            # Stop music and leave voice chat
            await self.music_player.stop_audio(chat_id)
            
            # Clear queue
            self.queue_manager.clear_queue(chat_id)
            
            await update.message.reply_text("🛑 **Stopped** music and left voice chat", parse_mode='Markdown')
        
        async def skip_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            """Handle /skip command"""
            chat_id = update.effective_chat.id
            
            current_song = self.queue_manager.get_current_song(chat_id)
            if not current_song:
                await update.message.reply_text("❌ No song is currently playing!")
                return
            
            # Remove current song and get next
            self.queue_manager.remove_from_queue(chat_id, current_song)
            next_song = self.queue_manager.get_current_song(chat_id)
            
            if next_song:
                await update.message.reply_text(f"⏭️ **Skipped!** Now playing: {next_song['title']}", parse_mode='Markdown')
                await self.music_player.play_audio(chat_id, next_song['file_path'])
            else:
                await self.music_player.stop_audio(chat_id)
                await update.message.reply_text("⏭️ **Skipped!** No more songs in queue")
        
        async def queue_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            """Handle /queue command"""
            chat_id = update.effective_chat.id
            
            queue_list = self.queue_manager.get_queue(chat_id)
            
            if not queue_list:
                await update.message.reply_text("📝 **Queue is empty!**", parse_mode='Markdown')
                return
            
            queue_text = "📝 **Current Queue:**\n\n"
            for i, song in enumerate(queue_list, 1):
                status = "🎵 " if i == 1 else f"{i}. "
                queue_text += f"{status}**{song['title']}**\n"
                
                if i >= 10:  # Limit display to 10 songs
                    remaining = len(queue_list) - 10
                    if remaining > 0:
                        queue_text += f"\n... and {remaining} more songs"
                    break
            
            await update.message.reply_text(queue_text, parse_mode='Markdown')
        
        # Add handlers to application
        self.application.add_handler(CommandHandler("start", start_command))
        self.application.add_handler(CommandHandler("help", help_command))
        self.application.add_handler(CommandHandler("play", play_command))
        self.application.add_handler(CommandHandler("pause", pause_command))
        self.application.add_handler(CommandHandler("resume", resume_command))
        self.application.add_handler(CommandHandler("stop", stop_command))
        self.application.add_handler(CommandHandler("skip", skip_command))
        self.application.add_handler(CommandHandler("queue", queue_command))
    
    async def _handle_song_finished(self, chat_id: int):
        """Handle when a song finishes playing"""
        # Remove current song from queue
        current_song = self.queue_manager.get_current_song(chat_id)
        if current_song:
            self.queue_manager.remove_from_queue(chat_id, current_song)
        
        # Play next song if available
        next_song = self.queue_manager.get_current_song(chat_id)
        if next_song:
            await self.music_player.play_audio(chat_id, next_song['file_path'])
        else:
            # No more songs, leave voice chat
            await self.music_player.stop_audio(chat_id)
    
    def run(self):
        """Run the bot"""
        logging.info("Starting Music Bot...")
        self.application.run_polling()