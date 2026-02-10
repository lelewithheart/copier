#!/usr/bin/env python3
"""
Example demonstration of writer.py features.
This shows how to use the human-like typing simulator.
"""

def hello_world():
    """Simple hello world function"""
    message = "Hello, World!"
    print(message)
    return message

def calculate_sum(a, b):
    """Calculate sum of two numbers"""
    result = a + b
    print(f"{a} + {b} = {result}")
    return result

if __name__ == "__main__":
    # Run examples
    hello_world()
    calculate_sum(5, 3)
    
    # Test with special characters
    special_chars = {'key': 'value', 'items': [1, 2, 3]}
    print(special_chars)
