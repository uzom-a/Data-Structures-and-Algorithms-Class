# Student Grade Categorization System

## CS 236 - Data Structures and Algorithms Lab Assignment #1

### Project Overview
This Python program is a comprehensive Student Grade Categorization System that allows users to manage student records, categorize grades based on performance levels, and perform various operations on student data. The system implements key programming concepts including arrays, nested if statements, input validation, and user interaction.

### Team Members
- **Dharambir** - Grade validation and categorization logic, statistical calculations
- **Uzoma** - Student management system and data input functionality
- **Kelvin** - User interface and data display functionality

## Features

### Core Functionality
- **Add Students**: Register new students with names and grades (maximum 10 students)
- **View Students**: Display all student records in a formatted table
- **Delete Students**: Remove student records by ID
- **Grade Categorization**: Automatic categorization based on performance levels
- **Statistical Analysis**: Calculate average, maximum, and minimum grades

### Grade Categories
The system categorizes grades using the following scale:
- **Excellent**: 90-100 points
- **Good**: 80-89 points
- **Average**: 70-79 points
- **Needs Improvement**: Below 70 points

### Data Structure
The program uses four separate arrays to store student information:
- `names[]` - Student names
- `grades[]` - Student grades (0-100)
- `categories[]` - Grade categories
- `student_ids[]` - Unique student identifiers

## Technical Requirements Met

### 1. Arrays Implementation
- ✅ Four separate arrays for data storage
- ✅ Synchronized data management across all arrays
- ✅ Dynamic array operations (add, delete, retrieve)

### 2. Nested If Statements
- ✅ Grade categorization using nested conditional logic
- ✅ Input validation with multiple condition checks
- ✅ Menu selection handling

### 3. Data Validation
- ✅ Grade range validation (0-100)
- ✅ Student limit enforcement (maximum 10 students)
- ✅ Input type validation (integer checking)
- ✅ Empty input handling

### 4. User Interaction
- ✅ Interactive menu system
- ✅ User prompts for data entry
- ✅ Formatted output display
- ✅ Error message handling

## Program Structure

### Main Functions

#### Grade Management (Dharambir)
```python
def categorize_grade(marks)
```
- Categorizes grades based on performance scale
- Uses nested if statements for classification

```python
def validate_grade(grade)
```
- Validates grade input (0-100 range)
- Returns boolean for validation status

```python
def average_grade(), max_grade(), min_grade()
```
- Statistical calculation functions
- Handles empty dataset scenarios

#### Student Operations (Uzoma)
```python
def add_student()
```
- Adds new student records
- Implements input validation and limit checking
- Manages all four arrays synchronously

#### Display Interface (Kelvin)
```python
def display_students()
```
- Formats and displays student data in table format
- Shows statistical information
- Handles empty dataset display

#### Utility Functions
```python
def delete_student()
```
- Removes student records by ID
- Maintains array synchronization

```python
def main()
```
- Main program loop
- Menu system implementation

## Usage Instructions

### Running the Program
1. Execute the Python file: `python Index.py`
2. Follow the interactive menu prompts
3. Select options 1-4 for different operations

### Menu Options
1. **Add Student** - Enter student name and grade
2. **View All Students** - Display formatted student table
3. **Delete Student** - Remove student by ID
4. **Exit** - Close the program

### Sample Output
```
------------------------------------
Welcome to Student Portal
------------------------------------

ID    Name            Grade   Category          
---------------------------------------------
1     Alice           95      Excellent         
2     Bob             82      Good              
3     Charlie         67      Needs Improvement 
---------------------------------------------
Average Grade: 81.33
Maximum Grade: 95
Minimum Grade: 67
```

## User-Friendly Features

### 1. Smart Input Validation with Retry Loops
Instead of returning to the main menu on invalid input, the system allows users to correct their mistakes immediately:

#### Name Validation
- **Requirement**: Names must contain only letters and spaces
- **User-Friendly**: Continuous prompt until valid name is entered
- **Smart Logic**: Rejects pure numbers but allows letter-only names with spaces
- **Example**: "John Smith" ✅, "123" ❌, "John2" ❌

#### Grade Validation  
- **Requirement**: Integer between 0-100
- **User-Friendly**: Persistent validation loop with specific error messages
- **Handles**: Both type errors (non-integers) and range errors (out of bounds)
- **Benefit**: User doesn't lose progress when making input mistakes

### 2. Dynamic Context-Aware Menu System
The menu adapts based on current system state:
- **Add Student**: Only shown when under 10-student limit
- **View Students**: Only appears when students exist
- **Delete Student**: Hidden when no students are registered
- **Real-time Status**: Shows current student count and remaining capacity

### 3. Batch Student Addition
- **Feature**: Add multiple students in one session
- **Smart Prompting**: Shows exact range of allowed additions
- **Efficiency**: Reduces menu navigation for multiple entries
- **Example**: "How many student(s) you want to add between 1 and 7:"

### 4. Comprehensive Error Recovery
- **No System Crashes**: All invalid inputs are caught and handled
- **Clear Messages**: Specific error descriptions for each validation failure
- **Retry Opportunities**: Users can correct mistakes without losing context
- **Graceful Degradation**: System continues functioning even with invalid inputs

### Input Validation Details

#### Grade Validation
- Must be integer between 0-100
- Non-integer inputs prompt for retry
- Out-of-range values show specific error messages
- Validation loop continues until correct input

#### Name Validation
- Must contain only alphabetic characters and spaces
- Numbers in names are rejected
- Empty names are rejected
- Continuous validation until proper format

#### Student Limit Management
- Maximum 10 students enforced
- Dynamic capacity display
- Intelligent menu option filtering
- Clear limit-reached messaging

#### Error Handling Scenarios
- Invalid menu selections with retry prompts
- Non-numeric input for grades and IDs
- Empty dataset operations handled gracefully
- Student ID not found scenarios with clear messages
- Batch addition validation with range checking

## File Structure
```
Data-Structures-and-Algorithms-Class/
├── Index.py          # Main program file
└── README.md         # Project documentation
```

## Development Approach

### Team Collaboration
Each team member contributed specific functionality:

**Dharambir's Contributions:**
- Implemented grade categorization logic with nested if statements
- Created grade validation function
- Developed statistical calculation functions (average, max, min)
- Ensured proper grade range enforcement

**Uzoma's Contributions:**
- Designed and implemented the add_student() function
- Created comprehensive input validation system
- Implemented student limit enforcement (10 students maximum)
- Managed array synchronization for student data

**Kelvin's Contributions:**
- Developed the user interface and display system
- Created formatted table output for student records
- Implemented the display_students() function with statistical summaries
- Designed the main menu system and user interaction flow

### Design Decisions
1. **Four Array Structure**: Maintains data separation while allowing synchronized operations
2. **ID System**: Unique identifiers for reliable student record management
3. **Input Validation**: Multiple layers of validation for robust error handling
4. **Modular Design**: Separate functions for different operations enhance maintainability

### User Experience Improvements Implemented

Based on the team's analysis and feedback, several key improvements were made to enhance user experience:

#### Kelvin's UX Contributions:
- **Limit Management**: Implemented smart handling when 10-student limit is reached
- **Menu Dynamics**: Created context-aware menu that only shows relevant options
- **Name Validation**: Ensured numbers are rejected in names while allowing proper letter combinations
- **Status Display**: Added real-time display of student count and remaining capacity

#### Dharambir's Input Enhancements:
- **Batch Processing**: Added ability to specify number of students to add in one session
- **Grade Editing**: Implemented persistent validation loops for grade corrections
- **Range Validation**: Enhanced grade validation with specific error messaging

#### Uzoma's System Improvements:
- **Delete Protection**: Ensured delete option only appears when students exist
- **Error Recovery**: Implemented comprehensive error handling that doesn't crash the system
- **Session Management**: Created smooth workflow that maintains user context

#### Key UX Philosophy:
- **No Dead Ends**: Users never get stuck or forced to restart
- **Clear Feedback**: Every action provides immediate, specific feedback
- **Intelligent Adaptation**: System adapts interface based on current state
- **Error Tolerance**: Mistakes are handled gracefully with retry opportunities

## Testing Scenarios

### Edge Cases Handled
- Empty student list operations
- Maximum student limit (10 students)
- Invalid grade inputs (negative, >100, non-numeric)
- Invalid student ID for deletion
- Non-numeric menu selections

### Test Cases
1. Add 10 students (test limit)
2. Attempt to add 11th student (should be blocked)
3. Enter invalid grades (-1, 101, "abc")
4. Delete non-existent student ID
5. View empty student list
6. Test all grade categories (0-69, 70-79, 80-89, 90-100)

## Future Enhancements
- Search functionality by name or grade
- Grade modification capability
- Data persistence (file save/load)
- Sorting options (by name, grade, category)
- Grade history tracking
- Export functionality

## Academic Objectives Achieved
- ✅ Array manipulation and management
- ✅ Nested conditional statements
- ✅ Input validation and error handling
- ✅ User interface design
- ✅ Collaborative programming
- ✅ Code documentation and commenting
- ✅ Problem-solving and algorithm design

---

**Course**: CS 236 - Data Structures and Algorithms  
**Assignment**: Lab #1 - Student Grade Categorization System  
**Date**: August 2025  
**Team**: Dharambir, Uzoma, Kelvin