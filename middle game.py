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



def count_control(board):
    white_control = 0
    black_control = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            if piece.color == chess.WHITE:
                white_control += 1
            else:
                black_control += 1

    return white_control, black_control

def count_space_control(board, color):
    space_control = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None and piece.color == color:
            space_control += len(board.attacks(square))
    return space_control

def evaluate_king_safety(board, color ):


    # Example: Favor castled positions and pawn shelter
    pawn_shelter_score = len(board.attacks( board.king(color) ))  # You might want to customize this based on your criteria
    castling_bonus = 0 if board.has_kingside_castling_rights(color) else -1

    king_safety_score = pawn_shelter_score + castling_bonus

    return king_safety_score

## --------------------------------------------------------------- MAIN SECTION ---------------------------------------------------------------
    
# Reading excel file
file_path =r'C:\Users\Badral\Desktop\chees analysis data\sql_data.xlsx'

# Excel file into a pandas 
df = pd.read_excel(file_path)

board = chess.Board()

game = 0
index = 0
while index  < len(df)  :

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

   
    # Calculate center control based on the current board
    board_files = set(chess.square_file(square) for square in chess.SQUARES)
    board_ranks = set(chess.square_rank(square) for square in chess.SQUARES)
    
    center_squares = [square for square in chess.SQUARES if chess.square_file(square) in board_files and chess.square_rank(square) in board_ranks]
    white_control = sum(1 for square in center_squares if board.piece_at(square) and board.piece_at(square).color == chess.WHITE)
    black_control = sum(1 for square in center_squares if board.piece_at(square) and board.piece_at(square).color == chess.BLACK)

    df['center_squares_white'][index] = white_control
    df['center_squares_black'][index] = black_control


    df['space_control_white'][index] = count_space_control(board, chess.WHITE)
    df['space_control_black'][index] = count_space_control(board, chess.BLACK) 


    df['king_safety_white'][index] = evaluate_king_safety(board,chess.WHITE)
    df['king_safety_black'][index] = evaluate_king_safety(board,chess.BLACK)

    index += 1


print(df)

df.to_excel(r'C:\Users\Badral\Desktop\chees analysis data\middle_game_analysis.xlsx', index=False)


