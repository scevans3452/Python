def init():
    global SCREEN_WIDTH, SCREEN_HEIGHT, POW_WIDTH, POW_HEIGHT, MIN_INTERVAL, MAX_INTERVAL, BULLET_HEIGHT, BULLET_WIDTH, MODIFIER, ACTUAL_VOLUME

    SCREEN_WIDTH    = 1280
    SCREEN_HEIGHT   = 720
    POW_WIDTH       = 25
    POW_HEIGHT      = 25
    BULLET_WIDTH    = 32        # 32 looks good
    BULLET_HEIGHT   = 8         # 8 looks good
    MIN_INTERVAL    = 2000      # 2 second min
    MAX_INTERVAL    = 12000     # 12 second max
    MODIFIER        = 1
    ACTUAL_VOLUME   = 1