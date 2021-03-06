from machine import ADC,SPI,PWM,Pin
from FlagArcade import *
import LCD
import time
import network
import socket

mineDragon='Dragon01'

# 螢幕初始設定
spi = SPI(1, baudrate=40000000)
screen = LCD.LCD(spi, 15, 5, 0)
screen.init()
screen.clearLCD()

# 按鈕腳位設定
adc = ADC(0)

# 蜂鳴器腳位與強度設定
buzzer = PWM(Pin(4))
amp = 512

# 設計遊戲音效
def ding():
    buzzer.freq(988)
    buzzer.duty(amp)
    time.sleep(.05)
    buzzer.duty(0)

def toot():
    buzzer.freq(494)
    buzzer.duty(amp)
    time.sleep(.01)
    buzzer.duty(0)
    
def buzz():
    buzzer.freq(247)
    buzzer.duty(amp)
    time.sleep(.5)
    buzzer.duty(0)

# 建立遊戲角色
t1=(
b"     111     "
b"     111     "
b"      1      "
b"11    1    11"
b"      1      "
b"11111 1 11111"
b"  111 1 111  "
b"1111 111 1111"
b"  1 11 11 1  "
b"111 1   1 111"
b"  1 11111 1  "
b"1111 111 1111"
b"  111   111  "
b"1111111111111"
b"             "
b"11         11"
b"             "
)
t2=(
b"     111     "
b"     111     "
b"      1      "
b"      1      "
b"11    1    11"
b"  111 1 111  "
b"11111 1 11111"
b"  11 111 11  "
b"111 11 11 111"
b"  1 1   1 1  "
b"111 11111 111"
b"  11 111 11  "
b"11111   11111"
b"  111111111  "
b"11         11"
b"             "
b"11         11"
)
uf=(
b" 1 "
b"111"
b"111"
b"1 1"
)
# -----------------
e1=(
b"             "
b"11         11"
b"             "
b"1111111111111"
b"  111   111  "
b"1111 111 1111"
b"  1 11111 1  "
b"111 1   1 111"
b"  1 11 11 1  "
b"1111 111 1111"
b"  111 1 111  "
b"11111 1 11111"
b"      1      "
b"11    1    11"
b"      1      "
b"     111     "
b"     111     "
)
e2=(
b"11         11"
b"             "
b"11         11"
b"  111111111  "
b"11111   11111"
b"  11 111 11  "
b"111 11111 111"
b"  1 1   1 1  "
b"111 11 11 111"
b"  11 111 11  "
b"11111 1 11111"
b"  111 1 111  "
b"11    1    11"
b"      1      "
b"      1      "
b"     111     "
b"     111     "
)
df=(
b"1 1"
b"111"
b"111"
b" 1 "
)

redTank = Character([t1], 13, 17, screen, LCD.RED)
purFire = Character(uf, 3, 4, screen, LCD.PURPLE)

bluTank = Character([e1], 13, 17, screen, LCD.BLUE)
cyaFire = Character(df, 3, 4, screen, LCD.CYAN)

redTank.show(60,140)



ap=network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=mineDragon,password="12345678")
print(ap.ifconfig()[0])


sock=socket.socket() # 建立socket 
sock.bind(('0.0.0.0',9999)) # ip+port,0.0.0.0表示所有ip皆可以接收
sock.listen(1) # 只允許一個連接
print(sock)
# screen.text(30,70,'waiting',LCD.YELLOW)

(csock, adr) = sock.accept()
print(adr)

bluTank.show(60,3)

redWin=False
bluWin=False


i=0

while True :
    i+=1
    
    get=csock.recv(1024).decode('utf-8')
    csock.send(str(redTank.x)+','+str(purFire.x)+','+str(purFire.y-10))
    print(i,get)
    
    # 顯示敵方位置
    arr=get.split(',')
    bluTank.show(int(arr[0]),3)
    cyaFire.show(int(arr[1]),156-int(arr[2]))
    
    
    key=getKey(adc.read())
    # 控制紅坦克
    if key=='r' and redTank.x<110 :
        redTank.move(3,0)
        toot()
    elif key=='l' and redTank.x>0:
        redTank.move(-3,0)
        toot()
    else:
        redTank.plot()
        
    # 紅坦克手動發射砲彈        
    if key=="m" and purFire.y<=-10:
        ding()
        purFire.show(redTank.x+5,redTank.y-4)           
    if purFire.y>-10:
        purFire.move(0,-10)
    else:
        purFire.show(150,-50)
        purFire.hide()
        
        
    # 紅坦克被打到，遊戲結束
    if redTank.touch(cyaFire):
        bluWin=True
        buzz()
  
    # 打到藍坦克得分
    if bluTank.touch(purFire):
        redWin=True
        buzz()

    if redWin and bluWin :
        print('兩敗俱傷')
        break
    elif bluWin :
        print('戰敗')
        break
    elif redWin :
        print('勝利')
        break



