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

def build_executable():
    """Build the executable using PyInstaller"""
    print("🔨 Building executable...")
    
    # PyInstaller command with options
    cmd = [
        "pyinstaller",
        "--onefile",  # Create a single executable file
        "--console",  # Show console window
        "--name=YouTube_Video_Downloader",  # Name of the executable
        "--icon=NONE",  # No icon for now
        "--clean",  # Clean cache before building
        "main.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("✅ Executable built successfully!")
        print(f"📁 Executable location: {os.path.join('dist', 'YouTube_Video_Downloader.exe')}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error building executable: {e}")
        return False
    
    return True

def main():
    """Main build function"""
    print("🚀 YouTube Video Downloader - Build Script")
    print("=" * 50)
    
    try:
        # Install requirements
        install_requirements()
        
        # Install PyInstaller
        install_pyinstaller()
        
        # Build executable
        if build_executable():
            print("\n🎉 Build completed successfully!")
            print("\n📋 Next steps:")
            print("1. Navigate to the 'dist' folder")
            print("2. Run 'YouTube_Video_Downloader.exe'")
            print("3. Follow the prompts to download YouTube videos")
        else:
            print("\n❌ Build failed!")
            
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main() 