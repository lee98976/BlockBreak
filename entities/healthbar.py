from entities.heart import Heart
heartSet = {
    "pos": (200,200),

    "img_paths": [
        "assets/heartEmpty.png",
        "assets/heartDamage.png",
        "assets/heartHeal1.png",
        "assets/heartHeal2.png",
        "assets/heartHeal3.png",
    ],

    "anims": [
        [(0, 200)], # empty
        [(4, 200)], # full
        [(1, 30)], # ouch!
        [(2,15),(3,15),(4,15)], # heal
    ]
}

class HealthBar:
    def __init__(self, groupToAdd):
        self.hearts = [Heart(heartSet, (i * 40 + 20, 420)) for i in range(5)]
        for i in self.hearts:
            groupToAdd.add(i)
    
    def updateHealth(self, hp):
        for i in range(1, 5 + 1):
            curHeart = self.hearts[i - 1]
            if hp >= i:
                if not curHeart.on: curHeart.turnOn()
            else:
                if curHeart.on: curHeart.turnOff()
