import os,sys,time
from pathlib import Path
dir=Path.cwd()

print('제어판 항목:')
tmp=''
with open(os.path.join(dir, 'SYS32','SYSF','openbtmn.arsys'), 'r', encoding='utf-8') as f:
    bootmn = f.readline().strip()
print(f'부팅 건너 뛰기 여부: {bootmn}')