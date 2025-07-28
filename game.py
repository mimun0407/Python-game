import pygame as pg
import sys, time
from bird import Bird
from pipe import Pipe

pg.init()

class Game:
    def __init__(self):
        # setting window config
        self.width = 600
        self.height = 768
        self.scale_factor = 1.5
        self.win = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption("Flappy Bird by You")
        self.clock = pg.time.Clock()
        self.move_speed = 250

        self.bird = Bird(self.scale_factor)
        self.is_enter_pressed = False
        self.is_game_over = False
        self.pipes = []
        self.pipe_generate_counter = 71

        self.score = 0
        self.font = pg.font.SysFont("Arial", 48, bold=True)

        # ✅ Load âm thanh
        self.sound_flap = pg.mixer.Sound("assets/sfx/flap.wav")
        self.sound_dead = pg.mixer.Sound("assets/sfx/dead.wav")
        self.sound_score = pg.mixer.Sound("assets/sfx/score.wav")

        self.setUpBgAndGround()
        self.gameLoop()

    def gameLoop(self):
        last_time = time.time()
        while True:
            new_time = time.time()
            dt = new_time - last_time
            last_time = new_time

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        if self.is_game_over:
                            self.resetGame()
                        else:
                            self.is_enter_pressed = True
                            self.bird.update_on = True
                    if event.key == pg.K_SPACE and self.is_enter_pressed and not self.is_game_over:
                        self.bird.flap(dt)
                        self.sound_flap.play()  # ✅ phát âm khi vỗ cánh

            self.updateEverything(dt)
            self.checkCollisions()
            self.drawEverything()
            pg.display.update()
            self.clock.tick(60)

    def resetGame(self):
        self.score = 0
        self.pipes.clear()
        self.bird.rect.center = (100, 100)
        self.bird.y_velocity = 0
        self.bird.update_on = True
        self.pipe_generate_counter = 71
        self.ground1_rect.x = 0
        self.ground2_rect.x = self.ground1_rect.right
        self.is_enter_pressed = True
        self.is_game_over = False

    def endGame(self):
        self.bird.update_on = False
        self.is_enter_pressed = False
        self.is_game_over = True
        self.sound_dead.play()  # ✅ phát âm khi game over

    def checkCollisions(self):
        if len(self.pipes):
            if self.bird.rect.bottom > 568:
                self.endGame()
            if (self.bird.rect.colliderect(self.pipes[0].rect_down) or
                    self.bird.rect.colliderect(self.pipes[0].rect_up)):
                self.endGame()

    def updateEverything(self, dt):
        if self.is_enter_pressed and not self.is_game_over:
            # moving the ground
            self.ground1_rect.x -= int(self.move_speed * dt)
            self.ground2_rect.x -= int(self.move_speed * dt)

            if self.ground1_rect.right < 0:
                self.ground1_rect.x = self.ground2_rect.right
            if self.ground2_rect.right < 0:
                self.ground2_rect.x = self.ground1_rect.right

            # generating pipes
            if self.pipe_generate_counter > 70:
                self.pipes.append(Pipe(self.scale_factor, self.move_speed))
                self.pipe_generate_counter = 0
            self.pipe_generate_counter += 1

            # moving the pipes and checking for score
            for pipe in self.pipes:
                pipe.update(dt)
                if not hasattr(pipe, "passed") and pipe.rect_up.right < self.bird.rect.left:
                    pipe.passed = True
                    self.score += 1
                    self.sound_score.play()  # ✅ phát âm khi ghi điểm

            # removing pipes if out of screen
            if len(self.pipes) != 0 and self.pipes[0].rect_up.right < 0:
                self.pipes.pop(0)

        self.bird.update(dt)

    def drawEverything(self):
        self.win.blit(self.bg_img, (0, -300))
        for pipe in self.pipes:
            pipe.drawPipe(self.win)
        self.win.blit(self.ground1_img, self.ground1_rect)
        self.win.blit(self.ground2_img, self.ground2_rect)
        self.win.blit(self.bird.image, self.bird.rect)

        # draw score
        score_surface = self.font.render(str(self.score), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(self.width // 2, 50))
        self.win.blit(score_surface, score_rect)

        # draw game over
        if self.is_game_over:
            game_over_text = self.font.render("Game Over", True, (255, 0, 0))
            game_over_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2 - 50))
            self.win.blit(game_over_text, game_over_rect)

            score_text = self.font.render(f"Your Score: {self.score}", True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(self.width // 2, self.height // 2 + 10))
            self.win.blit(score_text, score_rect)

            restart_text = pg.font.SysFont("Arial", 32).render("Press Enter to Restart", True, (200, 200, 200))
            restart_rect = restart_text.get_rect(center=(self.width // 2, self.height // 2 + 60))
            self.win.blit(restart_text, restart_rect)

    def setUpBgAndGround(self):
        self.bg_img = pg.transform.scale_by(pg.image.load("assets/bg.png").convert(), self.scale_factor)
        self.ground1_img = pg.transform.scale_by(pg.image.load("assets/ground.png").convert(), self.scale_factor)
        self.ground2_img = pg.transform.scale_by(pg.image.load("assets/ground.png").convert(), self.scale_factor)

        self.ground1_rect = self.ground1_img.get_rect()
        self.ground2_rect = self.ground2_img.get_rect()

        self.ground1_rect.x = 0
        self.ground2_rect.x = self.ground1_rect.right
        self.ground1_rect.y = 568
        self.ground2_rect.y = 568


if __name__ == "__main__":
    game = Game()