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
        
        return {
            'issues': self.issues,
            'suggestions': self.suggestions,
            'alternatives': self.alternatives,
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
                'example': 'std::vector<int> arr(size); instead of int arr[size];'
            })
        
        # printf vs cout
        if language == 'cpp' and 'printf(' in code:
            self.alternatives.append({
                'approach': 'Use std::cout instead of printf()',
                'benefit': 'Type-safe, no format specifiers needed, better C++ integration',
                'example': 'std::cout << value << std::endl; instead of printf("%d", value);'
            })
        
        # scanf vs cin
        if language == 'cpp' and 'scanf(' in code:
            self.alternatives.append({
                'approach': 'Use std::cin instead of scanf()',
                'benefit': 'Type-safe input, no format specifiers needed, better error handling',
                'example': 'std::cin >> value; instead of scanf("%d", &value);'
            })
        
        # Manual memory management
        if language == 'cpp' and ('malloc(' in code or 'new ' in code):
            self.alternatives.append({
                'approach': 'Use smart pointers (C++11 and later)',
                'benefit': 'Automatic memory management, exception safety, no manual delete needed',
                'example': 'std::unique_ptr<Type> ptr = std::make_unique<Type>(); instead of Type* ptr = new Type();'
            })
        
        # C-style casts
        if language == 'cpp' and re.search(r'\([a-zA-Z_]\w*\s*\*?\s*\)', code):
            self.alternatives.append({
                'approach': 'Use C++ style casts',
                'benefit': 'More explicit, searchable, compile-time checking',
                'example': 'static_cast<int>(value) instead of (int)value'
            })
    
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
