#include "stdio.h"
#include "stdint.h"
#include "mraa.h"

typedef uint32_t ws2811_led_t;  //< 0xWWRRGGBB
typedef struct
{
  int gpionum;                  //< GPIO Pin with PWM alternate function, 0 if unused
  int invert;                   //< Invert output signal
  int count;                    //< Number of LEDs, 0 if channel is unused
  int brightness;               //< Brightness value between 0 and 255
  int strip_type;               //< Strip color layout -- one of WS2811_STRIP_xxx constants
  ws2811_led_t *leds;           //< LED buffers, allocated by driver based on count
} ws2811_channel_t;

uint32_t Color(uint8_t white, uint8_t red, uint8_t green, uint8_t blue) {
  return (white << 24) | (red << 16)| (green << 8) | blue;
}

int main(int argc, char const *argv[])
{
  ws2811_channel_t neopixels = {
    .gpionum = 15,
    .invert = 0,
    .count = 8,
    .brightness = 255,
  };
  mraa_gpio_context gpio;
  gpio = NPInit(&neopixels);

  uint32_t wrgb = Color(0, 255, 255, 255);
  int i=0;
  for (i=0; i<neopixels.count; i++) {
    neopixels.leds[i] = wrgb;
  }

  while(1) {
    NPRender(&neopixels, gpio);
    usleep(50000);
  }
  return 0;
}