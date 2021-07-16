import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import sys
import random
from google_trans_new import google_translator

# Pull the known, unknown and unidentified words from the memory
words = []
known = []
unknown = []
wordsfile = open(r'vocab\words.txt', 'r', encoding='utf-8')
knownfile = open(r'vocab\known.txt', 'r', encoding='utf-8')
unknownfile = open(r'vocab\known.txt', 'r', encoding='utf-8')
for word in wordsfile.readlines():
    words.append(word.replace('\n', ''))
wordsfile.close()
for word in knownfile.readlines():
    known.append(word.replace('\n', ''))
knownfile.close()
for word in unknownfile.readlines():
    unknown.append(word.replace('\n', ''))
unknownfile.close()

# Defining the save function
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
        
# GUI Setup
t = google_translator()
pygame.init()
WHITE = (255, 255, 255)
RED = (0, 255, 0)
BLACK = (0, 0, 0)
CYAN = (0, 255, 120)
PINK = (240, 100, 100)
YELLOW = (250, 250, 30)
ORANGE = (250, 100, 30)
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Vocab Mapper")

# Initialize the values
word = random.choice(words)
translation = ''
score = len(known)
print(known)
randomColor = random.choice([CYAN, PINK, YELLOW, ORANGE])

done = False
clock = pygame.time.Clock()

# The Main Loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save()
            done = True
        elif event.type == pygame.KEYDOWN:
            # Save the game
            if event.key == pygame.K_s:
                save()
            # Show the translation in a random color
            elif event.key == pygame.K_LSHIFT:
                try:
                    translation = t.translate(word, 'en')
                except:
                    translation = '*Unable to connect to google translate*'
                randomColor = random.choice([CYAN, PINK, YELLOW, ORANGE])
            # Mark the word as unknown and pull a new word
            elif event.key == pygame.K_SPACE:
                unknown.append(word)
                # Removing the marked word
                words.pop(words.index(word))
                # Pulling a new word
                word = random.choice(words)
                translation = ''
                randomColor = random.choice([CYAN, PINK, YELLOW, ORANGE])
            # Mark the word as known, update the score and pull a new word
            elif event.key == pygame.K_RETURN:
                known.append(word)
                score = len(known)
                # Removing the marked word
                words.pop(words.index(word))
                # Pulling a new word
                word = random.choice(words)
                translation = ''
                randomColor = random.choice([CYAN, PINK, YELLOW, ORANGE])
            # Quit the test after saving 
            elif event.key == pygame.K_ESCAPE:
                save()
                done = True
 
    screen.fill(BLACK)
  
    # The Chinese Word
    font = pygame.font.Font(r'fonts\SIMSUN.ttf', 100)
    label = font.render(word, True, WHITE)
    position = label.get_rect()
    position.center = (350, 200)
    screen.blit(label, position)

    # The English Translation
    font = pygame.font.Font('freesansbold.ttf', 28)
    label = font.render(translation, True, WHITE)
    position = label.get_rect()
    position.center = (350, 290)
    screen.blit(label, position)

    # The Score Count
    font = pygame.font.Font('freesansbold.ttf', 24)
    label = font.render('Score: {}'.format(score), True, WHITE)
    position = label.get_rect()
    position.center = (60, 30)
    screen.blit(label, position)
    
    pygame.display.flip()
  
    clock.tick(60)
    
pygame.quit()
sys.exit()
