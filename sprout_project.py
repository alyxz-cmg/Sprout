import math
import time
import random


# --- Sprite: bananas ---
@event.on_green_flag
def green_flag_script():
    sprite.looks.show()
    sprite.motion.go_to(target="_random_")

@event.on_broadcast_received('bananasEaten')
def receive_bananaseaten():
    sprite.motion.go_to(target="_random_")

@event.on_broadcast_received('haycartTouched')
def receive_haycarttouched():
    sprite.motion.go_to(target="_random_")


# --- Sprite: haycart ---
@event.on_green_flag
def green_flag_script():
    sprite.looks.show()
    sprite.motion.go_to(target="_random_")

@event.on_broadcast_received('bananasEaten')
def receive_bananaseaten():
    sprite.motion.go_to(target="_random_")

@event.on_broadcast_received('haycartTouched')
def receive_haycarttouched():
    sprite.motion.go_to(target="_random_")


# --- Sprite: larry ---
@event.on_key_pressed('up arrow')
def key_pressed_up_arrow():
    sprite.direction = 0
    sprite.motion.move(10)

@event.on_key_pressed('right arrow')
def key_pressed_right_arrow():
    sprite.direction = 90
    sprite.motion.move(10)

@event.on_key_pressed('left arrow')
def key_pressed_left_arrow():
    sprite.direction = "-90"
    sprite.motion.move(10)

@event.on_key_pressed('down arrow')
def key_pressed_down_arrow():
    sprite.direction = 180
    sprite.motion.move(10)

@event.on_green_flag
def green_flag_script():
    sprite.rotation_style = "left-right"

@event.on_green_flag
def green_flag_script():
    sprite.rotation_style = "left-right"
    sprite.draggable = True
    sprite.ui.show_variable('var_score')
    sprite.ui.show_variable('var_timer')
    var_score = 0
    var_timer = 20
    while not (("timer" == 0)):
    time.sleep(1)
    var_timer += "-1"
    if sprite.sensing.is_touching("bananas"):
    sprite.sound.play("larryRoar")
    sprite.events.broadcast("bananasEaten")
    var_score += 1

if sprite.sensing.is_touching("haycart"):
var_score += "-1"
sprite.costume = "larrycry"
sprite.sound.play_until_done("Crunch2")
sprite.costume = "larry"
sprite.events.broadcast("haycartTouched")
