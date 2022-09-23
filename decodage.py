import PIL.Image

#Entree de l'image et recuperation de la hauteur et de la largeur
filePic = input("Nom du fichier a décoder: ") #Adresse a modifier en cas de deplacement de de la photo de sortie



img = PIL.Image.open(filePic + '.png')
largeur, hauteur = img.size



###Decodage de la longeur du message ###
length = ''
for x in range(5):
    rvb = img.getpixel((x, 0))
    for i in range(3):
        length += bin(rvb[i])[-1]

length = int(length, 2)


###Recuperation des valeurs RVB ###
parcoursBits = 0 #Pour sortir de la boucle une fois un nombre suffisant de codes RVB de pixels parcourus
binPixels = []
for y in range(hauteur):
    for x in range(largeur):
        if x >= 5 or y > 0:

            rvb = img.getpixel((x, y))
            for i in range(3):
                binPixel = bin(rvb[i])[2:]
                binPixels.append((binPixel))
                parcoursBits += 1
    if parcoursBits >= length*8:
        break
            



### Decodage des lettres ###
binLetters = []
letter = ''


for i in range(length*8): # = len(binPixels)
    if len(letter) == 8:
        binLetters.append(chr(int(letter, 2)))
        letter = ""
    letter += binPixels[i][-1]

### Affichage final ###
print("".join(binLetters))
