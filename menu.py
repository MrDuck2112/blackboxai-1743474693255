import pygame
import sys
from constants import *

class Button:
    def __init__(self, x, y, width, height, text, font_size=32):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font_size = font_size
        self.is_hovered = False
        
        # Button colors
        self.normal_color = (100, 100, 255)
        self.hover_color = (150, 150, 255)
        self.text_color = WHITE
        
        # Button animation
        self.current_scale = 1.0
        self.target_scale = 1.0
        self.scale_speed = 0.2

    def draw(self, screen):
        # Animate button scale
        self.current_scale += (self.target_scale - self.current_scale) * self.scale_speed
        
        # Calculate scaled dimensions
        scaled_width = int(self.rect.width * self.current_scale)
        scaled_height = int(self.rect.height * self.current_scale)
        x = self.rect.centerx - scaled_width // 2
        y = self.rect.centery - scaled_height // 2
        
        # Draw button background with rounded corners
        button_surface = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
        pygame.draw.rect(button_surface, 
                        self.hover_color if self.is_hovered else self.normal_color,
                        (0, 0, scaled_width, scaled_height),
                        border_radius=15)
        
        # Add shadow effect
        shadow_surface = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, (0, 0, 0, 50),
                        (4, 4, scaled_width, scaled_height),
                        border_radius=15)
        screen.blit(shadow_surface, (x, y))
        
        # Draw main button
        screen.blit(button_surface, (x, y))
        
        # Draw text
        font = pygame.font.Font(None, self.font_size)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.centery))
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            # Check if mouse is hovering over button
            self.is_hovered = self.rect.collidepoint(event.pos)
            self.target_scale = 1.1 if self.is_hovered else 1.0
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.buttons = []
        self.setup_buttons()
        
        # Title properties
        self.title_font = pygame.font.Font(None, 74)
        self.title_color = WHITE
        self.title_pos = (SCREEN_WIDTH // 2, 100)
        
        # Background properties
        self.bg_color = (30, 30, 50)
        self.bg_squares = [(pygame.Rect(x * 50, y * 50, 40, 40), (40, 40, 60)) 
                          for x in range(-1, SCREEN_WIDTH // 50 + 1)
                          for y in range(-1, SCREEN_HEIGHT // 50 + 1)]
        self.bg_offset = 0

    def setup_buttons(self):
        button_y = SCREEN_HEIGHT // 2
        self.buttons = [
            Button(SCREEN_WIDTH//2 - BUTTON_WIDTH//2, button_y, 
                  BUTTON_WIDTH, BUTTON_HEIGHT, "Start Game"),
            Button(SCREEN_WIDTH//2 - BUTTON_WIDTH//2, button_y + BUTTON_HEIGHT + BUTTON_PADDING,
                  BUTTON_WIDTH, BUTTON_HEIGHT, "Options"),
            Button(SCREEN_WIDTH//2 - BUTTON_WIDTH//2, button_y + (BUTTON_HEIGHT + BUTTON_PADDING) * 2,
                  BUTTON_WIDTH, BUTTON_HEIGHT, "Quit")
        ]

    def draw_background(self):
        # Fill base color
        self.screen.fill(self.bg_color)
        
        # Animate background squares
        self.bg_offset = (self.bg_offset + 0.5) % 50
        
        # Draw animated grid
        for rect, color in self.bg_squares:
            moved_rect = rect.copy()
            moved_rect.y = (rect.y + self.bg_offset) % (SCREEN_HEIGHT + 50) - 50
            pygame.draw.rect(self.screen, color, moved_rect)

    def draw_title(self):
        # Create gradient effect for title
        base_font = pygame.font.Font(None, 74)
        text_surface = base_font.render(MENU_TITLE, True, self.title_color)
        
        # Add shadow
        shadow_surface = base_font.render(MENU_TITLE, True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect(center=(self.title_pos[0] + 3, self.title_pos[1] + 3))
        self.screen.blit(shadow_surface, shadow_rect)
        
        # Draw main title
        text_rect = text_surface.get_rect(center=self.title_pos)
        self.screen.blit(text_surface, text_rect)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Handle button events
                for i, button in enumerate(self.buttons):
                    if button.handle_event(event):
                        if i == 0:  # Start Game
                            return "game"
                        elif i == 1:  # Options
                            return "options"
                        elif i == 2:  # Quit
                            pygame.quit()
                            sys.exit()

            # Draw everything
            self.draw_background()
            self.draw_title()
            for button in self.buttons:
                button.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)