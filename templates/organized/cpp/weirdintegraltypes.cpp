#include <iostream>

int main(){
    short int var1{10};
    short int var2{20}; // 2byt 
    char var3{34}; // 1byt 
    char var4{44};
    // < 4 bytes no no arithmatic operations
    std::cout << sizeof(var1) << std::endl;
    auto result1= var1+var2;
    auto r2=var3+var4;
    std::cout << result1 << '\n' << r2 << "\n" << sizeof(r2) << "\n" << sizeof(result1) << std::endl;
    return 0;
}