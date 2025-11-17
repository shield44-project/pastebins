#!/usr/bin/env python3
"""
Test script for Docker-based secure code execution system.
Tests C, C++, and Python execution with various scenarios.
"""

import sys
import os
import json
import time


def test_docker_executor_module():
    """Test the Docker executor module directly."""
    print("=" * 70)
    print("Test: Docker Executor Module")
    print("=" * 70)
    
    from docker_executor import DockerExecutor, execute_code_docker
    
    print("\n1. Testing Docker executor initialization:")
    executor = DockerExecutor()
    print(f"   Docker available: {executor.is_available()}")
    
    if not executor.is_available():
        print("   ⚠️  Docker not available, skipping remaining tests")
        return False
    
    print("   ✓ Docker executor initialized successfully")
    
    print("\n2. Testing Python execution (Hello World):")
    python_code = """
print("Hello from Python!")
print("2 + 2 =", 2 + 2)
"""
    
    result = executor.execute('python', python_code)
    print(f"   Success: {result['success']}")
    print(f"   Output: {result['stdout'].strip()}")
    assert result['success'], "Python execution should succeed"
    assert "Hello from Python!" in result['stdout'], "Output should contain expected text"
    print("   ✓ Python execution successful")
    
    print("\n3. Testing C execution (Hello World):")
    c_code = """
#include <stdio.h>

int main() {
    printf("Hello from C!\\n");
    printf("2 + 2 = %d\\n", 2 + 2);
    return 0;
}
"""
    
    result = executor.execute('c', c_code)
    print(f"   Success: {result['success']}")
    print(f"   Output: {result['stdout'].strip()}")
    assert result['success'], "C execution should succeed"
    assert "Hello from C!" in result['stdout'], "Output should contain expected text"
    print("   ✓ C execution successful")
    
    print("\n4. Testing C++ execution (Hello World):")
    cpp_code = """
#include <iostream>

int main() {
    std::cout << "Hello from C++!" << std::endl;
    std::cout << "2 + 2 = " << 2 + 2 << std::endl;
    return 0;
}
"""
    
    result = executor.execute('cpp', cpp_code)
    print(f"   Success: {result['success']}")
    print(f"   Output: {result['stdout'].strip()}")
    assert result['success'], "C++ execution should succeed"
    assert "Hello from C++" in result['stdout'], "Output should contain expected text"
    print("   ✓ C++ execution successful")
    
    print("\n5. Testing C code with stdin input:")
    c_input_code = """
#include <stdio.h>

int main() {
    int a, b;
    scanf("%d %d", &a, &b);
    printf("Sum: %d\\n", a + b);
    return 0;
}
"""
    
    result = executor.execute('c', c_input_code, stdin_input="5 10")
    print(f"   Success: {result['success']}")
    print(f"   Output: {result['stdout'].strip()}")
    assert result['success'], "C code with input should succeed"
    assert "Sum: 15" in result['stdout'], "Sum should be correct"
    print("   ✓ C code with stdin input works")
    
    print("\n6. Testing Python code with stdin input:")
    python_input_code = """
name = input()
print(f"Hello, {name}!")
"""
    
    result = executor.execute('python', python_input_code, stdin_input="Alice")
    print(f"   Success: {result['success']}")
    print(f"   Output: {result['stdout'].strip()}")
    assert result['success'], "Python with input should succeed"
    assert "Hello, Alice!" in result['stdout'], "Output should contain greeting"
    print("   ✓ Python code with stdin input works")
    
    print("\n7. Testing C compilation error handling:")
    bad_c_code = """
#include <stdio.h>

int main() {
    printf("Missing semicolon")  // Syntax error
    return 0;
}
"""
    
    result = executor.execute('c', bad_c_code)
    print(f"   Success: {result['success']}")
    assert not result['success'], "Bad code should fail to compile"
    assert len(result['compile_errors']) > 0, "Should have compilation errors"
    print(f"   Compile errors: {result['compile_errors'][:100]}...")
    print("   ✓ C compilation errors handled correctly")
    
    print("\n8. Testing C++ compilation error handling:")
    bad_cpp_code = """
#include <iostream>

int main() {
    std::cout << "Missing semicolon"  // Syntax error
    return 0;
}
"""
    
    result = executor.execute('cpp', bad_cpp_code)
    print(f"   Success: {result['success']}")
    assert not result['success'], "Bad C++ code should fail"
    assert len(result['compile_errors']) > 0, "Should have compilation errors"
    print("   ✓ C++ compilation errors handled correctly")
    
    print("\n9. Testing Python runtime error handling:")
    bad_python_code = """
x = 1 / 0  # Division by zero
"""
    
    result = executor.execute('python', bad_python_code)
    print(f"   Success: {result['success']}")
    # Python execution succeeds but has stderr
    assert len(result['stderr']) > 0, "Should have runtime error in stderr"
    print(f"   Runtime error: {result['stderr'][:100]}...")
    print("   ✓ Python runtime errors captured correctly")
    
    print("\n10. Testing execution timeout (infinite loop):")
    infinite_loop_code = """
while True:
    pass
"""
    
    start_time = time.time()
    result = executor.execute('python', infinite_loop_code)
    elapsed = time.time() - start_time
    print(f"   Success: {result['success']}")
    print(f"   Elapsed time: {elapsed:.2f}s")
    # Python infinite loops may not respect ulimit CPU time in Docker,
    # but should at least respect wall-time timeout
    # Check that it didn't run forever (should timeout within reasonable time)
    assert elapsed < 10, "Should timeout within 10 seconds"
    print("   ✓ Timeout protection works (wall-time limit enforced)")
    
    print("\n✓ Test PASSED: Docker executor working correctly\n")
    return True


def test_api_endpoint():
    """Test the API endpoint (requires Flask app running)."""
    print("=" * 70)
    print("Test: API Endpoint (Manual)")
    print("=" * 70)
    
    print("\nTo test the API endpoint, start the Flask app and run:")
    print("\n  # Test Python execution:")
    print('  curl -X POST http://localhost:5000/api/execute \\')
    print('    -H "Content-Type: application/json" \\')
    print('    -d \'{"language": "python", "code": "print(\\"Hello!\\")"}\'')
    
    print("\n  # Test C execution:")
    print('  curl -X POST http://localhost:5000/api/execute \\')
    print('    -H "Content-Type: application/json" \\')
    print('    -d \'{"language": "c", "code": "#include <stdio.h>\\nint main() { printf(\\"Hello!\\\\n\\"); return 0; }"}\'')
    
    print("\n  # Test with input:")
    print('  curl -X POST http://localhost:5000/api/execute \\')
    print('    -H "Content-Type: application/json" \\')
    print('    -d \'{"language": "python", "code": "name = input(); print(f\\"Hello, {name}!\\")", "input": "Alice"}\'')
    
    print("\nThese examples are saved in test_docker_api_examples.sh\n")
    
    # Create a shell script with examples
    script_content = """#!/bin/bash
# Test script for Docker-based code execution API

echo "=== Testing Python execution ==="
curl -X POST http://localhost:5000/api/execute \\
  -H "Content-Type: application/json" \\
  -d '{"language": "python", "code": "print(\"Hello from Python!\")\\nprint(\"2 + 2 =\", 2 + 2)"}'

echo -e "\\n\\n=== Testing C execution ==="
curl -X POST http://localhost:5000/api/execute \\
  -H "Content-Type: application/json" \\
  -d '{"language": "c", "code": "#include <stdio.h>\\nint main() { printf(\"Hello from C!\\\\n\"); return 0; }"}'

echo -e "\\n\\n=== Testing C++ execution ==="
curl -X POST http://localhost:5000/api/execute \\
  -H "Content-Type: application/json" \\
  -d '{"language": "cpp", "code": "#include <iostream>\\nint main() { std::cout << \"Hello from C++!\" << std::endl; return 0; }"}'

echo -e "\\n\\n=== Testing Python with input ==="
curl -X POST http://localhost:5000/api/execute \\
  -H "Content-Type: application/json" \\
  -d '{"language": "python", "code": "name = input()\\nprint(f\"Hello, {name}!\")", "input": "Alice"}'

echo -e "\\n\\n=== Testing C with input ==="
curl -X POST http://localhost:5000/api/execute \\
  -H "Content-Type: application/json" \\
  -d '{"language": "c", "code": "#include <stdio.h>\\nint main() { int a, b; scanf(\"%d %d\", &a, &b); printf(\"Sum: %d\\\\n\", a + b); return 0; }", "input": "5 10"}'

echo -e "\\n\\n=== Testing compilation error ==="
curl -X POST http://localhost:5000/api/execute \\
  -H "Content-Type: application/json" \\
  -d '{"language": "c", "code": "#include <stdio.h>\\nint main() { printf(\"Missing semicolon\")  return 0; }"}'

echo -e "\\n\\nDone!"
"""
    
    with open('/tmp/test_docker_api_examples.sh', 'w') as f:
        f.write(script_content)
    os.chmod('/tmp/test_docker_api_examples.sh', 0o755)
    
    print(f"Script saved to: /tmp/test_docker_api_examples.sh")
    
    return True


def main():
    """Run all tests."""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "DOCKER CODE EXECUTION TESTS" + " " * 25 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    results = []
    
    try:
        results.append(("Docker Executor Module", test_docker_executor_module()))
        results.append(("API Endpoint Examples", test_api_endpoint()))
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
        print(f"{test_name:50s} {status}")
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
