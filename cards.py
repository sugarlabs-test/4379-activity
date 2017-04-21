# cards.py
import utils,g,pygame,random

class Cards:

    def __init__(self):
        self.imgs=[]; self.deck=[]
        for i in range(52):
            img=utils.load_image(str(i+1)+'.png',True,'cards')
            self.imgs.append(img)
            self.deck.append(i+1)
        self.back=utils.load_image('back.png',True,'cards')
        self.width=self.back.get_width(); self.w2=int(self.width/2)
        self.height=self.back.get_height(); self.h2=int(self.height/2)
        self.ok=1; self.rule=0
        self._centres()
        self.back_c=(int(g.sx(16)),int(g.sy(10)))

    def _centres(self):
        self.centres=[]; yb=20
        posns=[(2.2,10),(6.0,5.75),(10,3.8),(14,2.95)]
        for i in range(4):
            x=g.sx(32-posns[i][0])
            y=g.sy(yb-posns[i][1])
            self.centres.append((int(x),int(y)))
        for i in range(3):
            x=g.sx(posns[3-i][0])
            y=g.sy(yb-posns[3-i][1])
            self.centres.append((int(x),int(y)))
        for i in range(4):
            x=g.sx(posns[i][0])
            y=g.sy(posns[i][1])
            self.centres.append((int(x),int(y)))
        for i in range(3):
            x=g.sx(32-posns[3-i][0])
            y=g.sy(posns[3-i][1])
            self.centres.append((int(x),int(y)))
        self.centres.reverse()
        self.centres=self.centres[13:]+self.centres[:13]
        c11=self.centres[11]; c12=self.centres[12]; c=(c12[0],c11[1])
        self.centres[12]=c

    def mouse_on_back(self):
        cx,cy=self.back_c; w2=self.w2; h2=self.h2
        if utils.mouse_in(cx-w2,cy-h2,cx+w2,cy+h2): return True
        return False

    def mouse_over(self):
        for i in range(10):
            c=self.centres[i]; cx=c[0]; cy=c[1]; w2=self.w2; h2=self.h2
            if utils.mouse_in(cx-w2,cy-h2,cx+w2,cy+h2):
                n=self.yes[i]; v=value(n); s=suit(n); h=self.help1()
                if h=='nos':
                    utils.display_number(v,c,g.font1,utils.CYAN,utils.ORANGE)
                elif h=='odd_even':
                    if odd(v):
                        utils.display_number(v,c,g.font1,utils.CYAN,utils.RED)
                    else:
                        utils.display_number(v,c,g.font1,utils.RED,utils.CYAN)
                elif h=='suit':
                    utils.centre_blit(g.screen,g.suits[s],c)
                elif h=='colour':
                    img=g.red
                    if colour(n)=='b': img=g.black
                    utils.centre_blit(g.screen,img,c)
                elif h=='castle':
                    utils.centre_blit(g.screen,g.castle,c)
                elif h=='castle_x':
                    utils.centre_blit(g.screen,g.castle_x,c)
                elif h=='xo1':
                    utils.centre_blit(g.screen,g.xo1,c)
                return

    def help1(self):
        if self.ok==2 and self.rule in (2,3): return 'nos'
        if self.ok==1 and self.rule in (1,2,3,4): return 'suit'
        if self.ok==2 and self.rule in (4,6): return 'suit'
        if self.ok==1 and self.rule in (5,6): return 'colour'
        if self.ok==2 and self.rule == 1: return 'colour'
        if self.ok==1 and self.rule in (9,10): return 'odd_even'
        if self.ok==2 and self.rule == 5: return 'odd_even'
        if self.ok==1 and self.rule == 7: return 'castle'
        if self.ok==1 and self.rule == 8: return 'castle_x'
        if self.ok==2 and self.rule >= 7: return 'xo1'
        return ''

    def setup(self):
        self.yes=[]
        self.rest=utils.copy_list(self.deck)
        self.rest=utils.shuffle(self.rest)
        self.display_last=0
        self.ms=pygame.time.get_ticks()
        g.state=1; g.display_last=0; g.perfect=True

    def start(self):
        k=10
        if self.ok==1:
            while len(self.yes)<k:
                n=self.next_card()
                if ok1(self.rule,n): self.yes.append(n)
        else:
            n1=self.next_card()
            self.yes=[n1]
            while len(self.yes)<k:
                n2=self.next_card()
                if ok2(self.rule,n1,n2,len(self.yes)):
                    self.yes.append(n2); n1=n2

    def next_card(self):
        if self.rest==[]: # ensure no cards are lost!
            fresh=utils.copy_list(self.deck); fresh=utils.shuffle(fresh)
            for n in fresh:
                if n not in self.yes: self.rest.append(n)
        n=self.rest.pop()
        return n

    def next_card1(self):
        ind=len(self.yes)-1; n1=self.yes[ind]
        if random.randint(1,3)==1: #get good card
            while True:
                n2=self.next_card()
                if self.ok==1:
                    if ok1(self.rule,n2): return n2
                else:
                    if ok2(self.rule,n1,n2,len(self.yes)-1): return n2
        else: #get bad card
            while True:
                n2=self.next_card()
                if self.ok==1:
                    if not ok1(self.rule,n2): return n2
                else:
                    if not ok2(self.rule,n1,n2,len(self.yes)-1): return n2

    def redeal(self):
        self.setup()
        self.start()       
        
    def next_rule(self):
        self.setup()
        self.rule+=1
        if self.ok==1:
            if self.rule>10: self.ok=2; self.rule=1
        else:
            if self.rule>9: self.ok=1; self.rule=1
        self.start()

    def good(self):
        l=utils.copy_list(self.yes)
        if self.ok==1:
            n=l.pop(); return ok1(self.rule,n)
        else:
            n2=l.pop(); n1=l.pop(); return ok2(self.rule,n1,n2,len(self.yes)-1)

    def rule_n(self):
        if self.ok==1: return self.rule
        return self.rule+10
        
def suit(n): # s,c,d,h
    v=(n-1)/13 # 0,1,2,3
    return v

def value(n): # 1,2,...,13(K)
    v=((n-1) % 13)+1
    return v

def even(n):
    t=n & 1
    if t==0: return True
    return False

def odd(n):
    t=n & 1
    if t==0: return False
    return True

def colour(n): # b,r
    s=suit(n)
    if s in [0,1]: return 'b'
    return 'r'

def ok1(rule,n):
    if rule==1: # clubs
        if suit(n)==1: return True
        return False
    if rule==2: # diamonds
        if suit(n)==2: return True
        return False
    if rule==3: # hearts
        if suit(n)==3: return True
        return False
    if rule==4: # spades
        if suit(n)==0: return True
        return False
    if rule==5: # red
        if colour(n)=='r': return True
        return False
    if rule==6: # black
        if colour(n)=='b': return True
        return False
    if rule==7: # royal
        v=value(n)
        if v>10 or v==1: return True
        return False
    if rule==8: # non-picture
        v=value(n)
        if v>1 and v<11: return True
        return False
    if rule==9: # even
        v=value(n)
        if even(v): return True
        return False
    if rule==10: # odd
        v=value(n)
        if odd(v): return True
        return False

def ok2(rule,n1,n2,yes_len):
    if rule==1: # r b r b r b ...
        c1=colour(n1); c2=colour(n2)
        if c1!=c2: return True
        return False
    if rule==2: # +1
        v1=value(n1); v2=value(n2)
        if v2==(v1+1): return True
        if v1==13 and v2==1: return True
        return False
    if rule==3: # -1
        v1=value(n1); v2=value(n2)
        if v2==(v1-1): return True
        if v1==1 and v2==13: return True
        return False
    if rule==4: # c d h s (alpha order)
        s1=suit(n1); s2=suit(n2)
        if s2==(s1+1): return True
        if s2==0 and s1==3: return True
        return False
    if rule==5: # odd even odd even ...
        v1=value(n1); v2=value(n2)
        if odd(v1) and even(v2): return True         
        if odd(v2) and even(v1): return True
        return False
    if rule==6: # suit triples
        s1=suit(n1); s2=suit(n2)
        if yes_len%3==0:
            if s1==s2: return False
            else: return True
        if s1==s2: return True
        return False
    if rule==7: # alternating color and increasing sequence
        v1=value(n1); v2=value(n2)
        c = colour(n1)!=colour(n2)
        if v2==(v1+1) and c: return True
        if v1==13 and v2==1 and c: return True
        return False
    if rule==8: # alternating color and decreasing sequence
        v1=value(n1); v2=value(n2)
        c = colour(n1)!=colour(n2)
        if v2==(v1-1) and c: return True
        if v1==1 and v2==13 and c: return True
        return False
    if rule==9: # same suit or value
        s1=suit(n1); s2=suit(n2)
        v1=value(n1); v2=value(n2)
        if s1==s2 or v1==v2: return True
        return False
    
           
        
    

    
            
            
