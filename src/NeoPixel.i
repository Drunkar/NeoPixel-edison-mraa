%module NeoPixel

%include "stdint.i"

%{
  #include "stdio.h"
  #include "mraa.h"
%}


%{
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
  mraa_gpio_context NPInit(ws2811_channel_t *channel_t);
  void NPLowCode(mraa_gpio_context gpio);
  void NPHiCode(mraa_gpio_context gpio);
  void NPReset(mraa_gpio_context gpio);
  void NPRenderColor(mraa_gpio_context gpio,int R,int G,int B);
  void NPRender(ws2811_channel_t *channel, mraa_gpio_context gpio);
%}


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
mraa_gpio_context NPInit(ws2811_channel_t *channel_t);
void NPLowCode(mraa_gpio_context gpio);
void NPHiCode(mraa_gpio_context gpio);
void NPReset(mraa_gpio_context gpio);
void NPRenderColor(mraa_gpio_context gpio,int R,int G,int B);
void NPRender(ws2811_channel_t *channel, mraa_gpio_context gpio);

%inline %{
  uint32_t NPRLedGet(ws2811_channel_t *channel, int lednum)
  {
    if (lednum >= channel->count)
    {
      return -1;
    }

    return channel->leds[lednum];
  }

  int NPRLedSet(ws2811_channel_t *channel, int lednum, uint32_t color)
  {
    if (lednum >= channel->count)
    {
      return -1;
    }

    channel->leds[lednum] = color;

    return 0;
  }
%}
