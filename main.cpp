#include "spdlog/spdlog.h"

bool print(bool x) {
    spdlog::info("Hello, {}!", "World");
    return x;
}

int main() {
    print(true);
    return 0;
}
