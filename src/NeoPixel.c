#include "string.h"
#include "stdio.h"
#include "mraa.h"

// 3 color R, G and B ordering
#define WS2811_STRIP_RGB                         0x00100800
#define WS2811_STRIP_RBG                         0x00100008
#define WS2811_STRIP_GRB                         0x00081000
#define WS2811_STRIP_GBR                         0x00080010
#define WS2811_STRIP_BRG                         0x00001008
#define WS2811_STRIP_BGR                         0x00000810

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

mraa_gpio_context NPInit(ws2811_channel_t *channel_t)
{
  mraa_gpio_context gpio;

  gpio = mraa_gpio_init(channel_t->gpionum);
  mraa_gpio_dir(gpio, MRAA_GPIO_OUT);
  mraa_gpio_use_mmaped(gpio, 1);
  channel_t->leds = malloc(sizeof(ws2811_led_t) * channel_t->count);
  if (!channel_t->leds)
  {
    return 0;
  }

  memset(channel_t->leds, 0, sizeof(ws2811_led_t) * channel_t->count);

  if (!channel_t->strip_type)
  {
    channel_t->strip_type=WS2811_STRIP_RGB;
  }

  return gpio;
}
void NPLowCode(mraa_gpio_context gpio)
{
  //---- T0H ----
  mraa_gpio_write(gpio , 1);
  //---- T0L ----
  mraa_gpio_write(gpio , 0);
  mraa_gpio_write(gpio , 0);
  mraa_gpio_write(gpio , 0);
  mraa_gpio_write(gpio , 0);
}
void NPHiCode(mraa_gpio_context gpio)
{
  //---- T1H ----
  mraa_gpio_write(gpio , 1);
  mraa_gpio_write(gpio , 1);
  mraa_gpio_write(gpio , 1);
  mraa_gpio_write(gpio , 1);
  //---- T1L ----
  mraa_gpio_write(gpio , 0);
}
void NPReset(mraa_gpio_context gpio)
{
  int i=0;
  for(i=0;i<1000;i++) mraa_gpio_write(gpio , 0);
}

void NPRenderColor(mraa_gpio_context gpio,int R,int G,int B)
{
  int i=0;

  for(i=0;i<8;i++){
    if( (G & (0x80>>i)) ==0) NPLowCode(gpio);
    else NPHiCode(gpio);
  }
  for(i=0;i<8;i++){
    if( (R & (0x80>>i)) ==0) NPLowCode(gpio);
    else NPHiCode(gpio);
  }
  for(i=0;i<8;i++){
    if( (B & (0x80>>i)) ==0) NPLowCode(gpio);
    else NPHiCode(gpio);
  }
}

void NPRender(ws2811_channel_t *channel, mraa_gpio_context gpio)
{
  int scale   = (channel->brightness & 0xff) + 1;
  int wshift  = (channel->strip_type >> 24) & 0xff;
  int rshift  = (channel->strip_type >> 16) & 0xff;
  int gshift  = (channel->strip_type >> 8)  & 0xff;
  int bshift  = (channel->strip_type >> 0)  & 0xff;

  int i=0;
  int j=0;
  int k=0;
  uint8_t array_size = 3; // Assume 3 color LEDs, RGB
  for (i = 0; i < channel->count; i++) {
    uint8_t color[] =
    {
        (((channel->leds[i] >> gshift) & 0xff) * scale) >> 8, // green
        (((channel->leds[i] >> rshift) & 0xff) * scale) >> 8, // red
        (((channel->leds[i] >> bshift) & 0xff) * scale) >> 8, // blue
        (((channel->leds[i] >> wshift) & 0xff) * scale) >> 8, // white
    };

    for (j = 0; j < array_size; j++) {
      for (k = 0; k < 8; k++) {
        if( (color[j] & (0x80>>k)) ==0) NPLowCode(gpio);
        else NPHiCode(gpio);
      }
    }
  }
}
