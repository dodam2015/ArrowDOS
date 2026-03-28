import subprocess
import os
import sys

def open_file(path):
    path = os.path.abspath(path)          # ★ 절대 경로로 변환
    
    if sys.platform == "win32":
        subprocess.run(['start', '', path], shell=True)
        
    elif sys.platform == "darwin":
        subprocess.run(['open', path])
        
    else:
        subprocess.run(['xdg-open', path])