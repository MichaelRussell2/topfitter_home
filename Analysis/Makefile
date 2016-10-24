
CXX=g++ 
BOOST_ROOT=/Users/michael/Programs/boost_1_55_0/
INCDIR=-Iinclude -isystem$(BOOST_ROOT)
CXXFLAGS=--std=c++11 -m64 -fPIC -O2 -march=native $(INCDIR)
LDFLAGS= 
FLAGS= -Wall -Wextra
CFLAGS=-m64 -g3 -fPIC -pedantic -pg -O3 -march=native


SRCS=analysis.cc histo.cc lhe_read.cc
OBJS=$(subst .cc,.o,$(SRCS))

all: analysis

analysis: $(OBJS)
	$(CXX) $(CXXFLAGS) $(LDFLAGS) -o analysis  $(OBJS)

clean:
	rm -f *.o analysis

