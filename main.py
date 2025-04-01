import pygame
import sys
import os
from constants import *
from menu import Menu
from game import Game

class GameManager:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        
        # Try to initialize audio, but continue if it fails
        try:
            pygame.mixer.init()
        except pygame.error:
            print("Warning: Audio initialization failed. Game will run without sound.")
        
        # Set up display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(MENU_TITLE)
        
        # Create necessary directories if they don't exist
        self.create_directories()
        
        # Initialize states
        self.menu = Menu(self.screen)
        self.game = Game(self.screen)
        
        # State management
        self.current_state = "menu"
        self.running = True

    def create_directories(self):
        """Create necessary directories for assets"""
        try:
            os.makedirs(IMAGES_DIR, exist_ok=True)
            os.makedirs(SOUNDS_DIR, exist_ok=True)
        except Exception as e:
            print(f"Error creating directories: {e}")

    def handle_game_over(self):
        """Handle game over state"""
        font = pygame.font.Font(None, 74)
        game_over_text = font.render("Game Over!", True, RED)
        score_text = font.render(f"Score: {self.game.score}", True, WHITE)
        restart_text = font.render("Press SPACE to restart", True, WHITE)
        menu_text = font.render("Press ESC for menu", True, WHITE)

        text_positions = [
            (game_over_text, SCREEN_HEIGHT//2 - 100),
            (score_text, SCREEN_HEIGHT//2),
            (restart_text, SCREEN_HEIGHT//2 + 100),
            (menu_text, SCREEN_HEIGHT//2 + 160)
        ]

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.game = Game(self.screen)
                        return "game"
                    if event.key == pygame.K_ESCAPE:
                        return "menu"

            # Draw game over screen
            self.screen.fill((30, 30, 50))  # Dark background
            
            # Draw all text elements with shadow effect
            for text_surface, y_pos in text_positions:
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, y_pos))
                
                # Draw shadow
                shadow_surface = font.render(text_surface.get_string(), True, (0, 0, 0))
                shadow_rect = shadow_surface.get_rect(center=(SCREEN_WIDTH//2 + 3, y_pos + 3))
                self.screen.blit(shadow_surface, shadow_rect)
                
                # Draw text
                self.screen.blit(text_surface, text_rect)

            pygame.display.flip()

    def run(self):
        """Main game loop"""
        while self.running:
            if self.current_state == "menu":
                self.current_state = self.menu.run()
            elif self.current_state == "game":
                self.current_state = self.game.run()
            elif self.current_state == "game_over":
                self.current_state = self.handle_game_over()
            elif self.current_state == "quit":
                self.running = False
            else:
                print(f"Unknown state: {self.current_state}")
                self.running = False

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    try:
        game = GameManager()
        game.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        pygame.quit()
        sys.exit(1)