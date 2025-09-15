import pygame
import sys
import random
import json
import os
from collections import deque
from datetime import datetime

# Enable dummy video driver for headless automated tests if requested
if os.environ.get("PONG_HEADLESS_TEST") == "1":
    os.environ["SDL_VIDEODRIVER"] = "dummy"

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
FPS = 60

# Theme system
THEMES = {
    "Classic": {
        "bg": (10, 10, 10),
        "primary": (250, 250, 250),
        "secondary": (180, 180, 180),
        "accent": (0, 200, 255),
        "net": (60, 60, 60)
    },
    "Neon": {
        "bg": (5, 5, 20),
        "primary": (240, 240, 255),
        "secondary": (170, 170, 220),
        "accent": (255, 0, 180),
        "net": (40, 40, 80)
    },
    "Sunset": {
        "bg": (20, 8, 5),
        "primary": (255, 235, 220),
        "secondary": (255, 180, 140),
        "accent": (255, 90, 0),
        "net": (60, 30, 20)
    }
}

DEFAULT_SETTINGS = {
    "max_score": 7,
    "difficulty": "Normal",  # Easy, Normal, Hard
    "mouse_control": False,    # P1 mouse
    "theme": "Neon",
    "powerups": True
}

LEADERBOARD_PATH = "/workspace/leaderboard.json"

def get_theme(settings):
    return THEMES.get(settings.get("theme", "Neon"), THEMES["Neon"])

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_PATH):
        return {"players": {}, "matches": []}
    try:
        with open(LEADERBOARD_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"players": {}, "matches": []}

def save_leaderboard(data):
    try:
        with open(LEADERBOARD_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass

def record_match_result(winner_name, loser_name, left_score, right_score, mode, settings):
    data = load_leaderboard()
    for name, is_win in ((winner_name, True), (loser_name, False)):
        if name not in data["players"]:
            data["players"][name] = {"wins": 0, "losses": 0}
        if is_win:
            data["players"][name]["wins"] += 1
        else:
            data["players"][name]["losses"] += 1
    data["matches"].append({
        "date": datetime.utcnow().isoformat() + "Z",
        "winner": winner_name,
        "loser": loser_name,
        "left_score": left_score,
        "right_score": right_score,
        "mode": mode,
        "difficulty": settings.get("difficulty", "Normal"),
        "max_score": settings.get("max_score", 7),
        "theme": settings.get("theme", "Neon"),
        "powerups": settings.get("powerups", True)
    })
    # Keep only last 100 matches
    if len(data["matches"]) > 100:
        data["matches"] = data["matches"][-100:]
    save_leaderboard(data)

class Button:
    def __init__(self, text, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, 36)
        self.enabled = True
        self.hovered = False
    
    def draw(self, screen, theme):
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)
        bg_color = theme["secondary"] if self.hovered else theme["net"]
        text_color = BLACK if self.hovered else theme["primary"]
        pygame.draw.rect(screen, bg_color, self.rect, border_radius=10)
        pygame.draw.rect(screen, theme["accent"], self.rect, 2, border_radius=10)
        text_surf = self.font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
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
                if len(self.text) < 16:
                    self.text += event.unicode

    def draw(self, screen, theme):
        border_color = theme["accent"] if self.active else theme["secondary"]
        pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=8)
        text_color = theme["primary"]
        text_surf = self.font.render(self.text, True, text_color)
        screen.blit(text_surf, (self.rect.x + 8, self.rect.y + 6))

class OptionSelector:
    def __init__(self, label, options, x, y, w, h, initial_index=0):
        self.label = label
        self.options = options
        self.index = initial_index
        self.rect = pygame.Rect(x, y, w, h)
        self.font = pygame.font.Font(None, 32)
        self.left_rect = pygame.Rect(x - 40, y, 32, h)
        self.right_rect = pygame.Rect(x + w + 8, y, 32, h)

    def value(self):
        return self.options[self.index]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.left_rect.collidepoint(event.pos):
                self.index = (self.index - 1) % len(self.options)
            if self.right_rect.collidepoint(event.pos):
                self.index = (self.index + 1) % len(self.options)

    def draw(self, screen, theme):
        label_surf = self.font.render(self.label, True, theme["secondary"])
        screen.blit(label_surf, (self.rect.x, self.rect.y - 28))
        pygame.draw.rect(screen, theme["net"], self.rect, border_radius=8)
        pygame.draw.rect(screen, theme["accent"], self.rect, 2, border_radius=8)
        value_surf = self.font.render(str(self.value()), True, theme["primary"])
        value_rect = value_surf.get_rect(center=self.rect.center)
        screen.blit(value_surf, value_rect)
        # arrows
        pygame.draw.polygon(screen, theme["secondary"], [
            (self.left_rect.right, self.left_rect.centery),
            (self.left_rect.right - 12, self.left_rect.centery - 10),
            (self.left_rect.right - 12, self.left_rect.centery + 10)
        ])
        pygame.draw.polygon(screen, theme["secondary"], [
            (self.right_rect.left, self.right_rect.centery),
            (self.right_rect.left + 12, self.right_rect.centery - 10),
            (self.right_rect.left + 12, self.right_rect.centery + 10)
        ])

def draw_background(screen, theme, t):
    screen.fill(theme["bg"])
    # Center dashed net line
    dash_h = 20
    gap = 15
    y = -int((t * 60) % (dash_h + gap))
    while y < HEIGHT:
        pygame.draw.rect(screen, theme["net"], (WIDTH//2 - 2, y, 4, dash_h))
        y += dash_h + gap

def show_menu(screen, settings):
    theme = get_theme(settings)
    title_font = pygame.font.Font(None, 88)
    small_font = pygame.font.Font(None, 28)
    buttons = [
        Button("1 Player", WIDTH//2 - 110, 320, 220, 54),
        Button("2 Players", WIDTH//2 - 110, 384, 220, 54),
        Button("Settings", WIDTH//2 - 110, 448, 220, 54),
        Button("Leaderboard", WIDTH//2 - 110, 512, 220, 54),
        Button("Quit", WIDTH//2 - 110, 576, 220, 54)
    ]
    input_box1 = InputBox(WIDTH//2 - 140, 200, 280, 36, "Player 1")
    input_box2 = InputBox(WIDTH//2 - 140, 248, 280, 36, "Player 2")
    clock = pygame.time.Clock()
    t = 0.0
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
                        if btn.text == "Settings":
                            settings_menu(screen, settings)
                        elif btn.text == "Leaderboard":
                            leaderboard_screen(screen, settings)
                        else:
                            mode = btn.text
                            p1 = input_box1.text or "Player 1"
                            p2 = input_box2.text or ("CPU" if mode == "1 Player" else "Player 2")
                            return mode, p1, p2, settings
        # Draw
        draw_background(screen, theme, t)
        title_surf = title_font.render("PONG", True, theme["primary"])
        title_rect = title_surf.get_rect(center=(WIDTH//2, 120))
        screen.blit(title_surf, title_rect)
        subtitle = small_font.render("Arcade Edition", True, theme["secondary"])
        screen.blit(subtitle, subtitle.get_rect(center=(WIDTH//2, 160)))
        input_box1.draw(screen, theme)
        input_box2.draw(screen, theme)
        for btn in buttons:
            btn.draw(screen, theme)
        pygame.display.flip()
        dt = clock.tick(FPS) / 1000.0
        t += dt

def game_over(screen, winner_name, settings, final_score):
    theme = get_theme(settings)
    font = pygame.font.Font(None, 74)
    small = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    buttons = [
        Button("New Game", WIDTH//2 - 110, 360, 220, 54),
        Button("Main Menu", WIDTH//2 - 110, 424, 220, 54)
    ]
    t = 0.0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in buttons:
                    if btn.rect.collidepoint(event.pos):
                        return btn.text
        draw_background(screen, theme, t)
        text = font.render(f"{winner_name} Wins!", True, theme["primary"])
        screen.blit(text, (WIDTH//2 - text.get_width()//2, 220))
        score_text = small.render(f"Final Score: {final_score[0]} - {final_score[1]}", True, theme["secondary"])
        screen.blit(score_text, score_text.get_rect(center=(WIDTH//2, 300)))
        for btn in buttons:
            btn.draw(screen, theme)
        pygame.display.flip()
        dt = clock.tick(FPS) / 1000.0
        t += dt

def settings_menu(screen, settings):
    theme = get_theme(settings)
    title_font = pygame.font.Font(None, 64)
    clock = pygame.time.Clock()
    t = 0.0
    # Build selectors
    difficulty_opts = ["Easy", "Normal", "Hard"]
    difficulty_idx = difficulty_opts.index(settings.get("difficulty", "Normal")) if settings.get("difficulty", "Normal") in difficulty_opts else 1
    theme_opts = list(THEMES.keys())
    theme_idx = theme_opts.index(settings.get("theme", "Neon")) if settings.get("theme", "Neon") in theme_opts else 0
    max_score_opts = [5, 7, 9, 11, 15]
    try:
        max_score_idx = max_score_opts.index(int(settings.get("max_score", 7)))
    except Exception:
        max_score_idx = 1
    powerup_opts = ["On", "Off"]
    powerup_idx = 0 if settings.get("powerups", True) else 1
    mouse_opts = ["On", "Off"]
    mouse_idx = 0 if settings.get("mouse_control", False) else 1

    selectors = [
        OptionSelector("Difficulty", difficulty_opts, WIDTH//2 - 140, 180, 280, 40, difficulty_idx),
        OptionSelector("Theme", theme_opts, WIDTH//2 - 140, 240, 280, 40, theme_idx),
        OptionSelector("Max Score", max_score_opts, WIDTH//2 - 140, 300, 280, 40, max_score_idx),
        OptionSelector("Power-Ups", powerup_opts, WIDTH//2 - 140, 360, 280, 40, powerup_idx),
        OptionSelector("P1 Mouse Control", mouse_opts, WIDTH//2 - 140, 420, 280, 40, mouse_idx)
    ]
    back_btn = Button("Back", WIDTH//2 - 80, 500, 160, 50)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for sel in selectors:
                sel.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.rect.collidepoint(event.pos):
                    # Apply
                    settings["difficulty"] = selectors[0].value()
                    settings["theme"] = selectors[1].value()
                    settings["max_score"] = int(selectors[2].value())
                    settings["powerups"] = selectors[3].value() == "On"
                    settings["mouse_control"] = selectors[4].value() == "On"
                    return
        draw_background(screen, theme, t)
        title = title_font.render("Settings", True, theme["primary"])
        screen.blit(title, title.get_rect(center=(WIDTH//2, 110)))
        for sel in selectors:
            sel.draw(screen, theme)
        back_btn.draw(screen, theme)
        pygame.display.flip()
        dt = clock.tick(FPS) / 1000.0
        t += dt

def leaderboard_screen(screen, settings):
    theme = get_theme(settings)
    title_font = pygame.font.Font(None, 64)
    small_font = pygame.font.Font(None, 28)
    clock = pygame.time.Clock()
    t = 0.0
    back_btn = Button("Back", WIDTH//2 - 80, 520, 160, 50)
    data = load_leaderboard()
    players = sorted(data.get("players", {}).items(), key=lambda kv: (-kv[1].get("wins", 0), kv[0]))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and back_btn.rect.collidepoint(event.pos):
                return
        draw_background(screen, theme, t)
        title = title_font.render("Leaderboard", True, theme["primary"])
        screen.blit(title, title.get_rect(center=(WIDTH//2, 80)))
        # top 10
        y = 140
        rank = 1
        for name, rec in players[:10]:
            line = f"{rank}. {name} — {rec.get('wins',0)}W/{rec.get('losses',0)}L"
            surf = small_font.render(line, True, theme["secondary"])
            screen.blit(surf, (WIDTH//2 - 200, y))
            y += 32
            rank += 1
        back_btn.draw(screen, theme)
        pygame.display.flip()
        dt = clock.tick(FPS) / 1000.0
        t += dt

def main_game(screen, game_mode, p1_name, p2_name, settings):
    theme = get_theme(settings)
    max_score = int(settings.get("max_score", 7))
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
    small_font = pygame.font.Font(None, 28)

    clock = pygame.time.Clock()
    running = True
    left_move = 0
    right_move = 0
    paused = False
    need_countdown = False
    countdown_timer = 0
    last_hitter = None  # 'left' or 'right'
    score_pop_timer = 0
    score_pop_side = None

    # Ball trail
    trail = deque(maxlen=12)

    # Power-ups
    powerups_enabled = bool(settings.get("powerups", True))
    active_powerups = {"left": {}, "right": {}, "ball": {}}
    powerup_rect = None
    powerup_type = None
    next_powerup_time = pygame.time.get_ticks() + random.randint(5000, 9000)

    def reset_ball(scored_side=None):
        nonlocal ball_dx, ball_dy, need_countdown, countdown_timer, score_pop_timer, score_pop_side
        ball.center = (WIDTH//2, HEIGHT//2)
        ball_dx = BALL_SPEED_X * random.choice((1, -1))
        ball_dy = BALL_SPEED_Y * random.choice((1, -1))
        trail.clear()
        need_countdown = True
        countdown_timer = 1800  # ms
        if scored_side is not None:
            score_pop_timer = 600
            score_pop_side = scored_side

    def apply_powerup(pu_type, holder):
        now = pygame.time.get_ticks()
        duration = 6000
        if pu_type == "paddle_enlarge":
            active_powerups[holder]["paddle_enlarge"] = now + duration
        elif pu_type == "paddle_shrink":
            active_powerups[holder]["paddle_shrink"] = now + duration
        elif pu_type == "ball_speed_up":
            active_powerups["ball"]["ball_speed_up"] = now + duration
        elif pu_type == "ball_slow":
            active_powerups["ball"]["ball_slow"] = now + duration

    def current_paddle_height(holder):
        base = PADDLE_HEIGHT
        if active_powerups[holder].get("paddle_enlarge", 0) > pygame.time.get_ticks():
            base = int(base * 1.5)
        if active_powerups[holder].get("paddle_shrink", 0) > pygame.time.get_ticks():
            base = int(base * 0.7)
        return max(50, min(220, base))

    def current_ball_speed_scale():
        now = pygame.time.get_ticks()
        scale = 1.0
        if active_powerups["ball"].get("ball_speed_up", 0) > now:
            scale *= 1.35
        if active_powerups["ball"].get("ball_slow", 0) > now:
            scale *= 0.7
        return scale

    def ai_move(difficulty):
        # Return -1, 0, 1 for right paddle movement
        target_y = ball.centery
        error = 0
        react_chance = 1.0
        if difficulty == "Easy":
            error = random.randint(-35, 35)
            react_chance = 0.6
        elif difficulty == "Normal":
            error = random.randint(-20, 20)
            react_chance = 0.8
        else:  # Hard
            error = random.randint(-8, 8)
            react_chance = 0.95
        if ball_dx < 0 and random.random() < 0.7:
            return 0
        if random.random() > react_chance:
            return 0
        if right_paddle.centery < target_y + error:
            return 1
        if right_paddle.centery > target_y + error:
            return -1
        return 0

    reset_ball()

    # Fast start for automated tests
    if os.environ.get("PONG_FAST_START") == "1":
        need_countdown = False
        countdown_timer = 0
        ball.left = 2
        ball.centery = HEIGHT // 2
        ball_dx = -abs(ball_dx)
        ball_dy = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    paused = not paused
                    if not paused:
                        need_countdown = True
                        countdown_timer = 1800
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

        # Mouse control for P1
        if settings.get("mouse_control", False):
            mouse_y = pygame.mouse.get_pos()[1]
            # Smoothly follow mouse
            if mouse_y < left_paddle.centery - 4:
                left_move = -1
            elif mouse_y > left_paddle.centery + 4:
                left_move = 1
            else:
                left_move = 0

        # AI movement for single player
        if game_mode == "1 Player":
            right_move = ai_move(settings.get("difficulty", "Normal"))

        if not paused and not need_countdown:
            # Move paddles
            left_paddle.y += left_move * PADDLE_SPEED
            right_paddle.y += right_move * PADDLE_SPEED

            # Update paddle heights based on power-ups
            lp_h = current_paddle_height("left")
            rp_h = current_paddle_height("right")
            left_paddle.height = lp_h
            right_paddle.height = rp_h

            # Keep paddles on screen
            left_paddle.y = max(0, min(HEIGHT - left_paddle.height, left_paddle.y))
            right_paddle.y = max(0, min(HEIGHT - right_paddle.height, right_paddle.y))

            # Move ball
            speed_scale = current_ball_speed_scale()
            ball.x += int(ball_dx * speed_scale)
            ball.y += int(ball_dy * speed_scale)

            # Ball collision with walls
            if ball.top <= 0 or ball.bottom >= HEIGHT:
                ball_dy *= -1

            # Ball collision with paddles
            if ball.colliderect(left_paddle):
                if ball_dx < 0:
                    ball_dx *= -1
                    last_hitter = "left"
                    # tweak angle based on hit position
                    offset = (ball.centery - left_paddle.centery) / (left_paddle.height / 2)
                    ball_dy = BALL_SPEED_Y * offset
            elif ball.colliderect(right_paddle):
                if ball_dx > 0:
                    ball_dx *= -1
                    last_hitter = "right"
                    offset = (ball.centery - right_paddle.centery) / (right_paddle.height / 2)
                    ball_dy = BALL_SPEED_Y * offset

            # Power-up spawn and pickup
            if powerups_enabled:
                now = pygame.time.get_ticks()
                if powerup_rect is None and now >= next_powerup_time:
                    powerup_type = random.choice(["paddle_enlarge", "paddle_shrink", "ball_speed_up", "ball_slow"])
                    px = random.randint(WIDTH//3, 2*WIDTH//3)
                    py = random.randint(80, HEIGHT-80)
                    powerup_rect = pygame.Rect(px-12, py-12, 24, 24)
                if powerup_rect is not None and ball.colliderect(powerup_rect):
                    holder = last_hitter or ("left" if ball_dx > 0 else "right")
                    apply_powerup(powerup_type, holder)
                    powerup_rect = None
                    powerup_type = None
                    next_powerup_time = now + random.randint(6000, 12000)

            # Scoring
            if ball.left <= 0:
                right_score += 1
                reset_ball(scored_side="right")
            elif ball.right >= WIDTH:
                left_score += 1
                reset_ball(scored_side="left")

        # Countdown logic
        dt_ms = clock.tick(FPS)
        if need_countdown:
            countdown_timer -= dt_ms
            if countdown_timer <= 0:
                need_countdown = False

        if score_pop_timer > 0:
            score_pop_timer -= dt_ms

        # Check win condition
        if left_score >= max_score or right_score >= max_score:
            winner = p1_name if left_score >= max_score else p2_name
            loser = p2_name if winner == p1_name else p1_name
            record_match_result(winner, loser, left_score, right_score, game_mode, settings)
            return winner, (left_score, right_score)

        # Drawing
        t = pygame.time.get_ticks() / 1000.0
        draw_background(screen, theme, t)

        # Draw ball trail
        trail.append((ball.centerx, ball.centery))
        trail_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for i, (tx, ty) in enumerate(list(trail)):
            alpha = int(180 * (i / len(trail))) if len(trail) > 0 else 0
            pygame.draw.circle(trail_surface, (*theme["accent"], max(0, min(120, alpha))), (tx, ty), 10)
        screen.blit(trail_surface, (0, 0))

        # Draw paddles and ball
        pygame.draw.rect(screen, theme["primary"], left_paddle, border_radius=6)
        pygame.draw.rect(screen, theme["primary"], right_paddle, border_radius=6)
        pygame.draw.ellipse(screen, theme["primary"], ball)

        # Draw power-up
        if powerups_enabled and powerup_rect is not None:
            color = theme["accent"]
            pygame.draw.rect(screen, color, powerup_rect, border_radius=6)

        # Draw scores
        left_color = theme["primary"] if score_pop_side != "left" else theme["accent"]
        right_color = theme["primary"] if score_pop_side != "right" else theme["accent"]
        left_scale = 1.0 + (0.3 * (score_pop_timer / 600.0) if score_pop_side == "left" else 0)
        right_scale = 1.0 + (0.3 * (score_pop_timer / 600.0) if score_pop_side == "right" else 0)
        ls = font.render(str(left_score), True, left_color)
        rs = font.render(str(right_score), True, right_color)
        if left_scale != 1.0:
            ls = pygame.transform.rotozoom(ls, 0, left_scale)
        if right_scale != 1.0:
            rs = pygame.transform.rotozoom(rs, 0, right_scale)
        screen.blit(ls, (WIDTH//4 - ls.get_width()//2, 20))
        screen.blit(rs, (3*WIDTH//4 - rs.get_width()//2, 20))

        # Draw player names
        p1_text = small_font.render(p1_name, True, theme["secondary"])
        screen.blit(p1_text, (50, HEIGHT - 40))
        p2_text = small_font.render(p2_name, True, theme["secondary"])
        screen.blit(p2_text, (WIDTH - 50 - p2_text.get_width(), HEIGHT - 40))

        # Pause overlay or countdown
        if paused or need_countdown:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            screen.blit(overlay, (0, 0))
            if paused:
                txt = small_font.render("Paused - Press P/Esc", True, theme["primary"])
                screen.blit(txt, txt.get_rect(center=(WIDTH//2, HEIGHT//2)))
            else:
                secs = max(1, int(1 + countdown_timer / 1000.0))
                ctxt = font.render(str(secs), True, theme["accent"])
                screen.blit(ctxt, ctxt.get_rect(center=(WIDTH//2, HEIGHT//2)))

        pygame.display.flip()

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong Arcade")
    settings = DEFAULT_SETTINGS.copy()
    while True:
        game_mode, p1_name, p2_name, settings = show_menu(screen, settings)
        while True:
            winner, final_score = main_game(screen, game_mode, p1_name, p2_name, settings)
            action = game_over(screen, winner, settings, final_score)
            if action == "New Game":
                continue
            elif action == "Main Menu":
                break

if __name__ == "__main__":
    # Headless automated simulation mode
    if os.environ.get("PONG_HEADLESS_TEST") == "1":
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        test_settings = DEFAULT_SETTINGS.copy()
        test_settings.update({
            "max_score": 1,
            "powerups": False,
            "mouse_control": False,
            "difficulty": "Easy",
            "theme": "Classic"
        })
        os.environ.setdefault("PONG_FAST_START", "1")
        winner, final_score = main_game(screen, "1 Player", "Test1", "CPU", test_settings)
        print("TEST_RESULT", winner, final_score[0], final_score[1])
        pygame.quit()
        sys.exit(0)
    else:
        main()
