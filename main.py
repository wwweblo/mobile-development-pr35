from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        # Метод обрабатывает отскок мяча от ракетки
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        # Метод перемещает мяч в соответствии с его текущей скоростью
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self, vel=(4, 0)):
        # Метод начинает новую игру, устанавливая мяч в центре и задавая ему начальную скорость
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        # Метод обновляет состояние игры на каждом кадре
        self.ball.move()

        # Отскок от ракеток
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # Отскок мяча от верхней и нижней стенок
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        # Проверка на выход мяча за границы экрана и начисление очков
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.right > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

        # Управление вторым игроком (компьютером)
        if self.ball.center_y > self.player2.center_y:
            self.player2.center_y += min(2, self.ball.center_y - self.player2.center_y)
        elif self.ball.center_y < self.player2.center_y:
            self.player2.center_y -= min(2, self.player2.center_y - self.ball.center_y)

    def on_touch_move(self, touch):
        # Обработчик события перемещения пальца по экрану для управления первым игроком
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y


class PongApp(App):
    def build(self):
        # Метод создает и возвращает экземпляр игрового класса
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    PongApp().run()
