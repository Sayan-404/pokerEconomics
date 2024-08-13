# Building the evaluator

```shell
mkdir -p build
cd build
cmake ..
make pheval
cd ..
(for mac: rename build/libpheval.0.6.0.dylib to build/libpheval.so.0.6.0)
gcc -fPIC -shared -I include/ hs.c build/libpheval.so.0.6.0 -o hs.so 
OR
g++ -fPIC --shared -std=c++11 -I include/ potential.c build/libpheval.so.0.6.0 -o pot.so
```

## Usage

```python
  # Make sure that it imports from parent directory
  from poker_metrics.hand_strength.hs import handStrength
```
