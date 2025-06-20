CC=gcc
CFLAGS=-g                       # <- keep -g so GDB understands debug symbols

all: pond
pond: pond.c
	$(CC) $(CFLAGS) pond.c -o pond

clean:
	rm -f pond
