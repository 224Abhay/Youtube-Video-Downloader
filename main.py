import os
import sys
import re
import subprocess
import zipfile
import urllib.request
import tempfile
from urllib.parse import urlparse
import requests
import yt_dlp
import threading
import time
from tqdm import tqdm
import json

# --- User data directory for ffmpeg ---
def get_userdata_ffmpeg_dir():
    if sys.platform == 'win32':
        base = os.environ.get('LOCALAPPDATA') or os.environ.get('APPDATA')
        if not base:
            base = os.path.expanduser('~')
        return os.path.join(base, 'YouTubeDownloader', 'ffmpeg')
    else:
        # For Linux/Mac
        return os.path.expanduser('~/.local/share/YouTubeDownloader/ffmpeg')

def check_ffmpeg():
    """Check if our downloaded FFmpeg is available"""
    # Only check for our downloaded FFmpeg, not system PATH
    local_ffmpeg = os.path.join(get_userdata_ffmpeg_dir(), 'ffmpeg.exe')
    if os.path.exists(local_ffmpeg):
        try:
            result = subprocess.run([local_ffmpeg, '-version'], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            return False
    return False

def download_ffmpeg():
    """Download and install FFmpeg for Windows with progress bar (to user data dir)"""
    print("🔧 FFmpeg not found. Downloading and installing FFmpeg...")
    try:
        ffmpeg_dir = get_userdata_ffmpeg_dir()
        os.makedirs(ffmpeg_dir, exist_ok=True)
        
        # Try multiple FFmpeg download URLs (more reliable)
        ffmpeg_urls = [
            "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip",
            "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip",
            "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl-shared.zip"
        ]
        
        temp_file = None
        successful_download = False
        
        for url_index, ffmpeg_url in enumerate(ffmpeg_urls, 1):
            try:
                print(f"📥 Attempting download from source {url_index}/{len(ffmpeg_urls)}...")
                
                # Get file size for progress bar
                with urllib.request.urlopen(ffmpeg_url) as response:
                    file_size = int(response.headers.get('content-length', 0))
                
                # Download FFmpeg with progress bar
                temp_file = tempfile.NamedTemporaryFile(suffix='.zip', delete=False)
                
                with urllib.request.urlopen(ffmpeg_url) as response:
                    with tqdm(total=file_size, unit='B', unit_scale=True, 
                             desc=f"Downloading FFmpeg (Source {url_index})", ncols=80) as pbar:
                        while True:
                            chunk = response.read(8192)  # 8KB chunks
                            if not chunk:
                                break
                            temp_file.write(chunk)
                            pbar.update(len(chunk))
                
                temp_file.close()
                
                # Verify it's actually a zip file
                try:
                    with zipfile.ZipFile(temp_file.name, 'r') as test_zip:
                        # Try to read the file list to verify it's valid
                        test_zip.namelist()
                    successful_download = True
                    print(f"✅ Successfully downloaded from source {url_index}")
                    break
                except zipfile.BadZipFile:
                    print(f"❌ Source {url_index} failed - not a valid zip file")
                    os.unlink(temp_file.name)
                    temp_file = None
                    continue
                    
            except Exception as e:
                print(f"❌ Source {url_index} failed: {str(e)}")
                if temp_file:
                    os.unlink(temp_file.name)
                    temp_file = None
                continue
        
        if not successful_download or not temp_file:
            raise Exception("All download sources failed")
        
        print("📦 Extracting FFmpeg...")
        
        # Extract the zip file
        with zipfile.ZipFile(temp_file.name, 'r') as zip_ref:
            file_list = zip_ref.namelist()
            with tqdm(total=len(file_list), desc="Extracting FFmpeg", ncols=80) as pbar:
                for file in file_list:
                    zip_ref.extract(file, ffmpeg_dir)
                    pbar.update(1)
        
        # Clean up temp file
        os.unlink(temp_file.name)
        
        # Find the extracted folder (it has a random name)
        extracted_folders = [f for f in os.listdir(ffmpeg_dir) 
                           if os.path.isdir(os.path.join(ffmpeg_dir, f))]
        
        if not extracted_folders:
            raise Exception("Could not find extracted FFmpeg folder")
        
        # Look for ffmpeg.exe in various possible locations
        possible_ffmpeg_paths = []
        for folder in extracted_folders:
            source_folder = os.path.join(ffmpeg_dir, folder)
            possible_paths = [
                os.path.join(source_folder, 'bin', 'ffmpeg.exe'),
                os.path.join(source_folder, 'ffmpeg.exe'),
                os.path.join(source_folder, 'bin', 'ffmpeg', 'ffmpeg.exe')
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    possible_ffmpeg_paths.append((path, source_folder))
        
        if not possible_ffmpeg_paths:
            raise Exception("FFmpeg executable not found in downloaded files")
        
        # Use the first found ffmpeg.exe
        ffmpeg_exe_path, source_folder = possible_ffmpeg_paths[0]
        
        # Copy ffmpeg.exe to the main directory
        import shutil
        final_ffmpeg_path = os.path.join(ffmpeg_dir, 'ffmpeg.exe')
        shutil.copy2(ffmpeg_exe_path, final_ffmpeg_path)
        
        # Clean up extracted folder
        shutil.rmtree(source_folder)
        
        print("✅ FFmpeg installed successfully!")
        return final_ffmpeg_path
        
    except Exception as e:
        print(f"❌ Failed to download FFmpeg: {str(e)}")
        # Clean up any partial downloads
        if 'temp_file' in locals() and temp_file and os.path.exists(temp_file.name):
            try:
                os.unlink(temp_file.name)
            except:
                pass
        return None

def get_ffmpeg_path():
    """Get FFmpeg path, download if not available (user data dir only)"""
    # First check if our downloaded FFmpeg exists
    local_ffmpeg = os.path.join(get_userdata_ffmpeg_dir(), 'ffmpeg.exe')
    if os.path.exists(local_ffmpeg):
        return local_ffmpeg
    
    # Download FFmpeg if not found
    ffmpeg_path = download_ffmpeg()
    if ffmpeg_path:
        return ffmpeg_path
    
    return None

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Print the application banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    YouTube Video Downloader                  ║
    ║                        Made by Abhay                         ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def is_valid_youtube_url(url):
    """Check if the URL is a valid YouTube URL"""
    youtube_patterns = [
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=[\w-]+',
        r'(?:https?://)?(?:www\.)?youtu\.be/[\w-]+',
        r'(?:https?://)?(?:www\.)?youtube\.com/embed/[\w-]+',
        r'(?:https?://)?(?:www\.)?youtube\.com/v/[\w-]+'
    ]
    
    for pattern in youtube_patterns:
        if re.match(pattern, url):
            return True
    return False

def get_video_info(url):
    """Get video information from YouTube URL"""
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info
    except Exception as e:
        print(f"❌ Error getting video info: {str(e)}")
        return None

def display_video_info(info):
    """Display video information"""
    print(f"\n📹 Video Title: {info.get('title', 'Unknown')}")
    print(f"👤 Channel: {info.get('uploader', 'Unknown')}")
    
    # Format duration
    duration = info.get('duration', 0)
    if duration:
        minutes = duration // 60
        seconds = duration % 60
        print(f"⏱️  Duration: {minutes}:{seconds:02d}")
    
    print(f"👁️  Views: {info.get('view_count', 'Unknown'):,}" if info.get('view_count') else "👁️  Views: Unknown")
    print(f"📅 Upload Date: {info.get('upload_date', 'Unknown')}")
    print("-" * 60)

def get_best_video_format(info, preferred_quality="1080p"):
    """Get the best available video format up to preferred quality"""
    formats = []
    if 'formats' not in info:
        print("❌ No formats available for this video.")
        return None
    for fmt in info['formats']:
        if (fmt.get('vcodec') != 'none' and 
            fmt.get('acodec') == 'none' and 
            fmt.get('height') is not None):
            format_info = {
                'format_id': fmt.get('format_id', 'Unknown'),
                'ext': fmt.get('ext', 'Unknown'),
                'filesize': fmt.get('filesize'),
                'format_note': fmt.get('format_note', ''),
                'height': fmt.get('height'),
                'width': fmt.get('width'),
                'fps': fmt.get('fps'),
                'vcodec': fmt.get('vcodec'),
                'format': fmt
            }
            formats.append(format_info)
    if not formats:
        print("❌ No video-only formats found for this video.")
        return None
    formats.sort(key=lambda x: (-(x['height'] or 0), -(x['fps'] or 0)))
    quality_map = {
        "4k": 2160,
        "2k": 1440,
        "1080p": 1080,
        "720p": 720
    }
    target_height = quality_map.get(preferred_quality, 1080)
    target_fps = 60
    for fmt in formats:
        height = fmt['height'] or 0
        fps = fmt['fps'] or 0
        if height <= target_height and fps <= target_fps:
            return fmt
    return formats[0]

def display_selected_format(format_info):
    """Display the selected video format"""
    print(f"\n📋 Selected Quality:")
    print(f"   Resolution: {format_info['height']}p")
    print(f"   FPS: {format_info['fps'] or 'Unknown'}")
    print(f"   Size: {format_info['filesize'] / (1024*1024):.1f} MB" if format_info['filesize'] else "   Size: Unknown")
    print("💡 Audio will be automatically downloaded and merged with your selected video quality.")

def download_video_with_audio(url, format_id, output_path, filename):
    """Download video with automatic audio merge"""
    try:
        print(f"\n🚀 Starting download: {filename}")
        print("📹 Downloading video and audio, then merging...")
        
        # Create output directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)
        
        # Get FFmpeg path
        ffmpeg_path = get_ffmpeg_path()
        if not ffmpeg_path:
            print("❌ FFmpeg is required but could not be installed. Please install FFmpeg manually.")
            return
        
        # Configure yt-dlp options for video + audio merge with AAC audio
        ydl_opts = {
            'format': f'{format_id}+bestaudio[ext=m4a]/bestaudio[ext=aac]/bestaudio/best',  # Video + best AAC audio
            'outtmpl': os.path.join(output_path, filename),
            'progress_hooks': [progress_hook],
            'merge_output_format': 'mp4',  # Force MP4 output
            'ffmpeg_location': ffmpeg_path,  # Use our FFmpeg
            # Force audio codec to AAC for better compatibility
            'postprocessor_args': [
                '-c:v', 'copy',  # Copy video stream without re-encoding
                '-c:a', 'aac',   # Convert audio to AAC
                '-b:a', '192k',  # Audio bitrate
                '-ar', '44100',  # Audio sample rate
            ],
        }
        
        # Download the video with audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        print("\n✅ Download completed successfully!")
        print(f"📁 File saved to: {os.path.join(output_path, filename)}")
        print("🔊 Audio converted to AAC format for better compatibility")
        
    except Exception as e:
        print(f"\n❌ Download failed: {str(e)}")
        # Try fallback method without audio conversion
        print("🔄 Trying fallback method...")
        try:
            fallback_ydl_opts = {
                'format': f'{format_id}+bestaudio/best',  # Simple format selection
                'outtmpl': os.path.join(output_path, filename),
                'progress_hooks': [progress_hook],
                'merge_output_format': 'mp4',
                'ffmpeg_location': ffmpeg_path,
            }
            
            with yt_dlp.YoutubeDL(fallback_ydl_opts) as ydl:
                ydl.download([url])
            
            print("\n✅ Download completed with fallback method!")
            print(f"📁 File saved to: {os.path.join(output_path, filename)}")
            
        except Exception as fallback_error:
            print(f"\n❌ Fallback method also failed: {str(fallback_error)}")

def progress_hook(d):
    """Progress hook for download tracking"""
    if d['status'] == 'downloading':
        if 'total_bytes' in d and d['total_bytes']:
            percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
            print(f"\r📊 Progress: {percent:.1f}%", end='', flush=True)
    elif d['status'] == 'finished':
        print("\n✅ Download finished!")
    elif d['status'] == 'postprocess':
        print("\n🔧 Merging video and audio...")

def format_filename(title):
    """Format filename by removing invalid characters"""
    # Remove invalid characters for filename
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        title = title.replace(char, '')
    
    # Limit length
    if len(title) > 100:
        title = title[:100]
    
    return title.strip()

# --- Config file helpers ---
def get_userdata_config_dir():
    if sys.platform == 'win32':
        base = os.environ.get('LOCALAPPDATA') or os.environ.get('APPDATA')
        if not base:
            base = os.path.expanduser('~')
        return os.path.join(base, 'YouTubeDownloader')
    else:
        return os.path.expanduser('~/.local/share/YouTubeDownloader')

def get_config_path():
    return os.path.join(get_userdata_config_dir(), 'config.json')

def load_config():
    config_path = get_config_path()
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    # Default config
    return {"quality": "1080p"}

def save_config(config):
    config_dir = get_userdata_config_dir()
    os.makedirs(config_dir, exist_ok=True)
    config_path = get_config_path()
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)

def settings_menu():
    config = load_config()
    valid_qualities = ['4k', '2k', '1080p', '720p']
    current_quality = config.get('quality', '1080p')
    if current_quality not in valid_qualities:
        current_quality = '1080p'
    while True:
        print("\n===== Settings =====")
        print(f"1. Preferred Quality: {current_quality}")
        print("2. Back to downloader")
        choice = input("Select an option: ").strip()
        if choice == '1':
            print("\nSelect preferred video quality:")
            print("1. 4K (2160p)")
            print("2. 2K (1440p)")
            print("3. 1080p")
            print("4. 720p")
            q_choice = input("Enter choice (1-4): ").strip()
            q_map = {
                '1': '4k',
                '2': '2k',
                '3': '1080p',
                '4': '720p'
            }
            if q_choice in q_map:
                config['quality'] = q_map[q_choice]
                save_config(config)
                current_quality = q_map[q_choice]
                print(f"✅ Preferred quality set to {q_map[q_choice]}")
            else:
                print("❌ Invalid choice.")
        elif choice == '2':
            break
        else:
            print("❌ Invalid option.")

def main():
    clear_screen()
    print_banner()
    print("🔍 Checking for FFmpeg...")
    ffmpeg_path = get_ffmpeg_path()
    if ffmpeg_path:
        print("✅ FFmpeg is ready!")
    else:
        print("❌ FFmpeg installation failed. The application may not work properly.")
    print("\n" + "="*60)
    while True:
        try:
            print("\n🔗 Please enter a YouTube video URL:")
            print("   (type 'settings' to change quality, or 'quit' to exit)")
            url = input("   URL: ").strip()
            if url.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Thank you for using YouTube Video Downloader!")
                break
            if url.lower() == 'settings':
                settings_menu()
                clear_screen()
                print_banner()
                continue
            if not url:
                print("❌ Please enter a valid URL.")
                continue
            if not is_valid_youtube_url(url):
                print("❌ Invalid YouTube URL. Please enter a valid YouTube video URL.")
                continue
            print("\n⏳ Fetching video information...")
            info = get_video_info(url)
            if not info:
                continue
            display_video_info(info)
            config = load_config()
            preferred_quality = config.get('quality', '1080p')
            selected_format = get_best_video_format(info, preferred_quality)
            if not selected_format:
                continue
            display_selected_format(selected_format)
            output_dir = os.getcwd()
            base_filename = format_filename(info.get('title', 'video'))
            filename = f"{base_filename}.mp4"
            download_video_with_audio(url, selected_format['format_id'], output_dir, filename)
            clear_screen()
            print_banner()
        except KeyboardInterrupt:
            print("\n\n👋 Download cancelled. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {str(e)}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
