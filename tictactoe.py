import tkinter as tk
from tkinter import messagebox
import random


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title('Tic Tac Toe')
        self.player_turn = True 
        self.board = [""] * 9
        self.buttons = [tk.Button(
            self.root, text = '', font = ('normal', 40), height = 1, width = 2, 
            command = lambda idx = i: self.on_button_click(idx)
        )
            for i in range(9)]
        self.setup_grid()

    def setup_grid(self):
        for i in range(9):
            row, col = divmod(i, 3)
            self.buttons[i].grid(row = row, column = col)

    def on_button_click(self, idx):
        if self.buttons[idx]['text'] == '' and self.check_winner() is None:
            self.make_move(idx, "X")
            self.check_game_over()
            if "" in self.board and self.check_winner() is None:
                self.root.after(100, self.computer_move)

    def make_move(self, idx, player):
        self.buttons[idx]['text'] = player
        self.board[idx] = player

    def computer_move(self):
        move_made = False

        for player in ['O', 'X']:
            for i in range(9):
                if self .board[i] == '':
                    self.board[i] = player
                    if self.check_winner() == player:
                        self.make_move(i, 'O')
                        move_made = True
                        break
                    self.board[i] = ''
            if move_made:
                break
        if not move_made:
            available_moves = [i for i in range(9) if self.board[i] == ""]
            if available_moves:
                self.make_move(random.choice(available_moves), "O")

        self.check_game_over()

    def check_winner(self):
            wins = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
            for a, b, c in wins:
                if self.board[a] == self.board[b] == self.board[c] != '':
                    return self.board[a]
            return None
    
    def check_game_over(self):
        winner = self.check_winner()
        if winner:
            messagebox.showinfo("Game Over", f"{winner} wins!")
            self.reset_game()
        elif '' not in self.board:
            messagebox.showinfo("Game Over", f"CAT GAME!!!")
            self.reset_game()

    def reset_game(self):
        self.board = [""] * 9
        for button in self.buttons:
            button.config(text = "")



            

def main():
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()

if __name__ == '__main__':
    main()