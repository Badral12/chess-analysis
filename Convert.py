from numpy import NAN
import pandas as pd
import xlrd 
import openpyxl
import nltk
from nltk import sent_tokenize
import chess.pgn
from io import StringIO
import re


## Checking starting move of game 
#  it helps to know when game is end or when game is about to begin  
def is_it_game_start(a):
    check = a.split(' ')
    if len(check) > 1 :
        if check[0].replace('.','') == '1':
            game_start_point = True
        else :
            game_start_point = False
        game_start_moves = ['a3','a4','a5','a6','b3','b4','b5','b6','c3','c4','c5','c6','d3','d4','d5','d6','e3','e4','e5','e6','f3','f4','f5','f6','g3','g4','g5','g6','h3','h4','h5','h6','Nc3','Nc6','Nf3','Nf6']
        for i in game_start_moves:
            if i == check[1] and game_start_point:
                return True
        return False    
    else : return False           
          

def count_variables(variable_list):
    # define a list of strings to check against
    lowercase_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    uppercase_letters = ['N', 'B', 'Q', 'K', 'R','O']
    only_numbers = []
    # check if each element in the list starts with any of the given strings
    # if so, append the whole element to the only_numbers list
    for variable in variable_list:
        # Skip if the variable is empty
        if variable == '':
            continue
        if  variable[0] in lowercase_letters+uppercase_letters :
            only_numbers.append(variable)
    if len(only_numbers) % 2 != 0:
        only_numbers.append(' ')
    return only_numbers


# Reading excel file
file_path =r'C:\Users\Badral\Desktop\chees analysis data\fulldata.xlsx'

# Excel file into a pandas 
df = pd.read_excel(file_path)


# Initialize an empty DataFrame
dfa = pd.DataFrame(columns=['Game' , 'Move', 'White', 'Black', 'Result', 'WhiteRank', 'BlackRank'])
game_details_join = []
game_cnt = 0
z = 1 


while game_cnt < len(df['name']) :
    index = str(df['name'][game_cnt])
    if  index[:7] == '[WhiteE' :
        print(index)
        white_rank =  index.split(' ')[-1][1:-2]

    if  index[:7] == '[BlackE' :
        print(index)
        black_rank =  index.split(' ')[-1][1:-2]

    if index[:7] == '[Result' :
        print(index)
        if index == '[Result "0-1"]':
            result = '0-1'
        elif index == '[Result "1-0"]':
            result = '1-0'
        elif index == '[Result "1/2-1/2"]':
            result = '1/2-1/2' 
    
    if isinstance(index, str) and index[:1] != '[' and  len(index) < 300:
        print(index)
        true_status = is_it_game_start(index)
        check = index.split(' ')
        if isinstance(index, str) and true_status and len(game_details_join) != 0 :    
            i = 0
            a = [] 
            move = 1
            a = count_variables(game_details_join)
            while i < len(a) :
                game = 'Game ' + str(z)     
                piece = a[i]
                piece2 = a[i+1]
                dfa = dfa.append({'Game' : game , 'Move': str(move), 'White': piece, 'Black': piece2, 
                                'Result' : result , 'WhiteRank' : white_rank, 'BlackRank': black_rank }, ignore_index=True) 
                i = i + 2
                move = move + 1 
            print(dfa)
            z += 1
            game_details_join = []
            game_details_join.extend(check)   
        else : 
            game_details_join.extend(check)      

    if isinstance(index, str) and index[0] == '1' and len(index) > 300:
        # Split the moves by space
        split_moves = index.split(' ')
        i = 0
        a = [] 
        move = 1
        result = split_moves[-1]
        a = count_variables(split_moves)
        while i < len(a) :
            game = 'Game ' + str(z)     
            piece = a[i]
            piece2 = a[i+1]
            dfa = dfa.append({'Game' : game , 'Move': str(move), 'White': piece, 'Black': piece2, 'Result' : result , 'WhiteRank' : white_rank, 'BlackRank': black_rank }, ignore_index=True) 
            i = i + 2
            move = move + 1
        print(dfa)
        z += 1
    game_cnt += 1
dfa.to_excel(r'C:\Users\Badral\Desktop\chees analysis data\first_example________________.xlsx', index=False)