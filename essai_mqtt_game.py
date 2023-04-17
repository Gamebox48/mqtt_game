from likeprocessing.processing import *
from mqtt_game import MqttGame

ihm = IhmScreen()
nb_joueurs_maxi = 3
nb_joueur_mini = 2
joueur = "Gauche"
mqtt_broker = "mqtt.eclipseprojects.io"
jeu = MqttGame(mqtt_broker, "mygamebox", joueur, nb_joueurs_maxi, nb_joueur_mini)
tour = 0


def deco():
    global tour
    # if tour != 0 and jeu.player == jeu.player_list[tour-1]:
    #     tour = tour % (jeu.nb_joueurs-1)+1
    #     jeu.send(tour)
    jeu.deconnect()
    set_quit(True)


def jouer():
    jeu.to_hand_over()


def ppc(name):
    print(name)


def lancer():
    global nb_joueurs_maxi
    if len(jeu.player_list) > 1:
        jeu.start_game = True
        jeu.start_room_game()
        nb_joueurs_maxi = jeu.nb_joueur_maxi


def setup():
    createCanvas(400, 200)
    background("grey")
    ihm.init()
    ihm.addObjet(MultiLineText(ihm, (10, 10, 380, 100), str(jeu), stroke="black"), "afficheur")
    ihm.addObjet(Bouton(ihm, (10, 120, 50, 20), "déconnection", command=deco), "deco")
    ihm.addObjet(Bouton(ihm, (10, 120, 50, 20), "jouer", command=jouer, disabled=True), "jouer")
    ihm.addObjet(Bouton(ihm, (10, 120, 50, 20), "pierre", command=ppc, name="pierre", disabled=True), "pierre")
    ihm.addObjet(Bouton(ihm, (10, 120, 50, 20), "papier", command=ppc, name="papier", disabled=True), "papier")
    ihm.addObjet(Bouton(ihm, (10, 120, 50, 20), "ciseaux", command=ppc, name="ciseaux", disabled=True), "ciseaux")
    ihm.addObjet(Bouton(ihm, (10, 120, 50, 20), "lancer", command=lancer, visible=False), "lancer")
    ihm.pack(["afficheur", ["deco", "jouer"], ["pierre", "papier", "ciseaux"], "lancer"], expand="X", pady=2)

    title(jeu.player)
    jeu.loop_start()


def compute():
    global tour
    ihm.scan_events()
    ihm.objet_by_name("afficheur").text(str(jeu))
    if jeu.master:
        ihm.objet_by_name("lancer").visible = True
    else:
        ihm.objet_by_name("lancer").visible = False
    if jeu.all_connected:
        if jeu.hand_is_me():
            ihm.objet_by_name('jouer').disabled = False
        else:
            ihm.objet_by_name('jouer').disabled = True

def draw():
    ihm.draw()
    if not jeu.all_connected:
        text("Attente des autres joueurs", 10, 160, 100, 30)
    else:
        try:
            text(f"à {jeu.courant_player()}\nde jouer", 10, 160, 100, 30)
        except:
            print(tour, jeu.player_list)
            raise IndexError


run(globals())
