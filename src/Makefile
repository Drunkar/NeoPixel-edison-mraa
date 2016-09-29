NeoPixel:
	# shared object for python
	swig -python NeoPixel.i 
	gcc -lmraa -Wall -fPIC -c NeoPixel.c NeoPixel_wrap.c  -I /usr/include/python2.7/
	gcc -lmraa -shared -o _NeoPixel.so NeoPixel.o NeoPixel_wrap.o

	# shared object for c
	gcc -lmraa -Wall -fPIC -c NeoPixel.c
	gcc -lmraa -shared -o NeoPixel.so NeoPixel.o

clean:
	rm NeoPixel_wrap.c *.o *.so