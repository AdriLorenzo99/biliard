import pygame
import math
import random
import sys
import os

# =============================================================================
# [KONFIGURASI & KONSTANTA]
# =============================================================================
# Pengaturan Lingkungan
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

# Resolusi & Dimensi
GAME_WIDTH = 1280
GAME_HEIGHT = 720
GAME_RATIO = GAME_WIDTH / GAME_HEIGHT
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540

# Margin Area Permainan (Meja)
TABLE_MARGIN_X = 100
TABLE_MARGIN_Y = 100
PLAY_AREA_LEFT = TABLE_MARGIN_X
PLAY_AREA_TOP = TABLE_MARGIN_Y
PLAY_AREA_WIDTH = GAME_WIDTH - (2 * TABLE_MARGIN_X)
PLAY_AREA_HEIGHT = GAME_HEIGHT - (2 * TABLE_MARGIN_Y)
PLAY_AREA_RIGHT = PLAY_AREA_LEFT + PLAY_AREA_WIDTH
PLAY_AREA_BOTTOM = PLAY_AREA_TOP + PLAY_AREA_HEIGHT

# Palet Warna
COLOR_BG_DARK = (20, 20, 20)
COLOR_TABLE_FELT = (0, 100, 0)
COLOR_CUSHION = (0, 80, 0)
COLOR_WOOD = (101, 67, 33)
COLOR_WOOD_LIGHT = (140, 90, 50)
COLOR_DIAMOND = (200, 200, 200)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED_UI = (200, 50, 50)
COLOR_HOVER = (255, 100, 100)
COLOR_HIGHLIGHT = (255, 255, 0)

# Warna Bola (1-15)
BALL_COLORS = {
    1: (255, 215, 0), 2: (0, 0, 255), 3: (255, 0, 0), 4: (128, 0, 128),
    5: (255, 165, 0), 6: (0, 128, 0), 7: (128, 0, 0), 8: (0, 0, 0),
    9: (255, 215, 0), 10: (0, 0, 255), 11: (255, 0, 0), 12: (128, 0, 128),
    13: (255, 165, 0), 14: (0, 128, 0), 15: (128, 0, 0)
}

# Inisialisasi Layar
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Pro Billiard Master - Final Presentation")
canvas = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
clock = pygame.time.Clock()

# Font
font_title = pygame.font.SysFont("impact", 64)
font_large = pygame.font.SysFont("arial", 48, bold=True)
font_medium = pygame.font.SysFont("arial", 32)
font_small = pygame.font.SysFont("arial", 20, bold=True)
font_btn = pygame.font.SysFont("arial", 18, bold=True)

# =============================================================================
# [CLASSES - OOP STRUCTURE]
# =============================================================================

class Ball:
    """Base class untuk semua bola (Encapsulation)."""
    def __init__(self, x, y, radius, color):
        self.pos = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.radius = radius
        self.color = color
        self.is_moving = False
        self.friction = 0.988 

    def move(self):
        """Menangani pergerakan bola berdasarkan kecepatan dan gesekan."""
        if self.velocity.length() > 0.05:
            self.pos += self.velocity
            self.velocity *= self.friction
            self.is_moving = True
        else:
            self.velocity = pygame.math.Vector2(0, 0)
            self.is_moving = False

    def check_wall_collision(self):
        """Memantulkan bola jika menabrak dinding meja (Cushions)."""
        if self.pos.x <= PLAY_AREA_LEFT + self.radius:
            self.pos.x = PLAY_AREA_LEFT + self.radius
            self.velocity.x *= -0.85
        elif self.pos.x >= PLAY_AREA_RIGHT - self.radius:
            self.pos.x = PLAY_AREA_RIGHT - self.radius
            self.velocity.x *= -0.85
        
        if self.pos.y <= PLAY_AREA_TOP + self.radius:
            self.pos.y = PLAY_AREA_TOP + self.radius
            self.velocity.y *= -0.85
        elif self.pos.y >= PLAY_AREA_BOTTOM - self.radius:
            self.pos.y = PLAY_AREA_BOTTOM - self.radius
            self.velocity.y *= -0.85

class CueBall(Ball):
    """Subclass khusus untuk bola putih (Inheritance)."""
    def __init__(self, x, y):
        super().__init__(x, y, radius=14, color=COLOR_WHITE)

    def draw(self, surface):
        # Efek bayangan dan penanda titik merah (Polymorphism)
        pygame.draw.circle(surface, (0,0,0, 50), (int(self.pos.x)+2, int(self.pos.y)+2), self.radius)
        pygame.draw.circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)
        pygame.draw.circle(surface, (255, 0, 0), (int(self.pos.x), int(self.pos.y)), 2)

class ObjectBall(Ball):
    """Subclass untuk bola berwarna/target (Inheritance)."""
    def __init__(self, x, y, number):
        color = BALL_COLORS.get(number, COLOR_BLACK)
        super().__init__(x, y, radius=14, color=color)
        self.number = number
        self.is_stripe = number > 8
        self.value = 10 

    def draw(self, surface):
        """Menggambar bola dengan nomor dan motif stripe/solid."""
        x, y = int(self.pos.x), int(self.pos.y)
        pygame.draw.circle(surface, (0,0,0, 50), (x+2, y+2), self.radius)
        if not self.is_stripe:
            pygame.draw.circle(surface, self.color, (x, y), self.radius)
        else:
            pygame.draw.circle(surface, COLOR_WHITE, (x, y), self.radius)
            rect_height = self.radius * 1.2
            pygame.draw.rect(surface, self.color, (x - self.radius, y - rect_height//2, self.radius*2, rect_height))
        
        pygame.draw.circle(surface, COLOR_WHITE, (x, y), self.radius // 2)
        text = font_small.render(str(self.number), True, COLOR_BLACK)
        rect = text.get_rect(center=(x, y))
        surface.blit(text, rect)

class Pocket:
    """Kelas abstraksi untuk lubang biliar."""
    def __init__(self, x, y, is_corner=False):
        self.pos = pygame.math.Vector2(x, y)
        self.radius = 28 if is_corner else 24
        
    def draw(self, surface):
        pygame.draw.circle(surface, (10, 10, 10), (int(self.pos.x), int(self.pos.y)), self.radius)
        pygame.draw.circle(surface, (50, 50, 50), (int(self.pos.x), int(self.pos.y)), self.radius + 2, 2)
        
    def check_potted(self, ball):
        return self.pos.distance_to(ball.pos) < self.radius

class CueStick:
    """Kelas untuk mengontrol stik biliar dan input pengguna."""
    def __init__(self):
        self.angle = 0
        self.visible = True
        self.pull_dist = 0
        self.max_pull = 200
        self.active = False 

    def update(self, mouse_pos_game, cue_ball_pos):
        # Hitung sudut menggunakan Atan2
        dx = mouse_pos_game[0] - cue_ball_pos.x
        dy = mouse_pos_game[1] - cue_ball_pos.y
        self.angle = math.degrees(math.atan2(dy, dx))

    def draw(self, surface, cue_ball_pos):
        if not self.visible: return
        rad = math.radians(self.angle)
        gap = 20 + self.pull_dist
        
        # Hitung koordinat stik agar selalu di BELAKANG bola
        start_x = cue_ball_pos.x - math.cos(rad) * gap
        start_y = cue_ball_pos.y - math.sin(rad) * gap
        stick_len = 350
        end_x = start_x - math.cos(rad) * stick_len
        end_y = start_y - math.sin(rad) * stick_len
        
        pygame.draw.line(surface, COLOR_WOOD, (start_x, start_y), (end_x, end_y), 10)
        pygame.draw.line(surface, (30, 30, 30), (end_x + math.cos(rad) * 100, end_y + math.sin(rad) * 100), (end_x, end_y), 11)

        # Power Indicator
        if self.pull_dist > 10:
            percentage = self.pull_dist / self.max_pull
            color = (int(255 * percentage), int(255 * (1-percentage)), 0)
            pygame.draw.circle(surface, color, (int(start_x), int(start_y)), 8)

    def draw_guideline(self, surface, cue_ball_pos):
        if not self.visible: return
        rad = math.radians(self.angle)
        start_dist = 20
        end_dist = 500
        curr = start_dist
        while curr < end_dist:
            p1 = (cue_ball_pos.x + math.cos(rad)*curr, cue_ball_pos.y + math.sin(rad)*curr)
            p2 = (cue_ball_pos.x + math.cos(rad)*(curr+10), cue_ball_pos.y + math.sin(rad)*(curr+10))
            pygame.draw.line(surface, (255, 255, 255), p1, p2, 1)
            curr += 20

class Button:
    """UI Helper untuk tombol interaktif."""
    def __init__(self, x, y, w, h, text, color, text_color=COLOR_WHITE):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.hover = False

    def draw(self, surface):
        col = COLOR_HOVER if self.hover else self.color
        pygame.draw.rect(surface, col, self.rect, border_radius=8)
        pygame.draw.rect(surface, COLOR_WHITE, self.rect, 2, border_radius=8)
        txt_surf = font_btn.render(self.text, True, self.text_color)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        surface.blit(txt_surf, txt_rect)

    def check_hover(self, mouse_pos_game):
        self.hover = self.rect.collidepoint(mouse_pos_game)

    def is_clicked(self, event, mouse_pos_game):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(mouse_pos_game)
        return False

# =============================================================================
# [HELPER FUNCTIONS]
# =============================================================================

def draw_fancy_table(surface):
    """Menggambar meja dengan detail tekstur dan diamond markers."""
    surface.fill(COLOR_BG_DARK)
    outer_rect = (PLAY_AREA_LEFT - 40, PLAY_AREA_TOP - 40, PLAY_AREA_WIDTH + 80, PLAY_AREA_HEIGHT + 80)
    pygame.draw.rect(surface, COLOR_WOOD, outer_rect, border_radius=15)
    pygame.draw.rect(surface, COLOR_WOOD_LIGHT, outer_rect, 3, border_radius=15)
    
    # Diamond Markers
    for i in range(1, 4):
        x = PLAY_AREA_LEFT + (PLAY_AREA_WIDTH / 4) * i
        pygame.draw.circle(surface, COLOR_DIAMOND, (int(x), PLAY_AREA_TOP - 20), 4)
        pygame.draw.circle(surface, COLOR_DIAMOND, (int(x), PLAY_AREA_BOTTOM + 20), 4)
    
    # Area Main (Hijau)
    pygame.draw.rect(surface, COLOR_TABLE_FELT, (PLAY_AREA_LEFT, PLAY_AREA_TOP, PLAY_AREA_WIDTH, PLAY_AREA_HEIGHT))
    
    # Cushions
    d = 20
    pygame.draw.rect(surface, COLOR_CUSHION, (PLAY_AREA_LEFT, PLAY_AREA_TOP, PLAY_AREA_WIDTH, d))
    pygame.draw.rect(surface, COLOR_CUSHION, (PLAY_AREA_LEFT, PLAY_AREA_BOTTOM-d, PLAY_AREA_WIDTH, d))
    pygame.draw.rect(surface, COLOR_CUSHION, (PLAY_AREA_LEFT, PLAY_AREA_TOP, d, PLAY_AREA_HEIGHT))
    pygame.draw.rect(surface, COLOR_CUSHION, (PLAY_AREA_RIGHT-d, PLAY_AREA_TOP, d, PLAY_AREA_HEIGHT))

def resolve_collisions(balls):
    """Menangani fisika tumbukan antar bola (Elastic Collision)."""
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            b1, b2 = balls[i], balls[j]
            dist_vec = b1.pos - b2.pos
            dist = dist_vec.length()
            if dist < b1.radius + b2.radius:
                # Correct Overlap
                overlap = (b1.radius + b2.radius) - dist
                n = dist_vec.normalize()
                b1.pos += n * (overlap / 2)
                b2.pos -= n * (overlap / 2)
                
                # Resolve Velocity
                tangent = pygame.math.Vector2(-n.y, n.x)
                dp_tan1 = b1.velocity.dot(tangent)
                dp_tan2 = b2.velocity.dot(tangent)
                dp_norm1 = b1.velocity.dot(n)
                dp_norm2 = b2.velocity.dot(n)
                b1.velocity = tangent * dp_tan1 + n * dp_norm2
                b2.velocity = tangent * dp_tan2 + n * dp_norm1

def init_game_objects():
    """Menginisialisasi objek game: Bola Putih, Bola Target, dan Pocket."""
    # Posisi Awal CueBall
    start_pos_cue = (PLAY_AREA_LEFT + PLAY_AREA_WIDTH * 0.25, GAME_HEIGHT // 2)
    cue_ball = CueBall(*start_pos_cue)
    
    # Setup Rack Bola (Segitiga)
    object_balls = []
    start_x = PLAY_AREA_RIGHT - 300
    start_y = GAME_HEIGHT // 2
    r, s = 14, 1 # radius, spacing
    
    positions = []
    for row in range(5):
        for col in range(row + 1):
            x = start_x + (row * (r * 2 + s) * 0.866)
            y = start_y + ((col * (r * 2 + s)) - ((row * (r * 2 + s)) / 2))
            positions.append((x, y))
            
    # Smart Racking: 8 di tengah, 1 di depan
    mapping = [0]*15
    avail = [i for i in range(2, 16) if i != 8]
    random.shuffle(avail)
    mapping[0] = 1
    mapping[4] = 8
    idx = 0
    for i in range(15):
        if i not in [0, 4]:
            mapping[i] = avail[idx]
            idx += 1
            
    for i in range(15):
        object_balls.append(ObjectBall(positions[i][0], positions[i][1], mapping[i]))
        
    pockets = [
        Pocket(PLAY_AREA_LEFT, PLAY_AREA_TOP, True),
        Pocket(PLAY_AREA_LEFT + PLAY_AREA_WIDTH/2, PLAY_AREA_TOP - 5),
        Pocket(PLAY_AREA_RIGHT, PLAY_AREA_TOP, True),
        Pocket(PLAY_AREA_LEFT, PLAY_AREA_BOTTOM, True),
        Pocket(PLAY_AREA_LEFT + PLAY_AREA_WIDTH/2, PLAY_AREA_BOTTOM + 5),
        Pocket(PLAY_AREA_RIGHT, PLAY_AREA_BOTTOM, True),
    ]
    return cue_ball, object_balls, pockets

def get_game_mouse_pos(screen_mouse_pos, offset_x, offset_y, scale):
    """Konversi koordinat mouse layar ke koordinat game virtual."""
    mx = screen_mouse_pos[0] - offset_x
    my = screen_mouse_pos[1] - offset_y
    game_x = mx / scale
    game_y = my / scale
    return (game_x, game_y)

# =============================================================================
# [UI DRAWING FUNCTIONS]
# =============================================================================

def draw_main_menu(surface, selected_mode):
    surface.fill(COLOR_BG_DARK)
    pygame.draw.rect(surface, COLOR_TABLE_FELT, (0, GAME_HEIGHT//2 - 120, GAME_WIDTH, 240))
    title = font_title.render("BILLIARD MASTER", True, COLOR_WHITE)
    surface.blit(title, (GAME_WIDTH//2 - title.get_width()//2, 120))
    
    opts = ["1 PLAYER (Practice)", "2 PLAYER (PvP)", "EXIT GAME"]
    for i, txt in enumerate(opts):
        color = COLOR_HIGHLIGHT if selected_mode == (i+1) else (150, 150, 150)
        rend = font_large.render(txt, True, color)
        rect = rend.get_rect(center=(GAME_WIDTH//2, 350 + i*80))
        surface.blit(rend, rect)
        if selected_mode == (i+1):
            pygame.draw.rect(surface, COLOR_WHITE, rect.inflate(40, 20), 2)
    
    info = font_small.render("Controls: ARROWS to Select, ENTER to Confirm", True, COLOR_WHITE)
    surface.blit(info, (GAME_WIDTH//2 - info.get_width()//2, 650))

def draw_pause_menu(surface):
    overlay = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(COLOR_BLACK)
    surface.blit(overlay, (0,0))
    
    txt = font_title.render("GAME PAUSED", True, COLOR_WHITE)
    surface.blit(txt, (GAME_WIDTH//2 - txt.get_width()//2, 200))
    
    sub = font_medium.render("Press ESC to Resume", True, COLOR_HIGHLIGHT)
    surface.blit(sub, (GAME_WIDTH//2 - sub.get_width()//2, 300))

# =============================================================================
# [MAIN GAME LOOP]
# =============================================================================

def main():
    global screen
    running = True
    in_menu = True
    is_paused = False
    selected_mode = 1
    
    # Inisialisasi Objek Game
    cue_ball, object_balls, pockets = init_game_objects()
    cue_stick = CueStick()
    
    # Game Variables
    player_turn = 1
    scores = {1: 0, 2: 0}
    turn_in_progress = False
    ball_potted_this_turn = False
    
    # === FITUR BARU: BALL IN HAND ===
    placing_cue_ball = False
    
    # Tombol Menu dalam Game
    btn_restart = Button(20, GAME_HEIGHT - 60, 120, 40, "RESTART", (50, 100, 200))
    btn_menu = Button(150, GAME_HEIGHT - 60, 120, 40, "MAIN MENU", COLOR_RED_UI)

    # Scaling Vars
    scale = 1
    offset_x = 0
    offset_y = 0

    while running:
        # --- 1. HANDLING RESIZE & SCALE ---
        win_w, win_h = screen.get_size()
        win_ratio = win_w / win_h
        if win_ratio > GAME_RATIO:
            scale = win_h / GAME_HEIGHT
            new_w = GAME_WIDTH * scale
            offset_x = (win_w - new_w) // 2
            offset_y = 0
        else:
            scale = win_w / GAME_WIDTH
            new_h = GAME_HEIGHT * scale
            offset_x = 0
            offset_y = (win_h - new_h) // 2

        # Konversi Mouse
        real_mouse_pos = pygame.mouse.get_pos()
        game_mouse_pos = get_game_mouse_pos(real_mouse_pos, offset_x, offset_y, scale)
        
        # --- 2. EVENT HANDLING ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f: # Toggle Fullscreen
                    is_fs = screen.get_flags() & pygame.FULLSCREEN
                    screen = pygame.display.set_mode((0,0) if not is_fs else (WINDOW_WIDTH, WINDOW_HEIGHT), 
                                                     pygame.FULLSCREEN if not is_fs else pygame.RESIZABLE)
            
            # -- LOGIKA MENU UTAMA --
            if in_menu:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP: selected_mode = max(1, selected_mode - 1)
                    if event.key == pygame.K_DOWN: selected_mode = min(3, selected_mode + 1)
                    if event.key == pygame.K_RETURN:
                        if selected_mode == 3: running = False
                        else:
                            in_menu = False
                            is_paused = False
                            placing_cue_ball = False
                            cue_ball, object_balls, pockets = init_game_objects()
                            scores = {1: 0, 2: 0}
                            player_turn = 1
                            cue_stick.visible = True
            
            # -- LOGIKA DALAM GAME --
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: is_paused = not is_paused
                
                if is_paused: # Menu Pause
                    if btn_restart.is_clicked(event, game_mouse_pos):
                         cue_ball, object_balls, pockets = init_game_objects()
                         scores = {1: 0, 2: 0}
                         player_turn = 1
                         placing_cue_ball = False
                         turn_in_progress = False
                         is_paused = False
                    if btn_menu.is_clicked(event, game_mouse_pos):
                        in_menu = True
                    continue
                
                # Input Gameplay
                if placing_cue_ball:
                    # Logika Menaruh Bola Bebas
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        # Validasi: Tidak boleh menimpa bola lain
                        valid_spot = True
                        for b in object_balls:
                            if b.pos.distance_to(cue_ball.pos) < b.radius * 2:
                                valid_spot = False
                        if valid_spot:
                            placing_cue_ball = False
                            cue_stick.visible = True
                            cue_ball.velocity = pygame.math.Vector2(0,0)
                else:
                    # Logika Menembak
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                         if cue_stick.visible and not turn_in_progress:
                            cue_stick.active = True
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        if cue_stick.active:
                            cue_stick.active = False
                            power = cue_stick.pull_dist / 8.5
                            angle_rad = math.radians(cue_stick.angle)
                            cue_ball.velocity += pygame.math.Vector2(math.cos(angle_rad), math.sin(angle_rad)) * power
                            cue_stick.pull_dist = 0
                            cue_stick.visible = False
                            turn_in_progress = True
                            ball_potted_this_turn = False

        # --- 3. UPDATE LOGIC ---
        if not in_menu and not is_paused:
            if is_paused: pass 
            else:
                btn_restart.check_hover(game_mouse_pos)
                btn_menu.check_hover(game_mouse_pos)

                if placing_cue_ball:
                    # Bola putih mengikuti mouse
                    cue_ball.pos.x = max(PLAY_AREA_LEFT+15, min(PLAY_AREA_RIGHT-15, game_mouse_pos[0]))
                    cue_ball.pos.y = max(PLAY_AREA_TOP+15, min(PLAY_AREA_BOTTOM-15, game_mouse_pos[1]))
                    cue_ball.velocity = pygame.math.Vector2(0,0)

                elif not turn_in_progress:
                    # Update stik
                    if cue_stick.active:
                        dist = math.hypot(game_mouse_pos[0] - cue_ball.pos.x, game_mouse_pos[1] - cue_ball.pos.y)
                        cue_stick.pull_dist = min(dist, cue_stick.max_pull)
                    cue_stick.update(game_mouse_pos, cue_ball.pos)

                # Fisika Bola
                moving_count = 0
                all_balls = [cue_ball] + object_balls
                for b in all_balls:
                    if not placing_cue_ball:
                        b.move()
                        b.check_wall_collision()
                    if b.is_moving: moving_count += 1
                
                if not placing_cue_ball:
                    resolve_collisions(all_balls)
                
                # Cek Bola Masuk
                to_remove = []
                for ball in object_balls:
                    for p in pockets:
                        if p.check_potted(ball):
                            to_remove.append(ball)
                            scores[player_turn] += ball.value
                            ball_potted_this_turn = True
                            break
                for b in to_remove: object_balls.remove(b)
                    
                # Cek Scratch (Bola Putih Masuk)
                foul_scratch = False
                for p in pockets:
                    if p.check_potted(cue_ball):
                        foul_scratch = True
                        cue_ball.velocity = pygame.math.Vector2(0,0)
                        # Penalti Skor
                        scores[player_turn] = max(0, scores[player_turn] - 20)
                
                # Logic Pergantian Giliran (Turn System)
                if turn_in_progress and moving_count == 0:
                    turn_in_progress = False
                    
                    if selected_mode == 2: # Multiplayer
                        if foul_scratch:
                            # Jika scratch, ganti giliran DAN aktifkan Ball in Hand
                            player_turn = 3 - player_turn 
                            placing_cue_ball = True # <<< FITUR BARU
                            cue_stick.visible = False
                        elif not ball_potted_this_turn:
                            # Jika tidak ada bola masuk, ganti giliran biasa
                            player_turn = 3 - player_turn
                            cue_stick.visible = True
                        else:
                            # Jika bola masuk dan tidak scratch, lanjut main
                            cue_stick.visible = True
                    else:
                        # Single Player Logic
                        if foul_scratch:
                            cue_ball.pos = pygame.math.Vector2(PLAY_AREA_LEFT + PLAY_AREA_WIDTH*0.25, GAME_HEIGHT//2)
                        cue_stick.visible = True

        # --- 4. DRAWING ---
        if in_menu:
            draw_main_menu(canvas, selected_mode)
        else:
            draw_fancy_table(canvas)
            for p in pockets: p.draw(canvas)
            for b in object_balls: b.draw(canvas)
            cue_ball.draw(canvas)
            
            if placing_cue_ball:
                # Indikator visual saat menaruh bola
                pygame.draw.circle(canvas, (255, 255, 0), (int(cue_ball.pos.x), int(cue_ball.pos.y)), 16, 2)
                t = font_medium.render("BALL IN HAND: Click to Place", True, COLOR_HIGHLIGHT)
                canvas.blit(t, (GAME_WIDTH//2 - t.get_width()//2, 100))
            
            elif not turn_in_progress and not is_paused:
                cue_stick.draw_guideline(canvas, cue_ball.pos)
                cue_stick.draw(canvas, cue_ball.pos)
            
            # UI Header
            pygame.draw.rect(canvas, (0, 0, 0, 150), (0, 0, GAME_WIDTH, 60))
            if selected_mode == 1:
                t = font_large.render(f"SCORE: {scores[1]}", True, COLOR_WHITE)
                canvas.blit(t, (20, 10))
            else:
                c1 = COLOR_HIGHLIGHT if player_turn == 1 else (100, 100, 100)
                c2 = COLOR_HIGHLIGHT if player_turn == 2 else (100, 100, 100)
                canvas.blit(font_large.render(f"P1: {scores[1]}", True, c1), (20, 10))
                canvas.blit(font_large.render(f"P2: {scores[2]}", True, c2), (GAME_WIDTH - 180, 10))
                turn_t = font_medium.render(f"PLAYER {player_turn}'S TURN", True, COLOR_WHITE)
                canvas.blit(turn_t, (GAME_WIDTH//2 - turn_t.get_width()//2, 15))

            if is_paused:
                draw_pause_menu(canvas)
                btn_restart.draw(canvas)
                btn_menu.draw(canvas)

            # Game Over Screen
            if len(object_balls) == 0:
                overlay = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
                overlay.set_alpha(200)
                overlay.fill(COLOR_BLACK)
                canvas.blit(overlay, (0,0))
                w_txt = "GAME CLEAR!" if selected_mode == 1 else f"PLAYER {1 if scores[1]>scores[2] else 2} WINS!"
                if scores[1] == scores[2] and selected_mode == 2: w_txt = "DRAW!"
                
                fin = font_title.render(w_txt, True, COLOR_WHITE)
                canvas.blit(fin, (GAME_WIDTH//2 - fin.get_width()//2, GAME_HEIGHT//2 - 50))
                
                btn_menu.rect.center = (GAME_WIDTH//2, GAME_HEIGHT//2 + 80)
                btn_menu.draw(canvas)

        # Rendering Akhir (Scaling)
        screen.fill(COLOR_BLACK)
        scaled_surf = pygame.transform.smoothscale(canvas, (int(GAME_WIDTH * scale), int(GAME_HEIGHT * scale)))
        screen.blit(scaled_surf, (offset_x, offset_y))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()