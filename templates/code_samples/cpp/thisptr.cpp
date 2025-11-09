#include <iostream>
#include <string_view>

class Dog{
    public:
        Dog() = default;
        Dog(std::string_view name_param,std::string_view breed_param,int age_param );
        ~Dog();

        void print_info(){
            std::cout << "Dog (" << this << ") : [ name : " << name << " Breed : " << breed << " Age : " << *p_age << "]" << std::endl;
        }
        //Setters
        Dog& set_name(std::string_view name){
            this->name=name; // name=name not good
            return *this;
        }
        Dog& set_breed(std::string_view breed){
            this->breed=breed; // name=name not good
            return *this;
        }
        Dog& set_age(int age){
            *(this->p_age)=age; // name=name not good
            return *this;
        }

    private:
        std::string name;
        std::string breed;
        int* p_age{nullptr};
};
Dog::Dog(std::string_view name_param,std::string_view breed_param,int age_param){
    name=name_param;
    p_age=new int;
    breed=breed_param;
    *p_age=age_param;
    std::cout << "Dog constructor called for: " << name  << " at " << this << std::endl;

}

Dog::~Dog(){
    delete p_age;
    std::cout << "Dog destructor called for: " << name  << " at  " << this << std::endl;
}

int main(){
    Dog dog1("SSDXCD","Sheperfd",4); // constructor
    dog1.print_info();
    // dog1.set_name("Puma");
    // dog1.set_age(65);    
    // Chained calls using ptr
    // dog1.set_name("Lumba")->set_breed("Wolf breed") ->set_age(4);
    // Chained calls using references  
    dog1.set_name("Lumba").set_breed("Wolf breed").set_age(4);


    dog1.print_info();
    std::cout << "done" << std::endl;
    return 0;
}