CC = gcc
PLUGIN_OBJECTS := $(patsubst %.c,%.o,$(wildcard plugins/*/*.c))

all: $(PLUGIN_OBJECTS)

%.o: %.c
	$(CC) $< -o $@
