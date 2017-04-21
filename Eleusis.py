#!/usr/bin/python
# Eleusis.py
"""
    Copyright (C) 2010  Peter Hewitt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""
import g,utils,pygame,gtk,sys,cards,buttons

class Eleusis:
    
    def __init__(self):
        self.ok=1; self.rule=1
        self.journal=True # set to False if we come in via main()

    def display(self):
        g.screen.fill((0,180,0))
        buttons.draw()
        if g.state==1:
            for i in range(g.display_last):
                n=self.cards.yes[i]; c=self.cards.centres[i]
                utils.centre_blit(g.screen,self.cards.imgs[n-1],c)
        else:
            for i in range(len(self.cards.yes)):
                n=self.cards.yes[i]; c=self.cards.centres[i]
                utils.centre_blit(g.screen,self.cards.imgs[n-1],c)
            self.cards.mouse_over()
        if g.state in [2,4,6]:
            utils.centre_blit(g.screen,self.cards.back,self.cards.back_c)
        if g.state in [2,4,6,8]:
            if g.result<>None:
                ind=len(self.cards.yes)-1
                utils.centre_blit(g.screen,g.result,self.cards.centres[ind])
                if g.state==8:
                    ind=3
                else:
                    ind=(g.state/2)-1
                    yes=self.yes_bu[ind]; no=self.no_bu[ind]
                if g.result==g.tick:
                    if g.perfect: bu=self.yes_bu[ind-1]
                    else: bu=no
                else:
                    if g.perfect: bu=no
                    else: bu=yes
                bu.draw_down()
        s=str(self.cards.rule_n())+' / '+str(19)
        utils.text_blit1(g.screen,s,g.font2,(g.sx(1),g.sy(1)),(255,255,192))
        if g.state==8: utils.centre_blit(g.screen,g.smiley,self.cards.back_c)
        #utils.display_number(g.state,(40,120),g.font2,utils.BLUE) ###
       
    def update(self):
        if g.state==1:
            d=pygame.time.get_ticks()-self.cards.ms
            if d<0 or d>500:
                g.redraw=True
                g.display_last+=1
                if g.display_last>len(self.cards.yes):
                    g.state=2
                else:
                    self.cards.ms=pygame.time.get_ticks()
        if g.state in [2,4,6]:
            if not g.back_showing: g.redraw=True; g.back_showing=True

    def button(self,bu):
        if bu=='redeal':
            g.back_showing=False; g.advance=True; g.result=None
            self.bus_off()
            if g.state==8:
                self.cards.next_rule(); g.state=1; return
            else:
                self.cards.redeal(); return
        if bu=='yes':
            if self.cards.good(): # player correct
                g.state+=1; g.advance=True
            else: # player wrong
                g.state-=1; g.advance=False; g.perfect=False
        if bu=='no':
            if self.cards.good(): # player wrong
                g.state-=1; g.advance=False; g.perfect=False
            else: # player correct
                g.state-=1; g.advance=False
        if bu in ['yes','no']:
            self.bus_off()
            g.result=g.cross
            if self.cards.good(): g.result=g.tick

    def click(self):
        if g.state in [2,4,6]:
            if self.cards.mouse_on_back():
                if not g.perfect:
                    self.cards.yes=self.cards.yes[:10]
                    g.state=2; g.perfect=True
                else:
                    if not g.advance: self.cards.yes.pop()
                n=self.cards.next_card1()
                self.cards.yes.append(n)
                self.bus_off()
                t=g.state/2-1
                self.yes_bu[t].active=True; self.no_bu[t].active=True
                g.state+=1

    def bus_on(self):
        self.bus_off()
        if g.state in [3,5,7]:
            i=(g.state-1)/2-1
            self.yes_bu[i].active=True; self.no_bu[i].active=True

    def bus_off(self):
        for i in range(3):
            self.yes_bu[i].active=False; self.no_bu[i].active=False

    def run(self):
        g.init()
        if not self.journal:
            utils.load()
        else:
            g.ok=self.ok; g.rule=self.rule
        self.cards=cards.Cards()
        self.cards.ok=g.ok; self.cards.rule=g.rule
        self.cards.redeal()
        bx=g.sx(17.4); by1=g.sy(15.5); by2=g.sy(18.5)
        self.yes_bu=[]; self.no_bu=[]
        for i in range(3):
            bu=buttons.Button("yes",(bx,by1),True); bu.active=False
            self.yes_bu.append(bu)
            bu=buttons.Button("no",(bx,by2),True); bu.active=False
            self.no_bu.append(bu)
            bx+=self.cards.width+g.sy(.5)
        bx=g.sx(29.9); by=g.sy(14.2)
        buttons.Button("redeal",(bx,by),True)
        if self.journal: # Sugar only
            a,b,c,d=pygame.cursors.load_xbm('my_cursor.xbm','my_cursor_mask.xbm')
            pygame.mouse.set_cursor(a,b,c,d)
        going=True
        while going:
            # Pump GTK messages.
            while gtk.events_pending():
                gtk.main_iteration()

            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    if not self.journal:
                        g.ok=self.cards.ok; g.rule=self.cards.rule
                        utils.save()
                    going=False
                elif event.type == pygame.MOUSEMOTION:
                    g.redraw=True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    g.redraw=True
                    if event.button==2: # centre button
                        if not self.journal:
                            g.version_display=not g.version_display; break
                    bu=buttons.check()
                    if bu<>'': self.button(bu); break
                    self.click()
            if not going: break
            self.update()
            if g.redraw:
                self.display()
                if g.version_display: utils.version_display()
                pygame.display.flip()
                g.redraw=False
            tf=False
            if pygame.mouse.get_focused(): tf=True
            pygame.mouse.set_visible(tf)
            g.clock.tick(40)
            # be ready for xo quit at any time
            self.ok=self.cards.ok; self.rule=self.cards.rule

if __name__=="__main__":
    pygame.init()
    pygame.display.set_mode((800, 600))
    game=Eleusis()
    game.journal=False
    game.run()
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)
