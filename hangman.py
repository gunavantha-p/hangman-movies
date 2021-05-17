import random
import string
from movie_list import title
from movie_list import poster
from hangman_visual import lives_visual_dict
import tkinter as tk
from PIL import ImageTk, Image
import os
import requests
from io import BytesIO


def get_valid_word(title):
    word = random.choice(title)  # randomly chooses something from the list
    while '-' in word or ' ' in word or '!' in word or '?' in word:
        word = random.choice(title)
    
    return word


def hangman():
    word = get_valid_word(title)
    index = title.index(word)
    url = poster[index]
    word=word.upper()
    # print(word)    
    # print(index)
    # print(url)
    word_letters = set(word)  # letters in the word
    alphabet = set(string.ascii_uppercase)
    used_letters = set()  # what the user has guessed

    lives = 7

    # getting user input
    while len(word_letters) > 0 and lives > 0:
        # letters used
        # ' '.join(['a', 'b', 'cd']) --> 'a b cd'
        print('You have', lives, 'lives left and you have used these letters: ', ' '.join(used_letters))

        # what current word is (ie W - R D)
        word_list = [letter if letter in used_letters else '-' for letter in word]
        print(lives_visual_dict[lives])
        print('Current word: ', ' '.join(word_list))

        user_letter = input('Guess a letter: ').upper()
        if user_letter in alphabet - used_letters:
            used_letters.add(user_letter)
            if user_letter in word_letters:
                word_letters.remove(user_letter)
                print('')

            else:
                lives -= 1  # takes away a life if wrong
                print('\nYour letter,', user_letter, 'is not in the name if the movie.')

        elif user_letter in used_letters:
            print('\nYou have already used that letter. Guess another letter.')

        else:
            print('\nThat is not a valid letter.')

    # gets here when len(word_letters) == 0 OR when lives == 0
    if lives == 0:
        print(lives_visual_dict[lives])
        print('You died, sorry. The movie was', word)
    else:
        print('YAY! You guessed the movie', word, '!!')
    root = tk.Tk()
    response = requests.get(url)
    img_data = response.content
    img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
    panel = tk.Label(root, image=img)
    panel.pack(side="bottom", fill="both", expand="yes")
    root.mainloop()

if __name__ == '__main__':
    hangman()
