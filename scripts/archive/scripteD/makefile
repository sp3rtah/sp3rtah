CC:=gcc
LIBS:=-L/usr/lib/python3.8/config-3.8-x86_64-linux-gnu -L/usr/lib  -lcrypt -lpthread -ldl  -lutil -lm -lm -lpython3.8
FLAGS:= -I/usr/include/python3.8 -I/usr/include/python3.8  -Wno-unused-result -Wsign-compare -g -fdebug-prefix-map=/build/python3.8-4OrTnN/python3.8-3.8.10=. -specs=/usr/share/dpkg/no-pie-compile.specs -fstack-protector -Wformat -Werror=format-security  -DNDEBUG -g -fwrapv -O3 -Wall -fPIE

#folders
SRC:= src
INC:= include

BIN:= bin
MAIN:= $(BIN)/scripted
OBJECT:= $(BIN)/scripted.o

#dependancies
SRCS:= $(wildcard $(SRC)/*.c)
INCL:= $(wildcard $(INC)/*.h)

build: $(BIN) $(OBJECT) $(MAIN)

$(MAIN): $(OBJECT)
	$(CC) $^ $(LIBS) -o $@

$(OBJECT): $(SRCS) $(INCL)
	$(CC) $(FLAGS) $(SRCS) -c -o $@

$(BIN):
	mkdir $@

run: build
	./$(MAIN) divide divide 5 2

clean:
	rm -rf $(BIN) __pycache__
