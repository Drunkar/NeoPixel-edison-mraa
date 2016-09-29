#!/usr/bin/env python
import os
import sys
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../src")
import _NeoPixel as NPAPI

OUT_PIN = 15
NUM_LED = 16
BRIGHTNESS = 255


def Color(red, green, blue, white = 0):
    """Convert the provided red, green, blue color to a 24-bit color value.
    Each color component should be a value 0-255 where 0 is the lowest intensity
    and 255 is the highest intensity.
    """
    return (white << 24) | (red << 16)| (green << 8) | blue


class _LED_Data(object):
    """Wrapper class which makes a SWIG LED color data array look and feel like
    a Python list of integers.
    """

    def __init__(self, leds, size):
        self.size = size
        self._leds = leds

    def __getitem__(self, pos):
        """Return the 24-bit RGB color value at the provided position or slice
        of positions.
        """
        # Handle if a slice of positions are passed in by grabbing all the values
        # and returning them in a list.
        if isinstance(pos, slice):
            return [NPAPI.NPRLedGet(self._leds, n) for n in range(pos.indices(self.size))]
        # Else assume the passed in value is a number to the position.
        else:
            return NPAPI.NPRLedGet(self._leds, pos)

    def __setitem__(self, pos, value):
        """Set the 24-bit RGB color value at the provided position or slice of
        positions.
        """
        # Handle if a slice of positions are passed in by setting the appropriate
        # LED data values to the provided values.
        if isinstance(pos, slice):
            index = 0
            for n in range(pos.indices(self.size)):
                NPAPI.NPRLedSet(self._leds, n, value[index])
                index += 1
        # Else assume the passed in value is a number to the position.
        else:
            return NPAPI.NPRLedSet(self._leds, pos, value)


class NeoPixel(object):

    def __init__(self, out_pin, num_led, brightness, channel=1):
        self._leds = NPAPI.new_ws2811_channel_t()
        NPAPI.ws2811_channel_t_count_set(self._leds, num_led)
        NPAPI.ws2811_channel_t_gpionum_set(self._leds, out_pin)
        NPAPI.ws2811_channel_t_brightness_set(self._leds, brightness)

        self._gpio = NPAPI.NPInit(self._leds)
        self._num_led = num_led
        self._led_data = _LED_Data(self._leds, num_led)

        for i in range(self._num_led):
            self._led_data[i] = 0

    def numPixels(self):
        return self._num_led

    def  setPixelColor(self, n, color):
        """Set LED at position n to the provided 24-bit color value (in RGB order).
        """
        self._led_data[n] = color

    def show(self):
        NPAPI.NPRender(self._leds, self._gpio)


def colorWipe(neopixels, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(neopixels.numPixels()):
        neopixels.setPixelColor(i, color)
        neopixels.show()
        time.sleep(wait_ms/1000.0)


def theaterChase(neopixels, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, neopixels.numPixels(), 3):
                neopixels.setPixelColor(i+q, color)
            neopixels.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, neopixels.numPixels(), 3):
                neopixels.setPixelColor(i+q, 0)


def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


def rainbow(neopixels, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(neopixels.numPixels()):
            neopixels.setPixelColor(i, wheel((i+j) & 255))
        neopixels.show()
        time.sleep(wait_ms/1000.0)


def rainbowCycle(neopixels, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(neopixels.numPixels()):
            neopixels.setPixelColor(i, wheel(((i * 256 / neopixels.numPixels()) + j) & 255))
        neopixels.show()
        time.sleep(wait_ms/1000.0)


def theaterChaseRainbow(neopixels, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, neopixels.numPixels(), 3):
                neopixels.setPixelColor(i+q, wheel((i+j) % 255))
            neopixels.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, neopixels.numPixels(), 3):
                neopixels.setPixelColor(i+q, 0)

def main():
    neopixels = NeoPixel(OUT_PIN, NUM_LED, BRIGHTNESS)

    print ("Press Ctrl-C to quit.")
    while True:
        # Color wipe animations.
        colorWipe(neopixels, Color(255, 0, 0))  # Red wipe
        colorWipe(neopixels, Color(0, 255, 0))  # Blue wipe
        colorWipe(neopixels, Color(0, 0, 255))  # Green wipe
        # Theater chase animations.
        theaterChase(neopixels, Color(127, 127, 127))  # White theater chase
        theaterChase(neopixels, Color(127,   0,   0))  # Red theater chase
        theaterChase(neopixels, Color(  0,   0, 127))  # Blue theater chase
        # Rainbow animations.
        rainbow(neopixels)
        rainbowCycle(neopixels)
        theaterChaseRainbow(neopixels)


if __name__ == "__main__":
    main()