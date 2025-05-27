from pyautogui import press
import pygame
import sys


pygame.init()
WIDTH, HEIGHT = 700, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("YOU LOST ALL YOUR MONEY, farm met boerin Cynthia om terug geld te verdienen!") 

# Kleuren
GROEN = (34, 139, 34)
BRUIN = (139, 69, 19)
grijs = (150, 150, 150)
ZWART = (0, 0, 0)
WIT = (255, 255, 255)

font = pygame.font.SysFont(None, 24)

# Geld
geld = 1
vak_size = 80
margin = 10
ontgrendeld = 1

# Zaadtypes
zaden = {
    "Wortel": {"kleur": (255, 165, 0), "kost": 1, "opbrengst": 1.5 , "groei": 2},
    "Maïs": {"kleur": (255, 255, 0), "kost": 10, "opbrengst": 13, "groei": 3},
    "Aardbei": {"kleur": (255, 0, 100), "kost": 15, "opbrengst": 35, "groei": 4}
}
gekozen_zaad = "Wortel"

# Raster
raster = []

def bereken_rect(index):
    kol = index % 5
    rij = index // 5
    x = kol * (vak_size + margin) + 180
    y = rij * (vak_size + margin) + 80
    return pygame.Rect(x, y, vak_size, vak_size)

def nieuw_vak():
    return {
        "rect": bereken_rect(len(raster)),
        "geplant": False,
        "groei": 0,
        "zaad": None
    }

for i in range(25):
    raster.append(nieuw_vak())

# UI
def toon_tekst(tekst, x, y):
    t = font.render(tekst, True, ZWART)
    screen.blit(t, (x, y))

def kost_voor_volgend_vak():
    return 10 * ontgrendeld

def teken_vak(vak, actief):
    rect = vak["rect"]
    if not actief:
        pygame.draw.rect(screen, grijs, rect)
        pygame.draw.line(screen, ZWART, rect.topleft, rect.bottomright, 2)
        pygame.draw.line(screen, ZWART, rect.topright, rect.bottomleft, 2)
        return

    if not vak["geplant"]:
        pygame.draw.rect(screen, BRUIN, rect)
    else:
        zaadinfo = zaden[vak["zaad"]]
        groeistadium = vak["groei"] / zaadinfo["groei"]
        kleur = tuple(min(255, int(c * groeistadium + 100)) for c in zaadinfo["kleur"])
        pygame.draw.rect(screen, kleur, rect)

# Game loop
clock = pygame.time.Clock()
while True:
    screen.fill((220, 255, 220))

    # UI-knoppen voor zaden
    x_knop = 10
    for naam in zaden:
        kleur = zaden[naam]["kleur"]
        knop = pygame.Rect(x_knop, 10, 150, 30)
        pygame.draw.rect(screen, kleur, knop)
        pygame.draw.rect(screen, ZWART, knop, 2)
        toon_tekst(f"{naam} ({zaden[naam]['kost']}euro)", x_knop + 5, 15)
        if pygame.mouse.get_pressed()[0] and knop.collidepoint(pygame.mouse.get_pos()):
            gekozen_zaad = naam
        if gekozen_zaad == naam:
            pygame.draw.rect(screen, ZWART, knop, 3)
        x_knop += 160

    toon_tekst(f"Geld: {geld}", 10, 50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, vak in enumerate(raster):
                rect = vak["rect"]
                actief = i < ontgrendeld
                if rect.collidepoint(event.pos):
                    if actief:
                        if event.button == 1:
                            if vak["geplant"] and vak["groei"] >= zaden[vak["zaad"]]["groei"]:
                                geld += zaden[vak["zaad"]]["opbrengst"]
                                vak["geplant"] = False
                                vak["groei"] = 0
                                vak["zaad"] = None
                            elif not vak["geplant"]:
                                kost = zaden[gekozen_zaad]["kost"]
                                if geld >= kost:
                                    geld -= kost
                                    vak["geplant"] = True
                                    vak["groei"] = 0
                                    vak["zaad"] = gekozen_zaad
                        elif event.button == 3:
                            if vak["geplant"] and vak["groei"] < zaden[vak["zaad"]]["groei"]:
                                vak["groei"] += 1
                    else:
                        kosten = kost_voor_volgend_vak()
                        if i == ontgrendeld and geld >= kosten:
                            geld -= kosten
                            ontgrendeld += 1

    # Raster tekenen
    for i, vak in enumerate(raster):
        teken_vak(vak, i < ontgrendeld)

    if ontgrendeld < len(raster):
        toon_tekst(f"Klik grijs vak ({kost_voor_volgend_vak()}euro) om uit te breiden", 10, HEIGHT - 30)

    pygame.display.flip()
    clock.tick(30)
