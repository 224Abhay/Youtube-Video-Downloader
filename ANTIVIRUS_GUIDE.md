# Antivirus False Positive Guide

## Why This Happens

PyInstaller executables are often flagged by antivirus software because:
- They contain Python interpreter code
- They can dynamically load libraries
- Some malware uses similar packaging methods

**This is a FALSE POSITIVE** - our application is completely safe!

## Solutions

### Option 1: Use the .bat File (Recommended)
1. Use `run_downloader.bat` instead of the .exe
2. This runs the Python script directly
3. No antivirus issues

### Option 2: Add to Antivirus Exclusions

#### For McAfee:
1. Open McAfee Security Center
2. Go to "Settings" → "Real-Time Scanning"
3. Click "Excluded Files and Folders"
4. Add the folder containing the executable
5. Or add the specific .exe file

#### For Windows Defender:
1. Open Windows Security
2. Go to "Virus & threat protection"
3. Click "Manage settings"
4. Under "Exclusions", click "Add or remove exclusions"
5. Add the folder or file

### Option 3: Submit for Whitelisting
1. Go to McAfee's website
2. Submit the file for review
3. They will whitelist it within a few days

### Option 4: Run as Administrator
1. Right-click the executable
2. Select "Run as administrator"
3. This sometimes bypasses restrictions

## Alternative: Use Python Directly
If you have Python installed:
```bash
pip install yt-dlp requests tqdm
python main.py
```

## Safety Guarantee
- ✅ Open source code
- ✅ No malicious code
- ✅ Only downloads from YouTube
- ✅ No data collection
- ✅ No network access except YouTube

## Contact
If you continue having issues, please contact us for support. 