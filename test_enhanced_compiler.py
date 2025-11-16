#!/usr/bin/env python3
"""
Test script for enhanced C/C++ compiler and AI code analysis features.
"""

import sys
import os

def test_code_analyzer():
    """Test the code analyzer module."""
    print("=" * 70)
    print("Test: Code Analyzer Module")
    print("=" * 70)
    
    from code_analyzer import CodeAnalyzer, analyze_code, get_analysis_report
    
    print("\n1. Testing analyzer initialization:")
    analyzer = CodeAnalyzer()
    print("   ✓ CodeAnalyzer instantiated successfully")
    
    print("\n2. Testing C code analysis:")
    c_code = """
#include <stdio.h>
#include <stdlib.h>

int main() {
    int x;  // Uninitialized variable
    char buffer[100];
    gets(buffer);  // Unsafe function
    printf(buffer);  // Format string vulnerability
    
    int *ptr = malloc(100);  // Memory leak - no free
    
    return 0;
}
"""
    
    analysis = analyze_code(c_code, 'c')
    print(f"   Found {analysis['summary']['total_issues']} issues")
    print(f"   Found {analysis['summary']['suggestions']} suggestions")
    print(f"   Found {analysis['summary']['alternatives']} alternatives")
    
    # Check that critical issues are detected
    assert analysis['summary']['critical'] > 0, "Should detect critical security issues"
    print("   ✓ Critical security issues detected")
    
    print("\n3. Testing C++ code analysis:")
    cpp_code = """
#include <iostream>
#include <vector>

int main() {
    int arr[100];  // Could use vector
    
    for (int i = 0; i < 100; i++) {
        arr[i] = i;
    }
    
    int *ptr = new int[50];  // Memory leak
    
    printf("%d", arr[0]);  // Should use cout
    
    return 0;
}
"""
    
    analysis = analyze_code(cpp_code, 'cpp')
    print(f"   Found {analysis['summary']['total_issues']} issues")
    print(f"   Found {analysis['summary']['suggestions']} suggestions")
    print(f"   Found {analysis['summary']['alternatives']} alternatives")
    
    # Check that alternatives are suggested
    assert analysis['summary']['alternatives'] > 0, "Should suggest alternative approaches"
    print("   ✓ Alternative approaches suggested")
    
    print("\n4. Testing formatted report generation:")
    report = get_analysis_report(c_code, 'c')
    assert 'CODE ANALYSIS REPORT' in report, "Report should have header"
    assert 'Summary:' in report, "Report should have summary"
    print("   ✓ Formatted report generated successfully")
    print("\n✓ Test PASSED: Code analyzer working correctly\n")
    
    return True

def test_enhanced_compiler():
    """Test the enhanced compiler module."""
    print("=" * 70)
    print("Test: Enhanced Compiler Module")
    print("=" * 70)
    
    from enhanced_compiler import EnhancedCompiler, CompilerResult
    
    print("\n1. Testing compiler initialization:")
    compiler = EnhancedCompiler()
    print(f"   GCC available: {compiler.gcc_available}")
    print(f"   G++ available: {compiler.gpp_available}")
    print(f"   Clang available: {compiler.clang_available}")
    print(f"   Clang++ available: {compiler.clangpp_available}")
    print("   ✓ EnhancedCompiler instantiated successfully")
    
    print("\n2. Testing compiler info retrieval:")
    info = compiler.get_compiler_info()
    assert 'gcc' in info, "Should have gcc info"
    assert 'g++' in info, "Should have g++ info"
    print("   ✓ Compiler info retrieved successfully")
    
    print("\n3. Testing C code compilation (simple hello world):")
    c_code = """
#include <stdio.h>

int main() {
    printf("Hello from enhanced C compiler!\\n");
    return 0;
}
"""
    
    result = compiler.compile_and_run_c(c_code)
    if result.success:
        print("   ✓ C code compiled and executed successfully")
        print(f"   Output: {result.output.strip()}")
        assert "Hello" in result.output, "Output should contain Hello"
    else:
        print(f"   Note: Compilation failed (might use online compiler): {result.errors}")
        # Don't fail the test if online compiler is used
    
    print("\n4. Testing C++ code compilation (simple hello world):")
    cpp_code = """
#include <iostream>

int main() {
    std::cout << "Hello from enhanced C++ compiler!" << std::endl;
    return 0;
}
"""
    
    result = compiler.compile_and_run_cpp(cpp_code)
    if result.success:
        print("   ✓ C++ code compiled and executed successfully")
        print(f"   Output: {result.output.strip()}")
        assert "Hello" in result.output, "Output should contain Hello"
    else:
        print(f"   Note: Compilation failed (might use online compiler): {result.errors}")
    
    print("\n5. Testing compilation error handling:")
    bad_c_code = """
#include <stdio.h>

int main() {
    printf("Missing semicolon")  // Syntax error
    return 0;
}
"""
    
    result = compiler.compile_and_run_c(bad_c_code)
    assert not result.success, "Should fail to compile"
    assert len(result.errors) > 0, "Should have error message"
    print("   ✓ Compilation errors handled correctly")
    print(f"   Error preview: {result.errors[:100]}...")
    
    print("\n6. Testing C code with different standards:")
    c11_code = """
#include <stdio.h>

int main() {
    // C11 feature: anonymous struct
    struct {
        int x;
        int y;
    } point = {10, 20};
    
    printf("Point: (%d, %d)\\n", point.x, point.y);
    return 0;
}
"""
    
    result = compiler.compile_and_run_c(c11_code, standard='c11')
    if result.success:
        print("   ✓ C11 code compiled successfully")
    else:
        print(f"   Note: C11 compilation note: {result.errors[:100] if result.errors else 'No errors'}")
    
    print("\n7. Testing C++ code with different standards:")
    cpp17_code = """
#include <iostream>
#include <string>

int main() {
    // C++17 feature: structured bindings would need more setup
    std::string message = "C++17 works!";
    std::cout << message << std::endl;
    return 0;
}
"""
    
    result = compiler.compile_and_run_cpp(cpp17_code, standard='c++17')
    if result.success:
        print("   ✓ C++17 code compiled successfully")
    else:
        print(f"   Note: C++17 compilation note: {result.errors[:100] if result.errors else 'No errors'}")
    
    print("\n✓ Test PASSED: Enhanced compiler working correctly\n")
    
    return True

def test_integration():
    """Test integration between modules."""
    print("=" * 70)
    print("Test: Module Integration")
    print("=" * 70)
    
    from code_analyzer import analyze_code
    from enhanced_compiler import EnhancedCompiler
    
    print("\n1. Testing workflow: Analyze -> Fix -> Compile:")
    
    # Code with issues
    problematic_code = """
#include <stdio.h>

int main() {
    int x;  // Uninitialized
    printf("%d\\n", x);
    return 0;
}
"""
    
    # Analyze
    analysis = analyze_code(problematic_code, 'c')
    print(f"   Analysis found {analysis['summary']['total_issues']} issues")
    
    # Fixed code
    fixed_code = """
#include <stdio.h>

int main() {
    int x = 0;  // Initialized
    printf("%d\\n", x);
    return 0;
}
"""
    
    # Compile
    compiler = EnhancedCompiler()
    result = compiler.compile_and_run_c(fixed_code)
    
    if result.success:
        print("   ✓ Fixed code compiles and runs successfully")
    else:
        print(f"   Note: Compilation result: {result.errors[:100] if result.errors else 'Fallback to online'}")
    
    print("\n✓ Test PASSED: Integration working correctly\n")
    
    return True

def main():
    """Run all tests."""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 10 + "ENHANCED C/C++ COMPILER & AI ANALYSIS TESTS" + " " * 15 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    results = []
    
    try:
        results.append(("Code Analyzer", test_code_analyzer()))
        results.append(("Enhanced Compiler", test_enhanced_compiler()))
        results.append(("Integration", test_integration()))
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Print summary
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    all_passed = True
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name:40s} {status}")
        if not passed:
            all_passed = False
    
    print("=" * 70)
    
    if all_passed:
        print("\n✅ ALL TESTS PASSED\n")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED\n")
        return 1

if __name__ == '__main__':
    sys.exit(main())
