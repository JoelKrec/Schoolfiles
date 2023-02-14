
"""
Spiel "Zahlenraten", in Python programmiert.
"""

import random


print('Zahlenraten')

# initialisiere des Zufallszahlengenerators
random.seed()
while True:

    start_number = 0
    end_number = 0

    while True:
        print('\nLegen Sie Ihren Ratebereich fest\n')
        start_number = int(input('Untere Grenze: '))
        end_number = int(input('Obere Grenze: '))

        if start_number < end_number:
            break
        else:
            print('Eingabe ungültig')

    # erzeuge neue Zufallszahl zwischen 1 und 100
    correct_answer = random.randint(start_number, end_number)

    player_input = 0
    player_guesses = 0
    # solange der Spieler noch nicht die richtige Antwort eingegeben hat...
    while player_input != correct_answer:
        # lese Eingabe vom Spieler ein und parse den eingegebenen String zu einer Ganzzahl (int)
        player_input = int(input('Zahl eingeben: '))
        player_guesses += 1
        # vergleiche Eingabe mit der richtigen Antwort
        if player_input > correct_answer:
            print('Zahl zu groß!')
        elif player_input < correct_answer:
            print('Zahl zu klein!')
        else:
            print('Sie haben gewonnen mit ' + str(player_guesses) + ' Versuchen!')

    restart_input = 1
    while True:
        print('Möchten Sie noch einmal spielen?')

        restart_input = int(input('Ja = 1 / Nein = 0: '))

        if restart_input != 1 and restart_input != 0:
            print('Eingabe ungültig')
        else:
            break
    if restart_input == 0:
        print('\n\nExiting...')
        break
    else:
        print('\n\nRestarting...\n\n\n')

