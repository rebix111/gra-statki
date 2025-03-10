import pygame
import os

pygame.init()
pygame.mixer.init()

szerokosc_okna = 900
wysokosc_okna = 500
okno = pygame.display.set_mode((szerokosc_okna, wysokosc_okna))
pygame.display.set_caption("Gra!")

rekord_rund_zultego = 0
rekord_rund_czerwonego = 0

kolor_bialy = (255, 255, 255)
kolor_czorny = (0, 0, 0)
kolor_czerwont = (255, 0, 0)
zulty_kolor = (255, 255, 0)

przesuniencie = 5
wysokosc_statku, szerokosc_statku = 55, 40
poruszanie_pociskow = 14
border = pygame.Rect(szerokosc_okna / 2 - 5, 0, 10, wysokosc_okna)
narysuj_zdrowie = pygame.font.SysFont('comicsans', 30)
max_naboje = 3
zulty_udezony = pygame.USEREVENT + 1
czerwony_udezony = pygame.USEREVENT + 2

#dziwienk_pocisku = pygame.mixer.Sound('projekt_gry\\dziwięki\\Grenade+1.mp3')
#ogien_pocisku = pygame.mixer.Sound('projekt_gry\\dziwięki\\Gun+Silencer.mp3')
#sound_track = pygame.mixer.Sound('projekt_gry\\dziwięki\\pixel-perfect-112527.mp3')

#dziwienk_pocisku.set_volume(0.1)
#ogien_pocisku.set_volume(0.1)
#sound_track.set_volume(0.1)

zdrowie_zultego = 10
zdrowie_czerwonego = 10

zuty_statek = pygame.image.load(
    os.path.join('projekt_gry','tekstury', 'spaceship_yellow.png'))
zuty_statek = pygame.transform.rotate(pygame.transform.scale(zuty_statek, (wysokosc_statku, szerokosc_statku)), 90)

czerwony_statek = pygame.image.load(
    os.path.join('projekt_gry','tekstury', 'spaceship_red.png'))
czerwony_statek = pygame.transform.rotate(pygame.transform.scale(czerwony_statek, (wysokosc_statku, szerokosc_statku)), 270)

tlo = pygame.image.load(
    os.path.join('projekt_gry','tekstury', 'space.png'))

def wczytaj_liczbe_rund():
    if not os.path.exists('projekt_gry/rounds.txt'):
        with open('projekt_gry/rounds.txt', 'w') as file:
            file.write('0')
        return 0
    else:
        try:
            with open('projekt_gry/rounds.txt', 'r') as file:
                rounds = file.read().strip()
                return int(rounds) 
        except ValueError:  
            print("Błąd wczytywania liczby rund, ustawiono 0")
            return 0

def zapisz_liczbe_rund(liczba_rund):
    with open('projekt_gry/rounds.txt', 'w') as file:
        file.write(str(liczba_rund))

def wyswietl_tekst(tekst, kolor, x, y):
    czcionka = pygame.font.SysFont("comicsans", 70)
    tekst_obiekt = czcionka.render(tekst, True, kolor)
    okno.blit(tekst_obiekt, (x, y))

def okno_config(czerwony, zuty, zuty_pociski, czerwony_pociski, zdrowie_czerwonego, zdrowie_zultego, liczba_rund):
    okno.blit(tlo, (0, 0))
    pygame.draw.rect(okno, kolor_czorny, border)

    zdrowie_czerwonego_tekst = narysuj_zdrowie.render("HP: " + str(zdrowie_czerwonego), 1, kolor_bialy)
    zdrowie_zuletego_tekst = narysuj_zdrowie.render("HP: " + str(zdrowie_zultego), 1, kolor_bialy)
    liczba_rund_tekst = narysuj_zdrowie.render("Rundy na tym komputerze: " + str(liczba_rund), 1, kolor_bialy)

    okno.blit(zdrowie_czerwonego_tekst, (szerokosc_okna - zdrowie_czerwonego_tekst.get_width() - 10, 10))
    okno.blit(zdrowie_zuletego_tekst, (10, 10))
    okno.blit(liczba_rund_tekst, (szerokosc_okna / 2 - liczba_rund_tekst.get_width() / 2, 10))

    okno.blit(zuty_statek, (zuty.x, zuty.y))
    okno.blit(czerwony_statek, (czerwony.x, czerwony.y))

    for pocisku in czerwony_pociski:
        pygame.draw.rect(okno, kolor_czerwont, pocisku)

    for pocisku in zuty_pociski:
        pygame.draw.rect(okno, zulty_kolor, pocisku)
    pygame.display.update()

def kolizja_pocisku(zuty_pociski, czerwony_pociski, zuty, czerwony):
    for pocisk in zuty_pociski:
        pocisk.x += poruszanie_pociskow
        if czerwony.colliderect(pocisk):
            pygame.event.post(pygame.event.Event(czerwony_udezony))
            zuty_pociski.remove(pocisk)
        elif pocisk.x > szerokosc_okna:
            zuty_pociski.remove(pocisk)
    for pocisk in czerwony_pociski:
        pocisk.x -= poruszanie_pociskow
        if zuty.colliderect(pocisk):
            pygame.event.post(pygame.event.Event(zulty_udezony))
            czerwony_pociski.remove(pocisk)
        elif pocisk.x < 0:
            czerwony_pociski.remove(pocisk)

def reset_gra():
    global zdrowie_czerwonego, zdrowie_zultego
    zdrowie_czerwonego = 10
    zdrowie_zultego = 10
    return pygame.Rect(800, 200, szerokosc_statku, wysokosc_statku), pygame.Rect(100, 200, szerokosc_statku, wysokosc_statku), [], []

def zuty_movment(przycisk, zuty):
    if przycisk[pygame.K_a] and zuty.x - przesuniencie > 0:
        zuty.x -= przesuniencie
    if przycisk[pygame.K_d] and zuty.x + przesuniencie + szerokosc_statku < border.x:
        zuty.x += przesuniencie
    if przycisk[pygame.K_w] and zuty.y - przesuniencie > 0:
        zuty.y -= przesuniencie
    if przycisk[pygame.K_s] and zuty.y + przesuniencie + wysokosc_statku < wysokosc_okna:
        zuty.y += przesuniencie

def czerwony_movment(przycisk, czerwony):
    if przycisk[pygame.K_LEFT] and czerwony.x - przesuniencie > border.x + border.width:
        czerwony.x -= przesuniencie
    if przycisk[pygame.K_RIGHT] and czerwony.x + przesuniencie + wysokosc_statku < szerokosc_okna + 20:
        czerwony.x += przesuniencie
    if przycisk[pygame.K_UP] and czerwony.y - przesuniencie > 0:
        czerwony.y -= przesuniencie
    if przycisk[pygame.K_DOWN] and czerwony.y + przesuniencie + wysokosc_statku < wysokosc_okna:
        czerwony.y += przesuniencie

def main():
    global zdrowie_czerwonego, zdrowie_zultego, rekord_rund_zultego, rekord_rund_czerwonego
    liczba_rund = wczytaj_liczbe_rund()

    czerwony = pygame.Rect(800, 200, szerokosc_statku, wysokosc_statku)
    zuty = pygame.Rect(100, 200, szerokosc_statku, wysokosc_statku)

    zuty_pociski = []
    czerwony_pociski = []

    dziala = True
    czas = pygame.time.Clock()

    #sound_track.play(-1)

    while dziala:
        czas.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                dziala = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(zuty_pociski) < max_naboje:
                    pocisk = pygame.Rect(zuty.x + zuty.width, zuty.y + zuty.height / 2 - 2, 10, 5)
                    zuty_pociski.append(pocisk)
                    #dziwienk_pocisku.play()
                if event.key == pygame.K_RCTRL and len(czerwony_pociski) < max_naboje:
                    pocisk = pygame.Rect(czerwony.x, czerwony.y + czerwony.height / 2 - 2, 10, 5)
                    czerwony_pociski.append(pocisk)
                    #dziwienk_pocisku.play()

            if event.type == czerwony_udezony:
                zdrowie_czerwonego -= 1
               #ogien_pocisku.play()
            if event.type == zulty_udezony:
                zdrowie_zultego -= 1
                #ogien_pocisku.play()

        tekst_wygranej = ""
        if zdrowie_czerwonego == 0:
            tekst_wygranej = "Zółty wygrał!"
            rekord_rund_zultego += 1
            liczba_rund += 1
            zapisz_liczbe_rund(liczba_rund)
        if zdrowie_zultego == 0:
            tekst_wygranej = "Czerwoni wygrali!"
            rekord_rund_czerwonego += 1
            liczba_rund += 1
            zapisz_liczbe_rund(liczba_rund)

        if tekst_wygranej != "":
            wyswietl_tekst(tekst_wygranej, kolor_bialy, szerokosc_okna / 2 - 150, wysokosc_okna / 2 - 30)
            pygame.display.update()
            pygame.time.delay(2000)  
            czerwony, zuty, zuty_pociski, czerwony_pociski = reset_gra()  
        kolizja_pocisku(zuty_pociski, czerwony_pociski, zuty, czerwony)

        przycisk = pygame.key.get_pressed()
        zuty_movment(przycisk, zuty)
        czerwony_movment(przycisk, czerwony)
        okno_config(czerwony, zuty, zuty_pociski, czerwony_pociski, zdrowie_czerwonego, zdrowie_zultego, liczba_rund)


if __name__ == "__main__":
    main()
