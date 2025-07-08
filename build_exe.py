import os
import subprocess
import sys
import shutil

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
    cmd = [
        "pyinstaller",
        "--onefile",
        "--console",
        "--name=YouTube_Video_Downloader",
        "--clean",
        "--noupx",
        "--disable-windowed-traceback",
        "--log-level=WARN",
        "--distpath=dist",
        "--workpath=build",
        "--specpath=.",
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

def main():
    """Main build function"""
    print("🚀 YouTube Video Downloader - Antivirus-Friendly Build")
    print("=" * 60)
    try:
        install_requirements()
        install_pyinstaller()
        if build_executable_antivirus_friendly():
            print("\n✅ Antivirus-friendly executable created!")
            print("\n📋 Next steps:")
            print("1. Navigate to the 'dist_clean' folder")
            print("2. Run 'YouTube_Video_Downloader.exe'")
            print("3. Follow the prompts to download YouTube videos")
        else:
            print("\n❌ Executable build failed!")
        print("\n💡 Tips to avoid antivirus issues:")
        print("- Add the executable folder to antivirus exclusions")
        print("- Submit the file to McAfee for whitelisting")
        print("- Run as administrator if needed")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()

    shutil.rmtree("build")
    os.remove("YouTube_Video_Downloader.spec")