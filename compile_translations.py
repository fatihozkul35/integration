#!/usr/bin/env python
"""
Script to compile .po files to .mo files without requiring gettext tools.
This uses Python's built-in gettext module.
"""
import os
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
LOCALE_DIR = BASE_DIR / 'locale'

def compile_po_to_mo(po_file, mo_file):
    """Compile .po file to .mo file using Python's gettext"""
    try:
        from babel.messages import mofile
        from babel.messages.pofile import read_po
        
        with open(po_file, 'rb') as f:
            catalog_obj = read_po(f)
        
        with open(mo_file, 'wb') as f:
            mofile.write_mo(f, catalog_obj)
        print(f"OK: Compiled {po_file.name} -> {mo_file.name}")
        return True
    except Exception as e:
        print(f"Error compiling {po_file.name}: {e}")
        return False

def main():
    """Main function to compile all translation files"""
    print("Compiling translation files...\n")
    
    if not LOCALE_DIR.exists():
        print(f"Error: Locale directory not found: {LOCALE_DIR}")
        return
    
    compiled = 0
    failed = 0
    
    # Find all .po files
    for po_file in LOCALE_DIR.rglob('*.po'):
        mo_file = po_file.with_suffix('.mo')
        if compile_po_to_mo(po_file, mo_file):
            compiled += 1
        else:
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"Compiled: {compiled} files")
    if failed > 0:
        print(f"Failed: {failed} files")
    print(f"{'='*50}")

if __name__ == '__main__':
    main()

