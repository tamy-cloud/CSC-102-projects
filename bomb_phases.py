#################################
# CSC 102 Defuse the Bomb Project
# GUI and Phase class definitions
# Team: Tamara and her Minions
#################################

# import the configs
import pygame
from bomb_configs import *
# other imports
from tkinter import *
import tkinter
from threading import Thread
from time import sleep
import os
import sys

pygame.init()
#########
# classes
#########
# the LCD display GUI
class Lcd(Frame):
    def __init__(self, window):
        super().__init__(window, bg="black")
        # make the GUI fullscreen
        window.attributes("-fullscreen", True)
        # we need to know about the timer (7-segment display) to be able to pause/unpause it
        self._timer = None
        # we need to know about the pushbutton to turn off its LED when the program exits
        self._button = None
        # setup the initial "boot" GUI
        self.setupBoot()
        
        

    # sets up the LCD "boot" GUI
    def setupBoot(self):
        # set column weights
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        # the scrolling informative "boot" text
        self._lscroll = Label(self, bg="black", fg="white", font=("Courier New", 18), text="", justify=LEFT)
        self._lscroll.grid(row=0, column=0, columnspan=2, sticky=W)
        # serial number in top right corner
        self._lserial = Label(self, bg="black", fg="white", font=("Courier New", 18), text=f"sn{serial}")
        self._lserial.grid(row=0, column=2, sticky=E)
        self.pack(fill=BOTH, expand=True)

    # sets up the LCD GUI
    def setup(self):
        #see if the sound works
        pygame.mixer.music.load("freesound_community-ticking-timer-91503.mp3")
        pygame.mixer.music.play(-1)
        # the timer
        self._ltimer = Label(self, bg="black", fg="#ff6600", font=("Courier New", 18), text="Time left: ")
        self._ltimer.grid(row=1, column=0, columnspan=3, sticky=W)
        # the keypad passphrase
        self._lkeypad = Label(self, bg="black", fg="#ff6600", font=("Courier New", 18), text="Keypad phase: ")
        self._lkeypad.grid(row=2, column=0, columnspan=3, sticky=W)
        # the jumper wires status
        self._lwires = Label(self, bg="black", fg="#ff6600", font=("Courier New", 18), text="Wires phase: ")
        self._lwires.grid(row=3, column=0, columnspan=3, sticky=W)
        # the pushbutton status
        self._lbutton = Label(self, bg="black", fg="#ff6600", font=("Courier New", 18), text="Button phase: ")
        self._lbutton.grid(row=4, column=0, columnspan=3, sticky=W)
        # the toggle switches status
        self._ltoggles = Label(self, bg="black", fg="#ff6600", font=("Courier New", 18), text="Toggles phase: ")
        self._ltoggles.grid(row=5, column=0, columnspan=2, sticky=W)
        # the strikes left
        #Use yarn balls for stikes
        # create a frame to hold all 3 yarn balls in a row
        self._yarn_frame = Frame(self, bg="black")
        self._yarn_frame.grid(row=1, column=2, sticky=E)
        # load the yarn ball image
        '''I got this from claud just the resizing part'''
        from PIL import Image, ImageTk
        img = Image.open("yarnball.png")
        img = img.resize((50, 50))
        self._yarn_img = ImageTk.PhotoImage(img)
        # create 3 image labels inside the frame
        self._lyarn1 = Label(self._yarn_frame, bg="black", image=self._yarn_img)
        self._lyarn1.pack(side=LEFT)
        self._lyarn2 = Label(self._yarn_frame, bg="black", image=self._yarn_img)
        self._lyarn2.pack(side=LEFT)
        self._lyarn3 = Label(self._yarn_frame, bg="black", image=self._yarn_img)
        self._lyarn3.pack(side=LEFT)
        #for the key pad phrase
        self._lphrase = Label(self, bg="black", fg="#ff6600", font=("Courier New", 18), text=f"{keypad_phrase} 4123")
        self._lphrase.grid(row=5, column=1, sticky=E)
        self._lphrase.grid_remove()
        #
        cat = Image.open(cat_image)
        cat = cat.resize((100, 100))
        self._cat_img = ImageTk.PhotoImage(cat)
        self._lcat = Label(self, bg="black", image=self._cat_img)
        self._lcat.grid(row=8, column=2, sticky=SE)

        if (SHOW_BUTTONS):
            # the pause button (pauses the timer)
            self._bpause = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Pause", anchor=CENTER, command=self.pause)
            self._bpause.grid(row=6, column=0, pady=40)
            # the quit button
            self._bquit = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Quit", anchor=CENTER, command=self.quit)
            self._bquit.grid(row=6, column=2, pady=40)

    #subrotine for the blinking key pad phrase
    def show_phrase(self, visible=True, blinks=0):
        # I got this fro claude hopefully it workds
        if not hasattr(self, '_lphrase'):
            return
        if blinks < 6:
            # blink on and off
            if visible:
                self._lphrase.grid()
            else:
                self._lphrase.grid_remove()
            self.after(250, self.show_phrase, not visible, blinks + 1)
        else:
            # done blinking, hide for 5 seconds then repeat
            self._lphrase.grid_remove()
            self.after(5000, self.show_phrase, True, 0)
    # lets us pause/unpause the timer (7-segment display)
    def setTimer(self, timer):
        self._timer = timer

    # lets us turn off the pushbutton's RGB LED
    def setButton(self, button):
        self._button = button

    # pauses the timer
    def pause(self):
        if (RPi):
            self._timer.pause()

    # setup the conclusion GUI (explosion/defusion)
    def conclusion(self, success=False):
        # destroy/clear widgets that are no longer needed
        self._lscroll["text"] = ""
        self._ltimer.destroy()
        self._lkeypad.destroy()
        self._lwires.destroy()
        self._lbutton.destroy()
        self._ltoggles.destroy()
        self._yarn_frame.destroy()
        self._lphrase.destroy()
        self._lcat.destroy()
        pygame.mixer.music.stop()
        pygame.mixer.music.load("virtual_vibes-cat-meow-sound-383823.mp3")
        pygame.mixer.music.play(1)
        if (SHOW_BUTTONS):
            self._bpause.destroy()
            self._bquit.destroy()

        # reconfigure the GUI
        # the retry button
        if success:
            # claude helped me with the font of the test
            # winning screen
            self._ldefused = Label(self, bg="black", fg="#00ff00", font=("Courier New", 72, "bold"), text="DEFUSED")
            self._ldefused.grid(row=1, column=0, columnspan=3, pady=40)
            self._lcongrats = Label(self, bg="black", fg="#00ff00", font=("Courier New", 36), text="Congratulations!")
            self._lcongrats.grid(row=2, column=0, columnspan=3)
        else:
            # losing screen
            self._lboom = Label(self, bg="black", fg="red", font=("Courier New", 72, "bold"), text="BOOM!")
            self._lboom.grid(row=1, column=0, columnspan=3, pady=40)
            self._ldead = Label(self, bg="black", fg="red", font=("Courier New", 36), text="The cats get everything.")
            self._ldead.grid(row=2, column=0, columnspan=3)


            # re-attempts the bomb (after an explosion or a successful defusion)
            def retry(self):
                # re-launch the program (and exit this one)
                os.execv(sys.executable, ["python3"] + [sys.argv[0]])
                exit(0)

    # quits the GUI, resetting some components
    def quit(self):
        if (RPi):
            # turn off the 7-segment display
            self._timer._running = False
            self._timer._component.blink_rate = 0
            self._timer._component.fill(0)
            # turn off the pushbutton's LED
            for pin in self._button._rgb:
                pin.value = True
        # exit the application
        exit(0)

# template (superclass) for various bomb components/phases
class PhaseThread(Thread):
    def __init__(self, name, component=None, target=None):
        super().__init__(name=name, daemon=True)
        # phases have an electronic component (which usually represents the GPIO pins)
        self._component = component
        # phases have a target value (e.g., a specific combination on the keypad, the proper jumper wires to "cut", etc)
        self._target = target
        # phases can be successfully defused
        self._defused = False
        # phases can be failed (which result in a strike)
        self._failed = False
        # phases have a value (e.g., a pushbutton can be True/Pressed or False/Released, several jumper wires can be "cut"/False, etc)
        self._value = None
        # phase threads are either running or not
        self._running = False

# the timer phase
class Timer(PhaseThread):
    def __init__(self, component, initial_value, name="Timer"):
        super().__init__(name, component)
        # the default value is the specified initial value
        self._value = initial_value
        # is the timer paused?
        self._paused = False
        # initialize the timer's minutes/seconds representation
        self._min = ""
        self._sec = ""
        # by default, each tick is 1 second
        self._interval = 1

    # runs the thread
    def run(self):
        self._running = True
        while (self._running):
            if (not self._paused):
                # update the timer and display its value on the 7-segment display
                self._update()
                self._component.print(str(self))
                # wait 1s (default) and continue
                sleep(self._interval)
                # the timer has expired -> phase failed (explode)
                
                
                if (self._value == 0):
                    self._running = False
                self._value -= 1
            else:
                sleep(0.1)

    # updates the timer (only internally called)
    def _update(self):
        self._min = f"{self._value // 60}".zfill(2)
        self._sec = f"{self._value % 60}".zfill(2)

    # pauses and unpauses the timer
    def pause(self):
        # toggle the paused state
        self._paused = not self._paused
        # blink the 7-segment display when paused
        self._component.blink_rate = (2 if self._paused else 0)

    # returns the timer as a string (mm:ss)
    def __str__(self):
        return f"{self._min}:{self._sec}"

# the keypad phase
class Keypad(PhaseThread):
    def __init__(self, component, target, name="Keypad"):
        super().__init__(name, component, target)
        # the default value is an empty string
        self._value = ""

    # runs the thread
    def run(self):
        self._running = True
        while (self._running):
            # process keys when keypad key(s) are pressed
            if (self._component.pressed_keys):
                # debounce
                while (self._component.pressed_keys):
                    try:
                        key = self._component.pressed_keys[0]
                    except:
                        key = ""
                    sleep(0.1)
                # * clears the current input
                if (key == "*"):
                    self._value = ""
                # only log the key if we haven't reached the full length yet
                elif (len(self._value) < len(self._target)):
                    self._value += str(key)

                # only check once the user has typed the full length
                if (len(self._value) == len(self._target)):
                    if (self._value == self._target):
                        # correct -> defused
                        self._defused = True
                    else:
                        # wrong -> flash and reset
                        self._flash()
                        self._failed = True
                        self._value = ""
            sleep(0.1)


    def _flash(self):
        # flash the value on screen 3 times to signal wrong answer
        original = self._value
        for _ in range(3):
            self._value = ""
            sleep(0.2)
            self._value = original
            sleep(0.2)
        self._value = ""
        # returns the keypad combination as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            return self._value

# the jumper wires phase
class Wires(PhaseThread):
    def __init__(self, component, target, name="Wires"):
        super().__init__(name, component, target)

    # runs the thread
    def run(self):
        # TODO
        #Done by tamara
        self._running = True
        while (self._running):
            # get the jumper wire states (0->False, 1->True)
            self._value = "".join([str(int(pin.value)) for pin in self._component])
            # check if the binary value matches the target
            if (int(self._value, 2) == self._target):
                self._defused = True
            sleep(0.1)

    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            #tamara changed this  so i alctually says that you did something
            return f"{self._value}/{int(self._value, 2)}" 
        # returns the jumper wires state as a string


def next_color(c):
    lst = ["R", "G", "B"]
    current_index = lst.index(c)
    next_index = (current_index + 1 )% 3
    return lst[next_index]

# the pushbutton phase
class Button(PhaseThread):
    def __init__(self, component_state, component_rgb, target, color, timer, name="Button"):
        super().__init__(name, component_state, target)
        # the default value is False/Released
        self._value = False
        # has the pushbutton been pressed?
        self._pressed = False
        # we need the pushbutton's RGB pins to set its color
        self._rgb = component_rgb
        # the pushbutton's randomly selected LED color
        self._color = color
        # we need to know about the timer (7-segment display) to be able to determine correct pushbutton releases in some cases
        self._timer = timer

    # runs the thread
    def run(self):
        self._running = True
        # set the RGB LED color
        
        while (self._running):
            
            if self._timer._value % 5 == 0:
                self._color = next_color(self._color)
            
            
            #This actually changes the color based on the color variable
            self._rgb[0].value = False if self._color == "R" else True
            self._rgb[1].value = False if self._color == "G" else True
            self._rgb[2].value = False if self._color == "B" else True
            
            # get the pushbutton's state
            self._value = self._component.value
            # it is pressed
            if (self._value):
                # note it
                self._pressed = True
                if self._timer._value % 2 == 0 and self._color == "R":
                    self._defused = True
            # it is released
            #else:
                # was it previously pressed?
                #if (self._pressed):
                    # check the release parameters
                    # for R, nothing else is needed
                    # for G or B, a specific digit must be in the timer (sec) when released
                    #if (not self._target or self._target in self._timer._sec):
                    #    self._defused = True
                    #else:
                    #    self._failed = True
                     #note that the pushbutton was released
                    #self._pressed = False
            sleep(0.1)

    # returns the pushbutton's state as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            return str("Pressed" if self._value else "Released")


# the toggle switches phase
class Toggles(PhaseThread):
    def __init__(self, component, target, name="Toggles"):
        super().__init__(name, component, target) 
        self._wrong = False

    # runs the thread
    def run(self):
        # TODO
        #done by tamara
        self._running = True
        while (self._running):
            self._value = [pin.value for pin in self._component]
            #self._value = self._value.reverse()
            # convert toggle states to a number (binary -> decimal)
            total = int("".join([str(int(v)) for v in reversed(self._value)]), 2)
            
            # claude helped me with some od the logic of when it will start to check if ad answer is wrong or right
            if total > 0:
            #wait check for 3 seconds
                sleep(3)
                new_total = sum([self._value[i] * (2 ** i) for i in range(len(self._value))])
                
                if new_total == total:
                    if new_total == self._target:
                        self._defused = True
                    else:
                        self._wrong = True
                        self._failed = True
                        sleep(3)
                        self._wrong = False
                        self._failed = False
            sleep(0.1)

            #if (total == self._target):
            #    self._defused = True
            #sleep(0.1)

    # returns the toggle switches state as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        elif (self._wrong):
            return "WRONG"
        else:
            # TODO
            binary = "".join([str(int(v)) for v in reversed(self._value)])
            return f"{binary}/{int(binary, 2)}"
        
        
        
