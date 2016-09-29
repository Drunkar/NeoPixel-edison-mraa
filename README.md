# NeoPixel-edison-mraa

NeoPixel library for edison via mraa gpio.
Tested only in ubilinux and WS2812.

## Dependencies

* swig
* mraa

## Installation

### Install mraa to ubilinux

Follow this article: https://learn.sparkfun.com/tutorials/installing-libmraa-on-ubilinux-for-edison

If you face ``Unknown CMake command "target_include_directories".``, modify mraa source code -> https://github.com/Drunkar/mraa/commit/8c1891013a6665ac35d33ff00e13f1e3db3d53f5 .

### Install NeoPixel-edison-mraa

```
git clone https://github.com/Drunkar/NeoPixel-edison-mraa
cd NeoPixel-edison-mraa/src/
make
cd ../examples/

# python test
python strandtest.py

# c test
make
./whitetest
```