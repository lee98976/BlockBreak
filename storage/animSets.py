playerAnimSet = {
    "img_paths": [
        "assets/player/playerBasic.png",
        "assets/player/playerDash.png",
        *[f"assets/player/playerDeath{i}.png" for i in range(1, 11)],
        "assets/player/playerProjectile1.png",
        "assets/player/playerProjectile2.png"
    ],

    "anims": [
        [(0, 200)],
        [(1, 12)],
        [(i, 8) for i in range(2, 11)] + [(11, 9999)]
    ]
}

enemyAnimSet = {
    "img_paths": [
        # --- NORMAL ---
        "assets/reddie/Reddie_idle.png",

        # --- AMBUSH ---
        "assets/reddie/Ambush_idle.png",

        # --- NORMAL → AMBUSH ---
        *[f"assets/reddie/Reddie_transform_{i}.png" for i in range(1, 12)],

        # --- AMBUSH → NORMAL ---
        *[f"assets/reddie/Ambush_transform_{i}.png" for i in range(1, 6)],

        # --- DEATH ---
        "assets/reddie/reddieDeath1.png",
        "assets/reddie/reddieDeath2.png",
        "assets/reddie/reddieDeath3.png",
    ],

    "anims": [
        # 0: normal idle
        [(0, 200)],

        # 1: ambush idle
        [(1, 200)],

        # 2: normal → ambush
        [(i, 6) for i in range(2, 13)],

        # 3: ambush → normal
        [(i, 7) for i in range(13, 18)],

        # 4: death
        [(i, 10) for i in range(18, 21)]
    ]
}

bullieAnimSet = {
    "img_paths": [
        # --- IDLE ---
        "assets/bullie/bully_idle_1.png",
        "assets/bullie/bully_idle_2.png",
        "assets/bullie/bully_idle_3.png",

        # --- SELF PROJECTILE ---
        "assets/bullie/bully_projectile_1.png",
        "assets/bullie/bully_projectile_2.png",

        # --- PROJECTILE TYPES (1–4) ---
        *[f"assets/bullie/bully_{i}projectile_{j}.png" for i in range(1,5) for j in range(1,3)],

        # --- DEATH ---
        *[f"assets/bullie/bully_death_{i}.png" for i in range(1,9)],
    ],

    "anims": [
        # 0: idle
        [(0,10),(1,10),(2,10)],

        # 1: self projectile (spin / flash)
        [(3,6),(4,6)],

        # 2–5: projectile types (1–4)
        [(5,6),(6,6)],    # type 1
        [(7,6),(8,6)],    # type 2
        [(9,6),(10,6)],   # type 3
        [(11,6),(12,6)],  # type 4

        # 6: death
        [(i,5) for i in range(13,21)]
    ]
}

miniBossAnimSet = {
    "img_paths": [
        "assets/miniBoss/miniBossAwakened.png",
        *[f"assets/miniBoss/miniBossDeath{i}.png" for i in range(1, 13)]
    ],

    "anims": [
        [(0, 200)],
        [(i,6) for i in range(1,12)] + [(12, 9999)]
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
        "assets/heart/heartEmpty.png",
        "assets/heart/heartDamage.png",
        "assets/heart/heartHeal1.png",
        "assets/heart/heartHeal2.png",
        "assets/heart/heartHeal3.png",
    ],

    "anims": [
        [(0, 200)],
        [(4, 200)],
        [(1, 30)],
        [(2,15),(3,15),(4,15)],
    ]
}

doorSet = {
    "img_paths": [
        "assets/doors/door_closed.png",
        "assets/doors/door_open_1.png",
        "assets/doors/door_open_2.png",
        "assets/doors/door_open_3.png",
        "assets/doors/door_open_4.png",
        "assets/doors/door_open_5.png",
        "assets/doors/door_open_6.png",
        "assets/doors/door_open_7.png",
    ],

    "anims": [
        [(0, 9999)],
        [(i, 5) for i in range(1, 7)],
        [(7, 9999)]
    ]
}

buttonSet = {
    "img_paths": [
        "assets/buttons/button_1.png",
        "assets/buttons/button_2.png",
        "assets/buttons/button_3.png",
        "assets/buttons/button_4.png",
    ],

    "anims": {
        0: [(0, 9999)],
        1: [(1, 9999)],
        2: [(2, 9999)],
        3: [(3, 9999)],
    }
}

dashTrailSet = {
    "img_paths": [
        *[f"assets/dashTrail/dash_{i:02}.png" for i in range(11)]
    ],

    "anims": [
        [(i, 2) for i in range(11)]
    ],

    "rotation": 0
}

diagonalDashTrailSet = {
    "img_paths": [
        *[f"assets/diagonalDashTrail/topright_dash_{i:02}.png" for i in range(10)]
    ],

    "anims": [
        [(i, 2) for i in range(10)]
    ],

    "rotation": 0
}

bossAnimSet = {
    "img_paths": [
        "assets/oldBoss/bossAwakened.png",
        "assets/oldBoss/bossIdle.png",
        "assets/oldBoss/bossIdle1.png",
        "assets/oldBoss/bossIdle2.png",
        "assets/oldBoss/bossIdle3.png",
        *[f"assets/oldBoss/bossSummon{i}.png" for i in range(1,4)],
        *[f"assets/oldBoss/bossDeath{i}.png" for i in range(1,12)]
    ],

    "anims": [
        [(1,10),(2,10),(3,10),(4,10)],
        [(5,8),(6,8),(7,8)],
        [(i,6) for i in range(8,18)] + [(18, 9999)]
    ]
}

dialogueAnimSet = {
    "img_paths": [
        # --- PLAYER ---
        "assets/portraits/player1.png",
        "assets/portraits/player2.png",

        # --- BULLIE ---
        *[f"assets/portraits/bullie{i}.png" for i in range(1,13)],

        # --- REDDIE ---
        "assets/portraits/reddies1.png",
        "assets/portraits/reddies2.png",

        # --- BOSS (TEMP PLACEHOLDER) ---
        "assets/portraits/reddies1.png",

        "assets/transparent.png"
    ],

    "anims": [
        # 0: PLAYER (idle talking)
        [(0,15),(1,15)],

        # 1: BULLIE (expressive)
        [(i,5) for i in range(2,14)],

        # 2: REDDIE (simple loop)
        [(14,12),(15,12)],

        # 3: BOSS (placeholder)
        [(16,20)],

        # 4: GAME
        [(17, 99999)]
    ]
}