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



# getting know if black game list has caslte or didn't move any piece before game end      
def element_list_edit_black (a):
    b = []
    black_pawns = ['a7','b7','c7','d7','e7','f7','g7','h7']
    castle_list =  [ 'Ra8', 'Nb8','Bc8','Qd8'] 
    long_castle_list =  ['Bf8','Ng8', 'Rh8']
    game_list = [ 'Ra8', 'Nb8','Bc8','Qd8','Bf8','Ng8','Rh8']  
    d = ''
    e = ''
    i = 0 
    while i < len(a):   
        b.append(a[i])
        if a[i] == 'O-O' or a[i] == 'O-O+':
            b[-1] = 'Rf8'
            i = i + 1
            d = 'unen'
        elif a[i] == 'O-O-O' or a[i] == 'O-O-O+':
            b[-1] = 'Rd8'
            i = i + 1
            e = 'unen'
        i = i + 1
    if d == 'unen' :
        b.extend( castle_list + black_pawns )
    elif e == 'unen' :
        b.extend( long_castle_list + black_pawns )
    else : 
        b.extend( game_list +  black_pawns)
    return b 

# getting know if black game list has caslte or didn't move any piece before game end
def element_list_edit_white(a):
    b = []
    black_pawns = ['a2','b2','c2','d2','e2','f2','g2','h2']
    castle_list = [ 'Ra1', 'Nb1','Bc1','Qd1']
    long_castle_list = ['Bf1','Ng1', 'Rh1']
    game_list = [ 'Ra1', 'Nb1','Bc1','Qd1' , 'Bf1','Ng1', 'Rh1' ]  
    d = ''
    e = ''
    i = 0
    while i < len(a):
        b.append(a[i])
        if a[i] == 'O-O' or a[i] == 'O-O+':
            b[-1] = 'Rf1'
            i = i + 1
            d = 'unen'
        elif a[i] == 'O-O-O' or a[i] == 'O-O-O+':
            b[-1] = 'Rd1'
            i = i + 1
            e = 'unen'
        i = i + 1
    if d == 'unen' :
        b.extend( castle_list + black_pawns )
    elif e == 'unen' :
        b.extend( long_castle_list + black_pawns )
    else : 
        b.extend( game_list +  black_pawns)
    return b 

# checking pawn promoted or not 
def promoted_list (a):
    check =  any('+' in s for s in a)
    promoted  =  any('=' in s for s in a)
    if promoted:
        if check :
            return a[-2] +  re.split('x', str(a))[-1][:2]
        else : 
           return a[-1] +  re.split('x', str(a))[-1][:2]         
    else : 
        return a  

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

# If promoted true what peice player is promoted  
def promoted_is_true(promoted,a):
    promoted  =  any('=' in s for s in a)
    check =  any('+' in s for s in a)
    dd = re.split('x', str(a))[-1]
    if promoted:
        if check :
            if a[-2] == 'B':
                return ' and Promoted Bishop'
            elif a[-2] == 'N':
                return ' and Promoted Knight'  
            elif a[-2] == 'R':
                return ' and Promoted Rook'
            elif a[-2] == 'Q':
                return ' and Promoted Queen'   
        else : 
            if a[-1] == 'B':
                return ' and Promoted Bishop'
            elif a[-1] == 'N':
                return ' and Promoted Knight'  
            elif a[-1] == 'R':
                return ' and Promoted Rook'
            elif a[-1] == 'Q':
                return ' and Promoted Queen'           
    else : return ''

# White moved and analysis black moves to know white player take  or give check  
def move_analysis_black_by_white(a, black_moves_list):
    last_elements = []
    for i in range(len(black_moves_list)-1, -1, -1):
        last_elements.append(black_moves_list[i])
    last_elements = element_list_edit_black(last_elements)    
    dd = re.split('x', str(a.replace('+', '').replace('#','')))[-1]
    take =  any('x' in s for s in a)
    check =  any('+' in s for s in a)
    promoted  =  any('=' in s for s in a) 
    mate =  any('#' in s for s in a)
    if promoted :
        dd = dd.replace('=', '').replace('+', '' ).replace('#', '' )[:-1]
    if take:        
        for i in last_elements:
            if str(dd) ==  promoted_list(i).replace('+', '' ).replace('#','')[-2:] :
                if i[0] == 'B':
                   return f'Take Bishop{promoted_is_true(promoted,a)} {check_is_true(check)} {mate_is_true(mate)} '
                elif i[0] == 'N':
                   return f'Take Knight{promoted_is_true(promoted,a)} {check_is_true(check)} {mate_is_true(mate)} '
                elif i[0] == 'R':
                   return f'Take Rook{promoted_is_true(promoted,a)} {check_is_true(check)} {mate_is_true(mate)}'
                elif i[0] == 'Q':
                   return f'Take Queen{promoted_is_true(promoted,a)} {check_is_true(check)} {mate_is_true(mate)}'
                else :  
                    return f'Take Pawn{promoted_is_true(promoted,a)} {check_is_true(check)} {mate_is_true(mate)}' 
   
    elif a[:5] =='O-O-O' :  
        return f'Long Castle {check_is_true(check)} {mate_is_true(mate)}'
    elif a[:3] =='O-O' :
        return f'Castle {check_is_true(check)} {mate_is_true(mate)}'
    elif promoted:
        return f'Promoted {check_is_true(check)} {mate_is_true(mate)}'                    
    if check:
        return 'Check'  
    elif mate:
        return 'Check and Mate'  
    else:
        return 'Moved'

# har nuuj tsagaan list harna 
def move_analysis_white_by_black(a, white_moves_list):
    if a == ' ' :
        return ' '
    else :
        a = str(a)
        last_elements = []
        for i in range(len(white_moves_list)-1, -1, -1):
            last_elements.append(white_moves_list[i])
        last_elements = element_list_edit_white(last_elements)    
        # convert 'a' to a string, and then replace '+', ' ' and '#'
        str_a = str(a).replace('+', '').replace(' ', '').replace('#', '')
        # use re.split to split the string into a list of substrings
        split_str_a = re.split('x', str_a)
        # get the last element of the list (this will be the 'dd' value)
        dd = split_str_a[-1]
        take =  any('x' in s for s in a )
        check =  any('+' in s for s in a)
        promoted  =  any('=' in s for s in a) 
        mate =  any('#' in s for s in a)
        if promoted :
            dd = dd.replace('=', '').replace('+', '' ).replace('#','')[:-1]
        if take:        
            for i in last_elements:
                print ( f' hiiiiiiiiiiiiiiiiiiiiiiiii {a}   har nuusn {promoted_list(i)}')
                i = promoted_list(i)
                if str(dd) ==  promoted_list(i).replace('+', '' ).replace('#','')[-2:] :
                    if i[0] == 'B':
                        return f'Take Bishop{promoted_is_true(promoted,a)} {check_is_true(check)} {mate_is_true(mate)}' 
                    elif i[0] == 'N':
                        return f'Take Knight{promoted_is_true(promoted,a)} {check_is_true(check)} {mate_is_true(mate)}'
                    elif i[0] == 'R':
                        return f'Take Rook{promoted_is_true(promoted,a)} {check_is_true(check)} {mate_is_true(mate)}'
                    elif i[0] == 'Q':
                        return f'Take Queen{promoted_is_true(promoted,a)} {check_is_true(check)} {mate_is_true(mate)}'
                    else :  
                        return f'Take Pawn{promoted_is_true(promoted,a)} {check_is_true(check)} {mate_is_true(mate)}'
    
        elif a[:5] =='O-O-O' :  
            return f'Long Castle {check_is_true(check)} {mate_is_true(mate)}'
        elif a[:3] =='O-O' :
            return f'Castle {check_is_true(check)} {mate_is_true(mate)}'

        elif promoted:
            return f'Promoted {check_is_true(check)} {mate_is_true(mate)}'
        elif check:
            return 'Check'
        elif mate:
            return 'Check and Mate'     
        else:
            return 'Moved'    


def df_read(dfa,white_moves_list,black_moves_list,game, move, white, black, result, white_rank, black_rank):
    #  tsagaan nuune hariin list ees haina 
    a = move_analysis_black_by_white(white, black_moves_list)
    # har nuune tsagaanii list ees haina 
    b = move_analysis_white_by_black(black, white_moves_list)
    dfa = dfa.append({'Game' : game , 'Move' : move , 'White': white, 'White_moved' : a ,  'Black': black, 'Black_moved' : b, 
                        'Result' : result , 'WhiteRank': white_rank, 'BlackRank': black_rank}, ignore_index=True) 
    return dfa


## --------------------------------------------------------------- MAIN SECTION ---------------------------------------------------------------
    
# Reading excel file
file_path =r'C:\Users\Badral\Desktop\chees analysis data\first_example________________.xlsx'

# Excel file into a pandas 
df = pd.read_excel(file_path)

# Initialize an empty DataFrame
df_all = pd.DataFrame(columns=['Game' , 'Move', 'White', 'Black','White_moved', 'Black_moved', 'Result', 'WhiteRank', 'BlackRank'])

dfa = pd.DataFrame(columns=['Game', 'Move', 'White', 'Black','White_moved', 'Black_moved', 'Result', 'WhiteRank', 'BlackRank'])
white_moves_list = []
black_moves_list = []
index = 0
z = 1
while index + 1 < len(df) :    
    if len(white_moves_list) > 0 :
        white_moves_list.append( df.loc[index-1 ,'White']) 
    
    if df.loc[index,'Move'] != 1 and df.loc[index + 1,'Move'] == 1  :
        df_a = pd.DataFrame(df_read(dfa,white_moves_list,black_moves_list, z, df.loc[index,'Move'] , df.loc[index,'White'] , df.loc[index,'Black'], df.loc[index,'Result'] , df.loc[index,'WhiteRank'], df.loc[index,'BlackRank']  ))
        black_moves_list.append( df.loc[index,'Black']) 
        white_moves_list.append( df.loc[index + 1,'White']) 
        df_all = pd.concat([df_all, df_a]) 
        z += 1
        black_moves_list = []
        white_moves_list = []
    else : 
        df_a = pd.DataFrame(df_read(dfa,white_moves_list,black_moves_list, z, df.loc[index,'Move'] , df.loc[index,'White'] , df.loc[index,'Black'], df.loc[index,'Result'] , df.loc[index,'WhiteRank'], df.loc[index,'BlackRank']  ))
        black_moves_list.append( df.loc[index,'Black']) 
        white_moves_list.append( df.loc[index + 1,'White'])         
        df_all = pd.concat([df_all, df_a])

    index += 1 
    

print(df_all)

# extract dataframe into excel file 
df_all.to_excel(r'C:\Users\Badral\Desktop\chees analysis data\fulldata_output_output_.xlsx', index=False) 