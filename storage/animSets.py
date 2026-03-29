playerAnimSet = {
    "img_paths": [
        "assets/playerBasic.png",
        "assets/playerDash.png",
        *[f"assets/playerDeath{i}.png" for i in range(1, 11)],
        "assets/playerProjectile1.png",
        "assets/playerProjectile2.png"
    ],

    "anims": [

        [(0, 200)],

        [(1, 12)],

        [(i, 8) for i in range(2, 11)] + [(11, 9999)]

    ]
}

enemyAnimSet = {
    "img_paths": [
        "assets/enemyAwakened.png",
        "assets/enemyDeath1.png",
        "assets/enemyDeath2.png",
        "assets/enemyDeath3.png",
        "assets/enemyProjectile1.png",
        "assets/enemyProjectile2.png"
    ],

    "anims": [

        [(0, 200)],

        [(1,10),(2,10),(3,10)],

        [(4,6),(5,6)]

    ]
}

miniBossAnimSet = {
    "img_paths": [
        "assets/miniBossAwakened.png",
        *[f"assets/miniBossDeath{i}.png" for i in range(1, 13)]
    ],

    "anims": [

        [(0, 200)],

        [(i,6) for i in range(1,12)] + [(12, 9999)]

    ]
}

bossAnimSet = {
    "img_paths": [
        "assets/bossAwakened.png",
        "assets/bossIdle.png",
        "assets/bossIdle1.png",
        "assets/bossIdle2.png",
        "assets/bossIdle3.png",
        *[f"assets/bossSummon{i}.png" for i in range(1,4)],
        *[f"assets/bossDeath{i}.png" for i in range(1,12)]
    ],

    "anims": [

        [(1,10),(2,10),(3,10),(4,10)],

        [(5,8),(6,8),(7,8)],

        [(i,6) for i in range(8,18)] + [(18, 9999)] 

    ]
}

healthPackSet = {
    "img_paths": [
        "assets/healOrb.png"
    ],

    "anims": [
        [(0,200)]
    ]
}

heartSet = {
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