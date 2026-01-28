#!/usr/bin/env python3
"""
Build script for Flowbite Blazor WebAssembly Template
Supports: build, publish, watch, run, start, stop, status, test commands
"""

import sys
import os
import platform
import subprocess
import urllib.request
import signal
import time
import re
from pathlib import Path
from typing import Optional, Dict

# psutil is optional - only needed for start/stop/status commands
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


def require_psutil():
    """Exit with error if psutil is not available"""
    if not PSUTIL_AVAILABLE:
        print("Error: psutil is required for this command. Install with: pip install psutil")
        sys.exit(1)


REQUIRED_DOTNET_VERSION = "9.0"
TAILWIND_VERSION = "v4.1.8"
TOOLS_DIR = Path("tools")
SOLUTION_PATH = "Flowbite.Wasm.sln"
PROJECT_PATH = "Flowbite.Wasm.csproj"
PID_FILE = Path(".webapp.pid")
LOG_FILE = Path("webapp.log")
DIST_DIR = Path("dist")


def get_os_info() -> Dict[str, str]:
    """Detect OS and return tailwindcss download info"""
    system = platform.system()

    if system == "Linux":
        return {
            "url": f"https://github.com/tailwindlabs/tailwindcss/releases/download/{TAILWIND_VERSION}/tailwindcss-linux-x64",
            "exec_name": "tailwindcss",
            "os_name": "Linux"
        }
    elif system == "Darwin":
        return {
            "url": f"https://github.com/tailwindlabs/tailwindcss/releases/download/{TAILWIND_VERSION}/tailwindcss-macos-arm64",
            "exec_name": "tailwindcss",
            "os_name": "macOS"
        }
    elif system == "Windows":
        return {
            "url": f"https://github.com/tailwindlabs/tailwindcss/releases/download/{TAILWIND_VERSION}/tailwindcss-windows-x64.exe",
            "exec_name": "tailwindcss.exe",
            "os_name": "Windows"
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


def install_dotnet() -> Optional[str]:
    """Install .NET SDK locally using the official install script"""
    system = platform.system()

    if system == "Windows":
        print("Auto-install not supported on Windows. Please install .NET SDK manually.")
        return None

    print(f"Installing .NET SDK {REQUIRED_DOTNET_VERSION}...")
    dotnet_dir = Path("./dotnet")
    dotnet_dir.mkdir(exist_ok=True)

    try:
        # Download install script
        install_script = Path("dotnet-install.sh")
        urllib.request.urlretrieve(
            "https://dot.net/v1/dotnet-install.sh",
            install_script
        )
        install_script.chmod(0o755)

        # Run install script
        result = subprocess.run(
            ["./dotnet-install.sh", "-c", REQUIRED_DOTNET_VERSION, "-InstallDir", "./dotnet"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"Failed to install .NET SDK: {result.stderr}")
            return None

        dotnet_path = dotnet_dir / "dotnet"
        if dotnet_path.exists():
            # Verify installation
            version_result = subprocess.run(
                [str(dotnet_path), "--version"],
                capture_output=True,
                text=True
            )
            if version_result.returncode == 0:
                print(f"Successfully installed .NET SDK {version_result.stdout.strip()}")
                return str(dotnet_path)

        print("Failed to verify .NET SDK installation")
        return None

    except Exception as e:
        print(f"Error installing .NET SDK: {e}")
        return None


def check_dotnet() -> Optional[str]:
    """Check if dotnet is installed and meets version requirements, auto-install if needed"""
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
            print("Attempting to install required version...")
            return install_dotnet()
    else:
        print("No system .NET installation found")
        return install_dotnet()


def is_process_running(pid: int) -> bool:
    """Check if a process with given PID is running"""
    if not PSUTIL_AVAILABLE:
        return False
    try:
        process = psutil.Process(pid)
        return process.is_running() and process.status() != psutil.STATUS_ZOMBIE
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return False


def get_running_pid() -> Optional[int]:
    """Get PID of running application if it exists"""
    if not PID_FILE.exists():
        return None

    try:
        with open(PID_FILE, 'r') as f:
            pid = int(f.read().strip())

        if is_process_running(pid):
            return pid
        else:
            PID_FILE.unlink()
            return None
    except (ValueError, IOError):
        return None


def check_status() -> None:
    """Check if application is running"""
    require_psutil()
    pid = get_running_pid()

    if pid:
        print(f"[OK] WebApp is running (PID: {pid})")
        print(f"  URL: http://localhost:5269")
        print(f"  Log file: {LOG_FILE}")
    else:
        print("[--] WebApp is not running")


def start_background(dotnet_path: str) -> None:
    """Start application in background"""
    require_psutil()
    existing_pid = get_running_pid()
    if existing_pid:
        print(f"WebApp is already running (PID: {existing_pid})")
        print("Use 'python build.py stop' to stop it first")
        return

    print("Starting WebApp in background...")

    log_file = open(LOG_FILE, 'w')

    env = os.environ.copy()
    env["ASPNETCORE_ENVIRONMENT"] = "Development"

    if platform.system() == "Windows":
        process = subprocess.Popen(
            [dotnet_path, "run", "--project", PROJECT_PATH, "--no-restore"],
            stdout=log_file,
            stderr=subprocess.STDOUT,
            env=env,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )
    else:
        process = subprocess.Popen(
            [dotnet_path, "run", "--project", PROJECT_PATH, "--no-restore"],
            stdout=log_file,
            stderr=subprocess.STDOUT,
            env=env,
            start_new_session=True
        )

    with open(PID_FILE, 'w') as f:
        f.write(str(process.pid))

    print(f"WebApp started (PID: {process.pid})")
    print(f"Log output: {LOG_FILE}")

    time.sleep(3)

    if is_process_running(process.pid):
        print("[OK] WebApp is running at http://localhost:5269")
    else:
        print("[FAIL] WebApp failed to start. Check log file for details:")
        print(f"  python build.py log")


def stop_background() -> None:
    """Stop background application"""
    require_psutil()
    pid = get_running_pid()

    if not pid:
        print("No running WebApp found")
        return

    print(f"Stopping WebApp (PID: {pid})...")

    try:
        process = psutil.Process(pid)

        if platform.system() == "Windows":
            process.terminate()
        else:
            process.send_signal(signal.SIGTERM)

        try:
            process.wait(timeout=10)
            print("[OK] WebApp stopped gracefully")
        except psutil.TimeoutExpired:
            print("WebApp did not stop gracefully, forcing shutdown...")
            process.kill()
            process.wait(timeout=5)
            print("[OK] WebApp stopped forcefully")

        if PID_FILE.exists():
            PID_FILE.unlink()

    except psutil.NoSuchProcess:
        print("Process already stopped")
        if PID_FILE.exists():
            PID_FILE.unlink()

    except Exception as e:
        print(f"Error stopping WebApp: {e}")
        sys.exit(1)


def run_tailwind_css() -> None:
    """Run Tailwind CSS v4 for WebApp project

    Note: Uses Tailwind v4.x with CSS-first configuration
    """
    os_info = get_os_info()
    tailwind_path = (TOOLS_DIR / os_info["exec_name"]).resolve()

    if not tailwind_path.exists():
        print(f"Warning: Tailwind CSS not found at {tailwind_path}")
        return

    # Build CSS
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
    try:
        if command == "build":
            # Auto-stop any running application to prevent file lock issues
            pid = get_running_pid()
            if pid:
                print("Stopping running WebApp before build...")
                stop_background()

            # Run Tailwind CSS before dotnet build
            run_tailwind_css()

            print("Building solution...")
            subprocess.run(
                [dotnet_path, "build", SOLUTION_PATH],
                check=True
            )
            print("[OK] Successfully built solution")

        elif command == "watch":
            print("Starting WebApp with hot reload...")
            print("Press Ctrl+C to stop watching...")

            env = os.environ.copy()
            env["ASPNETCORE_ENVIRONMENT"] = "Development"

            subprocess.run(
                [dotnet_path, "watch", "--project", PROJECT_PATH, "--no-restore"],
                env=env
            )

        elif command == "run":
            print("Running WebApp...")
            print("Press Ctrl+C to stop...")

            env = os.environ.copy()
            env["ASPNETCORE_ENVIRONMENT"] = "Development"

            subprocess.run(
                [dotnet_path, "run", "--project", PROJECT_PATH, "--no-restore"],
                env=env
            )

        elif command == "start":
            # Auto-stop any running application
            pid = get_running_pid()
            if pid:
                print("Stopping running WebApp before build...")
                stop_background()

            # Run Tailwind CSS before dotnet build
            run_tailwind_css()

            # Auto-build before starting
            print("Building solution before start...")
            subprocess.run(
                [dotnet_path, "build", SOLUTION_PATH],
                check=True
            )
            start_background(dotnet_path)

        elif command == "stop":
            stop_background()

        elif command == "status":
            check_status()

        elif command == "publish":
            # Publish WebApp to dist/
            print(f"Publishing WebApp to {DIST_DIR}...")

            # Clean dist directory
            if DIST_DIR.exists():
                import shutil
                shutil.rmtree(DIST_DIR)

            subprocess.run(
                [dotnet_path, "publish", PROJECT_PATH, "-c", "Release", "-o", str(DIST_DIR)],
                check=True
            )

            print(f"[OK] Successfully published to {DIST_DIR}")
            print("")
            print("To serve locally:")
            print("  1. Ensure you have dotnet-serve installed: dotnet tool install -g dotnet-serve")
            print(f"  2. Run: cd {DIST_DIR}/wwwroot && dotnet serve")

        elif command == "test":
            # Placeholder for future test support
            print("[INFO] No test project configured")
            print("To add tests, create a test project and update build.py TEST_PROJECT variable")

        elif command == "test-integration":
            # Placeholder for future integration test support
            print("[INFO] No integration tests configured")
            print("To add integration tests, create a test project with integration tests")

        elif command == "test-publish":
            # Run publish as a test to catch pre-rendering errors
            print("Testing publish process (catches pre-rendering errors)...")
            print("")

            # Publish WebApp (this runs pre-rendering which catches binding errors)
            print(f"Publishing WebApp to {DIST_DIR} (with pre-rendering)...")

            # Clean dist directory
            if DIST_DIR.exists():
                import shutil
                shutil.rmtree(DIST_DIR)

            publish_result = subprocess.run(
                [dotnet_path, "publish", PROJECT_PATH, "-c", "Release", "-o", str(DIST_DIR)]
            )

            if publish_result.returncode != 0:
                print("")
                print("[FAIL] Publish test failed!")
                print("This usually indicates pre-rendering errors (e.g., missing @bind-Value).")
                print("Check the error output above for details.")
                sys.exit(1)

            print("")
            print("[OK] Publish test passed - all pages pre-rendered successfully")

        elif command == "test-all":
            # Run test-publish for now (no unit/integration tests yet)
            print("Running available tests (publish test only)...")
            print("")

            print("=" * 60)
            print("STEP 1: Running publish test (pre-rendering validation)...")
            print("=" * 60)

            if DIST_DIR.exists():
                import shutil
                shutil.rmtree(DIST_DIR)

            publish_result = subprocess.run(
                [dotnet_path, "publish", PROJECT_PATH, "-c", "Release", "-o", str(DIST_DIR)]
            )

            if publish_result.returncode != 0:
                print("")
                print("[FAIL] Publish test failed!")
                print("This usually indicates pre-rendering errors (e.g., missing @bind-Value).")
                sys.exit(1)

            print("[OK] Publish test passed")
            print("")
            print("=" * 60)
            print("[OK] All tests passed!")
            print("=" * 60)

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


def search_log(pattern: Optional[str] = None, tail: int = 0, level: Optional[str] = None) -> None:
    """Search or tail the log file

    Args:
        pattern: Regex pattern to search for (case-insensitive)
        tail: Number of lines to show from end (0 = all)
        level: Filter by log level (error, warn, info, debug)
    """
    if not LOG_FILE.exists():
        print(f"Log file not found: {LOG_FILE}")
        print("Start the WebApp first with: python build.py start")
        return

    try:
        with open(LOG_FILE, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()

        if tail > 0:
            lines = lines[-tail:]

        if level:
            level_upper = level.upper()
            level_pattern = re.compile(rf'\b{level_upper}\b|{level_upper}:', re.IGNORECASE)
            lines = [line for line in lines if level_pattern.search(line)]

        if pattern:
            try:
                regex = re.compile(pattern, re.IGNORECASE)
                lines = [line for line in lines if regex.search(line)]
            except re.error as e:
                print(f"Invalid regex pattern: {e}")
                return

        if lines:
            for line in lines:
                print(line.rstrip())
            print(f"\n--- {len(lines)} line(s) shown ---")
        else:
            print("No matching log entries found")

    except Exception as e:
        print(f"Error reading log file: {e}")


def print_usage() -> None:
    """Print usage information"""
    print("Usage: python build.py [command] [options]")
    print("")
    print("Build & Run Commands:")
    print("  build        - Build the solution (default)")
    print("  watch        - Run WebApp with hot reload (foreground)")
    print("  run          - Run WebApp (foreground)")
    print("  start        - Build & start WebApp in background (port 5269)")
    print("  stop         - Stop the background WebApp")
    print("  status       - Check if WebApp is running")
    print("")
    print("Package Commands:")
    print("  publish      - Publish WebApp to dist/")
    print("")
    print("Test Commands:")
    print("  test                     - Run unit tests (not yet configured)")
    print("  test-integration         - Run integration tests (not yet configured)")
    print("  test-publish             - Run publish to catch pre-rendering errors")
    print("  test-all                 - Run all tests (currently just publish test)")
    print("")
    print("Log Commands:")
    print("  log                      - Show last 50 lines of log")
    print("  log <pattern>            - Search log for regex pattern")
    print("  log --tail <n>           - Show last n lines")
    print("  log --level <level>      - Filter by level (error/warn/info/debug)")
    print("")
    print("Examples:")
    print("  python build.py              # Build solution")
    print("  python build.py start        # Build and start in background")
    print("  python build.py watch        # Hot reload development")
    print("  python build.py test-publish # Test pre-rendering")
    print("  python build.py log error    # Search for 'error' in logs")
    print("  python build.py log --tail 100 --level warn")


def main() -> None:
    """Main entry point"""
    command = sys.argv[1] if len(sys.argv) > 1 else "build"

    # Special commands that don't need setup
    if command in ["stop", "status"]:
        if command == "stop":
            stop_background()
        else:
            check_status()
        return

    # Log command
    if command == "log":
        pattern = None
        tail = 50  # Default to last 50 lines
        level = None

        args = sys.argv[2:]
        i = 0
        while i < len(args):
            if args[i] == "--tail" and i + 1 < len(args):
                try:
                    tail = int(args[i + 1])
                except ValueError:
                    print(f"Invalid tail value: {args[i + 1]}")
                    sys.exit(1)
                i += 2
            elif args[i] == "--level" and i + 1 < len(args):
                level = args[i + 1]
                i += 2
            elif not args[i].startswith("--"):
                pattern = args[i]
                i += 1
            else:
                print(f"Unknown option: {args[i]}")
                print_usage()
                sys.exit(1)

        search_log(pattern=pattern, tail=tail, level=level)
        return

    if command == "help" or command == "--help" or command == "-h":
        print_usage()
        return

    if command not in ["build", "watch", "run", "start", "publish", "test", "test-integration", "test-publish", "test-all"]:
        print(f"Unknown command: {command}")
        print_usage()
        sys.exit(1)

    # Setup prerequisites
    print("Setting up build environment...")
    setup_tailwindcss()

    # Check .NET (will auto-install if not found)
    dotnet_path = check_dotnet()
    if not dotnet_path:
        print("")
        print(f"Error: .NET SDK {REQUIRED_DOTNET_VERSION} or later is required.")
        print("Auto-installation failed. Please install manually from:")
        print("https://dotnet.microsoft.com/download")
        sys.exit(1)

    # Execute command
    run_dotnet_command(dotnet_path, command)


if __name__ == "__main__":
    main()
