# -*- coding: utf-8 -*-
import time
import random # random.choice()

def tulosta_kentta(nakyva_kentta):
	"""Tulostaa pelaajalle kaksiuloitteisen kentän näkyville."""
	for i in nakyva_kentta:
		print("".join(i))

def miinoita_satunnainen(piilo_kentta,jaljella):
	"""Miinoittaa yhden satunnaisen ruudun annetun kaksiulotteisen kenttälistan vapaista koordinaateista."""
	kord = random.choice(jaljella)
	piilo_kentta[kord[1]][kord[0]] = "m"
	return kord

def numero_taulukko(x, y, piilo_kentta):
	"""Käsittelee piilo_taulukon jokaista alkiota ja laskee niiden alkkioiden ympäroivien miinojen lukumäärää. Summan laskettua
	funktio lisää arvon miinataulukkoon."""
	luku_taulu = []
	for ye in [-1, 0, 1]:
		for xe in [-1,0,1]:
			if (y - ye) < 0 or (x - xe) < 0:
				continue
			else:
				try:
					piilo_kentta[y - ye][x - xe]
				except IndexError:
					pass
				else:
					if piilo_kentta[y - ye][x - xe] == "m":
						luku_taulu.append(1)
	lukusumma = sum(luku_taulu)
	lukusumma = str(lukusumma)
	return lukusumma

def tulvataytto(x, y, piilo_kentta, nakyva_kentta):
	"""Ottaa vastaan annettut koordinaatit ja käsittelee piilo_kentta niin että näkyvässä kentässä kaikki tyhjät kentät"""
	if piilo_kentta[y][x] == "1" or piilo_kentta[y][x] == "2" or piilo_kentta[y][x] == "3" or piilo_kentta[y][x] == "4" or piilo_kentta[y][x] == "5" or piilo_kentta[y][x] == "6" or piilo_kentta[y][x] == "7" or piilo_kentta[y][x] == "8":
		nakyva_kentta[y][x] = piilo_kentta[y][x]
		return
	if piilo_kentta[y][x] == "0":
		piilo_kentta[y][x] = "-"
		nakyva_kentta[y][x] = "-"
		if x > 0:
			tulvataytto(x - 1, y, piilo_kentta, nakyva_kentta) # vasemmalle
		if x < len(piilo_kentta[y]) - 1:
			tulvataytto(x + 1, y, piilo_kentta, nakyva_kentta) # oikealle
		if y > 0:
			tulvataytto(x, y - 1, piilo_kentta, nakyva_kentta) # ylös
		if y < len(piilo_kentta) - 1:
			tulvataytto(x, y + 1, piilo_kentta, nakyva_kentta) # alas
		
def tietojen_tallennus(min, sek, kierros, tulos, koko, miina_luku):
	"""Jäljellä olevien miinojen, avattujen ruutujen ja ajan tallentamista tekstitiedostoon."""
	tiedoston_nimi = time.strftime("%Y%m%d_%H_%M_%S") + ".txt"
	tiedosto = open(tiedoston_nimi, "w")
	tiedosto.write("aika: %d min %d sek \n kierroksien määrä:%d \n pelitilanne:%s \n kentän koko: %s \n miinojen lukum.: %d" % (min, sek, kierros,tulos, koko,miina_luku ))
	tiedosto.close()

def tarkistus(nakyva_kentta, miina_luku):
	"""Tarkistaa loopin lopussa onko avattavia ruutuja enään jäljellä."""
	ruudut = []
	for i in nakyva_kentta:
		for j in nakyva_kentta:
			if j == "o":
				ruudut.append(1)
	luku_1 = sum(ruudut)
	if luku_1 == miina_luku:
		return True

#Pääohjelma:

miina_luku = int(input("Kuinkas paljon miinoja laitetaan?: "))
leveys_x = int(input("Kuinka leveä kenttä(x)?: "))
pituus_y = int(input("Minkä pituinen(y)?: "))
nakyva_kentta = [["o" for i in range(leveys_x)] for i in range(pituus_y)]
piilo_kentta = [["t" for i in range(leveys_x)] for i in range(pituus_y)]
jaljella = [] #Aputaulukko miinojen sijoittamiseen. Random.choice funktion saman koordinaattien valinnan välttämiseen.
kierros = 0
koko = "%dx%d" % (leveys_x, pituus_y)
for x in range(leveys_x):
	for y in range(pituus_y):
		jaljella.append((x, y))

tulosta_kentta(nakyva_kentta)

for i in range(miina_luku):				#Sijoitetaan miinat piilokenttään
	kord = miinoita_satunnainen(piilo_kentta,jaljella)
	jaljella.remove(kord)
	
for y in range(len(piilo_kentta)):				#Sijoitetaan numerot piilokenttään
	for x in range(len(piilo_kentta[0])):
		if piilo_kentta[y][x] != "m":
			piilo_kentta[y][x] = numero_taulukko(x, y, piilo_kentta)
#Ajan mittaus
aloitus_aika = time.time()

while True:		
	
	#Kysytään koordinaatit pelaajalta.
	koordinaatit = input("Lopettaakseen pelin paina (q). Anna koordinaatit muodossa x,y: ")
	if koordinaatit == "q":
		break
	else:
		koordinaatit = koordinaatit.split(",")	#Sijoitetaan koordinaatit omiin muuttujiin
		x = int(koordinaatit[0])
		y = int(koordinaatit[1])
	if piilo_kentta[y][x] == "m":
		print("KHA-BOOM! Osuit miinaan")
		kulunut_aika = time.time() - aloitus_aika
		tulos = "kuolit..."
		min = kulunut_aika / 60
		sek = kulunut_aika % 60
		print("%d minuuttia %d sekuntia ja kierroksia %d. Pelitulos tallennettu" % (min, sek,kierros))
		tietojen_tallennus(min, sek, kierros, tulos, koko, miina_luku)
		break
	tulvataytto(x, y, piilo_kentta, nakyva_kentta)
	tulosta_kentta(nakyva_kentta)
	
	if tarkistus(nakyva_kentta, miina_luku) == True:
		print("HYVÄ! Löysit kaikki miinat!")
		kulunut_aika = time.time() - aloitus_aika
		tulos = "Selvisit hengissä"
		min = kulunut_aika / 60
		sek = kulunut_aika % 60
		print("%d minuuttia %d sekuntia ja kierroksia %d. Pelitulos tallennettu" % (min, sek, kierros))
		tietojen_tallennus(min, sek, kierros, tulos, koko, miina_luku)
		break
	kierros += 1












































