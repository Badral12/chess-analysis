import pandas as pd
import xlrd 
import openpyxl
import nltk
from nltk import sent_tokenize
import chess.pgn
from io import StringIO
import re
import numpy as np
from scipy import stats
import statsmodels.api as sm

# checking player move is take or not
def take_is_true(take) :
    if take:
        return ' and took' 
    else : return ''  

# checking is game ended by check mate 
def mate_is_true(mate) :
    if mate:
        return 'and mate' 
    else : return ''   

# checking player move is check or not  
def check_is_true(check) :
    if check:
        return 'and check' 
    else : return ''

def create_possible_bishop_moves(i, j):
    possible_moves = []
    for k in range(1, 8):
        for l in range(1, 8):
            if k == l :
                possible_moves.append((i - k, j - l))
                possible_moves.append((i + k, j + l))
                possible_moves.append((i + k, j - l))
                possible_moves.append((i - k, j + l))

    return possible_moves


def create_possible_knight_moves(i, j):
    possible_moves = [
        [i - 2, j - 1],
        [i - 1, j - 2],
        [i - 2, j + 1],
        [i - 1, j + 2],
        [i + 2, j - 1],
        [i + 1, j - 2],
        [i + 2, j + 1],
        [i + 1, j + 2],
    ]
    return possible_moves

def create_possible_rook_moves(i, j):
    possible_moves = []
    for k in range( 1, 8):
        possible_moves.append((i - k, j))
        possible_moves.append((i + k, j))
        possible_moves.append((i, j + k))
        possible_moves.append((i, j - k))
    return possible_moves


def letterNumberSwap(x):
    # change letters to numbers 
    if x == "a":
        return 1
    elif x == "b":
        return 2
    elif x == "c":
        return 3
    elif x == "d":
        return 4
    elif x == "e":
        return 5
    elif x == "f":
        return 6
    elif x == "g":
        return 7
    elif x == "h":
        return 8
    else : 
        return  print("Something is wrong.")
    

def knigh_posibleMoves(old_move, new_move, Piece_is_white ):
    # it's position of knights before game starts  
    # get position of queen side knight 
    queen_side_knight = old_move[0] 
    queen_i = letterNumberSwap( queen_side_knight[1] )
    queen_j = int(queen_side_knight[2])


    # get position of king side knight
    king_side_knight = old_move[1]
    king_i = letterNumberSwap ( king_side_knight[1] )
    king_j = int(king_side_knight[2])


    # get position of knight's move and knowing which side knight moved  
    if len(new_move) == 3:
        i = letterNumberSwap ( new_move[1:][0] )
        j = int( new_move[1:][1])

        possible = create_possible_knight_moves( i , j)

        for i in possible:
            if int(i[0]) == int(queen_i)  and int(i[1])  == int(queen_j)  :
                if Piece_is_white : 
                    knight_moves_white[0] = new_move
                    return  ' Queen side Knight moved' 
                else : 
                    knight_moves_black[0] = new_move
                    return  ' Queen side Knight moved' 
            elif int(i[0]) == int(king_i) and int(i[1]) == int(king_j) :
                if Piece_is_white:
                    knight_moves_white[1] = new_move
                    return  ' King side Knight moved'
                else : 
                    knight_moves_black[1] = new_move
                    return  ' King side Knight moved'
        
        return 'something wrong'    
    
    elif len(new_move) == 4: 
        check = letterNumberSwap (  new_move[1:][0] )
        i = letterNumberSwap ( new_move[1:][1] ) #rab1
        j = int( new_move[1:][2])

        if int(check) == int(queen_i)   :
            if Piece_is_white:
                knight_moves_white[0] = new_move[:1] + new_move[2:]
                return  ' Queen side Knight moved'
            else : 
                knight_moves_black[0] = new_move[:1] + new_move[2:]
                return  ' Queen side Knight moved'                 
        elif int(check) == int(king_i) :
            if Piece_is_white:
                knight_moves_white[1] = new_move[:1] + new_move[2:]
                return  ' King side Knight moved'
            else : 
                knight_moves_black[1] = new_move[:1] + new_move[2:]
                return  ' King side Knight moved'
    else : return 'Something wrong move'     
        
  

def bishop_posibleMoves (old_move, new_move, Piece_is_white):

    # it's position of knights before game starts  
    # get position of queen side knight 
    queen_side_bishop = old_move[0] 
    queen_i = letterNumberSwap( queen_side_bishop[1] )
    queen_j = int(queen_side_bishop[2])

    # get position of king side knight
    king_side_bishop = old_move[1]
    king_i = letterNumberSwap ( king_side_bishop[1] )
    king_j = int ( king_side_bishop[2] ) 


    # get position of knight's move and knowing which side knight moved  

    i = letterNumberSwap ( new_move[1:][0] )
    j = int( new_move[1:][1])


    possible = create_possible_bishop_moves( i , j)

    for i in possible:
        if int(i[0]) == int(queen_i)  and int(i[1])  == int(queen_j)  :
            if Piece_is_white :
                bishop_moves_white[0] = new_move
                return  ' Queen side Bishop moved' 
            else :
                bishop_moves_black[0] = new_move
                return  ' Queen side Bishop moved' 
        elif int(i[0]) == int(king_i) and int(i[1]) == int(king_j) :
            if Piece_is_white :
                bishop_moves_white[1] = new_move
                return  ' King side Bishop moved'
            else : 
                bishop_moves_black[1] = new_move
                return  ' King side Bishop moved'
        
    return 'something wrong'       
    

def rook_posibleMoves (old_move, new_move, Piece_is_white):
    # it's position of knights before game starts  
    # get position of queen side knight 
    queen_side_rook = old_move[0] 
    queen_i = letterNumberSwap( queen_side_rook[1] )
    queen_j = int( queen_side_rook[2] ) 

    # get position of king side knight
    king_side_rook = old_move[1]
    king_i = letterNumberSwap ( king_side_rook[1] )
    king_j = int(king_side_rook[2])


    
    # get position of knight's move and knowing which side knight moved  
    if len(new_move) == 3:
        i = letterNumberSwap ( new_move[1:][0] )
        j = int( new_move[1:][1])


        possible = create_possible_rook_moves( i , j)

        for i in possible:
            if int(i[0]) == int(queen_i)  and int(i[1])  == int(queen_j)  :
                if Piece_is_white :
                    rook_moves_white[0] = new_move
                    return  ' Queen side Rook moved'
                else :
                    rook_moves_black[0] = new_move
                    return  ' Queen side Rook moved'                     
            elif int(i[0]) == int(king_i) and int(i[1]) == int(king_j) :
                if Piece_is_white :
                    rook_moves_white[1] = new_move
                    return  ' King side Rook moved'
                else : 
                    rook_moves_black[1] = new_move
                    return  ' King side Rook moved'                    
        
        return 'something wrong'    
    elif len(new_move) == 4: 
        check = letterNumberSwap (  new_move[1:][0] )
        i = letterNumberSwap ( new_move[1:][1] ) #rab1
        j = int( new_move[1:][2])
 
        if int(check) == int(queen_i)   :
            rook_moves_white[0] = new_move[:1] + new_move[2:]
            return  ' Queen side Rook moved' 
        elif int(check) == int(king_i) :
            rook_moves_white[1] = new_move[:1] + new_move[2:]
            return  ' King side Rook moved'
    else : return 'Something wrong move'     



# what kind piece moved 
def board (move, knight_moves_white , bishop_moves_white, rook_moves_white , Piece_is_white  ):
    print(move)
    pawns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    if move ==  'end':
        return "game ended"
    elif move[0] in pawns :
       return  move[0] + ' pawm mowed ' 
    # knight 
    elif move[0] == 'N':
        take =  any('x' in s for s in move )
        check =  any('+' in s for s in move )
        mate =  any('#' in s for s in move)
        a = move.replace('+', '' ).replace('x','').replace('#','')
        return knigh_posibleMoves(knight_moves_white, a, Piece_is_white ) + take_is_true(take) + check_is_true(check) + mate_is_true(mate)
    elif move[0] == 'B':
        take =  any('x' in s for s in move )
        check =  any('+' in s for s in move )
        mate =  any('#' in s for s in move)
        a = move.replace('+', '' ).replace('x','').replace('#','')
        return bishop_posibleMoves(bishop_moves_white, a, Piece_is_white ) + take_is_true(take) + check_is_true(check) + mate_is_true(mate)
    elif move[0] == 'Q':
        take =  any('x' in s for s in move )
        check =  any('+' in s for s in move )
        mate =  any('#' in s for s in move)
        a = move.replace('+', '' ).replace('x','').replace('#','')
        q = 'Queen moved '
        return q + take_is_true(take) + check_is_true(check) + mate_is_true(mate)
    elif move[0] == 'K':
        take =  any('x' in s for s in move )
        a = move.replace('x','')
        q = 'King moved '
        return q + take_is_true(take) 
    elif move[0] == 'R':
        take =  any('x' in s for s in move )
        check =  any('+' in s for s in move )
        mate =  any('#' in s for s in move)
        a = move.replace('+', '' ).replace('x','').replace('#','')
        return rook_posibleMoves(rook_moves_white, a, Piece_is_white ) + take_is_true(take) + check_is_true(check) + mate_is_true(mate)   
    elif move == 'O-O-O':
        check =  any('+' in s for s in move )
        mate =  any('#' in s for s in move)
        a = move.replace('+', '' ).replace('#','')
        castle = 'Queen side castle '
        return castle + check_is_true(check) + mate_is_true(mate)   
    elif move == 'O-O':
        check =  any('+' in s for s in move )
        mate =  any('#' in s for s in move)
        a = move.replace('+', '' ).replace('#','')
        castle = 'King side castle '
        return castle +  check_is_true(check) + mate_is_true(mate)    
    else : 'Something is wrong'     

      
## --------------------------------------------------------------- MAIN SECTION ---------------------------------------------------------------
    
# Reading excel file
file_path =r'C:\Users\Badral\Desktop\chees analysis data\sql_data.xlsx'

# Excel file into a pandas 
df = pd.read_excel(file_path)

list_statuss = ['basic','beginner','competente','expert', 'masters' ] 


dfa = pd.DataFrame(columns=['Game' , 'Moves', 'Moves_details', 'Statuss'])
game_details_join = []      


# rook , knight , bishop , queen , king ,  bishop , knight , rook 
# queen side rook , queen side knight , queen side bishop , queen , king , king side bishop , king side knight , king side rook 

index = 0

knight_moves_white = ['Nb1','Ng1']
knight_moves_black = ['Nb8','Ng8']

bishop_moves_white = ['Bc1','Bf1']
bishop_moves_black = ['Bc8','Bf8']

rook_moves_white = ['Ra1','Rh1']
rook_moves_black = ['Ra8','Rh8']

game = 0
index = 0
while index  < len(df) :
    if df['Move'][index] < 11: 
        if df['Game'][index] != game :
            game = df['Game'][index] 
            knight_moves_white = ['Nb1','Ng1']
            knight_moves_black = ['Nb8','Ng8']

            bishop_moves_white = ['Bc1','Bf1']
            bishop_moves_black = ['Bc8','Bf8']

            rook_moves_white = ['Ra1','Rh1']
            rook_moves_black = ['Ra8','Rh8']

        # see what piece woved ? , and    
        print(index)
        a = board( df['White'][index] , knight_moves_white , bishop_moves_white, rook_moves_white , Piece_is_white = True   ) 
        df['move_detail_white'][index] = a
        print( a)
        b = board( df['Black'][index] , knight_moves_black , bishop_moves_black, rook_moves_black  , Piece_is_white = False   )    
        df['move_detail_black'][index] = b  
        print( b)
    
    index += 1        


print(df)

df.to_excel(r'C:\Users\Badral\Desktop\chees analysis data\early_game_analysis.xlsx', index=False)