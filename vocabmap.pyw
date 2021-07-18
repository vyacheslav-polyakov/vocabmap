import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame.constants import RESIZABLE
import pygame
import sys
import random
from google_trans_new import google_translator
import pinyin as p
import pygame.freetype
from scraper import findExamples

# Pull the known, unknown and unidentified words from the memory
words = []
known = []
unknown = []
wordsfile = open(r'vocab\words.txt', 'r', encoding='utf-8')
knownfile = open(r'vocab\known.txt', 'r', encoding='utf-8')
unknownfile = open(r'vocab\unknown.txt', 'r', encoding='utf-8')
for word in wordsfile.readlines():
    words.append(word.replace('\n', ''))
wordsfile.close()
for word in knownfile.readlines():
    known.append(word.replace('\n', ''))
knownfile.close()
for word in unknownfile.readlines():
    unknown.append(word.replace('\n', ''))
unknownfile.close()

# The Saving Function
def save():
    knownfile = open(r'vocab\known.txt', 'w', encoding='utf-8')
    for word in known:
        knownfile.write(word+'\n')
    knownfile.close()

    unknownfile = open(r'vocab\unknown.txt', 'w', encoding='utf-8')
    for word in unknown:
        unknownfile.write(word+'\n')
    unknownfile.close()

    wordsfile = open(r'vocab\words.txt', 'w', encoding='utf-8')
    for word in words:
        wordsfile.write(word+'\n')
    wordsfile.close()
'''
# The Multiple Line Text Display Function
def renderLines(text):

    font = pygame.font.Font(r'fonts\SIMSUN.ttf', 28)

    lines = text.splitlines()
    multiplier = 1
    if len(lines) >= 2:
        multiplier = 2
    for i, l in enumerate(lines):
        label = font.render(example, True, WHITE)
        position = label.get_rect()
        position.center = (350, 410)
        screen.blit(font.render(l, 0, WHITE), (position.x * multiplier, position.y + 30*i))
'''   
# GUI Setup
t = google_translator()
pygame.init()
WHITE = (255, 255, 255)
RED = (0, 255, 0)
BLACK = (10, 10, 10)
CYAN = (120, 255, 200)
BLUE = (0, 120, 255)
PINK = (255, 150, 130)
YELLOW = (243, 202, 32)
ORANGE = (245, 160, 40)
PURPLE = (240, 40, 240)
GREY = (200, 200, 200)
size = (1200, 700)
screen = pygame.display.set_mode(size, RESIZABLE)
pygame.display.set_caption("Vocab Mapper")

# Initialize the values
word = random.choice(words)
translation = ''
pinyin = ''
examples_cn = None
example_cn = ''
examples_en = None
example_en = ''
i = 0
score = len(known)
randomColor = random.choice([CYAN, PINK, YELLOW, ORANGE])

done = False
clock = pygame.time.Clock()
fullscreen = False 

# The Main Loop
while not done:
    for event in pygame.event.get():
        # Getting the current size of the screen
        w, h = pygame.display.get_surface().get_size()

        if event.type == pygame.QUIT:
            save()
            done = True
        # Resizable screen
        elif event.type == pygame.VIDEORESIZE:
            type = pygame.FULLSCREEN if fullscreen else pygame.RESIZABLE
            window = pygame.display.set_mode(event.size, type)
        elif event.type == pygame.KEYDOWN and len(words) >= 1:
            if not fullscreen and event.key == pygame.K_F11:
                fullscreen = True
                pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, size = size))
            if fullscreen and event.key == pygame.K_F12:
                fullscreen = False
                pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, size = size))
            # Save the game
            if event.key == pygame.K_s:
                save()
            # Show the pinyin
            elif event.key == pygame.K_LCTRL:
                pinyin = p.get(word, delimiter='')
            # Show the translation 
            elif event.key == pygame.K_LSHIFT and translation == '':
                try:
                    translation = t.translate(word, 'en')
                except:
                    translation = '*Unable to connect to google translate*'
            # Show an example 
            elif event.key == pygame.K_LALT:
                # First iteration
                if examples_cn == None:
                    i = 0
                    try:
                        structure = findExamples(word)
                        examples_cn = structure[0]
                        examples_en = structure[1]
                        if examples_cn == ['']:
                            examples_cn = ['No examples found']
                            examples_en = ['']
                    except:
                        examples_cn = ['No examples found.']
                        examples_en = ''
                # Any iteration
                try:
                    example_cn = examples_cn[i]
                    example_en = examples_en[i]
                    if i < len(examples_cn) - 1:
                        i += 1
                    else:
                        i = 0
                except IndexError:
                    i = 0
                    
            # Mark the word as unknown and pull a new word
            elif event.key == pygame.K_SPACE:
                unknown.append(word)
                # Removing the marked word
                words.pop(words.index(word))
                # Pulling a new word
                word = random.choice(words)
                translation = ''
                pinyin = ''
                examples_cn = None
                examples_en = None
                example_cn = ''
                example_en = ''
            # Mark the word as known, update the score and pull a new word
            elif event.key == pygame.K_RETURN:
                known.append(word)
                score = len(known)
                # Removing the marked word
                words.pop(words.index(word))
                # Pulling a new word
                word = random.choice(words)
                translation = ''
                pinyin = ''
                examples_cn = None
                examples_en = None
                example_cn = ''
                example_en = ''
            # Quit the test after saving 
            elif event.key == pygame.K_ESCAPE:
                save()
                done = True
 
    screen.fill(BLACK)

    # The Known Words Count
    font = pygame.font.Font('fonts\Gentium-R.ttf', 25)
    label = font.render('Known: {}'.format(len(known)), True, GREY)
    position = label.get_rect()
    position.center = (75, 40)
    screen.blit(label, position)

    # The Unknown Words Count
    font = pygame.font.Font('fonts\Gentium-R.ttf', 25)
    label = font.render('Unknown: {}'.format(len(unknown)), True, GREY)
    position = label.get_rect()
    position.center = (90, 70)
    screen.blit(label, position)

    # The New Words Count
    font = pygame.font.Font('fonts\Gentium-R.ttf', 25)
    label = font.render('New: {}'.format(len(words)), True, GREY)
    position = label.get_rect()
    position.center = (83, 100)
    screen.blit(label, position)
  
    # The Chinese Word
    font = pygame.font.Font(r'fonts\SIMSUN.ttf', 220)
    label = font.render(word, True, WHITE)
    position = label.get_rect()
    position.center = (w/2, h/2-120)
    screen.blit(label, position)

    # The Pinyin Pronunciation
    font = pygame.font.Font(r"fonts\Gentium-R.ttf", 48)
    label = font.render(pinyin, True, GREY)
    position = label.get_rect()
    position.center = (w/2, h/2-300)
    screen.blit(label, position)

    # The English Translation
    font = pygame.font.Font(r"fonts\Gentium-R.ttf", 48)
    label = font.render(translation, True, GREY)
    position = label.get_rect()
    position.center = (w/2, h/2+60)
    screen.blit(label, position)

    # Example in Chinese
    font = pygame.font.Font(r'fonts\SIMSUN.ttf', 38)
    label = font.render(example_cn, True, GREY)
    position = label.get_rect()
    position.center = ((w/2), h/2+250)
    screen.blit(label, position)

    # Example in English
    font = pygame.font.Font(r'fonts\Gentium-R.ttf', 38)
    label = font.render(example_en, True, GREY)
    position = label.get_rect()
    position.center = (w/2, h/2+300)
    screen.blit(label, position)
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()
sys.exit()
