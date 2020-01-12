"""
    This program is similar to a word generator where it takes an input of 1 to 7 letters in a rack as well as any placed tiles and generates words with the highest scores and longest lengths.
"""

BANNER = 'Scrabble Tool' # this is what the program prints upon initialization


import itertools
from operator import itemgetter # importing all the necessary libraries to do the project
SCORE_DICT ={'a': 1,'e':1,'i':1,'u':1,'l':1,'n':1,'s':1,'t':1,'e':1,'r':1,\
             'd':2, 'g':2,\
             'b':3, 'c':3, 'm':3, 'p':3,\
             'f':4, 'h':4, 'v':4, 'w':4, 'y':4,\
             'k':5,\
             'j':8, 'x':8,\
             'q':10, 'z':10} # this is a dict for all the letter values


def open_file(prompt_str):
    '''
        This function will take an input and try to open that file. 
        It'll keep asking until the file can be opened, and it will return the file pointer
    '''
    while True:
        test = input(prompt_str) # this prompts until the file can be opened and it'll return the file pointer
        try:
            fp = open(test, encoding = 'utf-8' )
            return fp
        
        except IOError:
            print("File not found. Try again.")

def read_file(fp):
    """
    This puts all the words over three characters and words without special characters into a dict
    """

    d = {}
    for line in fp: # reads over the file
        line = line.strip()     # strips out any non needed characters
        line = str(line) # converts the line to a string
        if len(line) < 3 or line.find("'") > 0 or line.find("-") > 0: # if the characters are special or if the length is under 3, don't add it
            pass
        else:    
            d[line] = 1   
    return d # returns the dict
        

        

def calculate_score(rack,word):
    """
    This will read the word and accociate the characters with the characters in the SCORE_DICT
    then return a value for the letters in the word
    
    If the word uses 7 or more characters, 50 pts is added to the score
    """
    final = 0    
    
    
    for letter in word: # goes over each letter in the word and adds the value to the final value
        final += SCORE_DICT[letter]
    
    if len(word) >= 7 and len(rack) == 7: # adds 50 if the length is over 7
        final += 50
    
    return int(final) #returns the int

def generate_combinations(rack,placed_tile):
    """
        This takes a rack and generates all the combinations of letters possible
        
        If placed tiles exists, then it will generate with each letter of the placed tile
    """
    final = set()
    rack = list(rack)
    
    if placed_tile: # if placed tile exists
        for letter in placed_tile: # adds letter in placed tile to the rack for generation
            rack.append(letter)
            
            for k in range(len(rack)+1): # for each letter in the rack
                
                for i in itertools.combinations(rack,k): # for each combo made
                    
                    if len(placed_tile) == 1 and len(i) >= 3 and placed_tile in i: #adds only the correct generations to the final list of tuples
                        final.add(i)
                        #print(final)
                    
                    else:
                        for letter in placed_tile:
                            if len(i) >= 3 and letter in i:
                                final.add(i)
                                #print(final)
            rack.pop() # takes out the added tile to avoid using the whole word in the generation
    
    
    else: # if there isnt a placed tile it ignores the need for the placed tile to be in the combo
        for k in range(len(rack)+1):
            for i in itertools.combinations(rack,k):
                
                if len(i) >= 3:
                    final.add(i)

    return final # returns the tuples

def generate_words(combo,scrabble_words_dict):    
    """
    This looks at the dict of all the words and compares the permutations 
    of the combinations to the keys in the dict
    """
    final = set()
    
    for w in itertools.permutations(combo): # puts all the letters into a string
        word = ''.join(w)
        
        if word in scrabble_words_dict: # looks at dict keys and adds it if its a word
            final.add(word)
    
    final = set(sorted(final, key= itemgetter(0))) # returns a set of words sorted alphabetically
    
    return final # returns the set

def generate_words_with_scores(rack,placed_tile,scrabble_words_dict):
    """
    This function uses most of the previous functions to generate a dict of words
    with the word as a key and the word score as the value
    """
    final = {}
    combos = generate_combinations(rack, placed_tile) # generates the combos
    
    for item in combos: # for each tuple in the list of generations
        thing = generate_words(item, scrabble_words_dict)
        
        if thing != set(): # the previous function generates empty sets if the combo isnt a word. This sorts through the empty sets
            
            for c in thing: # for the letter in the key
                c = ''.join([i for i in c if i.isalpha()]) # if the item is a letter it adds the letter to a string          
                final[c] = calculate_score(rack,c) # sets the string to have a value of the word score

    return final # returns the dict

    
def sort_words(dic):
    """
    The first list sorts the tuples by score, with ties
    sorted by length and alphabetically. This will be referenced as score sorting.
    The second list will be sorted by length, with ties sorted by score and alphabetically.
    """
    lst0 = []
    
    for k in dic: # puts the word, word score, and word length into a tuple
        item = (k, dic[k], len(k))
        lst0.append(item) # adds that tuple to a list

    lst1 = sorted(lst0, key= itemgetter(0), reverse= False) # sorts alplabetically
    lst2 = sorted(lst0, key= itemgetter(0), reverse= False)
    
    lst1 = sorted(lst1, key= itemgetter(1,2), reverse= True) # sorts by value then length
    lst2 = sorted(lst2, key= itemgetter(2,1), reverse= True) # sorts by length then value
    
    final = [lst1, lst2] # adds the two lists into a single list
    return final # returns the lists

def display_words(word_list,specifier):
    """
        This function will display the word list by either length or score,
        which is based on the specifier
    """
    
    if str(specifier) == 'length': # this will sort the list by length
        print("{:>7s} - {:s}".format('Length','Word'))
        if len(word_list) > 5: # this makes it so only the top 5 words get printed
            for i in range(5):
                print("{:>7d} - {:s}".format(word_list[i][2],word_list[i][0]))
        else:
            for i in range((len(word_list))): # if the list is under 5, then it just prints the list
                print("{:>7d} - {:s}".format(word_list[i][2],word_list[i][0]))
    
    
    elif str(specifier) == 'score': # this will sort the list by score
        print("{:>7s} - {:s}".format('Score','Word'))
        if len(word_list) >= 5: # this makes it so only the top 5 are printed
            for i in range(5):
                print("{:>7d} - {:s}".format(word_list[i][1],word_list[i][0]))
        else:
            for i in range((len(word_list))): # this prints the list if the list is under 5 words
                print("{:>7d} - {:s}".format(word_list[i][1],word_list[i][0]))
    
prompt_str = "Input word file: "
def main():
    """
    This function is what the user sees when they run the program
    this also makes it so the functions can be tested individually without inputs needed
    """
    print(BANNER)
    play = input("Would you like to enter an example (y/n): ") # if the user wants to actually run the program
    
    while True: # to keep the program cycling
        
        if play.lower() == 'y': # this doesnt break the loop
    
            in_file = open_file(prompt_str) # calls the open file function for a file pointer
            
            dic = read_file(in_file) # reads the file pointer and slaps the values in a dictionary
            
            #print(dic)
            in_file.close() # closes the file
            
            rack = input("Input the rack (2-7chars): ") # input for the rack of letters
            
            while len(rack) > 7 or len(rack) <  2 or not(rack.isalpha()): # if the rack isnt within the correct range or if its not letters
                print("Error: only characters and 2-7 of them. Try again.") # prompts until the input is acceptable
                rack = input("Input the rack (2-7chars): ")
            
            tile = input("Input tiles on board (enter for none): ") # placed tile doesnt have to have a value
            
            if not(tile) or tile.isalpha():
                pass
            
            else:
                while tile and not(tile.isalpha()): # but if there are tiles placed, they have to be letters
                    print("Error: tiles must be characters or empty")
                    tile = input("Input tiles on board (enter for none): ")
                
            
            a = generate_words_with_scores(rack,tile,dic) # this is the dict with the word scores
            
            final = sort_words(a) # sorted dictionary of words
            
            print('Word choices sorted by Score')
            
            display_words(final[0],'score') # prints words by scores
            print('\nWord choices sorted by Length')
            
            display_words(final[1],'length') # prints words by length
    
            play = input("Do you want to enter another example (y/n): ") # asks if the user wants to continue
            
        else: # if the user doesnt want to continue, it breaks the loop and exits the program
            print("Thank you for playing the game")
            break

if __name__ == "__main__":
    main()
