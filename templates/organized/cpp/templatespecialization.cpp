#include <iostream>
#include <cstring>

template <typename T>  T maximum(T a,T b){
    return (a>b)?a:b;
}
template <>
const char* maximum<const char*> (const char* a,const char* b){
    return (std::strcmp(a,b)>0)?a:b;
}
int main(){
    // int a{10};
    // int b{23};
    // double c{344.44};
    // double d{453.45};
    std::string e{"hakai"};
    std::string f{"world"};
    // auto max_int = maximum(a,b);
    const char* l{"lmao"};
    const char* s{"Disaster"};
    const char* res=maximum(l,s);
    std::cout << res << std::endl;
    return 0;
}
