#!/usr/bin/env python3
"""
Demo script showing the AI code analysis and enhanced compiler features.
"""

from code_analyzer import get_analysis_report
from enhanced_compiler import EnhancedCompiler

def demo_code_analysis():
    """Demonstrate AI code analysis on sample code with issues."""
    print("=" * 80)
    print("DEMO: AI CODE ANALYSIS")
    print("=" * 80)
    
    with open('demo_code_with_issues.c', 'r') as f:
        code = f.read()
    
    print("\n📝 Analyzing C code with common issues...\n")
    
    # Get formatted analysis report
    report = get_analysis_report(code, 'c')
    print(report)
    
    print("\n" + "=" * 80)

def demo_enhanced_compiler():
    """Demonstrate enhanced compiler with clean code."""
    print("\n" + "=" * 80)
    print("DEMO: ENHANCED C/C++ COMPILER")
    print("=" * 80)
    
    # Simple C program
    c_code = """
#include <stdio.h>

int main() {
    int n;
    printf("Enter a number: ");
    scanf("%d", &n);
    
    printf("Factorial of %d is: ", n);
    
    long long factorial = 1;
    for (int i = 1; i <= n; i++) {
        factorial *= i;
    }
    
    printf("%lld\\n", factorial);
    return 0;
}
"""
    
    print("\n🔧 Compiling and running C code (C11 standard)...\n")
    
    compiler = EnhancedCompiler()
    result = compiler.compile_and_run_c(
        c_code,
        stdin_input="5\n",  # Input: calculate factorial of 5
        standard='c11',
        optimization='-O2',
        use_warnings=True
    )
    
    if result.success:
        print("✅ Compilation successful!")
        print(f"⏱️  Compile time: {result.compile_time:.3f}s")
        print(f"⏱️  Execution time: {result.execution_time:.3f}s")
        print("\n📤 Output:")
        print(result.output)
        
        if result.warnings:
            print("\n⚠️  Warnings:")
            print(result.warnings)
    else:
        print("❌ Compilation failed!")
        print("\n🔴 Errors:")
        print(result.errors)
    
    print("\n" + "=" * 80)
    
    # C++ example with modern features
    cpp_code = """
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> numbers = {5, 2, 8, 1, 9, 3, 7};
    
    std::cout << "Original: ";
    for (const auto& num : numbers) {
        std::cout << num << " ";
    }
    std::cout << std::endl;
    
    std::sort(numbers.begin(), numbers.end());
    
    std::cout << "Sorted: ";
    for (const auto& num : numbers) {
        std::cout << num << " ";
    }
    std::cout << std::endl;
    
    return 0;
}
"""
    
    print("\n🔧 Compiling and running C++ code (C++17 standard)...\n")
    
    result = compiler.compile_and_run_cpp(
        cpp_code,
        stdin_input="",
        standard='c++17',
        optimization='-O2',
        use_warnings=True
    )
    
    if result.success:
        print("✅ Compilation successful!")
        print(f"⏱️  Compile time: {result.compile_time:.3f}s")
        print(f"⏱️  Execution time: {result.execution_time:.3f}s")
        print("\n📤 Output:")
        print(result.output)
        
        if result.warnings:
            print("\n⚠️  Warnings:")
            print(result.warnings)
    else:
        print("❌ Compilation failed!")
        print("\n🔴 Errors:")
        print(result.errors)
    
    print("\n" + "=" * 80)

def demo_compiler_info():
    """Display available compiler information."""
    print("\n" + "=" * 80)
    print("AVAILABLE COMPILERS")
    print("=" * 80)
    
    compiler = EnhancedCompiler()
    info = compiler.get_compiler_info()
    
    print("\n📦 Installed Compilers:")
    for name, details in info.items():
        if details['available']:
            status = "✅"
            version = details.get('version', 'Unknown version')
            if name == 'online':
                version = details.get('service', 'Online service')
        else:
            status = "❌"
            version = "Not installed"
        
        print(f"  {status} {name:12s} - {version}")
    
    print("\n" + "=" * 80)

if __name__ == '__main__':
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 15 + "AI CODE ANALYSIS & ENHANCED COMPILER DEMO" + " " * 22 + "║")
    print("╚" + "=" * 78 + "╝")
    
    # Show available compilers first
    demo_compiler_info()
    
    # Demo code analysis
    demo_code_analysis()
    
    # Demo enhanced compiler
    demo_enhanced_compiler()
    
    print("\n✨ Demo completed! Check ENHANCED_COMPILER_README.md for full documentation.\n")
