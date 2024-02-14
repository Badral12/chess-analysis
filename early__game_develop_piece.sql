/*
CREATE TABLE early_game_chess
(
    Game INT,
	Move INT,
    White VARCHAR(255),
    Black VARCHAR(255),
    move_detail_white VARCHAR(255),
    move_detail_black VARCHAR(255),
    White_moved	VARCHAR(255),
    Black_moved	VARCHAR(255),
    Result VARCHAR(255),
    WhiteRank INT,
    BlackRank INT,
    white_rank_text VARCHAR(255),
	black_rank_text	VARCHAR(255),
    statuss VARCHAR(255)
);
*/
/*
INSERT into early_game_chess (Game,	Move,	White,	Black,	move_detail_white,	move_detail_black,	White_moved,	Black_moved,	Result,	WhiteRank,	BlackRank,	white_rank_text,	black_rank_text,	statuss)
Values( 1,	1,	'd4',	'Nf6',	'd pawm mowed ',	' King side Knight moved',	'Moved',	'Moved',	'1--0',	1455,	1504,	'competente',	'competente',	'competente'),
( 1,	2,	'c4',	'c5',	'c pawm mowed ',	'c pawm mowed ',	'Moved',	'Moved',	'1--0',	1455,	1504,	'competente',	'competente',	'competente');
*/

select statuss, avg(cnt_unq_details) from ( 
select statuss , game, count( distinct move_details) as cnt_unq_details 
from ( 
		select game , move , move_detail_black,  statuss,case when move_detail_black like '%pawm mowed%' then move_detail_black
				  when move_detail_black like '%King side Knight moved%' then 'King side Knight moved'
                  when move_detail_black like '%Queen side Knight moved%' then 'Queen side Knight moved'
                  
                  when move_detail_black like '%King side Rook moved%' then 'King side Rook moved'
                  when move_detail_black like '%Queen side Rook moved%' then 'Queen side Rook moved'
                  
                  when move_detail_black like '%King side Bishop moved%' then 'King side Bishop moved'
                  when move_detail_black like '%Queen side Bishop moved%' then 'Queen side Bishop moved'
                  
                  when move_detail_black like 'King moved ' then 'King moved' 
                  when move_detail_black like 'Queen moved 'then 'Queen moved' 
                  
                  when move_detail_black like 'King side castle ' then 'King side castle'  
                  when move_detail_black like 'Queen side castle ' then 'Queen side castle'  end 'move_details'
				  from early_game_chess
		where move between 1 and 10 and move_detail_black <> 'game ended'
) aa
group by statuss, game 
UNION ALL 
select statuss , game, count( distinct move_details) as cnt_unq_details 
from ( 
		select game , move , move_detail_black,  statuss,case when move_detail_white like '%pawm mowed%' then move_detail_black
				  when move_detail_white like '%King side Knight moved%' then 'King side Knight moved'
                  when move_detail_white like '%Queen side Knight moved%' then 'Queen side Knight moved'
                  
                  when move_detail_white like '%King side Rook moved%' then 'King side Rook moved'
                  when move_detail_white like '%Queen side Rook moved%' then 'Queen side Rook moved'
                  
                  when move_detail_white like '%King side Bishop moved%' then 'King side Bishop moved'
                  when move_detail_white like '%Queen side Bishop moved%' then 'Queen side Bishop moved'
                  
                  when move_detail_white like 'King moved ' then 'King moved' 
                  when move_detail_white like 'Queen moved 'then 'Queen moved' 
                  
                  when move_detail_white like 'King side castle ' then 'King side castle'  
                  when move_detail_white like 'Queen side castle ' then 'Queen side castle'  end 'move_details'
				  from early_game_chess
		where move between 1 and 10 and move_detail_white <> 'game ended'
) aa
group by statuss, game 

) second_haalt
group by statuss
     
		




