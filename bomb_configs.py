#################################
# CSC 102 Defuse the Bomb Project
# Configuration file
# Team: Ken, Sophia, Tamara
#################################

# constants
DEBUG = False         # debug mode?
RPi = True          # is this running on the RPi?
SHOW_BUTTONS = False # show the Pause and Quit buttons on the main LCD GUI?
COUNTDOWN = 300      # the initial bomb countdown value (seconds)
NUM_STRIKES = 3      # the total strikes allowed before the bomb "explodes"
NUM_PHASES = 4       # the total number of initial active bomb phases

# imports
from random import randint, shuffle, choice
from string import ascii_uppercase
import random
if (RPi):
    import board
    from adafruit_ht16k33.segments import Seg7x4
    from digitalio import DigitalInOut, Direction, Pull
    from adafruit_matrixkeypad import Matrix_Keypad

#################################
# setup the electronic components
#################################
# 7-segment display
# 4 pins: 5V(+), GND(-), SDA, SCL
#         ----------7SEG---------
if (RPi):
    i2c = board.I2C()
    component_7seg = Seg7x4(i2c)
    # set the 7-segment display brightness (0 -> dimmest; 1 -> brightest)
    component_7seg.brightness = 0.5

# keypad
# 8 pins: 10, 9, 11, 5, 6, 13, 19, NA
#         -----------KEYPAD----------
if (RPi):
    # the pins
    keypad_cols = [DigitalInOut(i) for i in (board.D10, board.D9, board.D11)]
    keypad_rows = [DigitalInOut(i) for i in (board.D5, board.D6, board.D13, board.D19)]
    # the keys
    keypad_keys = ((1, 2, 3), (4, 5, 6), (7, 8, 9), ("*", 0, "#"))

    component_keypad = Matrix_Keypad(keypad_rows, keypad_cols, keypad_keys)
    
# jumper wires
# 10 pins: 14, 15, 18, 23, 24, 3V3, 3V3, 3V3, 3V3, 3V3
#          -------JUMP1------  ---------JUMP2---------
# the jumper wire pins
if (RPi):
    # the pins
    component_wires = [DigitalInOut(i) for i in (board.D14, board.D15, board.D18, board.D23, board.D24)]
    for pin in component_wires:
        # pins are input and pulled down
        pin.direction = Direction.INPUT
        pin.pull = Pull.DOWN

# pushbutton
# 6 pins: 4, 17, 27, 22, 3V3, 3V3
#         -BUT1- -BUT2-  --BUT3--
if (RPi):
    # the state pin (state pin is input and pulled down)
    component_button_state = DigitalInOut(board.D4)
    component_button_state.direction = Direction.INPUT
    component_button_state.pull = Pull.DOWN
    # the RGB pins
    component_button_RGB = [DigitalInOut(i) for i in (board.D17, board.D27, board.D22)]
    for pin in component_button_RGB:
        # RGB pins are output
        pin.direction = Direction.OUTPUT
        pin.value = True

# toggle switches
# 3x3 pins: 12, 16, 20, 21, 3V3, 3V3, 3V3, 3V3, GND, GND, GND, GND
#           -TOG1-  -TOG2-  --TOG3--  --TOG4--  --TOG5--  --TOG6--
if (RPi):
    # the pins
    component_toggles = [DigitalInOut(i) for i in (board.D12, board.D16, board.D20, board.D21)]
    for pin in component_toggles:
        # pins are input and pulled down
        pin.direction = Direction.INPUT
        pin.pull = Pull.DOWN

###########
# functions to generate targets for toggles/wires/keypad/Button
'''
if statements until you die
'''
###########
def genSerial():
    # Create your own logic of making a serial number (if needed)
    # TODO
    listS = ['@B026DE5', '2713980', '938-564!']
    rand_sn = random.choice(listS)
    return rand_sn

#Cat images for the cat lady grand may but I love cats so tis is just for me honestly
cat_image = random.choice(["cat1.png", "cat2.png", "cat3.png"])

def genTogglesTarget():
    # Create your own logic of making a target number for toggles
    # TODO
    if cat_image == "cat1.png":
        return 2   # 0010
    elif cat_image == "cat2.png":
        return 9   # 1001
    elif cat_image == "cat3.png":
        return 7   # 0111

def genWiresTarget():
    # Create your own logic of making a target number for wires
    # TODO
    if serial == '@B026DE5':
        return 21  # 10101
    elif serial == '2713980':
        return 27  # 11011
    elif serial == '938-564!':
        return 14  # 01110
    
# generates the keypad combination from a keyword and rotation key
keypad_phrase = random.choice(["Backass Catwards", "Mewbinachi"])

def genKeypadTarget():
    # Create your own logic of making a keypad combination number if needed
    # TODOgi
    if keypad_phrase == "Backass Catwards":
        return "1890"
    elif keypad_phrase == "Mewbinachi":
        return "5357"
    
'''
We can take away to serial numre and do the buttons or something
'''
# generate the color of the pushbutton (which determines how to defuse the phase)
button_color = choice(["R", "G", "B"])

def genButtonTarget():
    # TODO
    global button_color
    # Create your own logic of making a Button target
    # appropriately set the target (R is None)
    b_target = None
    # G is the first numeric digit in the serial number
    if (button_color == "G"):
        b_target = [ n for n in serial if n.isdigit() ][0]
    # B is the last numeric digit in the serial number
    elif (button_color == "B"):
        b_target = [ n for n in serial if n.isdigit() ][-1]

    return b_target

###############################
serial = genSerial()
toggles_target = genTogglesTarget()
wires_target = genWiresTarget()
keypad_target = genKeypadTarget()
button_target = genButtonTarget()

# set the bomb's LCD bootup text
boot_text = f"Welcome to your possible inheritance\n"\
          #  f"*Serial number: {serial}\n"\
            
