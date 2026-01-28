#!/usr/bin/env python3
"""
Build script for Flowbite Blazor MAUI Template
Supports: build, run, publish commands
"""

import sys
import os
import platform
import subprocess
import urllib.request
from pathlib import Path
from typing import Optional, Dict


REQUIRED_DOTNET_VERSION = "10.0"
TAILWIND_VERSION = "v4.1.8"
TOOLS_DIR = Path("tools")
PROJECT_PATH = "Flowbite.Maui.csproj"
DIST_DIR = Path("dist")


def get_os_info() -> Dict[str, str]:
    """Detect OS and return tailwindcss download info"""
    system = platform.system()

    if system == "Linux":
        return {
            "url": f"https://github.com/tailwindlabs/tailwindcss/releases/download/{TAILWIND_VERSION}/tailwindcss-linux-x64",
            "exec_name": "tailwindcss",
            "os_name": "Linux",
            "target_framework": None  # Linux not supported for MAUI desktop
        }
    elif system == "Darwin":
        return {
            "url": f"https://github.com/tailwindlabs/tailwindcss/releases/download/{TAILWIND_VERSION}/tailwindcss-macos-arm64",
            "exec_name": "tailwindcss",
            "os_name": "macOS",
            "target_framework": "net10.0-maccatalyst"
        }
    elif system == "Windows":
        return {
            "url": f"https://github.com/tailwindlabs/tailwindcss/releases/download/{TAILWIND_VERSION}/tailwindcss-windows-x64.exe",
            "exec_name": "tailwindcss.exe",
            "os_name": "Windows",
            "target_framework": "net10.0-windows10.0.19041.0"
        }
    else:
        print(f"Unsupported OS: {system}")
        sys.exit(1)


def setup_tailwindcss() -> None:
    """Check and download Tailwind CSS if needed"""
    os_info = get_os_info()
    tailwind_path = TOOLS_DIR / os_info["exec_name"]

    if tailwind_path.exists():
        print(f"Tailwind CSS executable already exists at {tailwind_path}")
        return

    print(f"Downloading Tailwind CSS executable for {os_info['os_name']}...")
    TOOLS_DIR.mkdir(parents=True, exist_ok=True)

    try:
        urllib.request.urlretrieve(os_info["url"], tailwind_path)

        # Make executable on Unix-like systems
        if platform.system() != "Windows":
            os.chmod(tailwind_path, 0o755)

        print(f"Tailwind CSS executable downloaded to {tailwind_path}")
    except Exception as e:
        print(f"Error downloading Tailwind CSS: {e}")
        sys.exit(1)


def get_dotnet_version() -> Optional[str]:
    """Get installed dotnet version, return None if not found"""
    try:
        result = subprocess.run(
            ["dotnet", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def version_greater_equal(current: str, required: str) -> bool:
    """Compare version numbers (major.minor)"""
    try:
        current_parts = [int(x) for x in current.split('.')[:2]]
        required_parts = [int(x) for x in required.split('.')[:2]]

        if current_parts[0] > required_parts[0]:
            return True
        elif current_parts[0] == required_parts[0]:
            return current_parts[1] >= required_parts[1]
        else:
            return False
    except (ValueError, IndexError):
        return current >= required


def check_dotnet() -> Optional[str]:
    """Check if dotnet is installed and meets version requirements"""
    dotnet_version = get_dotnet_version()

    if dotnet_version:
        print(f"Found .NET version: {dotnet_version}")

        version_parts = dotnet_version.split('.')[:2]
        current_version = '.'.join(version_parts)

        if version_greater_equal(current_version, REQUIRED_DOTNET_VERSION):
            print(f"Using system-installed .NET {dotnet_version}")
            return "dotnet"
        else:
            print(f"System .NET version {current_version} is older than required version {REQUIRED_DOTNET_VERSION}")
            print("Please install .NET 10 SDK from: https://dotnet.microsoft.com/download")
            return None
    else:
        print("No system .NET installation found")
        print("Please install .NET 10 SDK from: https://dotnet.microsoft.com/download")
        return None


def run_tailwind_css() -> None:
    """Run Tailwind CSS v4 for MAUI project"""
    os_info = get_os_info()
    tailwind_path = (TOOLS_DIR / os_info["exec_name"]).resolve()

    if not tailwind_path.exists():
        print(f"Warning: Tailwind CSS not found at {tailwind_path}")
        return

    print("Building CSS with Tailwind v4...")
    result = subprocess.run(
        [str(tailwind_path), "-i", "./wwwroot/css/app.css", "-o", "./wwwroot/css/app.min.css"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("[OK] CSS built")
    else:
        print(f"[WARN] CSS build failed: {result.stderr}")


def run_dotnet_command(dotnet_path: str, command: str) -> None:
    """Execute the appropriate dotnet command"""
    os_info = get_os_info()
    target_framework = os_info.get("target_framework")

    if not target_framework:
        print(f"Error: MAUI desktop apps are not supported on {os_info['os_name']}")
        print("MAUI desktop templates support Windows and macOS only.")
        sys.exit(1)

    try:
        if command == "build":
            run_tailwind_css()

            print(f"Building MAUI app for {os_info['os_name']}...")
            subprocess.run(
                [dotnet_path, "build", PROJECT_PATH, "-f", target_framework],
                check=True
            )
            print("[OK] Successfully built solution")

        elif command == "run":
            print(f"Running MAUI app for {os_info['os_name']}...")
            print("Press Ctrl+C to stop...")

            subprocess.run(
                [dotnet_path, "run", "--project", PROJECT_PATH, "-f", target_framework],
            )

        elif command == "publish":
            print(f"Publishing MAUI app to {DIST_DIR}...")

            if DIST_DIR.exists():
                import shutil
                shutil.rmtree(DIST_DIR)

            subprocess.run(
                [dotnet_path, "publish", PROJECT_PATH, "-f", target_framework, "-c", "Release", "-o", str(DIST_DIR)],
                check=True
            )

            print(f"[OK] Successfully published to {DIST_DIR}")

        elif command == "clean":
            print("Cleaning build artifacts...")
            subprocess.run(
                [dotnet_path, "clean", PROJECT_PATH],
                check=True
            )
            print("[OK] Clean complete")

        else:
            print(f"Unknown command: {command}")
            print_usage()
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\nShutdown requested. Exiting cleanly...")
        sys.exit(0)

    except subprocess.CalledProcessError:
        print(f"Error: Failed to {command}")
        sys.exit(1)


def print_usage() -> None:
    """Print usage information"""
    print("Usage: python build.py [command]")
    print("")
    print("Commands:")
    print("  build        - Build the MAUI application (default)")
    print("  run          - Build and run the MAUI application")
    print("  publish      - Publish the MAUI application to dist/")
    print("  clean        - Clean build artifacts")
    print("")
    print("Examples:")
    print("  python build.py              # Build the app")
    print("  python build.py run          # Build and run")
    print("  python build.py publish      # Create release build")
    print("")
    print("Note: MAUI desktop apps require .NET 10 SDK and support Windows and macOS.")


def main() -> None:
    """Main entry point"""
    command = sys.argv[1] if len(sys.argv) > 1 else "build"

    if command == "help" or command == "--help" or command == "-h":
        print_usage()
        return

    if command not in ["build", "run", "publish", "clean"]:
        print(f"Unknown command: {command}")
        print_usage()
        sys.exit(1)

    # Setup prerequisites
    print("Setting up build environment...")
    setup_tailwindcss()

    # Check .NET
    dotnet_path = check_dotnet()
    if not dotnet_path:
        print("")
        print(f"Error: .NET SDK {REQUIRED_DOTNET_VERSION} or later is required.")
        print("Please install from: https://dotnet.microsoft.com/download")
        sys.exit(1)

    # Execute command
    run_dotnet_command(dotnet_path, command)


if __name__ == "__main__":
    main()
