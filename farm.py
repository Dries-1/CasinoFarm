import pygame
import sys

# Initialisatie
pygame.init()
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("grow a garden met boer Harrie")

# Kleuren
GROEN = (34, 139, 34)
BRUIN = (139, 69, 19)
WIT = (255, 255, 255)
GRAAG = (150, 150, 150)
ZWART = (0, 0, 0)

font = pygame.font.SysFont(None, 24)

# Instellingen
geld = 10
MAX_GROEI = 3
vak_size = 80
margin = 10

# Vakjeslijst
raster = []
ontgrendeld = 1 # Start met 1 vakje

def bereken_rect(index):
    kol = index % 5
    rij = index // 5
    x = kol * (vak_size + margin) + 50
    y = rij * (vak_size + margin) + 70
    return pygame.Rect(x, y, vak_size, vak_size)

def nieuw_vak():
    rect = bereken_rect(len(raster))
    return {
        "rect": rect,
        "geplant": False,
        "groei": 0
    }

# Start met 25 mogelijke vakjes (5x5 grid)
for i in range(25):
    raster.append(nieuw_vak())

def teken_vak(vak, actief):
    rect = vak["rect"]
    if not actief:
        pygame.draw.rect(screen, GRAAG, rect)
        pygame.draw.line(screen, ZWART, rect.topleft, rect.bottomright, 2)
        pygame.draw.line(screen, ZWART, rect.topright, rect.bottomleft, 2)
        return

    if not vak["geplant"]:
        pygame.draw.rect(screen, BRUIN, rect)
    elif vak["groei"] == 0:
        pygame.draw.rect(screen, GROEN, rect)
    elif vak["groei"] == 1:
        pygame.draw.rect(screen, (0, 180, 0), rect)
    elif vak["groei"] == 2:
        pygame.draw.rect(screen, (0, 200, 0), rect)
    elif vak["groei"] >= MAX_GROEI:
        pygame.draw.rect(screen, (255, 165, 0), rect)

def toon_tekst(tekst, x, y):
    tekst_oppervlak = font.render(tekst, True, ZWART)
    screen.blit(tekst_oppervlak, (x, y))

def kost_voor_volgend_vak():
    return 10 * ontgrendeld

# Game loop
clock = pygame.time.Clock()
while True:
    screen.fill((220, 255, 220))  # achtergrond

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
                            # Oogsten als volgroeid
                            if vak["geplant"] and vak["groei"] >= MAX_GROEI:
                                vak["geplant"] = False
                                vak["groei"] = 0
                                geld += 10
                            # Planten
                            elif not vak["geplant"] and geld >= 5:
                                vak["geplant"] = True
                                vak["groei"] = 0
                                geld -= 5
                        elif event.button == 3:
                            if vak["geplant"] and vak["groei"] < MAX_GROEI:
                                vak["groei"] += 1
                    else:
                        kosten = kost_voor_volgend_vak()
                        if i == ontgrendeld and geld >= kosten:
                            ontgrendeld += 1
                            geld -= kosten

    # Tekenen
    for i, vak in enumerate(raster):
        actief = i < ontgrendeld
        teken_vak(vak, actief)

    # Info
    toon_tekst(f"Geld: {geld} munten", 10, 10)
    toon_tekst("Links: planten/oogsten | Rechts: water geven", 10, 30)

    if ontgrendeld < len(raster):
        volgende_kost = kost_voor_volgend_vak()
        toon_tekst(f"Klik op grijs vakje ({volgende_kost} munten) om uit te breiden", 10, 50)

    pygame.display.flip()
    clock.tick(30)
