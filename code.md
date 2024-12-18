################################################
# Programmeerimine I
# 2024/2025 sügissemester
#
# Projekti tiim RoRo
# Teema: Trips Traps Trull
#
# Autorid: Anastassia Käärmann, Emma Laikmaa
#
# mõningane eeskuju: Idee tuli tuttavalt.
#
# Käivitusjuhend: Mängu käivitamiseks vajutage rohelist Start nuppu (mängu käivitamiseks peab olema pygame, sys).
# Selleks, et mängu taaskäivitada/uuesti alustada vajutage Enter
##################################################

import pygame
import sys
from pygame.locals import *
import random
import numpy as np

pygame.init()

alusta_aja_lugemist = pygame.time.get_ticks()
väike_font = pygame.font.SysFont("Geneva", 25) #kellale

#võitude lugemise muutujad
x_võidud =0 
o_võidud =0

# Värvid
MUST = (0, 0, 0)
VALGE = (255, 255, 255)
PUNANE = (255, 0, 0)
TUMEPUNANE = (200, 0, 0)
SININE = (0, 0, 255)
NUPUVÄRV = VALGE

# Ekraan
laius, kõrgus = 450, 520 
ekraan = pygame.display.set_mode((laius, kõrgus))
pygame.display.set_caption("Trips-Traps-Trull")
#ekraan.fill(MUST)

piltide_järjend = ["meme1.jpg","meme2.jpg","meme3.jpg","meme4.jpg"]
milline_pilt = 0
link = piltide_järjend[0]

def taustapildiks(link): #funktsioon taustapildi rakenduseks 
    taustapilt = pygame.image.load(link)
    taustapilt = pygame.transform.scale(taustapilt, (laius, 450))
    return taustapilt
taustapildiks(link)

board = np.zeros((3, 3)) # teeme boardi 3x3, mis on põhimõtteliselt maatriks
ekraan.blit(taustapildiks(link), (0, 0)) # (0, 0) paneb pildi lguseks ülemise vasaku nurga
pygame.draw.line(ekraan, VALGE, (0, 470), (450, 470), 35)

# Funktsioonid
def joonistame_read():
    # 1 horisontaalne joon, ekraan, joonevärv, algkoordinaat, lõppkoorinaat, joonelaius
    pygame.draw.line(ekraan, VALGE, (0, 150), (450, 150), 5)
    # 2 horisontaalne joon
    pygame.draw.line(ekraan, VALGE, (0, 300), (450, 300), 5)
    # 1 vertikaalne joon
    pygame.draw.line(ekraan, VALGE, (150, 0), (150, 450), 5)
    # 2 vertikaalne joon
    pygame.draw.line(ekraan, VALGE, (300, 0), (300, 450), 5)
    
def joonista_XO(rida, veerg):
    if board[rida][veerg] == 1:  # joonista X
        pygame.draw.line(ekraan, VALGE, (veerg * 150 + 45, rida * 150 + 150 - 45), (veerg * 150 + 150 - 45, rida * 150 + 45), 23) #15
        pygame.draw.line(ekraan, VALGE, (veerg * 150 + 45, rida * 150 + 45), (veerg * 150 + 150 - 45, rida * 150 + 150 - 45), 23)
    elif board[rida][veerg] == 2:  # joonista O
        pygame.draw.circle(ekraan, VALGE, (int(veerg * 150 + 150 / 2), int(rida * 150 + 150 / 2)), 40, 14) #10
        
def kuva_taimer():
    möödunud_sekundid = (pygame.time.get_ticks() - alusta_aja_lugemist) // 1000
    pygame.draw.rect(ekraan, MUST, (0, 500, laius, 30))  # Puhastame vana taimeri ala
    # Kuvame uue taimeri teksti
    taimer_tekst = väike_font.render(f"Aeg: {möödunud_sekundid}s", True, VALGE) #render = kuvama
    taimer_x = (laius - taimer_tekst.get_width()) // 2  # horisontaalselt keskele
    ekraan.blit(taimer_tekst, (taimer_x, 500))  # taimeri teksti kuvamine

def kuva_võidu_teade(teade):
    global x_võidud, o_võidud
    font = pygame.font.SysFont("Geneva", 50)  # Suurem font võidu/viik jaoks
    võitude_font= pygame.font.SysFont("Geneva", 30) 
    tekst = font.render(teade, True, VALGE)  # Loome teate
    tekst_x = (laius - tekst.get_width()) // 2   # horisontaalselt keskele
    tekst_y = (450 - tekst.get_height()) // 2 - 25 # mängulaua keskelt 25 üles poole
    
    pygame.draw.rect(ekraan, PUNANE, (tekst_x - 20, tekst_y - 20, tekst.get_width() + 40, tekst.get_height() + 90), border_radius=20  )
                                        #ülemise vasaku nurga koordinaadid, laius, kõrgus, äärte ümarus
    
    ekraan.blit(tekst, (tekst_x, tekst_y))  # Kuvame teate
    
    if "X võitis" in teade: #kui keegi võitis suurendatakse 
        x_võidud += 1
    elif "O võitis" in teade:
        o_võidud += 1
    
    skoor_tekst = väike_font.render(f"X : {x_võidud} | O : {o_võidud}", True, VALGE) # teeb teksti sujuvaks (True--> peidab pikslid)
    skoor_x = (laius - skoor_tekst.get_width()) // 2
    skoor_y = tekst_y + 60  # Kuvame skoori veidi allpool võiduteadet
    ekraan.blit(skoor_tekst, (skoor_x, skoor_y))

def ruudud(rida, veerg, mängija): # märgime maatriksis ära, mis mängija kuhu toksas
    board[rida][veerg] = mängija
    
def kontrolliruutu(rida, veerg): # kontrollime kas ruut on vaba - kas saab märki panna või mitte
    if board[rida][veerg] == 0:
        return True
    else:
        return False
    
def ruudud_on_täis(rida, veerg):
    for rida in range(3):
        for veerg in range(3):
            if board[rida][veerg] == 0: # kui kehtib, siis leiti veel tühju ruute ning mäng saab jätkuda
                return False
    return True # tühjasid ruute ei leitud, mäng ei saa jätkuda

def kes_võitis(mängija):
    # vertikaalse võidu kontroll
    for veerg in range(3):
        if board[0][veerg] == mängija and board[1][veerg] == mängija and board[2][veerg] == mängija:
            joonistame_vertikaalse_kriipsu(veerg, mängija)
            return True #see lõpetab veergude kontrolli
        
    # horisontaalse võidu kontroll
    for rida in range(3):
        if board[rida][0] == mängija and board[rida][1] == mängija and board[rida][2] == mängija:
            joonistame_horisontaalse_kriipsu(rida, mängija)
            return True #see lõpetab veergude kontrolli
        
    # esimese diagonaali-võidu kontroll
    if board[2][0] == mängija and board[1][1] == mängija and board[0][2] == mängija:
        joonistame_esimese_diagonaali(mängija)
        return True
    
    # teise diagonaali-võidu kontroll
    if board[0][0] == mängija and board[1][1] == mängija and board[2][2] == mängija:
        joonistame_teise_diagonaali(mängija)
        return True
        
    return False

def joonistame_vertikaalse_kriipsu(veerg, mängija):
    X = veerg * 150 + 75
    pygame.draw.line(ekraan, VALGE, (X, 10), (X, 450 - 10), 10) # kuhu ta teeb, mis värviga, algus, lõpp, kui paksult
        
def joonistame_horisontaalse_kriipsu(rida, mängija):
    Y = rida * 150 + 75
    pygame.draw.line(ekraan, VALGE, (10, Y), (450 - 10, Y), 10) # kuhu ta teeb, mis värviga, algus, lõpp, kui paksult

def joonistame_esimese_diagonaali(mängija): # vasakult paremale - diagonaal
    pygame.draw.line(ekraan, VALGE, (15, 450 - 15), (450 - 15, 15), 15)

def joonistame_teise_diagonaali(mängija): # paremalt vasakule diagonaal
    pygame.draw.line(ekraan, VALGE, (15, 15), (450 - 15, 450 - 15), 15)
    
def mängijaükskord():
    pygame.draw.line(ekraan, PUNANE, (0, 470), (225, 470), 45) #karbike 
    pygame.draw.line(ekraan, VALGE, (225, 470), (450, 470), 45)
    
    pygame.draw.line(ekraan, MUST, (330, 459), (345, 476), 5) #X
    pygame.draw.line(ekraan, MUST, (345, 459), (330, 476), 5)
    
    pygame.draw.circle(ekraan, MUST, (112, 465), 10, 3) #O
    
    
def mängijakakskord():
    pygame.draw.line(ekraan, PUNANE, (225, 470), (450, 470), 45)#karbike
    pygame.draw.line(ekraan, VALGE, (0, 470), (225, 470), 45)
    
    pygame.draw.line(ekraan, MUST, (330, 459), (345, 476), 5) #X
    pygame.draw.line(ekraan, MUST, (345, 459), (330, 476), 5)
    
    pygame.draw.circle(ekraan, MUST, (112, 465), 10, 3) #O

def taimeri_karp():
    pygame.draw.line(ekraan, MUST, (0, 515), (450, 515), 45)


def restart():
    global milline_pilt, link, taustapilt, mängija, alusta_aja_lugemist
    alusta_aja_lugemist = pygame.time.get_ticks()  # Nullib taimeri
    milline_pilt += 1
    if milline_pilt == len(piltide_järjend):
        milline_pilt = 0
    link = piltide_järjend[milline_pilt]
    ekraan.blit(taustapildiks(link), (0, 0))
    mängijakakskord()
    joonistame_read()
    for rida in range(3):
        for veerg in range(3):
            board[rida][veerg] = 0
    mängija = 1

    for rida in range(3):
        for veerg in range(3):
            board[rida][veerg] = 0
            
    mängija=1
    
joonistame_read()
mängija = 1
mängulõpp = False

mängijakakskord()
taimeri_karp()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN and not mängulõpp: # Kontrollib kas me klikime ekraanil ja mängu lõppu
            hiirX = event.pos[0] # 0 näitab x koordinaadi
            hiirY = event.pos[1] # 1 näitab y koordinaadi
            
            clicked_rida = int(hiirY // 150) # et koordinaatidest saada indeksid, jagame
            clicked_veerg = int(hiirX // 150)
            
            if mängija == 1:
                mängijaükskord()
            else:
                mängijakakskord()
            
            if kontrolliruutu(clicked_rida, clicked_veerg):
                if mängija == 1:
                    ruudud(clicked_rida, clicked_veerg, 1) # märgime ruudu X-ga
                    if kes_võitis(mängija): # pärast igat käiku kontrollib kas keegi võitis
                        kuva_võidu_teade("X võitis!")
                        mängulõpp = True
                    mängija = 2 # peale käiku vahetame mängijat
                elif mängija == 2: # märgime ruudu O-ga
                    ruudud(clicked_rida, clicked_veerg, 2)
                    if kes_võitis(mängija):
                        kuva_võidu_teade("O võitis!")
                        mängulõpp = True
                    mängija = 1 # siin samuti vahetame mängijat
                if ruudud_on_täis(0, 0) and not mängulõpp:  # Kui kõik ruudud täis ja pole võitjat
                    kuva_võidu_teade("Viik!")  # Kuvame viigi teate
                    mängulõpp = True
                    
                joonista_XO(clicked_rida, clicked_veerg) # kuna ta joonistab viimase märgi pärast võidujoone tegemist, siis see viimane märk on joone peal, mitte selle all.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                restart()
                mängulõpp = False
    kuva_taimer()  # Kuvab taimeri ekraanile
    
    pygame.display.update()
    print(board)



