#!/usr/bin/env python
"""
Test Runner for CinemaHub Backend
Прста утиліта для запуску pytest тестів
"""

import subprocess
import sys
import os

def main():
    os.chdir(os.path.dirname(__file__))
    
    # Базова команда
    cmd = [sys.executable, '-m', 'pytest', 'tests/', '-v', '--tb=short']
    
    # Аргументи командної строки
    if len(sys.argv) > 1:
        cmd.extend(sys.argv[1:])
    
    # Запуск тестів
    result = subprocess.run(cmd)
    sys.exit(result.returncode)

if __name__ == '__main__':
    main()
