---
title: C-Cpp-Inspector
emoji: 🔍️©️/©️++💻
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.7.1
app_file: app.py
pinned: false
license: mit
---

# C/C++ Syntax and Features Inspector
This project analyzes C/C++ code to extract insights about syntax elements, memory management, and C++ specific features. The tool identifies primitive types, pointers, structs, control structures, memory operations, and C++ features like classes and templates, helping developers understand and improve their C/C++ code.

## Developer

Developed by Ramon Mayor Martins (2025)

- Email: rmayormartins@gmail.com
- Homepage: https://rmayormartins.github.io/
- Twitter: @rmayormartins
- GitHub: https://github.com/rmayormartins
- Space: https://huggingface.co/rmayormartins

## Key Features

### Basic Analysis
- **Syntax Elements**:
  - Detects primitive types and constants
  - Identifies variable declarations
  - Analyzes control structures (if/else, switch/case, loops)
  - Tracks operators (arithmetic, logical, bitwise)

### C-Specific Features
- **Memory Management**:
  - Tracks malloc/calloc/realloc usage
  - Monitors memory freeing operations
  - Analyzes memory operations (memcpy, memmove, etc.)
- **Data Structures**:
  - Identifies pointers and multiple pointers
  - Detects structs, unions, and enums
  - Analyzes arrays and typedefs

### C++ Features
- **OOP Analysis**:
  - Classes and objects
  - Templates and namespaces
  - Inheritance and polymorphism
  - Member access specifiers
- **Modern C++**:
  - STL usage detection
  - Modern C++ features (auto, nullptr, etc.)
  - References and operator overloading

## Interface Features
- Upload multiple ©️/©️++ files (.c, .cpp, .h, .hpp)
- Results organized in categorized tabs:
  - File Information
  - Basic Elements
  - Pointers and Structures
  - Control Flow
  - Operators
  - Input/Output
  - Memory Management
  - C++ Features

## How to Use
1. Open the application interface
2. Upload one or more C/C++ files
3. Click "Analisar Arquivos" (Analyze Files)
4. View detailed analysis in each category tab

## Installation

### Requirements
- Python 3.7+
- libclang
- gradio

### Local Development
To run locally:

```bash
# Install libclang (Ubuntu/Debian)
sudo apt-get install libclang-dev

# Install Python dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### Google Colab
To run in Google Colab:

```python
!apt-get update
!apt-get install -y libclang-dev
!pip install libclang gradio
```

## License
MIT License