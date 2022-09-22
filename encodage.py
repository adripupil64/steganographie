import PIL.Image

### Entree et verification de l'image et du message ###
#fileMessage = 'message'
#filePic = 'white'
fileMessage = input('Adresse du fichier texte (.txt):')


f = open('txts/'+ fileMessage + '.txt')
message = f.read()

f.close()

if len(message) >= 2**15:
    raise Exception("Taille de message trop grande (>32767 symboles)")
elif len(message) == 0:
    raise Exception("Le fichier .txt est vide")

filePic = input("Adresse du l' image initiale (.png):")
img = PIL.Image.open('pngs/'+ filePic + '.png')
largeur, hauteur = img.size

if 3*largeur*hauteur <= len(message)*8:
    raise Exception ("Resolution de photo insuffisante pour la taille du texte")


### Encodage en Unicode des lettres ###
binLetters = []
for letter in message:
    binCode = bin(ord(letter))
    binCode = binCode[:2] + (10 - len(binCode)) * '0' + binCode[2:] #Ajout de 0s pour normaliser la longeur de chaque element à 10 (0b inclus)

    binLetters.append((binCode))



### Recuperation des valeurs RVB de chaque pixels ###
binPixels = []
nbPixelsRestants = len(message)*8
for y in range(hauteur):
    if nbPixelsRestants < largeur:
        largeurParcours = nbPixelsRestants
    else:
        largeurParcours = largeur
    for x in range(largeurParcours):
        rvb = img.getpixel((x, y))
        for i in range(3):
            binPixels.append(bin(rvb[i]))
    nbPixelsRestants -= largeur
    if nbPixelsRestants < 0:
        break




### Encodage de la longeur du message ###
newBinPixels = []
binLength = bin(len(message))[2:]
binLength = (15-len(binLength))* '0' + binLength #Ajout de 0s pour que binLength soit de taille 15 (0b compris)

for i in range(15):
    newBinPixels.append(binPixels[i][:-1] + binLength[i]) #Encodage de la taille du message dans les codes RVB des 5 premiers pixels





### Encodage des lettres ###
posInBinPixels = 15 #On commence l'encodage à l'indice 15 (6eme pixel)

for elt in binLetters:
    for i in range(2, len(elt)):
        originalVal = binPixels[posInBinPixels]
        encodedVal = originalVal[:-1] + elt[i] #Le bit de pois faible (dernier element de la chaine) est remplace par les valeurs de chaque element de la lettre binLetters (elt)
        newBinPixels.append(encodedVal)


        posInBinPixels += 1

posInNewBinPixels = 0
exit = False
for y in range(hauteur):
    for x in range(largeur):
        rvb = img.getpixel((x, y))
        newRvb = []
        for i in range(3):
            if posInNewBinPixels < len(newBinPixels):
                newRvb.append(int(newBinPixels[posInNewBinPixels], 2))
                posInNewBinPixels += 1
            else:
                exit = True
                break
        if exit:
            break
        tupleRvb = tuple(newRvb)
        if len(tupleRvb) == 3:
            img.putpixel((x, y), tupleRvb)
    if exit:
        break


            
    









### Sauvegarde de la nouvelle image et affichage de celle-ci ###
img.save('out.png')
img.close()

print(f"Le message a été encodé dans l'image out.png avec succes")
img = PIL.Image.open('out.png')

img.show()
