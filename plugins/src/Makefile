CC = gcc
OBJECTS := $(patsubst %.c,%,$(wildcard *.c))

all: $(OBJECTS)

%: %.c
	$(CC) $< -o $@

install: all
	cp $(OBJECTS) ../
