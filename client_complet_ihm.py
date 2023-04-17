"""mini chat a deux personnes:
 dés que deux instances du programme sont lancées la connection s'établie sous
 réserve que les identifiant des joueurs soit différents
 Procedure d'essai dans le terminal pycharm:
 lancer :
 python.exe .\client_complet_ihm.py joueur1
python.exe .\client_complet_ihm.py joueur2
 """

from likeprocessing.processing import *
import paho.mqtt.client as mqtt
import sys


if len(sys.argv) == 1:
    joueur = "joueur1"
else:
    joueur = sys.argv[1]
# initialisation de mqtt
mqtt_broker = "mqtt.eclipseprojects.io"
client = mqtt.Client(joueur)
client.connect(mqtt_broker)
client.subscribe("mygamebox")
client.loop_start()
# creation de l'ihm
ihm = IhmScreen()
liste_des_joueurs = set()
liste_des_joueurs.add(joueur)
connecte = False


def on_message(client, userdata, message):
    global connecte, liste_des_joueurs
    msg = str(message.payload.decode('utf-8'))
    print(msg)
    msg = msg.split(":")
    liste_des_joueurs.add(msg[0])
    if len(liste_des_joueurs) == 2:
        if connecte is False:
            client.publish("mygamebox", f"{joueur}:{liste_des_joueurs}")
            connecte = True
        else:
            liste_des_joueurs = eval(f"set({msg[1]})")
    if len(msg) == 3 and msg[0] != joueur:
        ihm.objet_by_name("reception").text(msg[2])


client.on_message = on_message


def envoyer():
    client.publish("mygamebox", f"{joueur}:{liste_des_joueurs}:{ihm.objet_by_name('envoie').text()}")


def setup():
    createCanvas(400, 200)
    title(joueur)
    background("grey")
    # initialisation de l'ihm
    ihm.init()
    ihm.addObjet(Bouton(ihm, (10, 50, 100, 30), "envoyer", command=envoyer), "envoyer")
    ihm.addObjet(LineEdit(ihm, (10, 90, 100, 30), "", stroke="black"), "envoie")
    ihm.addObjet(Label(ihm, (10, 130, 100, 30), "", stroke="black"), "reception")
    ihm.pack(["envoyer", "envoie", "reception"], expand="X")
    ihm.disabled(["envoyer", "envoie"])
    client.publish("mygamebox", f"{joueur}:{liste_des_joueurs}")


def exit():
    liste_des_joueurs.remove(joueur)
    client.publish("mygamebox", f"{joueur}:{liste_des_joueurs}")


def compute():
    global connecte
    if len(liste_des_joueurs) == 2:
        ihm.enabled(["envoyer", "envoie"])
        connecte = True
    else:
        ihm.disabled(["envoyer", "envoie"])
        connecte = False
    ihm.scan_events()


def draw():
    ihm.draw()


run(globals())
client.loop_stop()
