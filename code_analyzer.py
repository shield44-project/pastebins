"""
AI-Powered Code Analysis Module for C/C++ Code
Provides static analysis, suggestions, and best practices for C and C++ code.
"""

import re
import json
from typing import Dict, List, Tuple, Optional


class CodeAnalyzer:
    """
    Analyzes C/C++ code and provides suggestions for improvements,
    potential issues, and alternative implementations.
    """
    
    def __init__(self):
        self.issues = []
        self.suggestions = []
        self.alternatives = []
    
    def analyze(self, code: str, language: str) -> Dict:
        """
        Main analysis method that runs all checks on the code.
        
        Args:
            code: The source code to analyze
            language: Either 'c' or 'cpp'
        
        Returns:
            Dictionary containing issues, suggestions, and alternatives
        """
        self.issues = []
        self.suggestions = []
        self.alternatives = []
        
        # Run various analysis checks
        self._check_common_errors(code, language)
        self._check_memory_issues(code, language)
        self._check_best_practices(code, language)
        self._check_security_vulnerabilities(code, language)
        self._suggest_optimizations(code, language)
        self._suggest_alternatives(code, language)
        
        # Generate practice problems and complete code examples
        practice_problems = self._generate_practice_problems(code, language)
        
        return {
            'issues': self.issues,
            'suggestions': self.suggestions,
            'alternatives': self.alternatives,
            'practice_problems': practice_problems,
            'summary': self._generate_summary()
        }
    
    def _check_common_errors(self, code: str, language: str):
        """Check for common syntax and logical errors."""
        
        # Check for missing semicolons (basic check)
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Skip empty lines, comments, and preprocessor directives
            if not stripped or stripped.startswith('//') or stripped.startswith('#') or stripped.startswith('/*'):
                continue
            
            # Check if line should end with semicolon
            if stripped and not stripped.endswith((';', '{', '}', ':', ',')):
                # Check for statements that typically need semicolons
                if any(keyword in stripped for keyword in ['int ', 'char ', 'float ', 'double ', 'return ', 'printf', 'cout', 'scanf', 'cin']):
                    if '{' not in stripped and '}' not in stripped:
                        self.issues.append({
                            'line': i,
                            'severity': 'warning',
                            'type': 'syntax',
                            'message': 'Possible missing semicolon',
                            'suggestion': f'Add semicolon at end of line: {stripped};'
                        })
        
        # Check for assignment in condition (common mistake)
        if re.search(r'if\s*\([^=!<>]*=[^=]', code):
            self.issues.append({
                'severity': 'warning',
                'type': 'logic',
                'message': 'Possible assignment in if condition',
                'suggestion': 'Use == for comparison instead of = for assignment'
            })
        
        # Check for uninitialized variables (basic)
        var_declarations = re.findall(r'(int|char|float|double)\s+(\w+)\s*;', code)
        for var_type, var_name in var_declarations:
            self.suggestions.append({
                'type': 'best_practice',
                'message': f'Variable "{var_name}" declared but not initialized',
                'suggestion': f'Initialize variable: {var_type} {var_name} = 0;'
            })
    
    def _check_memory_issues(self, code: str, language: str):
        """Check for potential memory-related issues."""
        
        # Check for malloc without free (C)
        if language == 'c':
            if 'malloc(' in code and 'free(' not in code:
                self.issues.append({
                    'severity': 'error',
                    'type': 'memory_leak',
                    'message': 'Memory allocated with malloc() but never freed',
                    'suggestion': 'Always free dynamically allocated memory with free() to prevent memory leaks'
                })
        
        # Check for new without delete (C++)
        if language == 'cpp':
            new_count = len(re.findall(r'\bnew\s+', code))
            delete_count = len(re.findall(r'\bdelete\s+', code))
            
            if new_count > delete_count:
                self.issues.append({
                    'severity': 'error',
                    'type': 'memory_leak',
                    'message': f'Found {new_count} new but only {delete_count} delete statements',
                    'suggestion': 'Consider using smart pointers (std::unique_ptr, std::shared_ptr) or ensure all new has matching delete'
                })
        
        # Check for buffer overflow risks
        if 'gets(' in code:
            self.issues.append({
                'severity': 'critical',
                'type': 'security',
                'message': 'Use of unsafe gets() function',
                'suggestion': 'Replace gets() with fgets() which is safer and prevents buffer overflows'
            })
        
        if 'strcpy(' in code:
            self.suggestions.append({
                'type': 'security',
                'message': 'strcpy() can cause buffer overflows',
                'suggestion': 'Consider using strncpy() or safer alternatives like snprintf()'
            })
    
    def _check_best_practices(self, code: str, language: str):
        """Check for best practices and coding standards."""
        
        # Check for magic numbers
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            # Skip includes and comments
            if line.strip().startswith('#') or line.strip().startswith('//'):
                continue
            
            # Find numeric literals (excluding 0, 1, common values)
            numbers = re.findall(r'\b(\d{2,})\b', line)
            for num in numbers:
                if int(num) > 10:  # Only flag larger magic numbers
                    self.suggestions.append({
                        'line': i,
                        'type': 'code_quality',
                        'message': f'Magic number {num} found',
                        'suggestion': f'Consider defining {num} as a constant with meaningful name'
                    })
        
        # Check for proper include guards (C/C++ headers)
        if re.search(r'\.(h|hpp)$', code) or '#ifndef' in code:
            if '#ifndef' in code and '#define' in code and '#endif' in code:
                pass  # Has include guards
            else:
                self.suggestions.append({
                    'type': 'best_practice',
                    'message': 'Missing or incomplete include guards',
                    'suggestion': 'Add include guards: #ifndef HEADER_H, #define HEADER_H, ... #endif'
                })
        
        # Check for proper error handling
        if 'fopen(' in code and 'fclose(' not in code:
            self.suggestions.append({
                'type': 'best_practice',
                'message': 'File opened but not explicitly closed',
                'suggestion': 'Always close files with fclose() after use'
            })
        
        # Suggest const for read-only parameters
        if language == 'cpp':
            if re.search(r'void\s+\w+\s*\([^)]*\bstring\b', code):
                self.suggestions.append({
                    'type': 'optimization',
                    'message': 'String parameter passed by value',
                    'suggestion': 'Pass strings by const reference for better performance: const string&'
                })
    
    def _check_security_vulnerabilities(self, code: str, language: str):
        """Check for potential security vulnerabilities."""
        
        # Check for format string vulnerabilities
        if re.search(r'printf\s*\(\s*\w+\s*\)', code):
            self.issues.append({
                'severity': 'critical',
                'type': 'security',
                'message': 'Potential format string vulnerability',
                'suggestion': 'Use printf("%s", variable) instead of printf(variable)'
            })
        
        # Check for unsafe scanf usage
        if 'scanf("%s"' in code or 'scanf(\"%s\"' in code:
            self.issues.append({
                'severity': 'error',
                'type': 'security',
                'message': 'Unsafe scanf usage can cause buffer overflow',
                'suggestion': 'Specify maximum field width in format: scanf("%99s", buffer) for char buffer[100]'
            })
        
        # Check for system() call
        if 'system(' in code:
            self.issues.append({
                'severity': 'warning',
                'type': 'security',
                'message': 'Use of system() can be dangerous',
                'suggestion': 'Avoid system() calls or carefully validate all inputs to prevent command injection'
            })
    
    def _suggest_optimizations(self, code: str, language: str):
        """Suggest performance optimizations."""
        
        if language == 'cpp':
            # Suggest using emplace_back instead of push_back
            if 'push_back(' in code:
                self.suggestions.append({
                    'type': 'optimization',
                    'message': 'Consider using emplace_back() instead of push_back()',
                    'suggestion': 'emplace_back() constructs objects in-place and can be more efficient'
                })
            
            # Suggest range-based for loops
            if re.search(r'for\s*\(\s*int\s+\w+\s*=\s*0', code):
                self.suggestions.append({
                    'type': 'modern_cpp',
                    'message': 'Consider using range-based for loop for containers',
                    'suggestion': 'Use: for (const auto& item : container) instead of indexed loops when possible'
                })
            
            # Suggest auto keyword
            if re.search(r'std::(vector|map|set|string)', code):
                self.suggestions.append({
                    'type': 'modern_cpp',
                    'message': 'Consider using auto keyword for complex types',
                    'suggestion': 'Use: auto var = std::vector<int>{...}; for cleaner code'
                })
        
        # Check for inefficient string concatenation in loops
        if re.search(r'for.*\n.*\+=.*"', code, re.MULTILINE):
            self.suggestions.append({
                'type': 'optimization',
                'message': 'String concatenation in loop can be inefficient',
                'suggestion': 'Consider using stringstream or reserve() for better performance'
            })
    
    def _suggest_alternatives(self, code: str, language: str):
        """Suggest alternative implementations or approaches."""
        
        # Arrays vs vectors
        if language == 'cpp' and re.search(r'\w+\s*\[\s*\d+\s*\]', code):
            self.alternatives.append({
                'approach': 'Use std::vector instead of raw arrays',
                'benefit': 'Automatic memory management, bounds checking, and better safety',
                'example': 'std::vector<int> arr(size); instead of int arr[size];',
                'recommended_code': self._generate_vector_refactor(code)
            })
        
        # printf vs cout
        if language == 'cpp' and 'printf(' in code:
            self.alternatives.append({
                'approach': 'Use std::cout instead of printf()',
                'benefit': 'Type-safe, no format specifiers needed, better C++ integration',
                'example': 'std::cout << value << std::endl; instead of printf("%d", value);',
                'recommended_code': self._refactor_printf_to_cout(code)
            })
        
        # scanf vs cin
        if language == 'cpp' and 'scanf(' in code:
            self.alternatives.append({
                'approach': 'Use std::cin instead of scanf()',
                'benefit': 'Type-safe input, no format specifiers needed, better error handling',
                'example': 'std::cin >> value; instead of scanf("%d", &value);',
                'recommended_code': self._refactor_scanf_to_cin(code)
            })
        
        # Manual memory management
        if language == 'cpp' and ('malloc(' in code or 'new ' in code):
            self.alternatives.append({
                'approach': 'Use smart pointers (C++11 and later)',
                'benefit': 'Automatic memory management, exception safety, no manual delete needed',
                'example': 'std::unique_ptr<Type> ptr = std::make_unique<Type>(); instead of Type* ptr = new Type();',
                'recommended_code': self._refactor_to_smart_pointers(code)
            })
        
        # C-style casts
        if language == 'cpp' and re.search(r'\([a-zA-Z_]\w*\s*\*?\s*\)', code):
            self.alternatives.append({
                'approach': 'Use C++ style casts',
                'benefit': 'More explicit, searchable, compile-time checking',
                'example': 'static_cast<int>(value) instead of (int)value',
                'recommended_code': self._convert_to_cpp_casts(code)
            })
        
        # gets() to fgets()
        if 'gets(' in code:
            self.alternatives.append({
                'approach': 'Replace unsafe gets() with fgets()',
                'benefit': 'Prevents buffer overflow vulnerabilities',
                'example': 'fgets(buffer, sizeof(buffer), stdin); instead of gets(buffer);',
                'recommended_code': self._refactor_gets_to_fgets(code)
            })
        
        # strcpy to strncpy
        if 'strcpy(' in code:
            self.alternatives.append({
                'approach': 'Replace strcpy() with strncpy() or safer alternatives',
                'benefit': 'Prevents buffer overflow by limiting copy length',
                'example': 'strncpy(dest, src, sizeof(dest)-1); dest[sizeof(dest)-1] = \'\\0\';',
                'recommended_code': self._refactor_strcpy_to_strncpy(code)
            })
        
        # Generate comprehensive refactored version combining all fixes
        if self.issues or self.suggestions:
            refactored = self._generate_full_refactored_code(code, language)
            if refactored != code:  # Only add if changes were made
                self.alternatives.append({
                    'approach': '🎯 Complete Refactored Version (All Improvements Applied)',
                    'benefit': 'Incorporates all security fixes, best practices, and modern features',
                    'example': 'See the complete refactored code below',
                    'recommended_code': refactored
                })
    
    def _generate_vector_example(self, code: str) -> str:
        """Generate example using std::vector instead of raw arrays."""
        # Find array declarations and suggest vector version
        array_pattern = r'(\w+)\s+(\w+)\s*\[\s*(\d+)\s*\]'
        matches = re.findall(array_pattern, code)
        if matches:
            type_name, var_name, size = matches[0]
            return f"// Instead of: {type_name} {var_name}[{size}];\n// Use:\n#include <vector>\nstd::vector<{type_name}> {var_name}({size});"
        return "std::vector<int> arr(10); // Example with size 10"
    
    def _convert_printf_to_cout(self, code: str) -> str:
        """Convert simple printf statements to cout."""
        # Handle common printf patterns
        examples = []
        if 'printf("%d' in code:
            examples.append('// Instead of: printf("%d", value);\n// Use:\nstd::cout << value << std::endl;')
        if 'printf("%s' in code:
            examples.append('// Instead of: printf("%s", str);\n// Use:\nstd::cout << str << std::endl;')
        if 'printf("%f' in code:
            examples.append('// Instead of: printf("%f", num);\n// Use:\nstd::cout << num << std::endl;')
        
        if examples:
            return '\n\n'.join(examples)
        return '// Include <iostream>\n#include <iostream>\nstd::cout << "Hello, World!" << std::endl;'
    
    def _convert_scanf_to_cin(self, code: str) -> str:
        """Convert scanf statements to cin."""
        examples = []
        if 'scanf("%d' in code:
            examples.append('// Instead of: scanf("%d", &value);\n// Use:\nstd::cin >> value;')
        if 'scanf("%s' in code:
            examples.append('// Instead of: scanf("%s", str);\n// Use:\n// For C-style strings:\nchar str[100];\nstd::cin >> str;\n// Or better, use std::string:\nstd::string str;\nstd::cin >> str;')
        if 'scanf("%f' in code:
            examples.append('// Instead of: scanf("%f", &num);\n// Use:\nstd::cin >> num;')
        
        if examples:
            return '\n\n'.join(examples)
        return '// Include <iostream>\n#include <iostream>\nint value;\nstd::cin >> value;'
    
    def _convert_to_smart_pointers(self, code: str) -> str:
        """Convert raw pointers to smart pointers."""
        examples = []
        if 'new ' in code:
            examples.append('// Instead of: Type* ptr = new Type();\n// Use:\n#include <memory>\nauto ptr = std::make_unique<Type>();\n// Or for shared ownership:\nauto ptr = std::make_shared<Type>();')
        if 'malloc(' in code:
            examples.append('// Instead of: ptr = (Type*)malloc(sizeof(Type));\n// Use:\n#include <memory>\nauto ptr = std::make_unique<Type>();')
        
        if examples:
            return '\n\n'.join(examples)
        return '#include <memory>\nauto ptr = std::make_unique<int>(42);\n// No need to call delete!'
    
    def _convert_to_cpp_casts(self, code: str) -> str:
        """Convert C-style casts to C++ style casts."""
        return '''// Instead of: int x = (int)value;
// Use:
int x = static_cast<int>(value);

// For pointers:
// Instead of: Derived* d = (Derived*)base;
// Use:
Derived* d = dynamic_cast<Derived*>(base);

// For const removal (use with caution):
// const_cast<Type*>(ptr)

// For reinterpretation (use rarely):
// reinterpret_cast<NewType*>(ptr)'''
    
    def _convert_gets_to_fgets(self, code: str) -> str:
        """Convert gets() to fgets()."""
        return '''// Instead of: gets(buffer);
// Use:
char buffer[100];
if (fgets(buffer, sizeof(buffer), stdin) != NULL) {
    // Remove trailing newline if present
    buffer[strcspn(buffer, "\\n")] = '\\0';
    // Use buffer safely
}'''
    
    def _convert_strcpy_to_strncpy(self, code: str) -> str:
        """Convert strcpy() to strncpy()."""
        return '''// Instead of: strcpy(dest, src);
// Use:
strncpy(dest, src, sizeof(dest) - 1);
dest[sizeof(dest) - 1] = '\\0'; // Ensure null termination

// Or better, use C++ std::string:
#include <string>
std::string dest = src; // Automatic memory management'''
    
    def _generate_vector_refactor(self, code: str) -> str:
        """Generate full refactored code using std::vector instead of raw arrays."""
        refactored = code
        
        # Replace array declarations with vector
        array_pattern = r'(\w+)\s+(\w+)\s*\[\s*(\d+)\s*\]\s*;'
        matches = re.finditer(array_pattern, code)
        
        replacements = []
        for match in matches:
            type_name, var_name, size = match.groups()
            old_decl = match.group(0)
            new_decl = f'std::vector<{type_name}> {var_name}({size});'
            replacements.append((old_decl, new_decl))
        
        for old, new in replacements:
            refactored = refactored.replace(old, new)
        
        # Add include if not present
        if '<vector>' not in refactored and replacements:
            if '#include' in refactored:
                # Add after last include
                last_include = max([m.end() for m in re.finditer(r'#include.*\n', refactored)])
                refactored = refactored[:last_include] + '#include <vector>\n' + refactored[last_include:]
            else:
                refactored = '#include <vector>\n' + refactored
        
        return refactored if refactored != code else self._generate_vector_example(code)
    
    def _refactor_printf_to_cout(self, code: str) -> str:
        """Generate full refactored code replacing printf with cout."""
        refactored = code
        
        # Replace common printf patterns
        replacements = [
            (r'printf\s*\(\s*"([^"]*\\n)"\s*\)', r'std::cout << "\1"'),
            (r'printf\s*\(\s*"%d\\n"\s*,\s*([^)]+)\)', r'std::cout << \1 << std::endl'),
            (r'printf\s*\(\s*"%s\\n"\s*,\s*([^)]+)\)', r'std::cout << \1 << std::endl'),
            (r'printf\s*\(\s*"%f\\n"\s*,\s*([^)]+)\)', r'std::cout << \1 << std::endl'),
            (r'printf\s*\(\s*"%c\\n"\s*,\s*([^)]+)\)', r'std::cout << \1 << std::endl'),
        ]
        
        for pattern, replacement in replacements:
            refactored = re.sub(pattern, replacement, refactored)
        
        # Replace stdio.h with iostream
        refactored = refactored.replace('#include <stdio.h>', '#include <iostream>')
        
        # Add namespace std if needed
        if 'std::cout' in refactored and 'using namespace std' not in refactored:
            # Add after includes
            if '#include' in refactored:
                last_include = max([m.end() for m in re.finditer(r'#include.*\n', refactored)])
                refactored = refactored[:last_include] + '\nusing namespace std;\n' + refactored[last_include:]
        
        return refactored if refactored != code else self._convert_printf_to_cout(code)
    
    def _refactor_scanf_to_cin(self, code: str) -> str:
        """Generate full refactored code replacing scanf with cin."""
        refactored = code
        
        # Replace common scanf patterns
        replacements = [
            (r'scanf\s*\(\s*"%d"\s*,\s*&([^)]+)\)', r'std::cin >> \1'),
            (r'scanf\s*\(\s*"%s"\s*,\s*([^)]+)\)', r'std::cin >> \1'),
            (r'scanf\s*\(\s*"%f"\s*,\s*&([^)]+)\)', r'std::cin >> \1'),
            (r'scanf\s*\(\s*"%c"\s*,\s*&([^)]+)\)', r'std::cin >> \1'),
        ]
        
        for pattern, replacement in replacements:
            refactored = re.sub(pattern, replacement, refactored)
        
        # Replace stdio.h with iostream
        refactored = refactored.replace('#include <stdio.h>', '#include <iostream>')
        
        # Add namespace std if needed
        if 'std::cin' in refactored and 'using namespace std' not in refactored:
            if '#include' in refactored:
                last_include = max([m.end() for m in re.finditer(r'#include.*\n', refactored)])
                refactored = refactored[:last_include] + '\nusing namespace std;\n' + refactored[last_include:]
        
        return refactored if refactored != code else self._convert_scanf_to_cin(code)
    
    def _refactor_to_smart_pointers(self, code: str) -> str:
        """Generate full refactored code using smart pointers."""
        refactored = code
        
        # Replace new with make_unique
        new_pattern = r'(\w+)\s*\*\s*(\w+)\s*=\s*new\s+(\w+)(?:\[(\d+)\])?'
        matches = re.finditer(new_pattern, code)
        
        replacements = []
        for match in matches:
            type_name, var_name, alloc_type, array_size = match.groups()
            old_stmt = match.group(0)
            if array_size:
                # Array allocation - use vector instead
                new_stmt = f'std::vector<{type_name}> {var_name}({array_size})'
            else:
                # Single object allocation
                new_stmt = f'auto {var_name} = std::make_unique<{type_name}>()'
            replacements.append((old_stmt, new_stmt))
        
        for old, new in replacements:
            refactored = refactored.replace(old, new)
        
        # Remove delete statements
        refactored = re.sub(r'delete\s+\w+\s*;', '// delete not needed with smart pointers', refactored)
        refactored = re.sub(r'delete\[\]\s+\w+\s*;', '// delete[] not needed with smart pointers or vectors', refactored)
        
        # Add includes
        if 'std::make_unique' in refactored and '<memory>' not in refactored:
            if '#include' in refactored:
                last_include = max([m.end() for m in re.finditer(r'#include.*\n', refactored)])
                refactored = refactored[:last_include] + '#include <memory>\n' + refactored[last_include:]
            else:
                refactored = '#include <memory>\n' + refactored
        
        if 'std::vector' in refactored and '<vector>' not in refactored:
            if '#include' in refactored:
                last_include = max([m.end() for m in re.finditer(r'#include.*\n', refactored)])
                refactored = refactored[:last_include] + '#include <vector>\n' + refactored[last_include:]
            else:
                refactored = '#include <vector>\n' + refactored
        
        return refactored if refactored != code else self._convert_to_smart_pointers(code)
    
    def _refactor_gets_to_fgets(self, code: str) -> str:
        """Generate full refactored code replacing gets with fgets."""
        refactored = code
        
        # Find gets() calls
        gets_pattern = r'gets\s*\(\s*(\w+)\s*\)'
        matches = re.finditer(gets_pattern, code)
        
        for match in matches:
            buffer_name = match.group(1)
            old_stmt = match.group(0)
            # Assume buffer size of 100 if we can't determine it
            new_stmt = f'fgets({buffer_name}, sizeof({buffer_name}), stdin)'
            refactored = refactored.replace(old_stmt, new_stmt)
        
        # Add newline removal after fgets if needed
        if 'fgets(' in refactored and 'strcspn' not in refactored:
            # Add a comment about removing newline
            refactored = '// Note: Use buffer[strcspn(buffer, "\\n")] = 0; to remove trailing newline after fgets\n' + refactored
        
        return refactored if refactored != code else self._convert_gets_to_fgets(code)
    
    def _refactor_strcpy_to_strncpy(self, code: str) -> str:
        """Generate full refactored code replacing strcpy with strncpy."""
        refactored = code
        
        # Find strcpy calls
        strcpy_pattern = r'strcpy\s*\(\s*(\w+)\s*,\s*([^)]+)\)'
        matches = re.finditer(strcpy_pattern, code)
        
        for match in matches:
            dest, src = match.groups()
            old_stmt = match.group(0)
            new_stmt = f'strncpy({dest}, {src}, sizeof({dest}) - 1); {dest}[sizeof({dest}) - 1] = \'\\0\''
            refactored = refactored.replace(old_stmt, new_stmt)
        
        return refactored if refactored != code else self._convert_strcpy_to_strncpy(code)
    
    def _generate_full_refactored_code(self, code: str, language: str) -> str:
        """Generate a complete refactored version of the code with all improvements."""
        refactored = code
        
        # Apply all security fixes
        if 'gets(' in refactored:
            refactored = self._refactor_gets_to_fgets(refactored)
        
        if 'strcpy(' in refactored:
            refactored = self._refactor_strcpy_to_strncpy(refactored)
        
        # Apply C++ improvements
        if language == 'cpp':
            if 'printf(' in refactored:
                refactored = self._refactor_printf_to_cout(refactored)
            
            if 'scanf(' in refactored:
                refactored = self._refactor_scanf_to_cin(refactored)
            
            if 'new ' in refactored or 'malloc(' in refactored:
                refactored = self._refactor_to_smart_pointers(refactored)
            
            if re.search(r'\w+\s*\[\s*\d+\s*\]', refactored):
                refactored = self._generate_vector_refactor(refactored)
        
        # Initialize variables that were uninitialized
        var_declarations = re.findall(r'(int|char|float|double)\s+(\w+)\s*;', refactored)
        for var_type, var_name in var_declarations:
            old_decl = f'{var_type} {var_name};'
            new_decl = f'{var_type} {var_name} = 0;  // Initialized to prevent undefined behavior'
            refactored = refactored.replace(old_decl, new_decl, 1)  # Only replace first occurrence
        
        return refactored
    
    def _generate_summary(self) -> Dict:
        """Generate a summary of the analysis."""
        critical_count = sum(1 for i in self.issues if i.get('severity') == 'critical')
        error_count = sum(1 for i in self.issues if i.get('severity') == 'error')
        warning_count = sum(1 for i in self.issues if i.get('severity') == 'warning')
        
        return {
            'total_issues': len(self.issues),
            'critical': critical_count,
            'errors': error_count,
            'warnings': warning_count,
            'suggestions': len(self.suggestions),
            'alternatives': len(self.alternatives)
        }
    
    def _generate_practice_problems(self, code: str, language: str) -> List[Dict]:
        """
        Generate 5 similar practice problems based on the analyzed code.
        Each problem includes a complete working solution.
        """
        problems = []
        
        # Detect what the code is doing
        has_arrays = bool(re.search(r'\w+\s*\[\s*\d+\s*\]', code))
        has_loops = 'for' in code or 'while' in code
        has_input = 'scanf' in code or 'cin' in code or 'input' in code
        has_output = 'printf' in code or 'cout' in code or 'print' in code
        has_pointers = '*' in code and language in ['c', 'cpp']
        has_strings = 'char' in code or 'string' in code
        has_math = any(op in code for op in ['+', '-', '*', '/', '%'])
        
        # Problem templates based on code characteristics
        if has_arrays and has_loops:
            problems.extend(self._generate_array_problems(language))
        
        if has_strings:
            problems.extend(self._generate_string_problems(language))
        
        if has_pointers and language in ['c', 'cpp']:
            problems.extend(self._generate_pointer_problems(language))
        
        if has_math:
            problems.extend(self._generate_math_problems(language))
        
        # Always add some fundamental problems
        if len(problems) < 5:
            problems.extend(self._generate_fundamental_problems(language))
        
        # Return exactly 5 problems
        return problems[:5]
    
    def _generate_array_problems(self, language: str) -> List[Dict]:
        """Generate array-related practice problems."""
        problems = []
        
        if language == 'c':
            problems.append({
                'title': 'Problem 1: Find Maximum Element in Array',
                'description': 'Write a program to find and print the maximum element in an array of integers.',
                'difficulty': 'Easy',
                'solution': '''#include <stdio.h>

int main() {
    int arr[] = {23, 45, 12, 67, 34, 89, 21};
    int n = sizeof(arr) / sizeof(arr[0]);
    int max = arr[0];
    
    // Find maximum
    for (int i = 1; i < n; i++) {
        if (arr[i] > max) {
            max = arr[i];
        }
    }
    
    printf("Maximum element: %d\\n", max);
    return 0;
}''',
                'explanation': 'This solution iterates through the array once, comparing each element with the current maximum and updating it when a larger value is found. Time complexity: O(n).'
            })
            
            problems.append({
                'title': 'Problem 2: Reverse an Array',
                'description': 'Write a program to reverse an array in-place without using extra space.',
                'difficulty': 'Easy',
                'solution': '''#include <stdio.h>

void reverseArray(int arr[], int n) {
    int start = 0;
    int end = n - 1;
    
    while (start < end) {
        // Swap elements
        int temp = arr[start];
        arr[start] = arr[end];
        arr[end] = temp;
        start++;
        end--;
    }
}

int main() {
    int arr[] = {1, 2, 3, 4, 5};
    int n = sizeof(arr) / sizeof(arr[0]);
    
    printf("Original array: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    
    reverseArray(arr, n);
    
    printf("\\nReversed array: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\\n");
    
    return 0;
}''',
                'explanation': 'Uses two-pointer approach: one starting from beginning and one from end. Swaps elements and moves pointers inward until they meet. Time: O(n), Space: O(1).'
            })
        
        elif language == 'cpp':
            problems.append({
                'title': 'Problem 1: Find Maximum Element Using STL',
                'description': 'Use C++ STL to find the maximum element in a vector.',
                'difficulty': 'Easy',
                'solution': '''#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {
    vector<int> arr = {23, 45, 12, 67, 34, 89, 21};
    
    // Using STL algorithm
    int max = *max_element(arr.begin(), arr.end());
    
    cout << "Maximum element: " << max << endl;
    
    // Alternative: using iterators
    int maxValue = arr[0];
    for (const auto& num : arr) {
        if (num > maxValue) {
            maxValue = num;
        }
    }
    cout << "Maximum (manual): " << maxValue << endl;
    
    return 0;
}''',
                'explanation': 'Demonstrates both STL max_element() function and manual iteration using range-based for loop. STL version is more concise and idiomatic C++.'
            })
            
            problems.append({
                'title': 'Problem 2: Vector Operations and Sorting',
                'description': 'Create a program that performs various operations on a vector including sorting, searching, and filtering.',
                'difficulty': 'Medium',
                'solution': '''#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {
    vector<int> numbers = {64, 34, 25, 12, 22, 11, 90};
    
    // Sort the vector
    sort(numbers.begin(), numbers.end());
    
    cout << "Sorted array: ";
    for (int num : numbers) {
        cout << num << " ";
    }
    cout << endl;
    
    // Binary search (only works on sorted array)
    int target = 25;
    bool found = binary_search(numbers.begin(), numbers.end(), target);
    cout << "Is " << target << " present? " << (found ? "Yes" : "No") << endl;
    
    // Filter even numbers
    vector<int> evens;
    copy_if(numbers.begin(), numbers.end(), back_inserter(evens),
            [](int n) { return n % 2 == 0; });
    
    cout << "Even numbers: ";
    for (int num : evens) {
        cout << num << " ";
    }
    cout << endl;
    
    return 0;
}''',
                'explanation': 'Showcases modern C++ features: STL algorithms (sort, binary_search, copy_if), lambda functions, and range-based loops for clean, efficient code.'
            })
        
        return problems
    
    def _generate_string_problems(self, language: str) -> List[Dict]:
        """Generate string-related practice problems."""
        problems = []
        
        if language == 'c':
            problems.append({
                'title': 'Problem 3: Check Palindrome String',
                'description': 'Write a program to check if a given string is a palindrome.',
                'difficulty': 'Easy',
                'solution': '''#include <stdio.h>
#include <string.h>
#include <ctype.h>

int isPalindrome(char str[]) {
    int left = 0;
    int right = strlen(str) - 1;
    
    while (left < right) {
        // Skip non-alphanumeric characters
        while (left < right && !isalnum(str[left])) left++;
        while (left < right && !isalnum(str[right])) right--;
        
        // Compare characters (case-insensitive)
        if (tolower(str[left]) != tolower(str[right])) {
            return 0; // Not a palindrome
        }
        left++;
        right--;
    }
    return 1; // Is a palindrome
}

int main() {
    char str1[] = "A man, a plan, a canal: Panama";
    char str2[] = "race a car";
    
    printf("\\"%s\\" is %s\\n", str1, 
           isPalindrome(str1) ? "a palindrome" : "not a palindrome");
    printf("\\"%s\\" is %s\\n", str2, 
           isPalindrome(str2) ? "a palindrome" : "not a palindrome");
    
    return 0;
}''',
                'explanation': 'Two-pointer technique comparing characters from both ends. Handles spaces and punctuation by skipping non-alphanumeric characters. Case-insensitive comparison using tolower().'
            })
        
        elif language == 'cpp':
            problems.append({
                'title': 'Problem 3: String Manipulation with STL',
                'description': 'Demonstrate various string operations using C++ string class and algorithms.',
                'difficulty': 'Medium',
                'solution': '''#include <iostream>
#include <string>
#include <algorithm>
#include <cctype>

using namespace std;

int main() {
    string text = "Hello, World! C++ Programming is FUN!";
    
    // Convert to uppercase
    string upper = text;
    transform(upper.begin(), upper.end(), upper.begin(), ::toupper);
    cout << "Uppercase: " << upper << endl;
    
    // Count vowels
    int vowelCount = count_if(text.begin(), text.end(), [](char c) {
        c = tolower(c);
        return c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u';
    });
    cout << "Vowel count: " << vowelCount << endl;
    
    // Reverse string
    string reversed = text;
    reverse(reversed.begin(), reversed.end());
    cout << "Reversed: " << reversed << endl;
    
    // Find and replace
    string modified = text;
    size_t pos = modified.find("World");
    if (pos != string::npos) {
        modified.replace(pos, 5, "C++");
    }
    cout << "Modified: " << modified << endl;
    
    return 0;
}''',
                'explanation': 'Demonstrates STL algorithms (transform, count_if, reverse, find, replace) with lambda functions for powerful string manipulation in modern C++.'
            })
        
        return problems
    
    def _generate_pointer_problems(self, language: str) -> List[Dict]:
        """Generate pointer-related practice problems."""
        problems = []
        
        if language == 'cpp':
            problems.append({
                'title': 'Problem 4: Smart Pointers and Memory Management',
                'description': 'Use smart pointers to manage dynamic memory safely without manual delete.',
                'difficulty': 'Medium',
                'solution': '''#include <iostream>
#include <memory>
#include <vector>

using namespace std;

class Student {
public:
    string name;
    int age;
    
    Student(string n, int a) : name(n), age(a) {
        cout << "Student " << name << " created" << endl;
    }
    
    ~Student() {
        cout << "Student " << name << " destroyed" << endl;
    }
    
    void display() {
        cout << "Name: " << name << ", Age: " << age << endl;
    }
};

int main() {
    // unique_ptr - exclusive ownership
    auto student1 = make_unique<Student>("Alice", 20);
    student1->display();
    
    // shared_ptr - shared ownership
    auto student2 = make_shared<Student>("Bob", 22);
    {
        auto student3 = student2; // Shared ownership
        cout << "Reference count: " << student2.use_count() << endl;
    }
    cout << "Reference count after scope: " << student2.use_count() << endl;
    
    // Vector of smart pointers
    vector<unique_ptr<Student>> students;
    students.push_back(make_unique<Student>("Charlie", 21));
    students.push_back(make_unique<Student>("David", 23));
    
    cout << "\\nAll students:" << endl;
    for (const auto& s : students) {
        s->display();
    }
    
    // Automatic cleanup - no delete needed!
    return 0;
}''',
                'explanation': 'Shows proper use of unique_ptr (exclusive ownership) and shared_ptr (shared ownership) for automatic memory management. No manual delete needed - RAII principle in action.'
            })
        
        return problems
    
    def _generate_math_problems(self, language: str) -> List[Dict]:
        """Generate math-related practice problems."""
        problems = []
        
        problem = {
            'title': 'Problem 5: Calculate Factorial with Recursion and Iteration',
            'description': 'Implement both recursive and iterative approaches to calculate factorial.',
            'difficulty': 'Easy'
        }
        
        if language == 'c':
            problem['solution'] = '''#include <stdio.h>

// Recursive approach
long long factorialRecursive(int n) {
    if (n <= 1) return 1;
    return n * factorialRecursive(n - 1);
}

// Iterative approach (more efficient)
long long factorialIterative(int n) {
    long long result = 1;
    for (int i = 2; i <= n; i++) {
        result *= i;
    }
    return result;
}

int main() {
    int n = 10;
    
    printf("Factorial of %d (recursive): %lld\\n", n, factorialRecursive(n));
    printf("Factorial of %d (iterative): %lld\\n", n, factorialIterative(n));
    
    // Calculate factorial of multiple numbers
    printf("\\nFactorial table:\\n");
    for (int i = 1; i <= 10; i++) {
        printf("%d! = %lld\\n", i, factorialIterative(i));
    }
    
    return 0;
}'''
        else:  # cpp
            problem['solution'] = '''#include <iostream>

using namespace std;

// Recursive approach
long long factorialRecursive(int n) {
    if (n <= 1) return 1;
    return n * factorialRecursive(n - 1);
}

// Iterative approach
long long factorialIterative(int n) {
    long long result = 1;
    for (int i = 2; i <= n; i++) {
        result *= i;
    }
    return result;
}

// Template version for any numeric type
template<typename T>
T factorial(T n) {
    T result = 1;
    for (T i = 2; i <= n; i++) {
        result *= i;
    }
    return result;
}

int main() {
    int n = 10;
    
    cout << "Factorial of " << n << " (recursive): " 
         << factorialRecursive(n) << endl;
    cout << "Factorial of " << n << " (iterative): " 
         << factorialIterative(n) << endl;
    
    // Using template version
    cout << "Factorial of " << n << " (template): " 
         << factorial(n) << endl;
    
    // Factorial table
    cout << "\\nFactorial table:" << endl;
    for (int i = 1; i <= 10; i++) {
        cout << i << "! = " << factorialIterative(i) << endl;
    }
    
    return 0;
}'''
        
        problem['explanation'] = 'Compares recursive vs iterative factorial. Recursive is elegant but uses more memory (stack). Iterative is more efficient. Template version shows C++ generic programming.'
        problems.append(problem)
        
        return problems
    
    def _generate_fundamental_problems(self, language: str) -> List[Dict]:
        """Generate fundamental programming problems."""
        problems = []
        
        if language == 'c':
            problems.append({
                'title': 'Problem: Sum of N Natural Numbers',
                'description': 'Calculate the sum of first N natural numbers using formula and loop.',
                'difficulty': 'Easy',
                'solution': '''#include <stdio.h>

int main() {
    int n = 100;
    
    // Method 1: Using formula n*(n+1)/2
    long long sum1 = (long long)n * (n + 1) / 2;
    printf("Sum using formula: %lld\\n", sum1);
    
    // Method 2: Using loop
    long long sum2 = 0;
    for (int i = 1; i <= n; i++) {
        sum2 += i;
    }
    printf("Sum using loop: %lld\\n", sum2);
    
    // Both should give same result
    printf("Results match: %s\\n", (sum1 == sum2) ? "Yes" : "No");
    
    return 0;
}''',
                'explanation': 'Formula method is O(1) constant time, while loop is O(n). For large n, formula is much faster. Demonstrates importance of choosing right algorithm.'
            })
        else:  # cpp
            problems.append({
                'title': 'Problem: Prime Number Checker with Optimization',
                'description': 'Check if a number is prime using optimized algorithm.',
                'difficulty': 'Easy',
                'solution': '''#include <iostream>
#include <cmath>

using namespace std;

bool isPrime(int n) {
    if (n <= 1) return false;
    if (n <= 3) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;
    
    // Check divisors up to sqrt(n)
    for (int i = 5; i * i <= n; i += 6) {
        if (n % i == 0 || n % (i + 2) == 0) {
            return false;
        }
    }
    return true;
}

int main() {
    int limit = 100;
    
    cout << "Prime numbers up to " << limit << ":" << endl;
    
    int count = 0;
    for (int i = 2; i <= limit; i++) {
        if (isPrime(i)) {
            cout << i << " ";
            count++;
            if (count % 10 == 0) cout << endl;
        }
    }
    
    cout << "\\nTotal primes: " << count << endl;
    
    return 0;
}''',
                'explanation': 'Optimized prime checking: skip even numbers, check only up to sqrt(n), and use 6k±1 pattern. Reduces time complexity significantly for large numbers.'
            })
        
        return problems
    
    def format_analysis_report(self, analysis: Dict) -> str:
        """
        Format the analysis results as a human-readable report.
        
        Args:
            analysis: Analysis dictionary from analyze() method
        
        Returns:
            Formatted string report
        """
        report = []
        
        # Summary
        summary = analysis['summary']
        report.append("=" * 70)
        report.append("CODE ANALYSIS REPORT")
        report.append("=" * 70)
        report.append(f"\nSummary:")
        report.append(f"  Total Issues: {summary['total_issues']}")
        report.append(f"    - Critical: {summary['critical']}")
        report.append(f"    - Errors: {summary['errors']}")
        report.append(f"    - Warnings: {summary['warnings']}")
        report.append(f"  Suggestions: {summary['suggestions']}")
        report.append(f"  Alternative Approaches: {summary['alternatives']}")
        report.append("")
        
        # Issues
        if analysis['issues']:
            report.append("-" * 70)
            report.append("ISSUES FOUND:")
            report.append("-" * 70)
            for i, issue in enumerate(analysis['issues'], 1):
                severity = issue.get('severity', 'info').upper()
                issue_type = issue.get('type', 'general')
                line = issue.get('line', 'N/A')
                
                report.append(f"\n{i}. [{severity}] {issue_type.upper()}")
                if line != 'N/A':
                    report.append(f"   Line: {line}")
                report.append(f"   Issue: {issue['message']}")
                report.append(f"   Fix: {issue['suggestion']}")
        
        # Suggestions
        if analysis['suggestions']:
            report.append("\n" + "-" * 70)
            report.append("SUGGESTIONS FOR IMPROVEMENT:")
            report.append("-" * 70)
            for i, suggestion in enumerate(analysis['suggestions'], 1):
                sug_type = suggestion.get('type', 'general')
                line = suggestion.get('line', 'N/A')
                
                report.append(f"\n{i}. [{sug_type.upper()}]")
                if line != 'N/A':
                    report.append(f"   Line: {line}")
                report.append(f"   {suggestion['message']}")
                report.append(f"   Suggestion: {suggestion['suggestion']}")
        
        # Alternatives
        if analysis['alternatives']:
            report.append("\n" + "-" * 70)
            report.append("ALTERNATIVE APPROACHES:")
            report.append("-" * 70)
            for i, alt in enumerate(analysis['alternatives'], 1):
                report.append(f"\n{i}. {alt['approach']}")
                report.append(f"   Benefit: {alt['benefit']}")
                report.append(f"   Example: {alt['example']}")
        
        report.append("\n" + "=" * 70)
        
        return "\n".join(report)


def analyze_code(code: str, language: str) -> Dict:
    """
    Convenience function to analyze code and return results.
    
    Args:
        code: The source code to analyze
        language: Either 'c' or 'cpp'
    
    Returns:
        Analysis dictionary with issues, suggestions, and alternatives
    """
    analyzer = CodeAnalyzer()
    return analyzer.analyze(code, language)


def get_analysis_report(code: str, language: str) -> str:
    """
    Convenience function to get a formatted analysis report.
    
    Args:
        code: The source code to analyze
        language: Either 'c' or 'cpp'
    
    Returns:
        Formatted string report
    """
    analyzer = CodeAnalyzer()
    analysis = analyzer.analyze(code, language)
    return analyzer.format_analysis_report(analysis)
