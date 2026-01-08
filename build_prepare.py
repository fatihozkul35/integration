#!/usr/bin/env python
"""
Pre-deployment build script.
Prepares the project for deployment by:
- Creating migration files
- Updating requirements.txt
- Checking for common issues
"""
import os
import sys
import subprocess
from pathlib import Path


def find_python():
    """Find the correct Python executable."""
    # Check for Windows venv
    win_venv_python = Path("venv/Scripts/python.exe")
    if win_venv_python.exists():
        return str(win_venv_python), "Windows venv"

    # Check for Linux/Mac venv
    linux_venv_python = Path("venv/bin/python")
    if linux_venv_python.exists():
        return str(linux_venv_python), "Linux/Mac venv"

    # Use system Python
    python_cmd = "python3" if sys.platform != "win32" else "python"
    # Verify it works
    try:
        subprocess.run([python_cmd, "--version"], 
                      capture_output=True, check=True)
        return python_cmd, "system Python"
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fallback to python
        try:
            subprocess.run(["python", "--version"], 
                          capture_output=True, check=True)
            return "python", "system Python"
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Error: Python not found!")
            sys.exit(1)


def run_command(cmd, description, allow_failure=False):
    """Run a command and handle errors."""
    print(f"{description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, 
                              capture_output=True, text=True)
        if result.stdout:
            print(result.stdout, end="")
        return True
    except subprocess.CalledProcessError as e:
        if allow_failure:
            print(f"Warning: {description} failed: {e.stderr.strip() if e.stderr else 'No error message'}")
            return False
        else:
            print(f"Error: {description} failed: {e.stderr.strip() if e.stderr else 'No error message'}")
            return False
    except Exception as e:
        if allow_failure:
            print(f"Warning: {description} failed: {str(e)}")
            return False
        else:
            print(f"Error: {description} failed: {str(e)}")
            return False


def main():
    print("****************************************************************")
    print("Building for pre-deployment (local preparation)...")
    print("****************************************************************")
    
    python_cmd, python_source = find_python()
    print(f"Using {python_source}...")
    print()
    
    # Get pip command
    if python_source == "Windows venv":
        pip_cmd = "venv\\Scripts\\pip.exe"
    elif python_source == "Linux/Mac venv":
        pip_cmd = "venv/bin/pip"
    else:
        pip_cmd = f"{python_cmd} -m pip"
    
    # 1. Create migration files
    print("1. Creating migration files...")
    run_command(f"{python_cmd} manage.py makemigrations", 
               "Creating migrations", allow_failure=True)
    print()
    
    # 2. Update requirements.txt
    print("2. Updating requirements.txt with installed packages...")
    run_command(f"{pip_cmd} freeze > requirements.txt", 
               "Updating requirements.txt", allow_failure=True)
    print()
    
    # 3. Check for common issues
    print("3. Checking for common issues...")
    if not Path(".env").exists():
        print("   Warning: .env file not found. Make sure environment variables are configured.")
    print()
    
    print("****************************************************************")
    print("Build completed successfully!")
    print("Next steps:")
    print("  1. Review the generated migration files")
    print("  2. Check requirements.txt for any unexpected packages")
    print("  3. Test locally: make migrateall")
    print("  4. Deploy to production")
    print("****************************************************************")


if __name__ == "__main__":
    main()

