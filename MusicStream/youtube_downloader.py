"""
YouTube downloader using yt-dlp
"""

import asyncio
import logging
import os
import tempfile
from typing import Dict, Optional
try:
    import yt_dlp
except ImportError:
    yt_dlp = None
    logging.warning("yt-dlp not available - YouTube functionality will be limited")

from pathlib import Path
from config import Config

class YouTubeDownloader:
    """Handles YouTube search and download functionality"""
    
    def __init__(self):
        """Initialize YouTube downloader"""
        self.ydl_available = yt_dlp is not None
        
        if self.ydl_available:
            self.ydl_opts = {
                'format': 'bestaudio/best',
                'extractaudio': True,
                'audioformat': Config.AUDIO_FORMAT,
                'audioquality': Config.AUDIO_BITRATE,
                'outtmpl': os.path.join(Config.DOWNLOAD_DIR, '%(title)s.%(ext)s'),
                'noplaylist': True,
                'no_warnings': True,
                'quiet': True,
                'extractflat': False,
                'writethumbnail': False,
                'writeinfojson': False,
                'writedescription': False,
                'writesubtitles': False,
                'writeautomaticsub': False,
                'ignoreerrors': True,
                'max_filesize': Config.MAX_DOWNLOAD_SIZE,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': Config.AUDIO_FORMAT,
                    'preferredquality': Config.AUDIO_BITRATE.replace('k', ''),
                }],
                'ffmpeg_location': Config.FFMPEG_PATH,
            }
        else:
            self.ydl_opts = {}
        
        logging.info("YouTube downloader initialized")
    
    async def search_youtube(self, query: str, max_results: int = 1) -> Optional[Dict]:
        """
        Search for videos on YouTube
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            Dict with video info or None if not found
        """
        if not self.ydl_available:
            logging.error("yt-dlp not available for YouTube search")
            return self._create_demo_result(query)
        
        try:
            # Create search options
            search_opts = self.ydl_opts.copy()
            search_opts.update({
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,
                'default_search': 'ytsearch' + str(max_results),
            })
            
            with yt_dlp.YoutubeDL(search_opts) as ydl:
                # Search for the query
                search_results = await asyncio.get_event_loop().run_in_executor(
                    None, 
                    lambda: ydl.extract_info(f"ytsearch{max_results}:{query}", download=False)
                )
                
                if search_results and 'entries' in search_results and search_results['entries']:
                    # Return first result
                    result = search_results['entries'][0]
                    return {
                        'id': result.get('id'),
                        'title': result.get('title', 'Unknown Title'),
                        'url': result.get('url') or f"https://www.youtube.com/watch?v={result.get('id')}",
                        'duration': result.get('duration', 0),
                        'uploader': result.get('uploader', 'Unknown'),
                    }
                
                return None
                
        except Exception as e:
            logging.error(f"Error searching YouTube: {e}")
            return None
    
    def _create_demo_result(self, query: str) -> Dict:
        """Create a demo result when yt-dlp is not available"""
        return {
            'id': 'demo123',
            'title': f"Demo Song: {query}",
            'url': 'https://www.youtube.com/watch?v=demo123',
            'duration': 180,
            'uploader': 'Demo Channel',
        }
    
    async def download_audio(self, video_info: Dict) -> Optional[str]:
        """
        Download audio from YouTube video
        
        Args:
            video_info: Video information dict
            
        Returns:
            Path to downloaded file or None if failed
        """
        if not self.ydl_available:
            logging.warning("yt-dlp not available - creating demo audio file")
            return self._create_demo_audio_file(video_info)
        
        try:
            # Sanitize filename
            safe_title = self._sanitize_filename(video_info['title'])
            output_path = os.path.join(Config.DOWNLOAD_DIR, f"{safe_title}.{Config.AUDIO_FORMAT}")
            
            # Check if file already exists
            if os.path.exists(output_path):
                logging.info(f"File already exists: {output_path}")
                return output_path
            
            # Download options
            download_opts = self.ydl_opts.copy()
            download_opts['outtmpl'] = os.path.join(Config.DOWNLOAD_DIR, f"{safe_title}.%(ext)s")
            
            with yt_dlp.YoutubeDL(download_opts) as ydl:
                # Download the video
                await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: ydl.download([video_info['url']])
                )
                
                # Check if file was created
                if os.path.exists(output_path):
                    logging.info(f"Successfully downloaded: {output_path}")
                    return output_path
                else:
                    # Try to find the downloaded file with different extension
                    base_path = os.path.join(Config.DOWNLOAD_DIR, safe_title)
                    for ext in ['mp3', 'm4a', 'webm', 'ogg']:
                        test_path = f"{base_path}.{ext}"
                        if os.path.exists(test_path):
                            # Rename to expected format if needed
                            if ext != Config.AUDIO_FORMAT:
                                os.rename(test_path, output_path)
                            return output_path
                    
                    logging.error("Downloaded file not found")
                    return None
                    
        except Exception as e:
            logging.error(f"Error downloading audio: {e}")
            return None
    
    def _create_demo_audio_file(self, video_info: Dict) -> str:
        """Create a demo audio file when yt-dlp is not available"""
        try:
            safe_title = self._sanitize_filename(video_info['title'])
            output_path = os.path.join(Config.DOWNLOAD_DIR, f"{safe_title}.{Config.AUDIO_FORMAT}")
            
            # Create a short silence audio file as demo
            # This would normally be the downloaded audio
            if not os.path.exists(output_path):
                try:
                    # Try to create a short silence audio file using ffmpeg
                    import subprocess
                    subprocess.run([
                        'ffmpeg', '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100',
                        '-t', '10', '-y', output_path
                    ], capture_output=True, timeout=30)
                    
                    if os.path.exists(output_path):
                        logging.info(f"Created demo audio file: {output_path}")
                        return output_path
                        
                except Exception as e:
                    logging.warning(f"Could not create demo audio with ffmpeg: {e}")
                
                # Fallback: create a simple text file as placeholder
                with open(output_path + ".txt", 'w') as f:
                    f.write(f"Demo audio file for: {video_info['title']}\n")
                    f.write("This is a placeholder. In production, this would be the actual audio file.\n")
                
                return output_path + ".txt"
            
            return output_path
            
        except Exception as e:
            logging.error(f"Error creating demo audio file: {e}")
            return None
    
    async def search_and_download(self, query: str) -> Optional[Dict]:
        """
        Search for a song and download it
        
        Args:
            query: Search query
            
        Returns:
            Dict with song info and file path or None if failed
        """
        try:
            # Search for the song
            video_info = await self.search_youtube(query)
            
            if not video_info:
                logging.warning(f"No results found for: {query}")
                return None
            
            # Download the audio
            file_path = await self.download_audio(video_info)
            
            if not file_path:
                logging.error(f"Failed to download: {video_info['title']}")
                return None
            
            return {
                'title': video_info['title'],
                'url': video_info['url'],
                'file_path': file_path,
                'duration': video_info.get('duration', 0),
                'uploader': video_info.get('uploader', 'Unknown'),
            }
            
        except Exception as e:
            logging.error(f"Error in search_and_download: {e}")
            return None
    
    def _sanitize_filename(self, filename: str) -> str:
        """
        Sanitize filename for safe file system usage
        
        Args:
            filename: Original filename
            
        Returns:
            Sanitized filename
        """
        # Remove or replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # Limit length
        if len(filename) > 100:
            filename = filename[:100]
        
        # Remove leading/trailing spaces and dots
        filename = filename.strip(' .')
        
        return filename or "unknown_song"
    
    def cleanup_old_files(self, max_age_hours: int = 24):
        """
        Clean up old downloaded files
        
        Args:
            max_age_hours: Maximum age of files to keep in hours
        """
        try:
            import time
            current_time = time.time()
            max_age_seconds = max_age_hours * 3600
            
            for filename in os.listdir(Config.DOWNLOAD_DIR):
                file_path = os.path.join(Config.DOWNLOAD_DIR, filename)
                
                if os.path.isfile(file_path):
                    file_age = current_time - os.path.getmtime(file_path)
                    
                    if file_age > max_age_seconds:
                        try:
                            os.remove(file_path)
                            logging.info(f"Cleaned up old file: {filename}")
                        except Exception as e:
                            logging.error(f"Error removing file {filename}: {e}")
                            
        except Exception as e:
            logging.error(f"Error during cleanup: {e}")