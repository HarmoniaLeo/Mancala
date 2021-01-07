# -*- coding: utf-8 -*-
import random
import numpy as np
import agent
from world import getLegalActions 
from minimaxAgent import minimaxAgent

class Mancala_RL:
    
    def __init__(self, mancala_agent=None):
        self.pockets = [4,4,4,4,4,4,0,4,4,4,4,4,4,0,True]
        # Load Mancala agent if necessary
        if mancala_agent is None:
            self.mancala_agent = agent.ReinforceAgent()
        else:
            self.mancala_agent = mancala_agent
        
    def play_game(self, reinforcement_learning = False):
        
        # Reset board
        self.pockets = [4,4,4,4,4,4,0,4,4,4,4,4,4,0,True]
        
        mancala_agent = self.mancala_agent
        mancala_agent.previous_state = self.get_state(player=False)
    
        player_turn = self.pockets[-1]
        previous_move = -1 # Previous move marked in board draw
        
        game_over = False
        while not(game_over):
            
            # Start by drawing the board
            
            # Ask for move from corresponding player
            if player_turn == True:

                # Basic computer randomly chooses a Mancala position
                valid_move = False
                while not(valid_move):
                    move = self.convert_move(random.randint(1,6),player_turn)
                    # move=minimaxAgent().play(self.get_state(player_turn).extend([player_turn]))+1
                    valid_move = self.valid_move(move, player_turn)
            else:
                # Basic computer randomly chooses a Mancala position
                valid_move = False
                while not(valid_move):
                    computer_action = mancala_agent.take_action(self.get_state(player_turn))
                    move = self.convert_move(computer_action, player_turn)
                    valid_move = self.valid_move(move, player_turn)
                    
                # Inject the state into the agent for learning
                mancala_agent.update_q(self.get_state(player_turn))
                    
            # Check if move is valid prior to performing
            if not(self.valid_move(move, player_turn)):
                print("INVALID MOVE")
                continue
            
            # Perform assumed valid move and determine next to move
            player_turn, game_over = self.simulate_move(move, player_turn)
            
            # Update previous move
            previous_move = move

        # Assume mancala agent is player 2 for now
        mancala_agent.update_q(self.get_state(player=False), self.pockets[13])

        # Update agent for persistence
        self.mancala_agent = mancala_agent
            
    def convert_move(self, move, player):
        """ Converts the standard 1-6 input of the player into the corresponding
        pocket for each player as needed
        """
        if player == True:
            return move-1 # Shift left once to get the pocket position
        if player == False:
            return move+6 # Shift right 6 spaces to refer to upper board spot
        return False # Error case handling
    
    def valid_move(self, pocket_position, player):
        
        # Move is invalid if player chooses anything other than own pockets
        player_1_side = (0 <= pocket_position <= 5)
        player_2_side = (7 <= pocket_position <= 12)
        
        # Must have stones in the pocket to be valid
        if self.pockets[pocket_position] > 0:
            if player_1_side and player==True:
                return True
            if player_2_side and player==False:
                return True
            
        # All other moves are false
        return False
    
    
    def check_game_over(self):
        """ Checks if all pockets are empty of stones. If so assigns all
            remaining stones to the appropriate mancala.
        """
        
        game_over = False
        
        empty_player_1 = sum(self.pockets[:6]) == 0
        empty_player_2 = sum(self.pockets[7:13]) == 0
        
        # If player 2 is empty, collect player 1's stones
        if empty_player_2:
            # Put remaining stones in player 2's mancala
            self.pockets[6] += sum(self.pockets[:6])
            self.pockets[:6] = [0]*6
            game_over = True
        
        # If player 1 is empty, collect player 1's stones
        if empty_player_1:
            # Put remaining stones in player 2's mancala
            self.pockets[13] += sum(self.pockets[7:13])
            self.pockets[7:13] = [0]*6
            game_over = True
        
        return game_over
    
    def determine_winner(self):
        
        if self.pockets[13]>self.pockets[6]:
            return "Player 2"
        elif self.pockets[13]<self.pockets[6]:
            return "Player 1"
        return "Draw"
    
    def switch_player(self, player):
        
        if player == True:
            return False
        return True
    
    def capture(self, pocket_position, mancala_pocket):
        """ Captures all stones in the pocket and pocket opposite, goes into
        The proper mancala pocket specified as input
        """
        
        opposite_pocket_dict = {0: 12, 1:11, 2:10, 3:9, 4:8, 5:7,
                                7:5, 8:4, 9:3, 10:2, 11:1, 12:0}
        
        # Take the stone from the pocket itself
        self.pockets[mancala_pocket] += self.pockets[pocket_position]
        self.pockets[pocket_position] = 0
        
        # Take the stones from the opposite pocket
        opposite_pocket = opposite_pocket_dict[pocket_position]
        self.pockets[mancala_pocket] += self.pockets[opposite_pocket]
        self.pockets[opposite_pocket] = 0
        
        return True
    
    def simulate_move(self, pocket_position, player):
        
        # Condense to local version of pockets
        pockets = self.pockets
        
        stones_drawn = pockets[pocket_position]
        pockets[pocket_position] = 0
        
        # Inefficient loop, clean up in future
        while stones_drawn > 0:
            pocket_position += 1
            
            # Case to handle looping back to start of board
            if pocket_position > 13:
                pocket_position = 0
                
            # Consider special cases (mancala pocket) before normal stone drops
            # 不考虑额外步骤
            # mancala_1_position = pocket_position==6
            # mancala_2_position = pocket_position==13
            player_1 = player == True
            player_2 = player == False
            # if mancala_1_position and player_2:
            #     continue # Skip stone drop and proceeding logic
            # if mancala_2_position and player_1:
            #     continue # Skip stone drop and proceeding logic
                
            # Stone drop
            pockets[pocket_position] += 1
            stones_drawn -= 1
        
        # Determine if capture occurs
        end_on_player_1_side = (0 <= pocket_position <= 5)
        end_on_player_2_side = (7 <= pocket_position <= 12)
        
        # Only capture if stone is empty (has 1 stone after placement)
        stone_was_empty = pockets[pocket_position] == 1
        
        # Player 1 capture
        if player_1 and end_on_player_1_side and stone_was_empty:
            self.capture(pocket_position, 6)
            
        # Player 2 capture
        if player_2 and end_on_player_2_side and stone_was_empty:
            self.capture(pocket_position, 13)
        
        # Determine next player
        # if mancala_1_position and player_1:
        #     next_player = player # Player 1 Mancala gets another turn
        # elif mancala_2_position and player_2:
        #     next_player = player # Player 2 Mancala gets another turn
        # else:
        next_player = self.switch_player(player) # All else switch player
        
        game_over = self.check_game_over()
        
        return next_player, game_over
    
    def get_state(self, player):
        """ Returns the unique numeric state of the board for each player from
            the players own perspective. Mancala pockets not necessary but they
            can act as the reward to the computer at the end of the game.
        """
        
        pocket_copy = list(self.pockets)
        
        # Flip the board interpretation if player 2
        if player == True:
            relevant_pockets = pocket_copy[:6] + pocket_copy[7:13]
        else:
            relevant_pockets = pocket_copy[7:13] + pocket_copy[:6]
            
                    
        return relevant_pockets