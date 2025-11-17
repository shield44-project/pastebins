#!/bin/bash
# Sample POST requests for Docker-based code execution API
# Usage: ./sample_api_requests.sh

BASE_URL="http://localhost:5000/api/execute"

echo "=========================================="
echo "Docker Code Execution API - Sample Requests"
echo "=========================================="
echo ""

echo "1. Python - Hello World"
echo "----------------------------------------"
curl -X POST $BASE_URL \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "print(\"Hello from Python!\")\nprint(\"2 + 2 =\", 2 + 2)"
  }' | python3 -m json.tool
echo -e "\n"

echo "2. C - Hello World"
echo "----------------------------------------"
curl -X POST $BASE_URL \
  -H "Content-Type: application/json" \
  -d '{
    "language": "c",
    "code": "#include <stdio.h>\nint main() {\n    printf(\"Hello from C!\\n\");\n    printf(\"2 + 2 = %d\\n\", 2 + 2);\n    return 0;\n}"
  }' | python3 -m json.tool
echo -e "\n"

echo "3. C++ - Hello World"
echo "----------------------------------------"
curl -X POST $BASE_URL \
  -H "Content-Type: application/json" \
  -d '{
    "language": "cpp",
    "code": "#include <iostream>\nint main() {\n    std::cout << \"Hello from C++!\" << std::endl;\n    std::cout << \"2 + 2 = \" << 2 + 2 << std::endl;\n    return 0;\n}"
  }' | python3 -m json.tool
echo -e "\n"

echo "4. C - With Input"
echo "----------------------------------------"
curl -X POST $BASE_URL \
  -H "Content-Type: application/json" \
  -d '{
    "language": "c",
    "code": "#include <stdio.h>\nint main() {\n    int a, b;\n    scanf(\"%d %d\", &a, &b);\n    printf(\"Sum: %d\\n\", a + b);\n    return 0;\n}",
    "input": "5 10"
  }' | python3 -m json.tool
echo -e "\n"

echo "5. Python - With Input"
echo "----------------------------------------"
curl -X POST $BASE_URL \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "name = input()\nprint(f\"Hello, {name}!\")",
    "input": "Alice"
  }' | python3 -m json.tool
echo -e "\n"

echo "6. C - Compilation Error"
echo "----------------------------------------"
curl -X POST $BASE_URL \
  -H "Content-Type: application/json" \
  -d '{
    "language": "c",
    "code": "#include <stdio.h>\nint main() {\n    printf(\"Missing semicolon\")\n    return 0;\n}"
  }' | python3 -m json.tool
echo -e "\n"

echo "7. Python - Runtime Error"
echo "----------------------------------------"
curl -X POST $BASE_URL \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "x = 1 / 0"
  }' | python3 -m json.tool
echo -e "\n"

echo "8. C - Loop with Array"
echo "----------------------------------------"
curl -X POST $BASE_URL \
  -H "Content-Type: application/json" \
  -d '{
    "language": "c",
    "code": "#include <stdio.h>\nint main() {\n    int arr[5] = {1, 2, 3, 4, 5};\n    int sum = 0;\n    for(int i = 0; i < 5; i++) {\n        sum += arr[i];\n    }\n    printf(\"Sum of array: %d\\n\", sum);\n    return 0;\n}"
  }' | python3 -m json.tool
echo -e "\n"

echo "9. C++ - Vector and STL"
echo "----------------------------------------"
curl -X POST $BASE_URL \
  -H "Content-Type: application/json" \
  -d '{
    "language": "cpp",
    "code": "#include <iostream>\n#include <vector>\nint main() {\n    std::vector<int> nums = {1, 2, 3, 4, 5};\n    int sum = 0;\n    for(int n : nums) sum += n;\n    std::cout << \"Sum: \" << sum << std::endl;\n    return 0;\n}"
  }' | python3 -m json.tool
echo -e "\n"

echo "10. Python - File Operations (in sandbox)"
echo "----------------------------------------"
curl -X POST $BASE_URL \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "# File operations are isolated in Docker\nimport os\nprint(\"Current directory:\", os.getcwd())\nprint(\"Files:\", os.listdir())"
  }' | python3 -m json.tool
echo -e "\n"

echo "=========================================="
echo "All sample requests completed!"
echo "=========================================="
