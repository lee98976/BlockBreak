from ui.heart import Heart

class HealthBar:
    def __init__(self, game):
        self.hearts = [Heart(game.heartSet, (i * 40 + 40, 460)) for i in range(5)]
        for i in self.hearts:
            game.ui_sprites.add(i)
    
    def updateHealth(self, hp):
        for i in range(1, 5 + 1):
            curHeart = self.hearts[i - 1]
            if hp >= i:
                if not curHeart.on: curHeart.turnOn()
            else:
                if curHeart.on: curHeart.turnOff()
