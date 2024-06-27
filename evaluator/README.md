# Building the evaluator

```shell
    mkdir -p build
    cd build
    cmake ..
    make pheval
    cd ..
    (for mac: rename build/libpheval.0.6.0.dylib to build/libpheval.so.0.6.0)
    g++ -fPIC --shared -std=c++11 -I include/ wrapper.cpp build/libpheval.so.0.6.0 -o wrapper.so
```

## Usage

```python
  # Make sure that it imports from parent directory
  from evaluator.evaluate_cards import evaluate_cards
```
