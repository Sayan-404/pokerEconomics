cd hand_evaluator
mkdir -p build
cd build
cmake ..
make pheval
cd ..
if [[ "$OSTYPE" == "darwin"* ]]; then
    g++ -fPIC --shared -std=c++11 -I include/ wrapper.cpp build/libpheval.0.6.0.dylib -o wrapper.so
else
    g++ -fPIC --shared -std=c++11 -I include/ wrapper.cpp build/libpheval.so.0.6.0 -o wrapper.so
fi
cd ..