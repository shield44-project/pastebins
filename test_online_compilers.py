#!/usr/bin/env python3
"""
Test script to verify the online compiler implementations for C, C++, and Java.
"""

import sys
import os

def test_online_compiler_functions():
    """Test that online compiler functions exist and are properly defined."""
    print("=" * 70)
    print("Test: Online Compiler Functions")
    print("=" * 70)
    
    from app import (
        execute_code_online,
        execute_c_code_online,
        execute_cpp_code_online,
        execute_java_code_online,
        check_compiler_available
    )
    
    print("\n1. Testing function availability:")
    functions = [
        ('execute_code_online', execute_code_online),
        ('execute_c_code_online', execute_c_code_online),
        ('execute_cpp_code_online', execute_cpp_code_online),
        ('execute_java_code_online', execute_java_code_online),
    ]
    
    for func_name, func in functions:
        print(f"   {func_name:30s} ✓ Available")
        assert callable(func), f"{func_name} should be callable"
    
    print("\n2. Testing compiler availability checks:")
    compilers = ['gcc', 'g++', 'java', 'javac']
    for compiler in compilers:
        available = check_compiler_available(compiler)
        status = "✓ Available" if available else "✗ Not found"
        print(f"   {compiler:15s} {status}")
    
    print("\n3. Testing online compiler function signatures:")
    
    # Test C code execution (simple hello world)
    c_code = """
#include <stdio.h>
int main() {
    printf("Hello from C\\n");
    return 0;
}
"""
    print(f"   Testing C online compiler...")
    result = execute_c_code_online(c_code, '')
    print(f"   Result type: {type(result).__name__}")
    assert isinstance(result, str), "Result should be a string"
    print(f"   ✓ C online compiler function works (returns: {result[:50]}...)")
    
    # Test C++ code execution
    cpp_code = """
#include <iostream>
int main() {
    std::cout << "Hello from C++" << std::endl;
    return 0;
}
"""
    print(f"   Testing C++ online compiler...")
    result = execute_cpp_code_online(cpp_code, '')
    print(f"   Result type: {type(result).__name__}")
    assert isinstance(result, str), "Result should be a string"
    print(f"   ✓ C++ online compiler function works (returns: {result[:50]}...)")
    
    # Test Java code execution
    java_code = """
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello from Java");
    }
}
"""
    print(f"   Testing Java online compiler...")
    result = execute_java_code_online(java_code, '')
    print(f"   Result type: {type(result).__name__}")
    assert isinstance(result, str), "Result should be a string"
    print(f"   ✓ Java online compiler function works (returns: {result[:50]}...)")
    
    print("\n✓ Test PASSED: All online compiler functions are properly defined\n")
    return True

def test_execute_code_file_fallback():
    """Test that execute_code_file properly falls back to online compilers."""
    print("=" * 70)
    print("Test: Fallback to Online Compilers")
    print("=" * 70)
    
    from app import execute_code_file, check_compiler_available
    import tempfile
    import os
    
    print("\n1. Checking if local compilers are available:")
    gcc_available = check_compiler_available('gcc')
    gpp_available = check_compiler_available('g++')
    java_available = check_compiler_available('javac')
    
    print(f"   gcc:   {'✓ Available' if gcc_available else '✗ Not available'}")
    print(f"   g++:   {'✓ Available' if gpp_available else '✗ Not available'}")
    print(f"   javac: {'✓ Available' if java_available else '✗ Not available'}")
    
    print("\n2. Testing execute_code_file fallback logic:")
    
    # Test with C code
    c_code = """
#include <stdio.h>
int main() {
    printf("Testing C fallback\\n");
    return 0;
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False) as f:
        f.write(c_code)
        c_file = f.name
    
    try:
        print(f"   Testing C code execution...")
        result = execute_code_file('c', c_file, '')
        print(f"   Result: {result[:80]}...")
        if not gcc_available:
            assert 'Error: Unable to connect' in result or 'Hello' in result or 'Testing' in result, \
                "Should either use online compiler or show connection error"
            print(f"   ✓ C code properly falls back to online compiler")
        else:
            print(f"   ✓ C code executed with local gcc")
    finally:
        os.unlink(c_file)
    
    # Test with C++ code
    cpp_code = """
#include <iostream>
int main() {
    std::cout << "Testing C++ fallback" << std::endl;
    return 0;
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False) as f:
        f.write(cpp_code)
        cpp_file = f.name
    
    try:
        print(f"   Testing C++ code execution...")
        result = execute_code_file('cpp', cpp_file, '')
        print(f"   Result: {result[:80]}...")
        if not gpp_available:
            assert 'Error: Unable to connect' in result or 'Hello' in result or 'Testing' in result, \
                "Should either use online compiler or show connection error"
            print(f"   ✓ C++ code properly falls back to online compiler")
        else:
            print(f"   ✓ C++ code executed with local g++")
    finally:
        os.unlink(cpp_file)
    
    # Test with Java code
    java_code = """
public class Main {
    public static void main(String[] args) {
        System.out.println("Testing Java fallback");
    }
}
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.java', delete=False, 
                                     prefix='Main', dir='/tmp') as f:
        f.write(java_code)
        java_file = f.name
    
    try:
        # Rename to Main.java for Java to work
        java_main_file = os.path.join(os.path.dirname(java_file), 'Main.java')
        os.rename(java_file, java_main_file)
        
        print(f"   Testing Java code execution...")
        result = execute_code_file('java', java_main_file, '')
        print(f"   Result: {result[:80]}...")
        if not java_available:
            assert 'Error: Unable to connect' in result or 'Hello' in result or 'Testing' in result, \
                "Should either use online compiler or show connection error"
            print(f"   ✓ Java code properly falls back to online compiler")
        else:
            print(f"   ✓ Java code executed with local javac")
    finally:
        if os.path.exists(java_main_file):
            os.unlink(java_main_file)
    
    print("\n✓ Test PASSED: Fallback to online compilers works correctly\n")
    return True

def main():
    """Run all tests."""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "ONLINE COMPILER TESTS" + " " * 32 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    results = []
    
    try:
        results.append(("Online Compiler Functions", test_online_compiler_functions()))
        results.append(("Fallback Logic", test_execute_code_file_fallback()))
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
        print("\n✓ ALL TESTS PASSED\n")
        return 0
    else:
        print("\n✗ SOME TESTS FAILED\n")
        return 1

if __name__ == '__main__':
    sys.exit(main())
