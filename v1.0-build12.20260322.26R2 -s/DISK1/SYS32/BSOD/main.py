import sys,base64, traceback,subprocess,time,os
from pathlib import Path
e=sys.argv[1]
dir=Path.cwd()
try:
    with open(os.path.join(dir, 'SYS32','osname.txt'), 'r', encoding='utf-8') as f:
        osname = [line.strip() for line in f.readlines()]
    print("\033[44m\033[97m")
    os.system('cls')
    print('BLUE_SCREEN')
    print('DOS-error')
    print(f'TARGET: {osname[0][:8]}')
    tb_text = traceback.format_exc()
    tb_base64 = base64.b64encode(tb_text.encode('utf-8')).decode('ascii')
    print('-' * 50)
    for i in range(0, len(tb_base64), 50):
        print(tb_base64[i:i+50])
    print('-' * 50)
    print(f'ERROR_MSG: {e}')
    bsodrsttim=5
    print(f'ERR: ARROWDOS_RESTART IN {bsodrsttim}S')
    time.sleep(bsodrsttim)
    subprocess.run([sys.executable,'mainboot.py'])
except(Exception,KeyboardInterrupt):
    subprocess.run([sys.executable,'mainboot.py'])