# g.py - globals
import pygame,utils,random

app='Eleusis'; ver='1.0'
ver='1.1'
# clear buttons on redeal
ver='1.2'
# added title
ver='1.3'
# must be correct on last to move on
ver='3.0'
# redraw implemented
ver='3.1'
# reworked UI
ver='3.2'
# added two rules by Martin Bahr
ver='4.0'
# new sugar cursor etc

def init(): # called by run()
    random.seed()
    global redraw
    global screen,w,h,font1,font2,clock
    global factor,offset,imgf,message,version_display
    redraw=True
    version_display=False
    screen = pygame.display.get_surface()
    pygame.display.set_caption(app)
    screen.fill((70,0,70))
    pygame.display.flip()
    w,h=screen.get_size()
    if float(w)/float(h)>1.5: #widescreen
        offset=(w-4*h/3)/2 # we assume 4:3 - centre on widescreen
    else:
        h=int(.75*w) # allow for toolbar - works to 4:3
        offset=0
    clock=pygame.time.Clock()
    factor=float(h)/24 # measurement scaling factor (32x24 = design units)
    imgf=float(h)/900 # image scaling factor - all images built for 1200x900
    if pygame.font:
        t=int(72*imgf); font1=pygame.font.Font(None,t)
        t=int(56*imgf); font2=pygame.font.Font(None,t)
    message=''
    
    # this activity only
    global state,display_last,suits,red,black,castle,castle_x,xo1
    global ok,rule,result,tick,cross,advance,smiley
    global back_showing,perfect
    perfect=True # set to False when player makes an error
    back_showing=False
    suits=[]
    for i in range(4):
        img=utils.load_image(str(i)+'.png',True,'suits')
        suits.append(img)
    red=utils.load_image('red.png',True)
    black=utils.load_image('black.png',True)
    castle=utils.load_image('castle.png',True)
    castle_x=utils.load_image('castle_x.png',True)
    xo1=utils.load_image('xo1.png',True)
    state=1; display_last=0
    ok=1 # 1 or 2 - indicates whether rule depends on previous card or not
         #  eg "even after odd" vs "must be red"
         # and specifies which group so rules run like this ...
         # ok=1 rule=1 to 10 ok=2 rule=1 to 9
    rule=1
    result=None; advance=True
    tick=utils.load_image('tick.png',True)
    cross=utils.load_image('cross.png',True)
    smiley=utils.load_image('smiley.png',True)
    #1=drawing cards
    #2= waiting for back click
    #3= waiting for Y/N click on card 1
    #4= waiting for back click
    #5= waiting for Y/N click on card 2
    #6= waiting for back click
    #7= waiting for Y/N click on card 3
    #8= waiting for next rule

def sx(f): # scale x function
    return f*factor+offset

def sy(f): # scale y function
    return f*factor

