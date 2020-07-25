from machine import ADC,SPI,PWM,Pin,freq
from FlagArcade import *
import LCD

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
cl1=(

b"       1         1  "
b"     1 1         1  "
b"  11111   111   111 "
b"111 1    1111  11111"
b"  1111    111   111 "
b"11111      1     1  "
b"1  11     111   11  "
b"  1111    111  111  "
b"  111111111111111   "
b"   11 11 11 11 1    "
b"                    "
)
cl2=(
b"       1         1  "
b"     1 1         1  "
b"  11111         1 1 "
b"11111    111   1 1 1"
b"111111  1111    111 "
b"1  11    111     1  "
b"   11     1     11  "
b"  1111    111  111  "
b"  111111111111111   "
b"   1 11 11 11 11    "
b"                    "
)
# ------------------

cr1=(
b"  1         1       "
b"  1         1 1     "
b" 111   111   11111  "
b"1 1 1  1111    1 111"
b" 111   111    1111  "
b"  1     1      11111"
b"  11   111     11  1"
b"  111  111    1111  "
b"   111111111111111  "
b"     11 11 11 11 1  "
b"                    "
)

cr2=(
b"  1         1       "
b"  1         1 1     "
b" 1 1         11111  "
b"11111   111    11111"
b" 111    1111  111111"
b"  1     111    11  1"
b"  11     1     11   "
b"  111  111    1111  "
b"   111111111111111  "
b"    11 11 11 11 1   "
b"                    "
)
# ------------------
fl1=(
b"    111111      1"
b"  111     11  111"
b"111 11      111 1"
b"11111 1     11 1 "
b"  111     11    1"
b"    111111       "
)
fl2=(
b"    111111       "
b"11111     11    1"
b"  111 1     11 1 "
b" 11111      111 1"
b"11111     11  111"
b"    111111      1"
)
# ------------------
fr1=(
b"1      111111    "    
b"111  11     111  "
b"1 111      11 111"
b" 1 11     1 11111"
b"1    11     111  "
b"       111111    "  
)
fr2=(
b"       111111    "    
b"1    11     11111"
b" 1 11     1 111  "
b"1 111      11111 "
b"111  11     11111"
b"1      111111    "  
)
# ------------------
zz=(
b"   1   " 
b"  111  "    
b"  111  " 
b" 11111 "    
b"  111  "
b"11 1 11"
b"111 111"    
)
# ------------------
boatLeft = Character([cl1,cl2], 20, 11, screen, LCD.PURPLE)
boatRigh = Character([cr1,cr2], 20, 11, screen, LCD.PURPLE)
fishLeft = Character([fl1,fl2], 17, 6, screen, LCD.CYAN)
fishRigh = Character([fr1,fr2], 17, 6, screen, LCD.CYAN)
zongzi = Character(zz, 7, 7, screen, LCD.GREEN)
boat=boatRigh


# 宣告全域變數
end=False
score=0
cx=60;cy= 20
past='r'
fishLeft.show(128,randint(40,150))
fishRigh.show(-20,randint(40,150))

# 建立常用函式
def resetGame():
    global end,score,cx,cy,boat,past
    boatLeft.hide()
    boatRigh.hide()
    boat=boatRigh
    past='r'
    cx=60;cy= 20
    zongzi.show(randint(0,110),180)
    screen.text(30,70, "Game Over",LCD.BLACK)
    end=False
    score=0
    printScore()

def printScore():
    global score 
    screen.text(10, 5,"score:"+str(score)+'   ')

resetGame()
printScore()

while True:
    key=getKey(adc.read())
    if not end :
        # 控制龍舟
        if past!=key:
            boat.hide()
            past=key       
        if key=='r':
            toot()
            boat=boatRigh
            cx=cx+3 
        if key=='l':
            toot()
            boat=boatLeft
            cx=cx-3 
        if key=='m':
            if zongzi.y>170:
                ding()
                zongzi.x=boat.x+5
                zongzi.y=35
        boat.show(cx,cy)
            
        # 粽子掉落 
        zongzi.move(randint(-1,1),3)
        
        fishLeft.move(-1,randint(-1,1))
        if fishLeft.x < -20 :
            fishLeft.show(128,randint(40,150))
        fishRigh.move(1,randint(-1,1))
        if fishRigh.x > 128 :
            fishRigh.show(-20,randint(40,150))

        # 魚吃到粽子
        if zongzi.touch(fishLeft) or zongzi.touch(fishRigh):
            buzz()
            zongzi.show(randint(0,110),180)
            score+=1
            printScore()
    # 遊戲重啟
    if end :
        if key=="rst":
            resetGame()
            printScore()
    # 切換靜音
    if key=="set" :
        if amp == 512 :
            amp = 0
        else :
            amp = 512
    
    
