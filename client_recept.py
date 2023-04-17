import paho.mqtt.client as mqtt
"""Emission d'un post avec MQTT"""
# adresse du broker (sans https:\\)
mqtt_broker = "mqtt.eclipseprojects.io"
# création d'une instance de client
client = mqtt.Client("client1")
# connection au broker
client.connect(mqtt_broker)
# abonnement au topic
client.subscribe("mon_sujet")
# boucle qui permet d'émettre un message avec input tant que
# msg!="fin"
msg=""

def reception_message(client, userdat, message):
    """Fonction associée à on_message"""
    global msg
    # récupération du message dans l'objet message et décodage
    msg = str(message.payload.decode('utf-8'))
    # affichage
    print(client.get, msg)

# association de la fonction réception_message avec client.on_message
client.on_message = reception_message

# création d'un thread de réception des messages
client.loop_start()
# boucle d'attente de réception des messages
while msg!="fin":
    msg = input("entrer votre message\n")
    # émettre msg sur le topic "mon_sujet"
    client.publish("mon_sujet", msg)
# arrêt du thread de réception des messages
client.loop_stop()
