#include "spdlog/spdlog.h"
//#include <wiringPi.h>
#include <stdio.h>
bool print(bool x) {
    spdlog::info("Hello, {}!", "World");
    return x;
}

int main() {
    print(true);
    print(true);
    print(false);
    print(true);

    //wiringPiSetup() ;
    //pinMode(0, OUTPUT) ;

    return 0;
}
