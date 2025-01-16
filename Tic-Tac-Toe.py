import tkinter as tk
from tkinter import messagebox
from typing import List, Tuple
import random

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe")
        self.window.configure(bg='#2C3E50')
        
        # Game state variables
        self.current_player = 'X'
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.game_active = False
        self.vs_computer = False
        self.scores = {'X': 0, 'O': 0}
        
        # Player information
        self.player1_name = tk.StringVar(value="Player 1")
        self.player2_name = tk.StringVar(value="Player 2")
        
        self._create_menu_frame()
        self._create_game_frame()
        self._create_score_frame()
        
    def _create_menu_frame(self):
        """Create the menu frame with player settings"""
        menu_frame = tk.Frame(self.window, bg='#2C3E50', pady=10)
        menu_frame.grid(row=0, column=0, sticky="ew")
        
        # Player 1 settings
        tk.Label(menu_frame, text="Player 1 (X):", font=('Arial', 12), bg='#2C3E50', fg='white').grid(row=0, column=0, padx=5)
        tk.Entry(menu_frame, textvariable=self.player1_name, font=('Arial', 12)).grid(row=0, column=1, padx=5)
        
        # Player 2 settings
        self.player2_label = tk.Label(menu_frame, text="Player 2 (O):", font=('Arial', 12), bg='#2C3E50', fg='white')
        self.player2_label.grid(row=0, column=2, padx=5)
        self.player2_entry = tk.Entry(menu_frame, textvariable=self.player2_name, font=('Arial', 12))
        self.player2_entry.grid(row=0, column=3, padx=5)
        
        # Game mode buttons
        tk.Button(menu_frame, text="Play vs Friend", command=self._start_pvp, font=('Arial', 12), bg='#3498DB', fg='white').grid(row=1, column=1, pady=10)
        tk.Button(menu_frame, text="Play vs Computer", command=self._start_pvc, font=('Arial', 12), bg='#3498DB', fg='white').grid(row=1, column=2, pady=10)
        
    def _create_game_frame(self):
        """Create the game board frame"""
        self.game_frame = tk.Frame(self.window, bg='#2C3E50')
        self.game_frame.grid(row=1, column=0, pady=10)
        
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(self.game_frame, text=' ', font=('Arial', 20, 'bold'),
                                 width=5, height=2, command=lambda r=i, c=j: self._make_move(r, c))
                button.grid(row=i, column=j, padx=3, pady=3)
                button['state'] = 'disabled'
                button.configure(bg='#34495E', fg='white', activebackground='#2C3E50')
                row.append(button)
            self.buttons.append(row)
            
    def _create_score_frame(self):
        """Create the score display frame"""
        score_frame = tk.Frame(self.window, bg='#2C3E50', pady=10)
        score_frame.grid(row=2, column=0)
        
        self.score_label = tk.Label(score_frame, text="Score: 0 - 0", font=('Arial', 14, 'bold'),
                                  bg='#2C3E50', fg='white')
        self.score_label.pack()
        
        tk.Button(score_frame, text="New Game", command=self._reset_board,
                 font=('Arial', 12), bg='#3498DB', fg='white').pack(pady=5)
        tk.Button(score_frame, text="Reset Scores", command=self._reset_scores,
                 font=('Arial', 12), bg='#3498DB', fg='white').pack(pady=5)
        
    def _start_pvp(self):
        """Start a player vs player game"""
        self.vs_computer = False
        self._start_game()
        
    def _start_pvc(self):
        """Start a player vs computer game"""
        self.vs_computer = True
        self.player2_name.set("Computer")
        self.player2_entry.configure(state='disabled')
        self._start_game()
        
    def _start_game(self):
        """Initialize the game board"""
        self.game_active = True
        self._reset_board()
        for row in self.buttons:
            for button in row:
                button['state'] = 'normal'
                
    def _make_move(self, row: int, col: int):
        """Handle a player's move"""
        if self.board[row][col] == ' ' and self.game_active:
            self.board[row][col] = self.current_player
            self.buttons[row][col].configure(text=self.current_player)
            
            if self._check_winner(self.current_player):
                self._handle_win()
            elif self._is_board_full():
                self._handle_draw()
            else:
                self._switch_player()
                if self.vs_computer and self.current_player == 'O' and self.game_active:
                    self.window.after(500, self._computer_move)
                    
    def _computer_move(self):
        """Make a move for the computer player"""
        # Try to win
        move = self._find_winning_move('O')
        if not move:
            # Try to block player's winning move
            move = self._find_winning_move('X')
        if not move:
            # Take center if available
            if self.board[1][1] == ' ':
                move = (1, 1)
            else:
                # Take random available move
                available_moves = [(i, j) for i in range(3) for j in range(3) 
                                 if self.board[i][j] == ' ']
                if available_moves:
                    move = random.choice(available_moves)
                    
        if move:
            row, col = move
            self._make_move(row, col)
            
    def _find_winning_move(self, player: str) -> Tuple[int, int]:
        """Find a winning move for the given player"""
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    self.board[i][j] = player
                    if self._check_winner(player):
                        self.board[i][j] = ' '
                        return (i, j)
                    self.board[i][j] = ' '
        return None
        
    def _check_winner(self, player: str) -> bool:
        """Check if the current player has won"""
        # Check rows and columns
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)) or \
               all(self.board[j][i] == player for j in range(3)):
                return True
                
        # Check diagonals
        if all(self.board[i][i] == player for i in range(3)) or \
           all(self.board[i][2-i] == player for i in range(3)):
            return True
            
        return False
        
    def _is_board_full(self) -> bool:
        """Check if the board is full"""
        return all(cell != ' ' for row in self.board for cell in row)
        
    def _handle_win(self):
        """Handle a win condition"""
        winner_name = self.player1_name.get() if self.current_player == 'X' else self.player2_name.get()
        self.scores[self.current_player] += 1
        self._update_score_label()
        messagebox.showinfo("Game Over", f"{winner_name} wins!")
        self.game_active = False
        
    def _handle_draw(self):
        """Handle a draw condition"""
        messagebox.showinfo("Game Over", "It's a draw!")
        self.game_active = False
        
    def _switch_player(self):
        """Switch the current player"""
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        
    def _reset_board(self):
        """Reset the game board"""
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_active = True
        for row in self.buttons:
            for button in row:
                button.configure(text=' ')
                
    def _reset_scores(self):
        """Reset the game scores"""
        self.scores = {'X': 0, 'O': 0}
        self._update_score_label()
        
    def _update_score_label(self):
        """Update the score display"""
        self.score_label.configure(
            text=f"Score: {self.player1_name.get()}: {self.scores['X']} - "
                 f"{self.player2_name.get()}: {self.scores['O']}")
        
    def run(self):
        """Start the game application"""
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
