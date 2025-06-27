import os
import subprocess
import sys

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("✅ Requirements installed successfully!")

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("✅ PyInstaller is already installed!")
    except ImportError:
        print("📦 Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller installed successfully!")

def build_executable_antivirus_friendly():
    """Build the executable with antivirus-friendly options"""
    print("🔨 Building antivirus-friendly executable...")
    
    # PyInstaller command with antivirus-friendly options
    cmd = [
        "pyinstaller",
        "--onefile",  # Create a single executable file
        "--console",  # Show console window
        "--name=YouTube_Video_Downloader",  # Name of the executable
        "--clean",  # Clean cache before building
        "--strip",  # Strip debug symbols (reduces file size and suspicion)
        "--noupx",  # Don't use UPX compression (often flagged by antivirus)
        "--disable-windowed-traceback",  # Disable windowed traceback
        "--log-level=WARN",  # Reduce logging
        "--distpath=dist_clean",  # Different output directory
        "--workpath=build_clean",  # Different work directory
        "--specpath=.",  # Spec file location
        "main.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("✅ Antivirus-friendly executable built successfully!")
        print(f"📁 Executable location: {os.path.join('dist_clean', 'YouTube_Video_Downloader.exe')}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error building executable: {e}")
        return False

def create_installer_script():
    """Create a simple installer script instead of exe"""
    print("📝 Creating installer script...")
    
    installer_content = '''@echo off
echo Installing YouTube Video Downloader...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.7+ first.
    pause
    exit /b 1
)

REM Install requirements
echo Installing required packages...
pip install yt-dlp==2024.12.13 requests==2.31.0 tqdm==4.66.1

REM Run the application
echo.
echo Starting YouTube Video Downloader...
python main.py

pause
'''
    
    with open('run_downloader.bat', 'w') as f:
        f.write(installer_content)
    
    print("✅ Installer script created: run_downloader.bat")
    print("💡 Users can run this .bat file instead of the exe")

def main():
    """Main build function"""
    print("🚀 YouTube Video Downloader - Antivirus-Friendly Build")
    print("=" * 60)
    
    try:
        # Install requirements
        install_requirements()
        
        # Install PyInstaller
        install_pyinstaller()
        
        print("\n🔍 Choose build method:")
        print("1. Antivirus-friendly executable (may still trigger some AV)")
        print("2. Installer script (.bat file - safest option)")
        print("3. Both")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice in ['1', '3']:
            # Build executable
            if build_executable_antivirus_friendly():
                print("\n✅ Antivirus-friendly executable created!")
            else:
                print("\n❌ Executable build failed!")
        
        if choice in ['2', '3']:
            # Create installer script
            create_installer_script()
            print("\n✅ Installer script created!")
        
        print("\n📋 Next steps:")
        if choice in ['1', '3']:
            print("1. Navigate to the 'dist_clean' folder")
            print("2. Run 'YouTube_Video_Downloader.exe'")
        if choice in ['2', '3']:
            print("3. Or use 'run_downloader.bat' (safest option)")
        print("4. Follow the prompts to download YouTube videos")
        
        print("\n💡 Tips to avoid antivirus issues:")
        print("- Add the executable folder to antivirus exclusions")
        print("- Submit the file to McAfee for whitelisting")
        print("- Use the .bat file instead of .exe")
        print("- Run as administrator if needed")
            
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main() 