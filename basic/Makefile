CC = gcc
CFLAGS = -Wall -pthread -g
LIBS = -lgpiod
BUILD_DIR = build
BIN_DIR = bin
INCLUDE_DIR = include
SRC_DIR = src
TARGET = basic
TARGET_PATH = $(BIN_DIR)/$(TARGET)
SRCS = $(wildcard $(SRC_DIR)/*.c)
OBJS = $(SRCS:$(SRC_DIR)%.c=$(BUILD_DIR)/%.o)

.PHONY: all dirs clean

all: dirs $(TARGET_PATH)

dirs:
	mkdir -p $(BUILD_DIR) $(BIN_DIR)

$(TARGET_PATH): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $(OBJS) $(LIBS)
	chmod +x $@

$(BUILD_DIR)/%.o: $(SRC_DIR)/%.c
	mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) -I$(INCLUDE_DIR) -c $< -o $@

clean:
	rm -rf $(BUILD_DIR) $(BIN_DIR)
