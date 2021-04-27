OBJS = newzpr.o multiPick.o misc.o
CC = g++  
DEBUG = #-g
CFLAGS =  -c -w $(DEBUG) -O5 
LFLAGS =  $(DEBUG) -lm -lGL -lGLU -lglut -lpthread #-framework Cocoa -framework GLUT -framework OpenGL
zpr: $(OBJS)
	$(CC)   $(OBJS) -o  multiPick.exe  $(LFLAGS)
newzpr.o: newzpr.cpp  newzpr.h
	$(CC) $(CFLAGS) newzpr.cpp
misc.o: misc.cpp  misc.h
	$(CC) $(CFLAGS) misc.cpp
multiPick.o:	multiPick.cpp	newzpr.h  newzpr.cpp
	$(CC)	    $(CFLAGS)	    multiPick.cpp
