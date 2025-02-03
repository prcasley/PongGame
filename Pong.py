import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_SIZE = 15
PADDLE_SPEED = 5
BALL_SPEED_X = 4
BALL_SPEED_Y = 3
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
MAX_SCORE = 7

class Button:
    def __init__(self, text, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, 36)
        
    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = GRAY
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def draw(self, screen):
        pygame.draw.rect(screen, self.color if not self.active else WHITE, self.rect, 2)
        text_surf = self.font.render(self.text, True, WHITE)
        screen.blit(text_surf, (self.rect.x + 5, self.rect.y + 5))

def show_menu(screen):
    screen.fill(BLACK)
    title_font = pygame.font.Font(None, 74)
    title_text = title_font.render("PONG GAME", True, WHITE)
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 100))
    
    buttons = [
        Button("1 Player", WIDTH//2 - 100, 250, 200, 50),
        Button("2 Players", WIDTH//2 - 100, 325, 200, 50),
        Button("Quit", WIDTH//2 - 100, 400, 200, 50)
    ]
    
    input_box1 = InputBox(WIDTH//2 - 100, 180, 200, 32, "Player 1")
    input_box2 = InputBox(WIDTH//2 - 100, 220, 200, 32, "Player 2")
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            input_box1.handle_event(event)
            input_box2.handle_event(event)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in buttons:
                    if btn.rect.collidepoint(event.pos):
                        if btn.text == "Quit":
                            pygame.quit()
                            sys.exit()
                        return btn.text, input_box1.text, input_box2.text

        input_box1.draw(screen)
        input_box2.draw(screen)
        for btn in buttons:
            btn.draw(screen)
            
        pygame.display.flip()
        pygame.time.Clock().tick(30)

def game_over(screen, winner_name):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    text = font.render(f"{winner_name} Wins!", True, WHITE)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, 200))
    
    buttons = [
        Button("New Game", WIDTH//2 - 100, 350, 200, 50),
        Button("Main Menu", WIDTH//2 - 100, 425, 200, 50)
    ]
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in buttons:
                    if btn.rect.collidepoint(event.pos):
                        return btn.text

        for btn in buttons:
            btn.draw(screen)
            
        pygame.display.flip()
        pygame.time.Clock().tick(30)

def main_game(screen, game_mode, p1_name, p2_name):
    # Game objects
    left_paddle = pygame.Rect(50, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, 
                             PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)

    ball_dx = BALL_SPEED_X * random.choice((1, -1))
    ball_dy = BALL_SPEED_Y * random.choice((1, -1))
    
    left_score = 0
    right_score = 0
    
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)
    
    clock = pygame.time.Clock()
    running = True
    left_move = 0
    right_move = 0

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    left_move = -1
                if event.key == pygame.K_s:
                    left_move = 1
                if event.key == pygame.K_UP:
                    right_move = -1
                if event.key == pygame.K_DOWN:
                    right_move = 1
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_w, pygame.K_s):
                    left_move = 0
                if event.key in (pygame.K_UP, pygame.K_DOWN):
                    right_move = 0

        # AI movement for single player
        if game_mode == "1 Player":
            if ball_dx > 0:  # Only move when ball is approaching
                if right_paddle.centery < ball.centery:
                    right_move = 1
                elif right_paddle.centery > ball.centery:
                    right_move = -1
                else:
                    right_move = 0
            else:
                right_move = 0

        # Move paddles
        left_paddle.y += left_move * PADDLE_SPEED
        right_paddle.y += right_move * PADDLE_SPEED

        # Keep paddles on screen
        left_paddle.y = max(0, min(HEIGHT - PADDLE_HEIGHT, left_paddle.y))
        right_paddle.y = max(0, min(HEIGHT - PADDLE_HEIGHT, right_paddle.y))

        # Move ball
        ball.x += ball_dx
        ball.y += ball_dy

        # Ball collision with walls
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_dy *= -1

        # Ball collision with paddles
        if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
            ball_dx *= -1
            ball_dy += random.uniform(-1, 1)

        # Scoring
        if ball.left <= 0:
            right_score += 1
            ball.center = (WIDTH//2, HEIGHT//2)
            ball_dx = BALL_SPEED_X * random.choice((1, -1))
            ball_dy = BALL_SPEED_Y * random.choice((1, -1))
        if ball.right >= WIDTH:
            left_score += 1
            ball.center = (WIDTH//2, HEIGHT//2)
            ball_dx = BALL_SPEED_X * random.choice((1, -1))
            ball_dy = BALL_SPEED_Y * random.choice((1, -1))

        # Check win condition
        if left_score >= MAX_SCORE or right_score >= MAX_SCORE:
            winner = p1_name if left_score >= MAX_SCORE else p2_name
            return winner

        # Drawing
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, left_paddle)
        pygame.draw.rect(screen, WHITE, right_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))

        # Draw scores
        left_text = font.render(str(left_score), True, WHITE)
        screen.blit(left_text, (WIDTH//4 - left_text.get_width()//2, 20))
        right_text = font.render(str(right_score), True, WHITE)
        screen.blit(right_text, (3*WIDTH//4 - right_text.get_width()//2, 20))

        # Draw player names
        p1_text = small_font.render(p1_name, True, WHITE)
        screen.blit(p1_text, (50, HEIGHT - 50))
        p2_text = small_font.render(p2_name, True, WHITE)
        screen.blit(p2_text, (WIDTH - 50 - p2_text.get_width(), HEIGHT - 50))

        pygame.display.flip()
        clock.tick(60)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong")
    
    while True:
        game_mode, p1_name, p2_name = show_menu(screen)
        while True:
            winner = main_game(screen, game_mode, p1_name, p2_name)
            action = game_over(screen, winner)
            if action == "New Game":
                continue
            elif action == "Main Menu":
                break

if __name__ == "__main__":
    main()
