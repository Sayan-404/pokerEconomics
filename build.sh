cd potential_data/evaluator
mkdir -p build
cd build
cmake ..
make pheval
cd ..
g++ -fPIC --shared -std=c++11 -I include/ wrapper.cpp build/libpheval.so.0.6.0 -o wrapper.so
