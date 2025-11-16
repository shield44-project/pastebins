#!/usr/bin/env python3
"""
Test script to manually verify online compiler functionality.
This script attempts to use the online compiler API directly.
"""

import sys
import os

def test_wandbox_api():
    """Test Wandbox API directly to verify it's working."""
    print("=" * 70)
    print("Test: Direct Wandbox API Call")
    print("=" * 70)
    
    import urllib.request
    import json
    
    # Test C code
    print("\n1. Testing C code compilation with Wandbox API:")
    c_code = """
#include <stdio.h>
int main() {
    printf("Hello from C on Wandbox!\\n");
    return 0;
}
"""
    
    try:
        url = 'https://wandbox.org/api/compile.json'
        payload = {
            'compiler': 'gcc-head',
            'code': c_code,
            'stdin': '',
            'options': '',
            'compiler-option-raw': '-O2 -Wall',
            'runtime-option-raw': '',
            'save': False
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"   API Response Keys: {list(result.keys())}")
            
            if 'program_output' in result:
                print(f"   ✓ C Code Output: {result['program_output']}")
            else:
                print(f"   ✗ No program output")
            
            if 'compiler_error' in result and result['compiler_error']:
                print(f"   Compiler Error: {result['compiler_error']}")
                
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        print(f"   Note: This is expected if network access is restricted or Wandbox is down")
    
    # Test C++ code
    print("\n2. Testing C++ code compilation with Wandbox API:")
    cpp_code = """
#include <iostream>
int main() {
    std::cout << "Hello from C++ on Wandbox!" << std::endl;
    return 0;
}
"""
    
    try:
        payload = {
            'compiler': 'gcc-head',
            'code': cpp_code,
            'stdin': '',
            'options': '',
            'compiler-option-raw': '-O2 -Wall -std=c++17',
            'runtime-option-raw': '',
            'save': False
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"   API Response Keys: {list(result.keys())}")
            
            if 'program_output' in result:
                print(f"   ✓ C++ Code Output: {result['program_output']}")
            else:
                print(f"   ✗ No program output")
                
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        print(f"   Note: This is expected if network access is restricted or Wandbox is down")
    
    # Test Java code
    print("\n3. Testing Java code compilation with Wandbox API:")
    java_code = """
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello from Java on Wandbox!");
    }
}
"""
    
    try:
        payload = {
            'compiler': 'openjdk-head',
            'code': java_code,
            'stdin': '',
            'options': '',
            'compiler-option-raw': '',
            'runtime-option-raw': '',
            'save': False
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"   API Response Keys: {list(result.keys())}")
            
            if 'program_output' in result:
                print(f"   ✓ Java Code Output: {result['program_output']}")
            else:
                print(f"   ✗ No program output")
                
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        print(f"   Note: This is expected if network access is restricted or Wandbox is down")
    
    print("\n")

def test_app_online_functions():
    """Test the app's online compiler functions."""
    print("=" * 70)
    print("Test: App Online Compiler Functions")
    print("=" * 70)
    
    from app import execute_c_code_online, execute_cpp_code_online, execute_java_code_online
    
    # Test C
    print("\n1. Testing execute_c_code_online:")
    c_code = """
#include <stdio.h>
int main() {
    printf("C test successful\\n");
    return 0;
}
"""
    result = execute_c_code_online(c_code, '')
    print(f"   Result (first 150 chars): {result[:150]}")
    
    # Test C++
    print("\n2. Testing execute_cpp_code_online:")
    cpp_code = """
#include <iostream>
int main() {
    std::cout << "C++ test successful" << std::endl;
    return 0;
}
"""
    result = execute_cpp_code_online(cpp_code, '')
    print(f"   Result (first 150 chars): {result[:150]}")
    
    # Test Java
    print("\n3. Testing execute_java_code_online:")
    java_code = """
public class Main {
    public static void main(String[] args) {
        System.out.println("Java test successful");
    }
}
"""
    result = execute_java_code_online(java_code, '')
    print(f"   Result (first 150 chars): {result[:150]}")
    
    print("\n")

def main():
    """Run all tests."""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 12 + "MANUAL ONLINE COMPILER VERIFICATION" + " " * 21 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    test_wandbox_api()
    test_app_online_functions()
    
    print("=" * 70)
    print("Manual verification complete.")
    print("If network access is available, you should see successful outputs above.")
    print("If not, you'll see error messages indicating network issues.")
    print("=" * 70)
    print()

if __name__ == '__main__':
    sys.exit(main())
