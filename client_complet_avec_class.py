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
from random import randint


class MqttGame(mqtt.Client):
    def __init__(self, broker: str, subscribe_name: str, player: str = "joueur", nb_joueurs=2):
        player += "".join([str(randint(0, 9)) for i in range(5)])
        super().__init__(player)
        self.subscribe_name = subscribe_name
        self.nb_joueur = nb_joueurs
        self.all_connected = False
        self.player = player
        self.player_list = set()
        self.player_list.add(self.player)
        self.reception = ""
        self.flag_reception = True
        self.connect(broker)
        self.subscribe(subscribe_name)
        self.publish(self.subscribe_name, f"{self.player}:{self.player_list}")
        self.on_message = self.message

    def message(self, client, userdata, message):
        msg = str(message.payload.decode('utf-8'))
        print(msg)
        msg = msg.split(":")
        self.player_list.add(msg[0])
        if len(self.player_list) == self.nb_joueur:
            if self.all_connected is False:
                self.publish(self.subscribe_name, f"{self.player}:{self.player_list}")
                self.all_connected = True
            else:
                self.player_list = eval(f"set({msg[1]})")
                if len(self.player_list) != self.nb_joueur:
                    self.all_connected = False
        if len(msg) == 3 and msg[0] != joueur:
            self.reception = msg[2]
            self.flag_reception = True

    def recept_message(self) -> bool:
        """retourne True si un nouveau message est reçu"""
        if self.flag_reception:
            self.flag_reception = False
            return True
        return False

    def send(self, message: str):
        self.publish(self.subscribe_name, f"{self.player}:{self.player_list}:{message}")

    def deconnect(self):
        self.player_list.remove(self.player)
        self.publish(self.subscribe_name, f"{self.player}:{self.player_list}:")
        self.all_connected = False


# initialisation de mqtt
joueur = "Pierre"
mqtt_broker = "mqtt.eclipseprojects.io"
jeu = MqttGame(mqtt_broker, "mygamebox", joueur)
# creation de l'ihm
ihm = IhmScreen()


# client.on_message = on_message


def envoyer():
    jeu.send(ihm.objet_by_name('envoie').text())


def setup():
    createCanvas(400, 200)
    title(jeu.player)
    background("grey")
    # initialisation de l'ihm
    ihm.init()
    ihm.addObjet(Bouton(ihm, (10, 50, 100, 30), "envoyer", command=envoyer), "envoyer")
    ihm.addObjet(LineEdit(ihm, (10, 90, 100, 30), "", stroke="black"), "envoie")
    ihm.addObjet(Label(ihm, (10, 130, 100, 30), "", stroke="black"), "reception")
    ihm.pack(["envoyer", "envoie", "reception"], expand="X")
    ihm.disabled(["envoyer", "envoie"])
    jeu.loop_start()


def exit():
    jeu.deconnect()


def compute():
    if jeu.all_connected:
        ihm.enabled(["envoyer", "envoie"])
    else:
        ihm.disabled(["envoyer", "envoie"])
    if jeu.recept_message() is True:
        ihm.objet_by_name("reception").text(jeu.reception)
    ihm.scan_events()


def draw():
    ihm.draw()


run(globals())
jeu.loop_stop()
