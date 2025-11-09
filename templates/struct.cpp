#include <iostream>

class Dog{
    std::string name;
}; // Members are private by default

struct Cat{
    std::string name;
}; // Members are public by default 
// Members can be made private or protected using access specifiers

struct Point{
    double x;
    double y;
};

int main(){
    Dog dog1;
    Cat cat1;
    // dog1.name = "Buddy"; // Error: 'name' is private within this context
    cat1.name = "Whiskers"; // OK: 'name' is public within this context
    std::cout << "Cat's name: " << cat1.name << std::endl;
    Point p1;
    p1.x = 10.5;
    p1.y = 20.5;
    std::cout << "Point coordinates: (" << p1.x << ", " << p1.y << ")" << std::endl;
    return 0;
}