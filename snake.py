import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 10
CELL_SIZE = 50
WINDOW_WIDTH = GRID_SIZE * CELL_SIZE + 200
WINDOW_HEIGHT = GRID_SIZE * CELL_SIZE + 100
FPS = 60
WIN_LENGTH = 5

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)
GREEN = (0, 200, 0)

class Board:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.board_x = 50
        self.board_y = 50
    
    def get_cell_from_mouse(self, mouse_pos):
        """Convert mouse position to grid cell coordinates"""
        x, y = mouse_pos
        cell_x = (x - self.board_x) // CELL_SIZE
        cell_y = (y - self.board_y) // CELL_SIZE
        
        # Check if click is within grid bounds
        if 0 <= cell_x < GRID_SIZE and 0 <= cell_y < GRID_SIZE:
            return (cell_x, cell_y)
        return None
    
    def is_valid_move(self, cell_x, cell_y):
        """Check if a move is valid"""
        if cell_x < 0 or cell_x >= GRID_SIZE or cell_y < 0 or cell_y >= GRID_SIZE:
            return False
        return self.grid[cell_y][cell_x] == 0
    
    def make_move(self, cell_x, cell_y, player):
        """Place a player's mark on the board"""
        if self.is_valid_move(cell_x, cell_y):
            self.grid[cell_y][cell_x] = player
            return True
        return False
    
    def check_winner(self, player):
        """Check if the given player has won"""
        # Check horizontal
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE - WIN_LENGTH + 1):
                if all(self.grid[y][x + i] == player for i in range(WIN_LENGTH)):
                    return True
        
        # Check vertical
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE - WIN_LENGTH + 1):
                if all(self.grid[y + i][x] == player for i in range(WIN_LENGTH)):
                    return True
        
        # Check diagonal (top-left to bottom-right)
        for y in range(GRID_SIZE - WIN_LENGTH + 1):
            for x in range(GRID_SIZE - WIN_LENGTH + 1):
                if all(self.grid[y + i][x + i] == player for i in range(WIN_LENGTH)):
                    return True
        
        # Check diagonal (top-right to bottom-left)
        for y in range(GRID_SIZE - WIN_LENGTH + 1):
            for x in range(WIN_LENGTH - 1, GRID_SIZE):
                if all(self.grid[y + i][x - i] == player for i in range(WIN_LENGTH)):
                    return True
        
        return False
    
    def is_board_full(self):
        """Check if the board is completely filled"""
        return all(self.grid[y][x] != 0 for y in range(GRID_SIZE) for x in range(GRID_SIZE))
    
    def draw(self, screen):
        """Draw the game board"""
        # Draw grid lines
        for i in range(GRID_SIZE + 1):
            # Horizontal lines
            pygame.draw.line(screen, LIGHT_GRAY,
                           (self.board_x, self.board_y + i * CELL_SIZE),
                           (self.board_x + GRID_SIZE * CELL_SIZE, self.board_y + i * CELL_SIZE), 1)
            # Vertical lines
            pygame.draw.line(screen, LIGHT_GRAY,
                           (self.board_x + i * CELL_SIZE, self.board_y),
                           (self.board_x + i * CELL_SIZE, self.board_y + GRID_SIZE * CELL_SIZE), 1)
        
        # Draw board border
        pygame.draw.rect(screen, WHITE,
                        (self.board_x, self.board_y, GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE), 2)
        
        # Draw X's and O's
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                cell_value = self.grid[y][x]
                cell_x = self.board_x + x * CELL_SIZE + CELL_SIZE // 2
                cell_y = self.board_y + y * CELL_SIZE + CELL_SIZE // 2
                
                if cell_value == 1:  # Player 1 (X)
                    offset = CELL_SIZE // 4
                    pygame.draw.line(screen, BLUE,
                                   (cell_x - offset, cell_y - offset),
                                   (cell_x + offset, cell_y + offset), 3)
                    pygame.draw.line(screen, BLUE,
                                   (cell_x + offset, cell_y - offset),
                                   (cell_x - offset, cell_y + offset), 3)
                elif cell_value == 2:  # Player 2 (O)
                    pygame.draw.circle(screen, RED, (cell_x, cell_y), CELL_SIZE // 4, 3)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tic Tac Toe 10x10 - 5 in a Row")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        self.small_font = pygame.font.Font(None, 28)
        
        self.board = Board()
        self.current_player = 1  # 1 for Player 1 (X), 2 for Player 2 (O)
        self.game_over = False
        self.winner = None
        self.move_count = 0
        
        # Timer setup - 5 minutes (300 seconds) per player
        self.total_time = 300  # 5 minutes in seconds
        self.player1_time = self.total_time
        self.player2_time = self.total_time
        self.last_time = pygame.time.get_ticks()
    
    def handle_events(self):
        """Handle user input and window events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.game_over:
                    cell = self.board.get_cell_from_mouse(event.pos)
                    if cell:
                        cell_x, cell_y = cell
                        if self.board.make_move(cell_x, cell_y, self.current_player):
                            self.move_count += 1
                            
                            # Check for winner
                            if self.board.check_winner(self.current_player):
                                self.game_over = True
                                self.winner = self.current_player
                            elif self.board.is_board_full():
                                self.game_over = True
                                self.winner = 0  # Draw
                            else:
                                # Switch player and update timer reference
                                self.current_player = 2 if self.current_player == 1 else 1
                                self.last_time = pygame.time.get_ticks()
                else:
                    # Restart game on click when game is over
                    self.__init__()
        
        return True
    
    def update(self):
        """Update game logic and timers"""
        if not self.game_over:
            # Update timer
            current_time = pygame.time.get_ticks()
            elapsed = (current_time - self.last_time) / 1000.0  # Convert to seconds
            
            if self.current_player == 1:
                self.player1_time -= elapsed
                if self.player1_time <= 0:
                    self.player1_time = 0
                    self.game_over = True
                    self.winner = 2  # Player 2 wins by timeout
            else:
                self.player2_time -= elapsed
                if self.player2_time <= 0:
                    self.player2_time = 0
                    self.game_over = True
                    self.winner = 1  # Player 1 wins by timeout
            
            self.last_time = current_time
    
    def format_time(self, seconds):
        """Format seconds to MM:SS"""
        minutes = int(seconds) // 60
        secs = int(seconds) % 60
        return f"{minutes}:{secs:02d}"
    
    def draw(self):
        """Draw everything on the screen"""
        self.screen.fill(BLACK)
        
        self.board.draw(self.screen)
        
        # Draw game info panel
        info_x = self.board.board_x + GRID_SIZE * CELL_SIZE + 20
        
        if not self.game_over:
            player_text = f"Player {self.current_player}'s Turn"
            player_display = "X (BLUE)" if self.current_player == 1 else "O (RED)"
            color = BLUE if self.current_player == 1 else RED
        else:
            if self.winner == 0:
                player_text = "DRAW!"
                player_display = ""
                color = WHITE
            elif self.winner == 1:
                player_text = "Player 1 Wins!"
                player_display = "X (BLUE)"
                color = BLUE
            else:
                player_text = "Player 2 Wins!"
                player_display = "O (RED)"
                color = RED
        
        # Draw current player/result
        title_text = self.font.render(player_text, True, color)
        self.screen.blit(title_text, (info_x, 50))
        
        if player_display:
            display_text = self.small_font.render(player_display, True, color)
            self.screen.blit(display_text, (info_x, 100))
        
        # Draw timers
        timer_label1 = self.small_font.render("Player 1 Time:", True, BLUE)
        timer_text1 = self.small_font.render(self.format_time(self.player1_time), True, BLUE)
        self.screen.blit(timer_label1, (info_x, 160))
        self.screen.blit(timer_text1, (info_x, 190))
        
        timer_label2 = self.small_font.render("Player 2 Time:", True, RED)
        timer_text2 = self.small_font.render(self.format_time(self.player2_time), True, RED)
        self.screen.blit(timer_label2, (info_x, 240))
        self.screen.blit(timer_text2, (info_x, 270))
        
        # Draw instructions
        if not self.game_over:
            instruction1 = self.small_font.render("Click to place", True, WHITE)
            instruction2 = self.small_font.render("your mark", True, WHITE)
            self.screen.blit(instruction1, (info_x, 330))
            self.screen.blit(instruction2, (info_x, 360))
        else:
            instruction = self.small_font.render("Click to restart", True, WHITE)
            self.screen.blit(instruction, (info_x, 330))
        
        # Draw move counter
        move_text = self.small_font.render(f"Moves: {self.move_count}", True, WHITE)
        self.screen.blit(move_text, (info_x, WINDOW_HEIGHT - 60))
        
        # Draw rules
        rule1 = self.small_font.render("10x10 Grid", True, GRAY)
        rule2 = self.small_font.render("5 in a row wins", True, GRAY)
        self.screen.blit(rule1, (info_x, WINDOW_HEIGHT - 90))
        self.screen.blit(rule2, (info_x, WINDOW_HEIGHT - 120))
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
