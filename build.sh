echo "Building hand_evaluator"
cd hand_evaluator
mkdir -p build
cd build
cmake ..
make pheval
cd ..
g++ -fPIC --shared -std=c++11 -I include/ wrapper.cpp build/libpheval.so.0.6.0 -o wrapper.so

cd ..

echo "\n\nBuilding simplified_hand_potential"
cd poker_metrics/simplified_hand_potential
mkdir -p build
cd build
cmake ..
make pheval
cd ..
gcc -fPIC --shared -I include/ simplified_hand_potential.c build/libpheval.so.0.6.0 -o potential.so
cd ../..