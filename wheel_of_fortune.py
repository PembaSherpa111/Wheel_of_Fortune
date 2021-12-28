import random
import json

#getting the random word from json file
def word():
    f = open('phrases.json') #json file needs to be in same folder 
    string_dictionary = f.read()
    dictionary = json.loads(string_dictionary) #converting the data type from string to dictionary
    random_index=random.randint(0,(len(dictionary)-1))
    random_word = list(dictionary.items())[random_index]
    f.close()
    return(random_word) #returns phrase and category

#spinning the wheel
def spin_the_wheel():
    wheel=['Bankrupt','Lose a Turn',900,850,800,750,700,650,600,550,500,450,400,350,300,250,200,150,150,150,100,100,100,100]
    spin_selection = random.choice(wheel)
    print(f'Spin result = {spin_selection}')
    return(spin_selection)

#checking if the letter is in the word
def check_letter_existence(phrase,guessed_word,letter):
    for i,x in enumerate(phrase): #required for cases where duplicate letters are present
        if x == letter.lower():
            guessed_word = guessed_word[:i] + letter.lower() + guessed_word[i+1:]
    return(guessed_word)            

#Round 1 and Round 2 gameplay
def initial_round(player_info,random_word):
    player_info = dict(player_info) # converting list to dictionary
    phrase = random_word[0].lower()
    hint = random_word[1]
    guessed_word = ('-' * len(phrase))
    revealed_letters = [" ","-","!","'",".","?","&"]
    for letter in revealed_letters:
        guessed_word = check_letter_existence(phrase,guessed_word,letter)

    i = 0
    while guessed_word != phrase:
        for i in range(0,3):
            print('================================')
            print(guessed_word)
            print(f'Hint: {hint}')
            print(f"\n{list(player_info.keys())[i]}'s turn")
            print(f'Your current bank amount is {player_info[list(player_info.keys())[i]]}')
            spin_again = True
            while spin_again == True:
                guess_the_word = input('Do you want to guess the word? Enter y/n: ')  #if player wants to guess the word at the start of his turn
                
                while guess_the_word.lower() not in ['y','n']: # making sure input is y or n.
                    guess_the_word = input('Do you want to guess the word? Enter y/n: ')
                
                if guess_the_word == 'y':
                    guess = input('Enter your guess: ')
                    if guess.lower() == phrase:
                        return(list(player_info.items())[i])
                    else:
                        spin_again = False
                else:
                    spin_selection = spin_the_wheel()  # if player wants to spin the wheel 
                    if spin_selection == 'Bankrupt':
                        player_info[list(player_info.keys())[i]] = 0
                        print(f'Your current bank amount is {player_info[list(player_info.keys())[i]]}')
                        spin_again = False
                    elif spin_selection == 'Lose a Turn':
                        print(f'Your current bank amount is {player_info[list(player_info.keys())[i]]}')
                        spin_again = False
                    else:
                        consonant = input('Enter a consonant: ') 
                        index = phrase.find(consonant.lower())
                        if index == -1:
                            spin_again = False
                        else:
                            guessed_word = check_letter_existence(phrase,guessed_word,consonant)
                            player_info[list(player_info.keys())[i]] = player_info[list(player_info.keys())[i]] + spin_selection #adding the dollar value to temporary bank
                            print(guessed_word)
                            print(f'Your current bank amount is {player_info[list(player_info.keys())[i]]}')
                            if guessed_word == phrase:
                                return(list(player_info.items())[i])
                            buy_vowel = 'y' #player can buy vowel if guessed correct consonant
                            while buy_vowel == 'y': #can buy vowel until incorrect guess
                                buy_vowel = input('Do you want to buy vowel? Enter y/n: ')
                                while buy_vowel.lower() not in ['y','n']: # making sure input is y or n.
                                    buy_vowel = input('Do you want to buy vowel? Enter y/n: ')
                                if buy_vowel == 'y':
                                    player_info[list(player_info.keys())[i]] = player_info[list(player_info.keys())[i]] - 250 #substracting the cost of vowel
                                    print(f'Your current bank amount is {player_info[list(player_info.keys())[i]]}')
                                    vowel = input('Enter a vowel: ')
                                    index = phrase.find(vowel.lower())
                                    if index == -1:
                                        spin_again = False
                                        buy_vowel = 'n'
                                    else:
                                        guessed_word = check_letter_existence(phrase,guessed_word,vowel)
                                        player_info[list(player_info.keys())[i]] = player_info[list(player_info.keys())[i]] + spin_selection #adding the dollar value to temporary bank
                                        print(guessed_word)
                                        print(f'Your current bank amount is {player_info[list(player_info.keys())[i]]}')
                                if guessed_word == phrase:
                                    return(list(player_info.items())[i])
    
#start of the game
#enter username for the players
player_name = []
player_name.append(input('Enter the username of player1: '))
player_name.append(input('Enter the username of player2: '))
player_name.append(input('Enter the username of player3: '))
temp_bank = [0,0,0] 

#round 1
print('Round 1 Begins')
random.shuffle(player_name) #randomly sorting the players turn
print(f'The randomly sorted order of turn is {player_name}')
player_info = list (zip (player_name, temp_bank))
random_word = word()
r1_winner= initial_round(player_info,random_word) # gives result as a tuple {'player_name', temp_bank}
print(f'\nWinner of 1st round is {r1_winner[0]} with bank amount {r1_winner[1]}')

#round 2
print('\nRound 2 Begins')
player_info.insert(3, player_info.pop(0)) #moving 1st player to last
random_word = word()
r2_winner = initial_round(player_info,random_word) # gives result as a tuple {'player_name', temp_bank}
print(f'\nWinner of 2nd round is {r2_winner[0]} with bank amount {r2_winner[1]}')
print('=================================\n')

#checking who goes to round 3
if r1_winner[0] == r2_winner[0]: #checking if the winner of 1st and 2nd round are same person
    final_prize_amount = r1_winner[1] + r2_winner[1]
    finalist = r1_winner[0]
    print(f'{finalist} goes to the final round with prize money {final_prize_amount}')
else: #if different winners checking who has more in the bank
    if r1_winner[1] > r2_winner[1]:
        final_prize_amount = r1_winner[1]
        finalist = r1_winner[0]
        print(f'{finalist} goes to the final round with prize money {final_prize_amount}')
    else:
        final_prize_amount = r2_winner[1]
        finalist = r2_winner[0]
        print(f'{finalist} goes to the final round with prize money {final_prize_amount}')

#Final Round
print('\nFinal Round Begins')
print(f'Good Luck {finalist}!\n')
random_word = word()
phrase = random_word[0].lower()
hint = random_word[1]
guessed_word = ('-' * len(phrase))
guessed_word = check_letter_existence(phrase,guessed_word,' ') #showing white spaces

revealed_letters = ['r','s','t','l','n','e']
for letter in revealed_letters:
    guessed_word = check_letter_existence(phrase,guessed_word,letter)
print(guessed_word)
print('Enter 3 consonants and 1 vowel letter.')
consonant = input('Enter 1st consonant: ')
guessed_word = check_letter_existence(phrase,guessed_word,consonant)
consonant = input('Enter 2nd consonant: ')
guessed_word = check_letter_existence(phrase,guessed_word,consonant)
consonant = input('Enter 3nd consonant: ')
guessed_word = check_letter_existence(phrase,guessed_word,consonant)
vowel = input('Enter 1 vowel: ')
guessed_word = check_letter_existence(phrase,guessed_word,vowel)
print(guessed_word)
guess = input('Enter the full word: ')
if guess.lower() == phrase:
    print(f'\nCongratulation! You win {final_prize_amount}')
else:
    print(f'\nYou lose! Correct answer is {phrase}')
