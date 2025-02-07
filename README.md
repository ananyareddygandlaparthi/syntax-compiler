# Syntax Compiler


This project is a custom compiler that validates and executes conditional and loop constructs, specifically if, while, and for loops. It is implemented using Python and PLY (Python Lex-Yacc) to perform lexical analysis and parsing of expressions. The compiler supports arithmetic operations, relational operators, and structured flow control statements.

The lexer tokenizes the input code, recognizing keywords, operators, and identifiers, while the parser ensures that the syntax follows the defined grammar. The if statement allows conditional branching, executing one of two possible statements based on a condition. The while loop executes a block of code repeatedly as long as the condition remains true, with a built-in iteration limit to prevent infinite loops. The for loop mimics Python's range-based iteration, iterating over a predefined number of times while executing a given statement.

To handle errors gracefully, the compiler includes mechanisms for detecting and reporting syntax errors, invalid expressions, and unsupported constructs. This ensures robustness and helps users debug incorrect input easily. The project provides a simple command-line interface where users can input statements and receive the evaluated results.

This compiler demonstrates fundamental principles of language parsing and execution control, making it a useful educational tool for understanding compilers, lexers, and parsers.
