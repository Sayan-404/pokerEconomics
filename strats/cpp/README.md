compile with

gcc -I ./include/ hand_potential.c newlookuptable.c libpheval.a -o hand_potential

First function improves the time by 0.003 seconds

To compile multi.cc

gcc -Iinclude -c hand_potential.c -o hand_potential.o  
gcc -Iinclude -c lookuptable.c -o lookuptable.o

g++ -Iinclude -Iinclude/lookuptable -Iinclude/phevaluator -Iinclude/quicksort \
 multi.cc hand_potential.o lookuptable.o -L. -lpheval -o multi
