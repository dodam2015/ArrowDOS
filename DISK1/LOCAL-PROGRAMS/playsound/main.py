import time, pygame, os
print("playsound by ArrowCorp.")
time.sleep(1)
def sound(a):
    a=os.path.join('SYS32','Sounds',a)
    pygame.mixer.music.load(a)   # 파일 경로 넣기
    pygame.mixer.music.play()
t=''
while t!='q':
    print("노래 이름을 입력하세요. (Sounds 폴더), q로 나가기")
    t=''
    t=input(":")
    sound(t)