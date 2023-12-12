def init():
    global SCREEN_WIDTH, SCREEN_HEIGHT, POW_WIDTH, POW_HEIGHT, MIN_INTERVAL, MAX_INTERVAL, BULLET_HEIGHT, BULLET_WIDTH, MODIFIER
    # Define constants for the screen width and height
    SCREEN_WIDTH    = 600
    SCREEN_HEIGHT   = 400
    POW_WIDTH       = 25
    POW_HEIGHT      = 25
    BULLET_WIDTH    = 32        # 32 looks good
    BULLET_HEIGHT   = 8         # 8 looks good
    MIN_INTERVAL    = 100     # 15 second min
    MAX_INTERVAL    = 300     # 30 second max
    MODIFIER        = 1