#include <iostream>

bool print(bool x) {
    std::cout << "Hello, World!" << std::endl;
    return x;
}

int main() {
    print(true);
    return 0;
}
