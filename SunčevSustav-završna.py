#kada se simulacija pkrene pojaviti će se prozor pygamea te je potrebno pritisnuti - u gornjem desnom kutu, NE isključiti program, i upisati koliko se planeta želi dodati (upisati 0 ako se ne želi dodati planete)
#kada se unesu podaci za nove planete ili 0 ako se ne želi unijeti novi planet potrebno je otvoriti prozor pygamea gdje se pojavi simulacija
import pygame
import math
import random

pygame.init()
širina, visina = 1000, 800
screen = pygame.display.set_mode((1000, 800))

FONT_1 = pygame.font.SysFont("Trebuchet MS", 21)
FONT_2 = pygame.font.SysFont("Trebuchet MS", 16)



class Planet:
    G = 6.67*10**-11
    AU = 149597870700
    t = 60 * 60 * 24  #ubrzava stvarno virjeme
    omjerudaljenosti = 10000/AU
    

    def __init__(self, x, y, r, boja, m):
        self.x = x
        self.y = y
        self.r = r
        self.boja = boja
        self.m = m
        self.svekord = []
        self.sunce = False
        self.UDALJENOST = 0 #udaljenost planeta od sunca
        self.brzinax = 0
        self.brzinay = 0

    def draw(self, screen, prikaži, pomakni_x, pomakni_y, linija):
        #stavlja sliku u sredinu
        x = self.x * self.omjerudaljenosti + širina / 2
        y = self.y * self.omjerudaljenosti + visina / 2
        if len(self.svekord) > 2:
            novekord = []
            for point in self.svekord:
                x, y = point
                x = x * self.omjerudaljenosti + širina / 2
                y = y * self.omjerudaljenosti + visina / 2
                
                novekord.append((x + pomakni_x, y +pomakni_y))
            if linija:
                pygame.draw.lines(screen, self.boja, False, novekord, 1)
        pygame.draw.circle(screen, self.boja, (x + pomakni_x, y + pomakni_y), self.r)
        if not self.sunce:
            #ispisuje udaljenosti
            t1 = FONT_2.render(f"{(round(self.UDALJENOST, 2))} ", True,
                                          bijela)
            if prikaži:
                screen.blit(t1, (x - t1.get_width() / 2 + pomakni_x,
                                            y - t1.get_height() / 2 - 20 + pomakni_y))

    def Gsila(self, novi):
        novi_x, novi_y = novi.x, novi.y
        udaljenost_x = novi_x - self.x
        udaljenost_y = novi_y - self.y
        udaljenost = math.sqrt(udaljenost_x ** 2 + udaljenost_y ** 2) #računa udaljenost između dva ojekta u svemiru preko njiovih koordinata x i y
        if novi.sunce:
            self.UDALJENOST = udaljenost
        sila = self.G * self.m* novi.m / udaljenost ** 2 #računa gravitacijsku silu
        alfa = math.atan2(udaljenost_y, udaljenost_x) #računa kut između udaljenosti 2 ojekta, udaljenost na y osi i udaljenost na x osi
        sila_x = math.cos(alfa) * sila
        sila_y = math.sin(alfa) * sila
        return sila_x, sila_y

    def novepozicije(self, planeti):
        svi_silax = svi_silay = 0
        for planet in planeti:
            if self == planet:
                continue
            silax, silay = self.Gsila(planet)
            #zbraja sile
            svi_silax += silax
            svi_silay += silay
        self.brzinax += svi_silax / self.m * self.t #F=ma, a=v/t
        self.brzinay += svi_silay / self.m * self.t
        self.x += self.brzinax * self.t
        self.y += self.brzinay * self.t
        self.svekord.append((self.x, self.y))

    def noviomjer(self, omjer2):
        self.r *= omjer2

bijela = (255,255,255)
žuta = (255, 215, 0)
plava = (0, 102, 204)
narančasta = (255, 153, 0)
siva = (150, 150, 150)
crvena = (205, 92, 92)
smeđa1 = (210, 105, 30)
smeđa2 = (218, 165, 32)
plava2 = (2, 119, 189)
tamnoplava = (26, 35, 126)
crna = (0, 0, 0)
planeti = []


def main():
    run=False
    brojPlaneta = int(input("Koliko planeta želite dodati: "))
    #dodaje planete
    if brojPlaneta > 0:
        for p in range(brojPlaneta):
            kordx = float(input("Unesite koordinatu x: "))
            kordy = float(input("Unesite koordinatu y: "))
            masa = int(input("Unesite masu planeta: "))
            radius = float(input("Unesite radijus planeta: "))
            by = int(input("upiši brzinu planeta"))
            
            b1 = random.randint(0, 255)
            b2 = random.randint(0, 255)
            b3 = random.randint(0, 255)
            bojan = (b1, b2, b3)
            
            noviplanet = Planet(kordx * Planet.AU, kordy * Planet.AU, radius * 10**-3, bojan, masa)
            noviplanet.brzinay=by

            planeti.append(noviplanet)
        
        run=True
    else:
        run=True
                

    pause = False
    prikaži_udaljenost = False
    clock = pygame.time.Clock()
    pomakni_x = 0
    pomakni_y = 0
    linija = True


    sunce = Planet(0, 0, 696000 *10**-1/50, žuta, 1.98892 * 10 ** 30)
    planeti.append(sunce)
    sunce.sunce = True
    merkur = Planet(-0.387 * Planet.AU, 0, 2439.5 /50 , siva, 3.30 * 10 ** 23)
    merkur.brzinay = 47.4 * 1000
    planeti.append(merkur)
    venera = Planet(-0.723 * Planet.AU, 0, 6052/50, narančasta, 4.8685 * 10 ** 24)
    venera.brzinay = 35.02 * 1000
    planeti.append(venera)
    zemlja = Planet(-1 * Planet.AU, 0, 6378 /50 , plava, 5.9722 * 10 ** 24)
    zemlja.brzinay = 29.783 * 1000
    planeti.append(zemlja)
    mars = Planet(-1.524 * Planet.AU, 0, 1737.5 /50, crvena, 6.39 * 10 ** 23)
    mars.brzinay = 24.077 * 1000
    planeti.append(mars)
    jupiter = Planet(-5.204 * Planet.AU, 0, 71492/60, smeđa1, 1.898 * 10 ** 27)
    jupiter.brzinay = 13.06 * 1000
    planeti.append(jupiter)
    saturn = Planet(-9.573 * Planet.AU, 0, 60268 /60, smeđa2, 5.683 * 10 ** 26)
    saturn.brzinay = 9.68 * 1000
    planeti.append(saturn)
    uran = Planet(-19.165 * Planet.AU, 0, 25559 /50, plava2, 8.681 * 10 ** 25)
    uran.brzinay = 6.80 * 1000
    planeti.append(uran)
    neptun = Planet(-30.178 * Planet.AU, 0, 24764 *50**-1 , tamnoplava, 1.024 * 10 ** 26)
    neptun.brzinay = 5.43 * 1000
    planeti.append(neptun)
    

    while run:
        clock.tick(60)
        screen.fill(crna)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and
                                             (event.key == pygame.K_x or event.key == pygame.K_ESCAPE)):
                run = False

            #pritiskom na tipku u prikazuju se udaljenosti
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                prikaži_udaljenost = not prikaži_udaljenost

            #dozvoljava korisniku povećavanje i smanjivanje slike
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                Planet.omjerudaljenosti *= 0.75
                for planet in planeti:
                    planet.noviomjer(0.75)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                Planet.omjerudaljenosti *= 1.25
                for planet in planeti:
                    planet.noviomjer(1.25)

        keys = pygame.key.get_pressed()

        udaljenost = 10
        #dozvoljava korisniku pomicanje slike strelicama
        if keys[pygame.K_LEFT]:
            pomakni_x += udaljenost
        if keys[pygame.K_RIGHT]:
            pomakni_x -= udaljenost
        if keys[pygame.K_UP]:
            pomakni_y += udaljenost
        if keys[pygame.K_DOWN]:
            pomakni_y -= udaljenost

        for planet in planeti:
            if not pause:
                planet.novepozicije(planeti)
            if prikaži_udaljenost:
                planet.draw(screen, 1, pomakni_x, pomakni_y, linija)
            else:
                planet.draw(screen, 0, pomakni_x, pomakni_y, linija)


        tekst1 = FONT_1.render("Za prikazati udaljenosti među planetima pritisni u", True, bijela)
        screen.blit(tekst1, (15, 45))

        tekst3= FONT_1.render("Može se zoomirati i pomicati stremicama", True, bijela,)
        screen.blit(tekst3, (15, 75))

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
