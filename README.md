# YouTube Video Downloader

A powerful and user-friendly YouTube video downloader application built with Python. This application allows you to download YouTube videos in various qualities and formats with automatic FFmpeg installation.

## 🎯 Features

- 🎯 **Easy to Use**: Simple command-line interface with clear prompts
- 📹 **High Quality**: Download videos up to 1080p 60fps
- 🎵 **Audio Merge**: Automatically download and merge audio with video
- 📊 **Video Information**: Display video details before downloading
- 📁 **Smart Output**: Downloads to current directory automatically
- 🔄 **Batch Downloads**: Download multiple videos in one session
- ✅ **Error Handling**: Robust error handling and validation
- 🔧 **Auto FFmpeg**: Automatically downloads and installs FFmpeg
- 🛡️ **Antivirus Friendly**: Built with antivirus-friendly options
- 🚀 **No Confirmation**: Streamlined download process
- ⚙️ **Settings Menu**: Change preferred video quality (4K, 2K, 1080p, 720p) from within the app

## 📋 Requirements

- Python 3.7 or higher
- Windows 10/11 (for executable)
- Internet connection
- No manual FFmpeg installation required (auto-downloaded)

## 🚀 Installation

### Option 1: Run from Source Code (Recommended for Developers)

1. **Clone this repository:**
   ```bash
   git clone https://github.com/yourusername/youtube-video-downloader.git
   cd youtube-video-downloader
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

### Option 2: Create Executable (Recommended for End Users)

1. **Run the build script:**
   ```bash
   python build_exe_alternative.py
   ```

2. **Choose build method:**
   - Option 1: Antivirus-friendly executable
   - Option 2: Installer script (.bat file - safest)
   - Option 3: Both

3. **Find your executable:**
   - Navigate to the `dist_clean` folder
   - Run `YouTube_Video_Downloader.exe`

## 📖 Usage

1. **Launch the application**
2. **Enter a YouTube URL** when prompted
3. **Review video information** (title, duration, views, etc.)
4. **Wait for automatic download** - no quality selection needed
5. **Find your video** in the current directory

### ⚙️ Settings Menu (Change Preferred Quality)

- At any prompt, type `settings` and press Enter.
- The settings menu will appear, allowing you to select your preferred video quality:
  - 4K (2160p)
  - 2K (1440p)
  - 1080p
  - 720p
- Your choice will be saved and used for future downloads.
- Type `2` in the settings menu to return to the downloader.

### Supported URL Formats

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`
- `https://www.youtube.com/v/VIDEO_ID`

### Download Features

- **Automatic Quality Selection**: Best quality up to 1080p 60fps
- **Audio Merge**: Automatically downloads and merges audio
- **AAC Audio**: Converts audio to AAC for better compatibility
- **MP4 Output**: All videos are saved as MP4 format
- **Smart Naming**: Automatic filename generation from video title

## 🔧 Technical Details

### FFmpeg Installation

The application automatically:
- Downloads FFmpeg to user data directory
- Installs it to `%LOCALAPPDATA%/YouTubeDownloader/ffmpeg/` (Windows)
- Uses only the downloaded FFmpeg (ignores system PATH)
- Handles all video/audio merging automatically

### Dependencies

- **yt-dlp**: YouTube video downloading engine
- **requests**: HTTP library for downloads
- **tqdm**: Progress bars for downloads
- **FFmpeg**: Auto-downloaded for video processing

## 🛡️ Antivirus Solutions

If your antivirus flags the executable:

### Option 1: Use .bat File (Safest)
- Use `run_downloader.bat` instead of .exe
- Runs Python script directly
- No antivirus issues

### Option 2: Add to Exclusions
- Add the executable folder to antivirus exclusions
- See `ANTIVIRUS_GUIDE.md` for detailed instructions

### Option 3: Submit for Whitelisting
- Submit the file to your antivirus vendor for review
- Usually whitelisted within a few days

## 🐛 Troubleshooting

### Common Issues

1. **"FFmpeg not found" error:**
   - The app will automatically download FFmpeg
   - Wait for the download to complete

2. **Download fails:**
   - Check your internet connection
   - Try a different YouTube URL
   - Ensure the video is not age-restricted

3. **Antivirus blocks the app:**
   - Use the .bat file instead
   - Add to antivirus exclusions
   - Run as administrator

4. **"nsig extraction failed" warning:**
   - This is normal and doesn't affect functionality
   - YouTube occasionally changes their system

### Error Messages

- **"ERROR: You have requested merging of multiple formats but ffmpeg is not installed"**
  - The app will automatically download FFmpeg
  - Wait for the installation to complete

- **"WARNING: ffmpeg-location ffmpeg does not exist!"**
  - The app will automatically download FFmpeg
  - This is expected behavior

## 📁 Project Structure

```
youtube-video-downloader/
├── main.py                      # Main application
├── build_exe.py                 # Original build script
├── build_exe_alternative.py     # Antivirus-friendly build script
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── ANTIVIRUS_GUIDE.md          # Antivirus troubleshooting guide
├── .gitignore                   # Git ignore rules
├── dist_clean/                  # Built executables
└── build_clean/                 # Build cache
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational purposes only. Please respect YouTube's Terms of Service and only download videos you have permission to download. The developers are not responsible for any misuse of this software.

## 🙏 Acknowledgments

- **yt-dlp**: The powerful YouTube downloading engine
- **FFmpeg**: Video processing and merging
- **Python community**: For the excellent libraries used

## 📞 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Look at the `ANTIVIRUS_GUIDE.md` for antivirus issues
3. Open an issue on GitHub with detailed information

---

**Made with ❤️ by Abhay** 