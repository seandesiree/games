import random  
import os  

def clear_screen():
    """Clears the console screen based on the operating system."""
    if os.environ.get('TERM'):  
        os.system('cls' if os.name == 'nt' else 'clear')  

class Game:
    """Defines the game logic for Hangman."""
    MAX_MOVES = 7  
    WORD_BANK = ("sculpturepark", "publicart", "generativeai", "deancollection", "artbasel",
                 "springbreak", "diabeacon", "processor", "socialpractice", "critique", "brooklynmuseum")  

    def __init__(self):
        """Initializes a new game instance with a random word and reset counters."""
        self.word = random.choice(Game.WORD_BANK)  
        self.guessed_letters = set()  
        self.number_of_moves = 0  

    def guess_letter(self, letter):
        """Processes a single letter guess and updates the game state."""
        if letter in self.guessed_letters:  
            return False, 'already guessed'
        self.guessed_letters.add(letter)  
        if letter in self.word: 
            return True, None
        else:
            self.number_of_moves += 1  
            return False, None

    def is_solved(self):
        """Checks if the entire word has been correctly guessed."""
        return all(letter in self.guessed_letters for letter in self.word)

    def has_guesses_left(self):
        """Determines if the player has remaining guesses."""
        return self.number_of_moves < Game.MAX_MOVES

    def get_masked_word(self):
        """Returns the current state of the word with unguessed letters masked."""
        return ' '.join([letter if letter in self.guessed_letters else '_' for letter in self.word])

    def get_remaining_moves(self):
        """Returns the number of remaining moves allowed."""
        return Game.MAX_MOVES - self.number_of_moves

class UserInterface:
    """Handles all user interactions."""
    def __init__(self, game):
        """Initializes the user interface with a game instance."""
        self.game = game  
        self.next_alert = ''  

    def display_game_state(self):
        """Displays the current game state and clears the previous content."""
        clear_screen()
        if self.next_alert: 
            print(self.next_alert)
            self.next_alert = ''  
        print(self.game.get_masked_word())  
        print(f"Guessed Letters: {', '.join(sorted(self.game.guessed_letters)) if self.game.guessed_letters else 'None'}")
        print(f"Moves left: {self.game.get_remaining_moves()}")  

    def update_alert(self, message):
        """Updates the message to be displayed on the next screen refresh."""
        self.next_alert = message

    def get_user_input(self):
        """Prompts the user for a letter or a word guess."""
        return input("Enter a letter or 'guess' to guess the whole word: ").strip().lower()

    def show_message(self, message):
        """Displays a message to the user."""
        if message:
            print(message)

    def user_won(self):
        """Displays a winning message."""
        print("Amazing work! You solved the art puzzle!")

    def user_lost(self):
        """Displays a losing message with the correct word."""
        print(f"Unfortunately, you didn't guess the word. :( It was '{self.game.word}'. Better luck next time!")

def main():
    """Main function to control the flow of the game."""
    game = Game()  
    ui = UserInterface(game)  

    while game.has_guesses_left() and not game.is_solved():  
        ui.display_game_state() 
        choice = ui.get_user_input() 

        if choice == 'guess':  
            word_guess = input("Guess the whole word: ").strip().lower()
            if word_guess == game.word:  
                ui.user_won()
                return
            else:
                ui.update_alert("Wrong guess!") 
                continue
        elif len(choice) == 1 and choice.isalpha():  
            correct, message = game.guess_letter(choice)  
            if not correct:
                alert_msg = "You already guessed that letter." if message == 'already guessed' else f"{choice} is not in the word."
                ui.update_alert(alert_msg) 
        else:
            ui.update_alert("Invalid input. Please enter a single letter.")  

    if not game.is_solved(): 
        ui.user_lost()  

if __name__ == "__main__":
    main()  