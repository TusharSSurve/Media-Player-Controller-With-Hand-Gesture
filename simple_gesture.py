from math import hypot
import pyautogui as pag
from scipy.interpolate import interp1d

def getDistance(p1,p2):
    return hypot(p1[0] - p2[0],p1[1] - p2[1])

def isThumbNearIndexFinger(p1,p2):
    return getDistance(p1,p2) < 20

def simpleGesture(fingers,p1,p2):
    if fingers.count(True)==5:
        return 'FIVE'  # K Play
    elif fingers.count(True)==0:
        return 'FIST' # L Pause
    elif fingers[0]==False and fingers[1]==True and fingers[2]==True and fingers[3]==True and fingers[4]==True:
        return 'FOUR' # Volume 
    elif fingers.count(True)==1 and fingers[0]==False and fingers[1]==True and fingers[2]==False and fingers[3]==False and fingers[4]==False:
        return 'INDEX' # left & right arrow key
    else:
        return 'NONE'

def keyBinding(res):
    if res=='FIVE':
        pag.press('k')
    elif res=='FIST':
        pag.press('l')
    elif res=='RIGHT':
        pag.press('right')
    elif res=='LEFT':
        pag.press('left')
    
def remap(x, in_min, in_max, out_min, out_max,flag=0):
    if x>360:
        return 400 if flag==1 else -63.5
    if x<90:
        return 150 if flag==1 else 0.0
    m = interp1d([in_min,in_max],[out_min,out_max])
    return float(m(x))