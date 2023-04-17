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
while msg!="fin":
    msg = input("entrer votre message\n")
    # émettre msg sur le topic "mon_sujet"
    client.publish("mon_sujet", msg)

