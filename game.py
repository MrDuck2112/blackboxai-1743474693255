import pygame
import random
import math
from constants import *

class Car:
    def __init__(self, x, y, image_path):
        try:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (60, 100))
        except pygame.error:
            print(f"Error loading car image: {image_path}")
            # Create a default car shape if image fails to load
            self.image = pygame.Surface((60, 100))
            self.image.fill(RED if "enemy" in image_path else BLUE)
        
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Physics properties
        self.velocity = 0
        self.acceleration = 0
        self.angle = 0
        self.steering = 0
        
        # Position for precise movement
        self.x = float(x)
        self.y = float(y)

    def rotate(self):
        """Rotate the car image based on its angle"""
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def move(self):
        """Update car position based on physics"""
        # Convert angle to radians for math calculations
        rad = math.radians(self.angle)
        
        # Update velocity based on acceleration and friction
        self.velocity += self.acceleration
        self.velocity *= (1 - FRICTION)
        
        # Clamp velocity
        self.velocity = max(-PLAYER_MAX_SPEED, min(PLAYER_MAX_SPEED, self.velocity))
        
        # Update position based on velocity and angle
        self.x += -math.sin(rad) * self.velocity
        self.y += -math.cos(rad) * self.velocity
        
        # Update rectangle position
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)
        
        # Update angle based on steering
        if self.velocity != 0:
            self.angle += self.steering * (self.velocity / PLAYER_MAX_SPEED)
        
        # Keep angle in reasonable range
        self.angle %= 360
        
        # Rotate sprite
        self.rotate()

    def draw(self, screen):
        """Draw the car on the screen"""
        screen.blit(self.image, self.rect)

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.lap_count = 0
        self.start_time = pygame.time.get_ticks()
        
        # Load game assets
        self.load_assets()
        
        # Create player car
        self.player = Car(SCREEN_WIDTH//2, SCREEN_HEIGHT-100, PLAYER_CAR_IMAGE)
        
        # Enemy cars list
        self.enemies = []
        self.enemy_spawn_timer = 0
        
        # Initialize sounds (with error handling)
        self.init_sounds()
        
        # Font for HUD
        self.font = pygame.font.Font(None, 36)

    def load_assets(self):
        """Load game assets with error handling"""
        try:
            self.background = pygame.image.load(BACKGROUND_IMAGE)
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except pygame.error:
            print("Error loading background image")
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill(GRAY)
            # Draw some road markings
            pygame.draw.rect(self.background, BLACK, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            for i in range(0, SCREEN_HEIGHT, 50):
                pygame.draw.rect(self.background, WHITE, (SCREEN_WIDTH//2 - 5, i, 10, 30))

    def init_sounds(self):
        """Initialize game sounds with error handling"""
        self.engine_sound = None
        self.crash_sound = None
        try:
            if pygame.mixer.get_init():
                self.engine_sound = pygame.mixer.Sound(ENGINE_SOUND)
                self.crash_sound = pygame.mixer.Sound(CRASH_SOUND)
        except (pygame.error, FileNotFoundError) as e:
            print(f"Sound initialization failed: {e}")
            # Continue without sound

    def spawn_enemy(self):
        """Spawn a new enemy car"""
        x = random.randint(100, SCREEN_WIDTH-100)
        enemy = Car(x, -100, ENEMY_CAR_IMAGE)
        enemy.angle = 180
        self.enemies.append(enemy)

    def update_enemies(self):
        """Update enemy cars positions and remove off-screen enemies"""
        for enemy in self.enemies[:]:
            enemy.y += ENEMY_SPEED
            enemy.rect.centery = int(enemy.y)
            
            # Remove if off screen
            if enemy.rect.top > SCREEN_HEIGHT:
                self.enemies.remove(enemy)
                self.score += 10

    def check_collisions(self):
        """Check for collisions between player and enemies"""
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                if self.crash_sound and pygame.mixer.get_init():
                    try:
                        self.crash_sound.play()
                    except pygame.error:
                        pass
                return True
        return False

    def draw_hud(self):
        """Draw heads-up display (score, lap time, etc.)"""
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw lap count
        lap_text = self.font.render(f"Lap: {self.lap_count}", True, WHITE)
        self.screen.blit(lap_text, (10, 50))
        
        # Draw timer
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        timer_text = self.font.render(f"Time: {elapsed_time}s", True, WHITE)
        self.screen.blit(timer_text, (10, 90))

    def handle_input(self):
        """Handle player input"""
        keys = pygame.key.get_pressed()
        
        # Vertical movement (acceleration/brake)
        self.player.acceleration = 0
        if keys[pygame.K_UP]:
            self.player.acceleration = PLAYER_ACCELERATION
            if self.engine_sound and pygame.mixer.get_init():
                try:
                    self.engine_sound.play(-1)
                except pygame.error:
                    pass
        elif keys[pygame.K_DOWN]:
            self.player.acceleration = -PLAYER_ACCELERATION
        else:
            if self.engine_sound and pygame.mixer.get_init():
                try:
                    self.engine_sound.stop()
                except pygame.error:
                    pass
        
        # Horizontal movement (steering)
        self.player.steering = 0
        if keys[pygame.K_LEFT]:
            self.player.steering = 3
        elif keys[pygame.K_RIGHT]:
            self.player.steering = -3

    def run(self):
        """Main game loop"""
        while self.running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "menu"

            # Handle input
            self.handle_input()
            
            # Update player
            self.player.move()
            
            # Spawn and update enemies
            self.enemy_spawn_timer += 1
            if self.enemy_spawn_timer >= 60:  # Spawn enemy every 60 frames
                self.spawn_enemy()
                self.enemy_spawn_timer = 0
            
            self.update_enemies()
            
            # Check collisions
            if self.check_collisions():
                return "game_over"
            
            # Draw everything
            self.screen.blit(self.background, (0, 0))
            self.player.draw(self.screen)
            for enemy in self.enemies:
                enemy.draw(self.screen)
            self.draw_hud()
            
            # Update display
            pygame.display.flip()
            self.clock.tick(FPS)

        return "quit"