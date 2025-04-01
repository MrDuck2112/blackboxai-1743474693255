import pygame
import os

def create_background():
    # Initialize pygame
    pygame.init()
    
    # Create a surface for the background
    width, height = 800, 600
    surface = pygame.Surface((width, height))
    
    # Fill with dark gray for the road
    surface.fill((50, 50, 50))
    
    # Draw road markings
    # Center line
    for y in range(0, height, 40):
        pygame.draw.rect(surface, (255, 255, 255), (width//2 - 5, y, 10, 20))
    
    # Side lines
    pygame.draw.line(surface, (255, 255, 0), (100, 0), (100, height), 5)
    pygame.draw.line(surface, (255, 255, 0), (width-100, 0), (width-100, height), 5)
    
    # Save the background
    pygame.image.save(surface, "assets/images/background.png")

def create_car():
    # Create a surface for the car
    width, height = 60, 100
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Draw car body (red)
    pygame.draw.rect(surface, (255, 0, 0), (10, 10, width-20, height-20))
    # Draw windows (blue)
    pygame.draw.rect(surface, (0, 0, 255), (15, 20, width-30, 30))
    # Draw wheels (black)
    pygame.draw.rect(surface, (0, 0, 0), (5, 5, 15, 25))
    pygame.draw.rect(surface, (0, 0, 0), (width-20, 5, 15, 25))
    pygame.draw.rect(surface, (0, 0, 0), (5, height-30, 15, 25))
    pygame.draw.rect(surface, (0, 0, 0), (width-20, height-30, 15, 25))
    
    # Save the player car
    pygame.image.save(surface, "assets/images/car.png")
    
    # Create enemy car (different color)
    surface.fill((0, 0, 0, 0))  # Clear surface
    pygame.draw.rect(surface, (0, 255, 0), (10, 10, width-20, height-20))
    pygame.draw.rect(surface, (0, 0, 255), (15, 20, width-30, 30))
    pygame.draw.rect(surface, (0, 0, 0), (5, 5, 15, 25))
    pygame.draw.rect(surface, (0, 0, 0), (width-20, 5, 15, 25))
    pygame.draw.rect(surface, (0, 0, 0), (5, height-30, 15, 25))
    pygame.draw.rect(surface, (0, 0, 0), (width-20, height-30, 15, 25))
    
    # Save the enemy car
    pygame.image.save(surface, "assets/images/enemy_car.png")

def create_empty_sounds():
    """Create empty sound files as placeholders"""
    # Create empty files for sounds
    open("assets/sounds/engine.wav", 'w').close()
    open("assets/sounds/crash.wav", 'w').close()

if __name__ == "__main__":
    # Create all assets
    create_background()
    create_car()
    create_empty_sounds()
    
    print("Assets created successfully!")