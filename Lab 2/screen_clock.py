import time
from time import strftime, sleep
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display.rgb import color565
import adafruit_rgb_display.st7789 as st7789
from random import choice

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()
screenColor = color565(125, 255, 255)



messages = [
    "Please have a nice day!",
    "Live long and prosper",
    "Valar Morghulis",
    "Valar Dohaeris",

]

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    #TODO: Lab 2 part D work should be filled in here. You should be able to look in cli_clock.py and stats.py 
    y = top
    txt1 = "Top: Current Time"
    txt2 = "Bottom: Time Period"
    txt3 = "Both: message"
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    draw.text((x, y), txt1, font=font, fill="#00FFFF")
    y += font.getsize(txt1)[1]
    draw.text((x, y), txt2, font=font, fill="#1AFD9C")
    # y += font.getsize(txt2)[1]
    # draw.text((x, y), txt3, font=font, fill="#0000FF")

    hour = int(strftime("%H"))
    if hour >= 0 and hour < 6:
        period = 'midnight'
        period_fill = "#FFFFFF"
    elif hour >= 6 and hour < 12:
        period = 'morning'
        period_fill = "#7FFFD4"
    elif hour >= 12 and hour < 18:
        period = 'afternoon'
        period_fill = "#FF60AF"
    elif hour >= 18 and hour < 24:
        period = 'evening'
        period_fill = "#0080FF"

        currentTime = strftime("%m/%d/%Y %H:%M:%S")
        sentence = choice(messages)
        y = top

        if buttonB.value and not buttonA.value:  # just button A pressed
            draw.rectangle((0, 0, width, height), outline=0, fill=0)
            draw.text((x, y), currentTime, font=font, fill="#FFFFFF")
        if buttonA.value and not buttonB.value:  # just button B pressed
            draw.rectangle((0, 0, width, height), outline=0, fill=period_fill)
            draw.text((x, y), period, font=font, fill="#0000FF")

            draw.text((x, y + 20), sentence, font=font, fill="#FFFFFF")
        if not buttonA.value and not buttonB.value:  # none pressed
            draw.rectangle((0, 0, width, height), outline=0, fill=0)
            draw.text((x, y), sentence, font=font, fill="#FFFFFF")

    # Display image.
    disp.image(image, rotation)
    time.sleep(1)
