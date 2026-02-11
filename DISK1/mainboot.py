try:
    import sys,os,time,subprocess,traceback,datetime,base64
    from tqdm import tqdm
    from pathlib import Path
    os.system('cls')
    print('\033[0m')
    os.system('cls')
    parent_name=Path.cwd().name
    print("\033[32mArrowDOS부팅매니저\033[34m-v1.0.7\033[0m")
    time.sleep(2)
    if parent_name=='DISK1':
        pass
    else:
        print('사용자의 arrowDOS에서 문제점을 발견했습니다.')
        print('컴퓨터를 재부팅합니다.' )
        for i in range(0,4096):
            print('err: 58424')
        subprocess.run([sys.executable,'mainboot.py'])
    print("사용하실 부팅 모드를 선택하세요.")
    print("1.\033[36m일반 모드\033[0m")
    print("2.\033[33m안전 모드\033[0m")
    print("3.\033[31mDOS모드\033[0m")
    while True:
        try:

            bootmod=int(input("번호를 입력하세요:"))
        except(KeyboardInterrupt):
            print("...")
            time.sleep(2)
            cmd=''
            os.system("cls")
            print("일반 모드로 부팅하려면 bootmod=1 을 입력해 주세요.")
            while True:
                cmd=input(f'{parent_name}>')
                if cmd=='bootmod=1':
                    bootmod=1
                    break
                else:
                    print(f"{cmd}는 유효한 경로나 파일, 응용 프로그램 단축이 아닙니다.")
        if bootmod==1:
            print("\033[36m일반 모드\033[0m를 선택하셨습니다.")
            print("\033[33m2\033[m초 후에 \033[36m일반 모드\033[0m로 진입합니다.")
            time.sleep(2)
            os.system("cls")
            subprocess.run([sys.executable, "SYS32/MAIN/main.py"])
            break
        elif bootmod==2:
            print("\033[33m안전 모드\033[0m를 선택하셨습니다.")
            print("\033[33m2\033[m초 후에 \033[33m안전 모드\033[0m로 진입합니다.")
            time.sleep(2)
            os.system("cls")
            print('구현되지 않았습니다.')
        elif bootmod==3:
            print("\033[31mDOS모드\033[0m를 선택하셨습니다.")
            print("\033[33m2\033[m초 후에 \033[31mDOS모드\033[0m로 진입합니다.")
            time.sleep(2)
            os.system("cls")
            print('구현되지 않았습니다.')
        else:
            print('입력한 번호를 재확인 하고 다시 입력해주세요.')
            print(f'입력한 번호는: {bootmod}입니다.')
except(Exception,KeyboardInterrupt) as e:
    try:
        def path_exists(path: str) -> bool:
            return os.path.exists(path) and os.path.isfile(path)
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