import os,sys,time

print('제어판 항목:')
tmp=''
with open(os.path.join(dir, 'Users','User','UserDATA.txt'), 'r', encoding='utf-8') as f:
    userdata = [line.strip() for line in f.readlines()]
print('1.계정 2.OS 3.시스템 4.소리')
ct=''
while True:
    ct=input('제어판 >')
    if ct=='1':
        ct=''
        print('1.계정 이름 변경 2.계정 비밀번호 변경')
        ct=input('제어판/계정 >')
        if ct==1:
            tmp = input('계정 비밀번호를 입력하세요:')
            if tmp==userdata[1]:
                tmp=''
                tmp=input('바꿀 계정 이름을 입력하세요:')
                