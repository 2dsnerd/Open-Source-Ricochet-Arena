from tkinter import *
import tkinter as tk
import RicochetArena

'''
Sounds Used:
 - death.wav | U by Kendrick Lamar | https://youtu.be/XGC4QpDIpJc?si=Bc-zwDCuh01phL2m
 - shoot.wav | https://pixabay.com/sound-effects/film-special-effects-pew-234075/
 - winso.wav | https://pixabay.com/sound-effects/film-special-effects-bell-323942/
 - woosh.mp3 | Plays When the Game is Reset | https://pixabay.com/sound-effects/film-special-effects-woosh-1-84800/
'''

DEFAULTS = {
    "GRAVITY": 0.44,
    "JUMP": -11,
    "SPEED": 4,
    "DISC_SPEED": 7,
    "DISC_MAX_AGE": 110,
    "KNOCKBACK_STR": 115
}

GRAVITY = DEFAULTS["GRAVITY"]
JUMP = DEFAULTS["JUMP"]
SPEED = DEFAULTS["SPEED"]
DISC_SPEED = DEFAULTS["DISC_SPEED"]
DISC_MAX_AGE = DEFAULTS["DISC_MAX_AGE"]
KNOCKBACK_STR = DEFAULTS["KNOCKBACK_STR"]

def resetDefault():
    global GRAVITY, JUMP, SPEED, DISC_SPEED, DISC_MAX_AGE, KNOCKBACK_STR

    GRAVITY = DEFAULTS["GRAVITY"]
    JUMP = DEFAULTS["JUMP"]
    SPEED = DEFAULTS["SPEED"]
    DISC_SPEED = DEFAULTS["DISC_SPEED"]
    DISC_MAX_AGE = DEFAULTS["DISC_MAX_AGE"]
    KNOCKBACK_STR = DEFAULTS["KNOCKBACK_STR"]

    spinboxGrav.delete(0, END); spinboxGrav.insert(0, GRAVITY)
    spinboxSpeed.delete(0, END); spinboxSpeed.insert(0, SPEED)
    spinboxJump.delete(0, END); spinboxJump.insert(0, JUMP)
    spinboxDS.delete(0, END); spinboxDS.insert(0, DISC_SPEED)
    spinboxDMA.delete(0, END); spinboxDMA.insert(0, DISC_MAX_AGE)
    spinboxKBS.delete(0, END); spinboxKBS.insert(0, KNOCKBACK_STR)

def startGame():
    settings = {
        "GRAVITY": float(spinboxGrav.get()),
        "JUMP": float(spinboxJump.get()),
        "SPEED": float(spinboxSpeed.get()),
        "DISC_SPEED": float(spinboxDS.get()),
        "DISC_MAX_AGE": float(spinboxDMA.get()),
        "KNOCKBACK_STR": float(spinboxKBS.get())
    }

    root.destroy()
    RicochetArena.run_game(settings)

root = Tk()
root.title("Open Source Ricochet Arena - Setup Menu")

tk.Label(root, text="Gravity").pack()
spinboxGrav = Spinbox(root, from_=0, to=1, increment=0.01)
spinboxGrav.pack()

tk.Label(root, text="Player Speed").pack()
spinboxSpeed = Spinbox(root, from_=0, to=256)
spinboxSpeed.pack()

tk.Label(root, text="Jump Force").pack()
spinboxJump = Spinbox(root, from_=-50, to=0)
spinboxJump.pack()

tk.Label(root, text="Disc Speed").pack()
spinboxDS = Spinbox(root, from_=0, to=256)
spinboxDS.pack()

tk.Label(root, text="Disc Max Lifetime").pack()
spinboxDMA = Spinbox(root, from_=0, to=600)
spinboxDMA.pack()

tk.Label(root, text="Disc Knockback Strength").pack()
spinboxKBS = Spinbox(root, from_=0, to=256)
spinboxKBS.pack()

resetDefault()

tk.Button(root, text="Reset to Default", command=resetDefault).pack()
tk.Button(root, text="Start Game", command=startGame).pack()

root.mainloop()
