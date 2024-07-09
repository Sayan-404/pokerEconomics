cd hand_evaluator
mkdir -p build
cd build
cmake ..
make pheval
cd ..
mv build/libpheval.0.6.0.dylib build/libpheval.so.0.6.0
g++ -fPIC --shared -std=c++11 -I include/ wrapper.cpp build/libpheval.so.0.6.0 -o wrapper.so
cd ..