# RicochetArena.py
import pygame, random, sys, math, os

def run_game(settings):
    GRAVITY = float(settings["GRAVITY"])
    JUMP = float(settings["JUMP"])
    SPEED = float(settings["SPEED"])
    DISC_SPEED = float(settings["DISC_SPEED"])
    DISC_MAX_AGE = float(settings["DISC_MAX_AGE"])
    KNOCKBACK_STR = float(settings["KNOCKBACK_STR"])
    KNOCKBACK = True
    DISC_LIFETIME = True

    # Pygame Setup
    pygame.init()
    pygame_icon = pygame.image.load('disc.png')
    pygame.display.set_icon(pygame_icon)

    pygame.mixer.init()
    death_sound = pygame.mixer.Sound("Sounds/death.wav")
    shoot_sound = pygame.mixer.Sound("Sounds/shoot.wav")
    test25 = pygame.mixer.Sound("Sounds/test25.mp3")
    win_sound = pygame.mixer.Sound("Sounds/winso.wav")
    woosh_sound = pygame.mixer.Sound("Sounds/woosh.mp3")

    W, H = 1280, 720
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Open Source Ricochet Arena")
    font = pygame.font.SysFont("consolas", 18, bold=True)
    big = pygame.font.SysFont("consolas", 48, bold=True)
    clock = pygame.time.Clock()

    # Randomized X Positons of Platforms for Heigher Replayability
    bpx = random.uniform(300, 600)
    startp1x = random.uniform(200, 500) # Player One Starting Position and Middle Left Pad
    startp2x = random.uniform(730, 900) # Player Two Starting Position and Middle Right Pad
    tlpx = random.uniform(220, 400)
    trpx = random.uniform(700, 900)
    tpx = random.uniform(400, 700)

    # Where Platforms Will Spawn at First Load
    PADS = [
        #            X         Y   Sx   Sy | S Means Scale
        pygame.Rect(bpx,      500, 200, 16), # Bottom Pad
        pygame.Rect(startp1x, 380, 160, 16), # Middle Left Pad
        pygame.Rect(startp2x, 380, 160, 16), # Middle Right Pad
        pygame.Rect(tlpx,     260, 160, 16), # Top Left Pad
        pygame.Rect(trpx,     260, 160, 16), # Top Right Pad
        pygame.Rect(tpx,      150, 160, 16), # Toppest Pad
    ]

    # Defines the Players Main Purpose
    class Player:
        def __init__(self, x, y, color, controls, name):
            self.x, self.y = float(x), float(y)
            self.vx = self.vy = 0.0
            self.w, self.h = 24, 28
            self.on_ground = False
            self.color = color
            self.controls = controls
            self.name = name
            self.lives = 3
            self.dead = False
            self.respawn_t = 0
            self.shoot_cd = 0
            self.facing = 1

        @property
        def rect(self):
            return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

        def update(self, keys, discs):
            if self.dead:
                self.respawn_t -= 1
                if self.respawn_t <= 0:
                    pad = random.choice(PADS)
                    self.x, self.y = pad.centerx - self.w // 2, pad.top - self.h
                    self.vx = self.vy = 0
                    self.dead = False
                return

            left, right, jump, shoot = self.controls

            if keys[left]:
                self.vx = -float(SPEED)
                self.facing = -1
            elif keys[right]:
                self.vx = float(SPEED)
                self.facing = 1
            else:
                self.vx *= 0.7

            if keys[jump] and self.on_ground:
                self.vy = float(JUMP)

            if keys[shoot] and self.shoot_cd == 0:
                dx, dy = self.facing, -0.3 if keys[jump] else 0
                mag = math.hypot(dx, dy) or 1
                discs.append(
                    Disc(
                        self.x + self.w // 2,
                        self.y + self.h // 2,
                        dx / mag * float(DISC_SPEED),
                        dy / mag * float(DISC_SPEED),
                        self,
                    )
                )
                if shoot_sound:
                    shoot_sound.play()
                self.shoot_cd = 25

            if self.shoot_cd > 0:
                self.shoot_cd -= 1

            self.vy += float(GRAVITY)
            self.x += self.vx
            self.y += self.vy
            self.on_ground = False

            r = self.rect
            for pad in PADS:
                if (r.bottom >= pad.top and r.bottom <= pad.top + 16 and r.right > pad.left and r.left < pad.right and self.vy >= 0):
                    self.y = pad.top - self.h
                    self.vy = 0
                    self.on_ground = True

            # The Player Dies
            if self.y > H + 20:
                if death_sound:
                    death_sound.play()
                self.lives -= 1
                self.dead = True
                self.respawn_t = 90

        def draw(self, surf):
            if self.dead:
                return
            pygame.draw.rect(surf, self.color, self.rect, border_radius=4)

    # Discs Collisions With the Enviorment and Players
    class Disc:
        def __init__(self, x, y, vx, vy, owner):
            self.x, self.y = float(x), float(y)
            self.vx, self.vy = vx, vy
            self.owner = owner
            self.alive = True
            self.bounces = 0
            self.age = 0
            self.trail = []

        def update(self, players):
            self.trail.append((self.x, self.y))
            if len(self.trail) > 8:
                self.trail.pop(0)

            self.x += self.vx
            self.y += self.vy

            if self.x < 0:
                self.vx = abs(self.vx)
                self.bounces += 1
            if self.x > W:
                self.vx = -abs(self.vx)
                self.bounces += 1
            if self.y < 0:
                self.vy = abs(self.vy)
                self.bounces += 1

            r = pygame.Rect(int(self.x) - 5, int(self.y) - 5, 10, 10)
            for pad in PADS:
                if r.colliderect(pad):
                    self.vy = -abs(self.vy)
                    self.bounces += 1
                    break

            # Players Collisions With the Discs
            for p in players:
                if p is self.owner or p.dead:
                    continue
                if p.rect.inflate(-4, -4).collidepoint(self.x, self.y):
                    if KNOCKBACK:
                        nx = 1 if self.vx >= 0 else -1
                        p.vx += nx * float(KNOCKBACK_STR)
                        p.vy = -5
                    else:
                        if death_sound:
                            death_sound.play()
                        p.lives -= 1
                        p.dead = True
                        p.respawn_t = 90

                    self.alive = False

            if (self.bounces > 4 or self.y > H + 40 or (DISC_LIFETIME and self.age > float(DISC_MAX_AGE))):
                self.alive = False

            self.age += 1

        def draw(self, surf):
            for i, (tx, ty) in enumerate(self.trail):
                s = pygame.Surface((8, 8), pygame.SRCALPHA)
                pygame.draw.circle(s, (*self.owner.color, int(180 * i / len(self.trail))), (4, 4), 4,)
                surf.blit(s, (int(tx) - 4, int(ty) - 4))

            pygame.draw.circle(surf, self.owner.color, (int(self.x), int(self.y)), 6)
            pygame.draw.circle(surf, (255, 255, 255), (int(self.x), int(self.y)), 6, 1)

    def new_game():
        p1 = Player(startp1x + 70, 340, (80, 160, 255), (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s), "P1") # Place Where Player One Will Spawn
        p2 = Player(startp2x + 70, 340, (255, 80, 80), (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN), "P2") # Place Where Player Two Will Spawn

        return p1, p2, []

    p1, p2, discs = new_game()
    players = [p1, p2]

    # Sets Frame Rate and Allows for Changes to All Keybindings, the Setup of the Game From the Pads Drawing to the Text
    while True:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    bpx = random.uniform(300, 600)
                    startp1x = random.uniform(200, 500)
                    startp2x = random.uniform(730, 900)
                    tlpx = random.uniform(220, 400)
                    trpx = random.uniform(700, 900)
                    tpx = random.uniform(400, 700)

                    PADS = [
                    #            X         Y   Sx   Sy | S Means Scale
                    pygame.Rect(bpx,      500, 200, 16), # Bottom Pad
                    pygame.Rect(startp1x, 380, 160, 16), # Middle Left Pad
                    pygame.Rect(startp2x, 380, 160, 16), # Middle Right Pad
                    pygame.Rect(tlpx,     260, 160, 16), # Top Left Pad
                    pygame.Rect(trpx,     260, 160, 16), # Top Right Pad
                    pygame.Rect(tpx,      150, 160, 16), # Toppest Pad
                    ]

                    p1, p2, discs = new_game()
                    woosh_sound.play()
                    players = [p1, p2]
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if e.key == pygame.K_BACKSLASH:
                    test25.play()

        keys = pygame.key.get_pressed()

        for p in players:
            p.update(keys, discs)

        for d in discs:
            d.update(players)

        discs = [d for d in discs if d.alive]

        screen.fill((5, 8, 18))

        for i in range(0, W, 60):
            pygame.draw.line(screen, (12, 18, 35), (i, 0), (i, H))

        for pad in PADS:
            pygame.draw.rect(screen, (30, 50, 100), pad, border_radius=3)
            pygame.draw.rect(screen, (60, 120, 220), pad, 2, border_radius=3)
            gs = pygame.Surface((pad.w, 8), pygame.SRCALPHA)
            gs.fill((40, 100, 255, 40))
            screen.blit(gs, (pad.x, pad.bottom))

        for d in discs:
            d.draw(screen)

        for p in players:
            p.draw(screen)

        for i, p in enumerate(players):
            x = 10 if i == 0 else W - 100
            screen.blit( font.render(f"{p.name} {'*' * p.lives}", True, p.color), (x, 5))
        winner = None
        for p in players:
            if p.lives <= 0:
                winner = next(q for q in players if q is not p)

        if winner:
            win_sound.play()
            text = big.render(f"{winner.name} WINS!", True, winner.color)
            screen.blit(text, text.get_rect(center=(W // 2, H // 2 - 20)))

            sub = font.render("R to Restart", True, (150, 150, 180))
            screen.blit(sub, sub.get_rect(center=(W // 2, H // 2 + 40)))

        screen.blit(font.render("P1: WASD - S TO SHOOT | P2: ARROW KEYS - DOWN TO SHOOT | R - Restart", True, (50, 60, 90)), (10, H - 22))

        pygame.display.flip()
