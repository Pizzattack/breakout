# -*- coding: utf-8 -*-
import pyxel
import random

###
# Initialisation de pyxel et des ressources
###########################################

pyxel.init(width=400, height=300, title="Breakout",display_scale=3,fps=30)
pyxel.load("breakout.pyxres")
pyxel.colors[8] = 0XFF0000

pyxel.images[1].load(0, 0, "skull.png")

###
# Initialisation des variables
##################################

# Drapeau pour dire si la balle boue ou pas
playstate = False
# Drapeau pour dire si on a fini le niveau ou s'il reste des briques
winstate  = False
# Drapeau pour dire si on a perdu la balle
losestate = False
# Position en X et en Y de la balle
ballX = int(pyxel.width/2)
ballY = int(pyxel.height/2)
# Position X/Y et largeur raquette raquette
paddleX = 0
paddleY = pyxel.height-18
paddleW = 5 # la largeur complète est 16 + W x 8 pixels
# Position de la balle en X/Y
ballX = 0
ballY = 0
# Viesse de la balle en X/Y
ballvitX = 0
ballvitY = 0
# Score et vies
myscore = 0
lives = 3
# Liste vide des briques du tableau
briques = []
# Numéro du niveau actuel
lvl = 0

###
# Génération d'un nouveau niveau
##################################
def newLevel():
    global briques,lvl
    lvl = lvl + 1
    for i in range (min(80,20*lvl)):
#    for i in range (1):
        overlap = True
        while(overlap):
            x = random.randint(10,pyxel.width-8*3-20)
            y = random.randint(30,pyxel.height-8*3-120)
            t = 1
            if (random.randint(1,10)>7):
                t = 2
            if (random.randint(1,10)>9):
                t = 3
            overlap=False
            for j in range(0,len(briques)):
                x2,y2,t2 = briques[j]
                if (abs(x-x2)<24) and (abs(y-y2)<12):
                    overlap=True
        briques.append ( [ x,y,t ] )

###
# Calculs avant d'afficher
##################################
def update():
    # Récupération des variables globales
    global myscore, playstate, winstate, losestate, lives 
    global ballX, ballY
    global ballvitX, ballvitY
    global paddleX, paddleY, paddleW
    global briques
    
    # Détection de la touche échap pour arrêter le  jeu
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()
       
    # Déplacement raquette
    paddleX = pyxel.mouse_x
    
    # Si on ne joue pas
    if (not playstate):
        # La balle suit la raquette
        ballX = paddleX + (1+paddleW)*4
        ballY = paddleY-8
        
        # Détection de toucher démarrer
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            # On débloque le déplacement de la balle
            playstate=True
            # Musique départ
            pyxel.play(2,6)
            # Si on était dans l'état perdu, on réunitialise tout
            if (losestate):
                myscore = 0
                briques=[]
                newLevel()
                lives = 3
                losestate = False
                playstate=False
            # Si on avait fini le niveau, on génère un nouveau niveau et on repart
            elif (winstate):
                newLevel()
                winstate=False       
            # Vitesse en X et en Y de la vitesse
            ballvitX = random.randint(3,5)
            ballvitY = random.randint(3,5)
            
    # Si on  joue    
    else:
        
        # Rebond sur la raquette
        if (ballY+8>=paddleY) and ((ballX+8>paddleX) and (ballX<=paddleX+8*(2+paddleW))):
            # Son de rebond
            pyxel.play(1,2)
            # On inverse la vitesse en Y
            ballvitY=-ballvitY  
            # La vitesse en X dépend d'où on tape sur la raquette
            ballvitX= ballvitX + ((ballX+4 - paddleX - (paddleW+1)*4)/4)
            # La balle accélère à chaque rebond
            ballvitX = ballvitX * 1.1
            ballvitY = ballvitY * 1.1
            # Mais on limite les vitesses trop grandes
            if (ballvitX>12):
                ballvitX=12
            if (ballvitX<-12):
                ballvitX=-12
            if (ballvitY>8):
                ballvitY=8
            if (ballvitY<-8):
                ballvitY=-8      
                
        # Rebond sur les bords gauche droite
        if (ballX<=0) or (ballX+8>=pyxel.width):
            # Son de rebond
            pyxel.play(1,2)
            # Inversion de la vitesse en X
            ballvitX=-ballvitX
        # Rebond en haut
        if (ballY<=0):
            # Son de bond
            pyxel.play(1,2)
            # Inversion de vitesse Y
            ballvitY=-ballvitY   
            
        # Si la balle sort de l'écran en bas, on arrête de jouer
        if (ballY+8>=pyxel.height):
            # On stoppe le jeu
            playstate = False
            # On perdu une vie
            lives = lives - 1
            # Si on en a plus, on joue un son
            if (lives <= 0):
                losestate = True
            # Son de vie perdue
            pyxel.play(2,4)

        # Boucle sur les briques 
        for i in range(0,len(briques)):
            x,y,t=briques[i]
            # Teste les collisions 
            if (ballX+8>=x) and (ballX<=x+24) and (ballY+8>=y) and (ballY<=y+12):
                # Si on tape sur le haut/bas, on inverse la vitesse en Y
                if (ballX+4>x) and (ballX+4<=x+24):
                    ballvitY=-ballvitY
                # Si on tape sur la gauche/droite, on inverse la vitesse en X
                if (ballY+4>y) and (ballY+4<=y+12):
                    ballvitX=-ballvitX
                # Son de collision
                pyxel.play(1,3)
                # On gagne un point
                myscore = myscore + 1  
                # On actualise la force de la brique
                t=t-1
                briques[i]=[x,y,t]
                # si elle est cassée, on la supprime
                if (t<=0):
                    del briques[i]
                    # Et s'il n'en reste plus du tout on a gagné
                    if (not len(briques)):
                        # Petite musique
                        pyxel.play(2,5)
                        # Etat gagner pour afficher le texte
                        winstate = True
                        # On arrête le jeu
                        playstate = False
                        # On gagne une vie (max 5)
                        lives = lives + 1
                        if lives > 5:
                            lives = 5
                        # On réduit la raquette (avec )
                        paddleW = max (1,paddleW-1)
                    break
            
        # Déplacement de la balle
        ballX = ballX + int(ballvitX)
        ballY = ballY + int(ballvitY)

###
# Affichage d'une frame
##################################
flipstate=8
def draw():
    global ballX, ballY
    global myscore,flipstate
    
    # On efface l'écran
    pyxel.cls(0)
    # Affichage du texte pour le score
    pyxel.text(5,5,"score : "+ str(myscore),9)
    # Affichage de la balle
    if not (pyxel.frame_count % 10):
        flipstate=-flipstate
    pyxel.blt(ballX, ballY, 1, 0, 0, flipstate, 8, 0)
    
    # Affichage de la raquette p(artie gauche, centre, droite)
    pyxel.blt(paddleX, paddleY, 0, 8, 0, 8, 8, 0)
    for i in range(0,paddleW):
        pyxel.blt(paddleX+i*8+8, paddleY, 0, 0, 8, 8, 8, 0)    
    pyxel.blt(paddleX+paddleW*8+8, paddleY, 0, 8, 8, 8, 8, 0)
    
    # Affichage des briques
    for i in range(0,len(briques)):
        x,y,t=briques[i]
        pyxel.blt(x, y, 0, 16, 0+(t-1)*13, 24, 13, 0)

    # AFfichage des coeurs vides, suivi des coeurs pleins
    for i in range(0,5):
        pyxel.blt(pyxel.width - 70+i*13, 5, 0, 40, 0, 12, 10, 0)
    for i in range(0,lives):
        pyxel.blt(pyxel.width - 70+i*13, 5, 0, 51, 0, 12, 10, 0)

    # Texte perdu
    if (losestate):
        text = "You LOSE ! Try gain"
        pyxel.text(pyxel.width/2 - len(text)*2,pyxel.height*3/4-20,text,9)
    # Texte gagné
    if (winstate):
        text = "You WIN !! You gain one life"
        pyxel.text(pyxel.width/2 - len(text)*2,pyxel.height*3/4-20,text,9)
    # Texte démarrer        
    if (not playstate):
        text = "Press SPACE or MOUSE button to start"
        pyxel.text(pyxel.width/2 - len(text)*2,pyxel.height*3/4,text,9)


###
# Programme principal
##################################

# On génère un nouveau niveau de briques
newLevel()
# Et c'est parti
pyxel.run(update, draw)