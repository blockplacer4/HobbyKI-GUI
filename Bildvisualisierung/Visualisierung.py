import pygame
import sys
import time
from pygame.locals import *
import pyttsx3
import threading
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("rate", 130)
engine.setProperty("voice", voices[0].id)
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Erstellen Sie ein Dictionary, das Funktionen den Buchstaben zuordnet
letter_functions = {
    'a': "Mund_Auf.png",
    'b': "Mund_Halb_Oben.png",
    'c': "Mund_Breit.png",
    'd': "Mund_Halb_Auf.png",
    'e': "Mund_Breit.png",
    'f': "Mund_offen_oben.png",
    'g': "Mund_Breit.png",
    'h': "Mund_Auf.png",
    'i': "Mund_Halb_Auf.png",
    'j': "Mund_Kreis.png",
    'k': "Mund_Halb_Auf.png",
    'l': "Mund_Halb_Auf.png",
    'm': "Mund_Halb_oben.png",
    'n': "Mund_Halb_Auf.png",
    'o': "Mund_Kreis.png",
    'p': "Mund_offen_oben.png",
    'q': "Mund_Kreis.png",
    'r': "Mund_offen_oben.png",
    's': "Mund_Halb_Auf.png",
    't': "Mund_offen_oben.png",
    'u': "Mund_Kreis.png",
    'v': "Mund_offen_oben.png",
    'w': "Mund_Halb_Auf.png",
    'x': "Mund_Halb_Auf.png",
    'y': "Mund_Kreis.png",
    'z': "Mund_Halb_Auf.png",
    'ä': "Mund_Auf.png",
    'ö': "Mund_Kreis.png",
    'ü': "Mund_Kreis.png",
    ',': "Mund_Zu.png",
    " ": "Mund_Zu.png"
}

input_string = "Das ist eine Testphrase. Diese ist einfach und zufällig"
running = True

time.sleep(1)

def display_mouth_image(text):
    time.sleep(0.1)
    for letter in text.lower():
        if letter in letter_functions:
            if letter == ",":
                for i in range(5):
                    image_path = "Images/Mund_Zu.png"
                    image = pygame.image.load(image_path)
                    screen.blit(image, (0, 0))
                    pygame.display.update()
                    time.sleep(0.2)
            image_path = "Images/" + letter_functions[letter]
        else:
            for i in range(5):
                image_path = "Images/Mund_Zu.png" 
                image = pygame.image.load(image_path)
                screen.blit(image, (0, 0))
                pygame.display.update()
                time.sleep(0.19)
        image = pygame.image.load(image_path)
        screen.blit(image, (0, 0))
        pygame.display.update()
        time.sleep(0.055)
    image = pygame.image.load("Images/Mund_Zu.png")
    screen.blit(image, (0, 0))
    pygame.display.update()
    time.sleep(0.02)

def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.2)
def start():
    thread = threading.Thread(target=text_to_speech, args=(input_string,))
    thread.start()
    thread2 = threading.Thread(target=display_mouth_image, args=(input_string,))
    thread2.start()
start()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
sys.exit()