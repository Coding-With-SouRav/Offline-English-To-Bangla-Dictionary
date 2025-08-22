# English to Bangla Dictionary Application

## Overview
This is a desktop dictionary application that translates English words to Bangla (Bengali). It features a modern GUI built with Tkinter and uses an efficient two-level hashing algorithm for fast word lookups.

## Key Features

### 1. Efficient Dictionary Implementation
- Uses a custom two-level hash table implementation
- Primary hash function: Universal hashing with random parameters
- Secondary hash function: Perfect hashing for collision resolution
- Polynomial rolling hash function for key generation

### 2. User Interface
- Modern dark theme with blue accent colors
- Responsive design with scrollable results area
- Real-time search suggestions as you type
- Custom icons and visual elements
- Support for both mouse and keyboard navigation

### 3. Technical Implementation
- Threaded dictionary loading to prevent UI freezing
- Cross-platform compatibility (Windows focus with fallbacks)
- PyInstaller support for executable creation
- Proper resource path handling for both development and deployed environments

## Code Structure

### Main Components

1. **Dictionary Class**:
   - Handles all dictionary operations
   - Implements efficient hashing algorithms
   - Manages word storage and retrieval

2. **DictionaryApp Class**:
   - Creates and manages the GUI
   - Handles user interactions
   - Implements search suggestions

3. **Support Functions**:
   - `resource_path()`: Handles resource loading for both development and deployed environments
   - `main()`: Application entry point

## Usage
1. Type an English word in the search box
2. View suggestions as you type (use arrow keys to navigate)
3. Press Enter or click the search button to see the Bangla translation
4. Multiple words will be translated sequentially

## Technical Details
- Hash table size: 103643 (prime number)
- Hash modulus: 100000000003
- Radix: 128 for polynomial hashing
- Dictionary data stored in JSON format

## Requirements
- Python 3.x
- Tkinter (usually included with Python)
- PIL/Pillow library for image handling
- Internet connection for initial data download (if not bundled)

The application is optimized for performance with large dictionaries and provides a smooth user experience with real-time feedback.
