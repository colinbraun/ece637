# For Linux or any machines with gcc compiler
CC = gcc

BUILD_DIR := ./build
SRC_DIRS := ../C-code/src/
# Every folder in ./src will need to be passed to GCC so that it can find header files
INC_DIRS := $(shell find $(SRC_DIRS) -type d)
# Add a prefix to INC_DIRS. So moduleA would become -ImoduleA. GCC understands this -I flag
INC_FLAGS := $(addprefix -I,$(INC_DIRS))
LIB_FLAGS := -L../lib/ -limg -lm

CFLAGS := -std=c99 -Wall -pedantic $(INC_FLAGS)

all: section3 section4 section5

clean:
	/bin/rm *.o

OBJ = util.o

section3: section3.o $(OBJ)
	# $(CC) $(CFLAGS) -o section3 section3.o $(OBJ) -lm
	$(CC) $(CFLAGS) -o section3 section3.o $(OBJ) $(LIB_FLAGS)
	mv section3 ./build

section4: section4.o $(OBJ)
	$(CC) $(CFLAGS) -o section4 section4.o $(OBJ) $(LIB_FLAGS)
	mv section4 ./build

section5: section5.o $(OBJ)
	$(CC) $(CFLAGS) -o section5 section5.o $(OBJ) $(LIB_FLAGS)
	mv section5 ./build

