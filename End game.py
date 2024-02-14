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
import chess
import chess.engine


def is_passed_pawn(board, square, color):
    file = square % 8
    rank = square // 8

    # Direction for pawn movement based on color
    direction = 1 if color == chess.WHITE else -1

    # Files to check: current, left, and right
    files_to_check = [file]
    if file > 0:
        files_to_check.append(file - 1)
    if file < 7:
        files_to_check.append(file + 1)

    # Check for opposing pawns in front of the pawn
    for file in files_to_check:
        for rank_offset in range(1, 8 - rank if color == chess.WHITE else rank + 1):
            target_square = chess.square(file, rank + rank_offset * direction)
            piece = board.piece_at(target_square)
            if piece and piece.piece_type == chess.PAWN and piece.color != color:
                return False

    return True

def identify_passed_pawns(board, color):
    passed_pawns = []
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece and piece.piece_type == chess.PAWN and piece.color == color:
            if is_passed_pawn(board, square, color):
                passed_pawns.append(square)

    return passed_pawns
#-------------------------- MAIN SECTION ---------------------------------------------------------------
    
# Reading excel file
file_path =r'C:\Users\Badral\Desktop\chees analysis data\middle_game_analysis.xlsx'

# Excel file into a pandas 
df = pd.read_excel(file_path)

board = chess.Board()

game = 0
index = 0
df['passing_pawn_white'] = 0
df['passing_pawn_black'] = 0

while index  <  len(df) :

    print(index)
    if df['Game'][index] != game :
        game = df['Game'][index] 
        board = chess.Board()


    board.push_san(df['White'][index])
    if df['Black'][index] == 'end':
        print('hi')
    else : 
        board.push_san(df['Black'][index]) 

    print(board)
    #df['isolated_pawns_white'][index] = len(analyze_pawn_structure(board, chess.WHITE))
    #df['isolated_pawns_black'][index] = len(analyze_pawn_structure(board, chess.BLACK))



    df['passing_pawn_white'][index] =len(identify_passed_pawns(board, chess.WHITE))
    df['passing_pawn_black'][index] =len(identify_passed_pawns(board, chess.BLACK))


    index += 1
print(df)


df.to_excel(r'C:\Users\Badral\Desktop\chees analysis data\end_game_analysis.xlsx', index=False)
