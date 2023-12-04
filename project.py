import string
import random
from fpdf import FPDF
import os

def choose_theme():
    """Displays and allows user to choose from a variety of available themes.

    :returns list: selected theme's word list
    """
    print("Available Themes:")
    print("1. Types of Birds")
    print("2. Tropical Fruits")
    print("3. Famous Movies")
    print("4. Famous Cities")
    print("5. Harry Potter")

    theme_choice = input("Choose a theme (1, 2, 3, 4, or 5): ")

    if theme_choice == "1":
        return ["PARROT", "OWL", "TOUCAN", "HUMMINGBIRD", "SPARROW", "FINCH", "FALCON", "CROW", "WARBLER", "OSTRICH", "WOODPECKER", "PENGUIN"]
    elif theme_choice == "2":
        return ["PINEAPPLE", "BANANA", "LYCHEE", "DRAGONFRUIT", "PAPAYA", "MANGO", "CITRUS", "GUAVA", "JACKFRUIT", "KIWI", "POMEGRANATE", "COCONUT"]
    elif theme_choice == "3":
        return ["JAWS", "SHREK", "TITANIC", "LIONKING", "JURRASICPARK","HARRYPOTTER", "SPIDERMAN", "FORRESTGUMP", "TRANSFORMERS", "MATRIX", "AVENGERS", "CLUELESS"]
    elif theme_choice == "4":
        return ["NEWYORK", "LONDON", "PARIS", "TOKYO", "LOSANGELES", "MUMBAI", "HONGKONG", "CHICAGO", "ROME", "ISTANBUL", "CANCUN", "DUBAI"]
    elif theme_choice == "5":
        return ["HERMIONE", "HAGRID", "QUIDDITCH", "GOLDENSNITCH", "WAND", "HOGWARTS", "VOLDEMORT", "HORCRUX", "WEASLEY", "DEMENTOR", "DUMBLEDORE", "WIZARD"]
    else:
        print("Invalid choice. Using default theme.")
        return ["PINEAPPLE", "BANANA", "LYCHEE", "DRAGONFRUIT", "PAPAYA", "MANGO", "CITRUS", "GUAVA", "JACKFRUIT", "KIWI", "POMEGRANATE", "COCONUT"]

def choose_difficulty():
    """Displays and allows user to choose from easy, medium, or hard difficulty levels.

    :returns list: grid width, grid height, and number of words for each selected difficulty level
    """
    print("Available Difficulty Levels:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")

    difficulty_choice = input("Choose a difficulty level (1, 2, or 3): ")

    #adjust the grid size and number of words for each level of difficulty
    if difficulty_choice == "1":
        return 15, 15, 6 
    elif difficulty_choice == "2":
        return 20, 20, 9
    elif difficulty_choice == "3":
        return 25, 25, 12
    #choose the medium level as default if user does not select one of the given choices
    else:
        print("Invalid choice. Using default difficulty.")
        return 20, 20, 9

width, height, num_words = choose_difficulty()

#get the word list of the user's selected theme
theme_words = choose_theme()

#generate random grid of uppercase letters with dimensions specified by 'width' and 'height'
grid = [[random.choice(string.ascii_uppercase) for i in range(0, width)] for j in range(0, height)]
#print grid onto terminal for visualization purposes
print("\n".join(map(lambda row: "  ".join(row), grid)))

#select a random subset of words from chosen theme based on word count of selected difficulty level, track occupied positions and errors on grid
word_list = list(set(random.sample(theme_words, num_words)))
already_taken = []
errors = []

def put_word(word, grid, already_taken, errors):
    """Places a word on the grid in a random direction.

    :param str word: word to be placed
    :param list grid: grid to place word
    :param list already_taken: list of positions that are already occupied by other words
    :param list errors: list to track errors
    
    :returns: updated grid and errors list
    """
    word = random.choice([word, word[::-1]]) 
    d = random.choice([[1,0],[0,1],[1,1]])
    xsize = width if d[0] == 0 else width - len(word) 
    ysize = width if d[1] == 0 else height - len(word)
    x = random.randrange(0, xsize)
    y = random.randrange(0, ysize)

    problem = []

    for i in range(0, len(word)):
        y_pos = y + d[1]*i
        x_pos = x + d[0]*i
        check = ([y_pos],[x_pos])
        if check in already_taken:
            problem.append(word)
            break
        else:
            already_taken.append(check)
            grid[y_pos][x_pos] = word[i]

    if len(problem) == 0:
        print(word, " inserted at ", [x, y]) 
    else: 
        print("Cannot place: ", word)
        errors.append(1)
    
    return grid, errors

#iterate through each word in word list and attempt to place on grid, retry up to 100 times to find a correct placement with no colisions
for word in word_list:
    stop = 0
    errors = []
    grid, errors = put_word(word, grid, already_taken, errors)
    while sum(errors) > 0 and stop < 100:
        errors = []
        print("retrying...")
        grid, errors = put_word(word, grid, already_taken, errors)
        stop += 1
    else:
        pass

#print final grid to terminal after word placement for visualization purposes
print(" ")
print("\n".join(map(lambda row: "  ".join(row), grid)))

#create PDF object with specified orientation, unit, and format
pdf = FPDF(orientation='P', unit='mm', format='A4')

#add new page to PDF
pdf.add_page()

#set title
pdf.set_font("Helvetica", size=25)
title = 'Word Search!'
grid_x = 200
grid_y = 8
pdf.cell(grid_x, 10, txt=title, ln=1, align='C')

#set text for grid cells and add blank cells between to create space
pdf.set_font("Courier", size=12)
pdf.cell(grid_x, grid_y, txt="", ln=1) 

#iterate through each row of grid and add to PDF
for i in grid:
    x = "  ".join(i)
    pdf.cell(grid_x, grid_y, txt=x, ln=1, align='C')

#display list of words to be found at the bottom of PDF
pdf.set_font("Courier", size=12)
pdf.cell(grid_x, grid_y, txt="", ln=1) 
hints_per_row = 6
split_lists = [word_list[x:x+hints_per_row] for x in range(0, len(word_list), hints_per_row)]

#iterate through each group of words and add them to PDF
for i in split_lists:
    wordx = ", ".join(i)
    pdf.cell(grid_x, 10, txt=wordx, ln=1, align='C')

#create path to output (save) final PDF file to user's Downloads folder
downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
pdf_path = os.path.join(downloads_folder, "WORD_SEARCH1.pdf")
pdf.output(pdf_path)
