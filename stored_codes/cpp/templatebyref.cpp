#include <iostream>

template <typename T> 
const T& maximum(const T& a,const T& b){
    std::cout << &a << std::endl;
    return (a>b)?a:b;
}
int main(){
    int a{1};
    int b{2};
    std::cout << &a << std::endl;
    auto result=maximum(a,b);    
    std::cout << &a << std::endl;
    std::cout << result << std::endl;
    return 0;
}

// while in pass by value addresses inside and outside are different while inside its same in ref