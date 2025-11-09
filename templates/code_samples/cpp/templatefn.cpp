#include <iostream>
#include <string>

template <typename T>
T maximum(T a,T b){
    return (a>b)?a:b;
}

int main(){
    int c{9};
    int d{10};
    double pie{3.14};
    double e{2.718};
    std::string s1{"All Hail"};  
    std::string s2{"Lelouch"};
    auto result = maximum(c,d);
    std::cout << result << std::endl;
    // Explicit template arguments
    maximum<double>(c,e); // Converts int to double  as it is implicit conversion 
    maximum<double>(c,d); // explicitly say that we want the double 
    // version called ,if an instance is not there
    // already it will be created
    //maximum<double>(a,e); // error : compiler error as cant convert string to double 
    return 0;
}

// we cant do templates on ptr bcs compiler will compare the addresses instead of values and cayses problems