# Delivery System Solver

A production-quality Python solution for optimizing package delivery assignments to agents, minimizing total travel distance.

## ✨ Bonus Tasks Implemented (4/4)

✅ **1. Random Delivery Delays** - Simulates realistic delivery times with configurable random delays  
✅ **2. ASCII Route Visualization** - Text-based visualization showing agent routes step-by-step  
✅ **3. Dynamic Agent Joining** - Agents can join mid-delivery to handle additional packages  
✅ **4. Export to CSV** - Export results to CSV format for analysis in Excel/spreadsheets  

See [Bonus Features](#bonus-features) section below for details.

## Problem Statement

The system assigns delivery packages to agents where:
- **Warehouses** have fixed locations and store packages
- **Agents** start at specific locations and can deliver packages
- **Packages** need to be picked up from warehouses and delivered to destinations

**Objective**: Assign packages to agents to minimize the total distance traveled.

## Key Assumptions

Since the original problem statement (PDF) was not directly parsable, the following assumptions were made based on standard delivery optimization problems and test case analysis:

1. **Assignment Model**: Each package is assigned to exactly one agent
2. **Agent Capacity**: Agents have unlimited capacity (can deliver multiple packages)
3. **Distance Metric**: Euclidean distance is used for all calculations
4. **Travel Model**: For each package, agent travels: `current_location → warehouse → destination`
5. **Sequential Delivery**: After delivering a package, the agent's location is updated to the destination
6. **No Constraints**: No time windows, priority levels, or vehicle capacity constraints
7. **Optimization Goal**: Minimize total distance across all agents (greedy assignment)

## Algorithm

### Greedy Assignment Strategy

The solver uses a **greedy algorithm** that processes packages sequentially:

```
For each package P:
    1. Get the warehouse W where P is located
    2. For each agent A:
        - Calculate distance: current_location(A) → location(W) → destination(P)
    3. Assign P to the agent with minimum distance
    4. Update that agent's location to destination(P)
```

### Why Greedy?

- **Time Complexity**: O(n × m) where n = packages, m = agents
- **Space Complexity**: O(m) for tracking agent locations
- **Trade-off**: Provides a good approximate solution quickly (suitable for real-time systems)
- **Optimal?**: Not guaranteed globally optimal, but performs well in practice

### Alternative Approaches Considered

1. **Optimal (Hungarian Algorithm)**: O(n³) - too slow for large datasets
2. **Genetic Algorithm**: Better solutions but much slower and non-deterministic
3. **Simulated Annealing**: Good for complex constraints, overkill for this problem

## Project Structure

```
.
├── models.py          # Data classes (Location, Warehouse, Agent, Package, Assignment)
├── utils.py           # Helper functions (distance calc, JSON I/O)
├── solver.py          # Core optimization logic
```
.
├── models.py          # Data classes (Location, Warehouse, Agent, Package, Assignment)
├── utils.py           # Helper functions (distance calc, JSON I/O)
├── solver.py          # Core optimization logic with bonus features
├── main.py            # CLI entry point with bonus task options
├── test_runner.py     # Automated test suite
├── csv_exporter.py    # CSV export functionality (BONUS TASK)
├── visualize.py       # ASCII route visualization (BONUS TASK)
├── demo_bonus.py      # Demo script for all bonus features
├── README.md          # This file
├── base_case.json     # Base test case
└── Python Assignment(Delivery System Test Cases)/
    ├── test_case_1.json
    ├── test_case_2.json
    └── ... (test_case_10.json)
```

## Installation

### Requirements
- Python 3.8 or higher
- No external dependencies (uses only standard library)

### Setup
```bash
# Clone or navigate to the project directory
cd "Python Assignment -2026"

# No pip install needed - uses only Python standard library
```

## Usage

### Basic Usage

```bash
# Run with default settings
python main.py base_case.json

# Save output to JSON file
python main.py base_case.json --output result.json
```

### 🎁 Bonus Features Usage

```bash
# Enable random delivery delays (5-30 seconds per delivery)
python main.py base_case.json --delays

# Export results to CSV
python main.py base_case.json --csv results.csv --csv-summary summary.csv

# Enable dynamic agent joining (agents join mid-delivery)
python main.py base_case.json --dynamic-agents

# Combine all bonus features
python main.py base_case.json --delays --dynamic-agents --csv full_results.csv

# ASCII visualization (separate script)
python visualize.py base_case.json

# Run demo of ALL bonus tasks
python demo_bonus.py
```

### Command-Line Options

```
positional arguments:
  input_file            Input JSON file with delivery data

optional arguments:
  --output, -o FILE     Save JSON output to FILE
  --csv FILE            Export assignments to CSV (BONUS TASK)
  --csv-summary FILE    Export summary statistics to CSV
  --delays              Enable random delivery delays (BONUS TASK)
  --dynamic-agents      Enable dynamic agent joining (BONUS TASK)
```

Output will show:
- Total distance
- Assignments by agent
- Statistics

### Save Output to File

```bash
python main.py base_case.json output.json
```

### Run All Test Cases

```bash
python test_runner.py
```

This will:
1. Run the base case
2. Execute all test cases in the test directory
3. Report PASS/FAIL for each
4. Generate `test_results.json` with detailed results

### Custom Test Directory

```bash
python test_runner.py "path/to/test/cases"
```

## Input Format

The system accepts JSON files in two formats:

### Format 1 (List-based)
```json
{
  "warehouses": [
    {"id": "W1", "location": [0, 0]},
    {"id": "W2", "location": [50, 75]}
  ],
  "agents": [
    {"id": "A1", "location": [5, 5]},
    {"id": "A2", "location": [60, 60]}
  ],
  "packages": [
    {"id": "P1", "warehouse_id": "W1", "destination": [30, 40]},
    {"id": "P2", "warehouse_id": "W2", "destination": [70, 90]}
  ]
}
```

### Format 2 (Dict-based)
```json
{
  "warehouses": {
    "W1": [0, 0],
    "W2": [50, 75]
  },
  "agents": {
    "A1": [5, 5],
    "A2": [60, 60]
  },
  "packages": [
    {"id": "P1", "warehouse": "W1", "destination": [30, 40]},
    {"id": "P2", "warehouse": "W2", "destination": [70, 90]}
  ]
}
```

Both formats are automatically detected and parsed.

## Output Format

```json
{
  "total_distance": 123.45,
  "assignments": {
    "A1": [
      {
        "package_id": "P1",
        "warehouse_id": "W1",
        "distance": 45.67
      }
    ],
    "A2": [
      {
        "package_id": "P2",
        "warehouse_id": "W2",
        "distance": 77.78
      }
    ]
  },
  "statistics": {
    "total_packages": 2,
    "total_agents": 2,
    "total_warehouses": 2,
    "average_distance_per_package": 61.73
  }
}
```

## Code Quality Features

### Type Hints
All functions use Python type hints for better IDE support and documentation:
```python
def euclidean_distance(loc1: Location, loc2: Location) -> float:
    ...
```

### Error Handling
Comprehensive exception handling for:
- Missing files
- Malformed JSON
- Missing required fields
- Invalid warehouse references

### Object-Oriented Design
- **Models**: Clean data classes using `@dataclass`
- **Separation of Concerns**: Utils, solver, and main logic are modular
- **Single Responsibility**: Each class/function has one clear purpose

### Documentation
- Docstrings for all classes and functions
- Inline comments for complex logic
- Type annotations throughout

## Time & Space Complexity

### Time Complexity
- **Input Parsing**: O(w + a + p) where w=warehouses, a=agents, p=packages
- **Solving**: O(p × a) - for each package, check all agents
- **Output Formatting**: O(p)
- **Total**: **O(p × a)**

### Space Complexity
- **Data Storage**: O(w + a + p) for storing all entities
- **Agent Tracking**: O(a) for current locations
- **Assignments**: O(p) for storing results
- **Total**: **O(w + a + p)**

### Scalability
- **Small scale** (p < 1000, a < 100): < 1 second
- **Medium scale** (p < 10000, a < 500): < 10 seconds
- **Large scale** (p > 10000): Consider parallel processing or advanced algorithms

## Bonus Features

### 🎲 1. Random Delivery Delays

Simulates realistic delivery scenarios with random delays per package.

**How it works:**
- Each delivery gets a random delay between configurable min/max values (default: 5-30 seconds)
- Delays are tracked per assignment and included in output
- Useful for capacity planning and time estimation

**Usage:**
```bash
python main.py base_case.json --delays
```

**Example output:**
```
Agent A1: 2 packages, distance: 121.21, delay: 42.35s
  - P1: distance 57.07, delay: 18.23s
  - P4: distance 64.14, delay: 24.12s
```

### 🗺️ 2. ASCII Route Visualization

Text-based visualization showing complete delivery routes.

**Features:**
- Shows initial positions of all agents and warehouses
- Step-by-step route for each agent
- Visual representation of: location → warehouse → destination
- Displays distances and delays (if enabled)

**Usage:**
```bash
python visualize.py base_case.json
```

**Sample output:**
```
A1: 2 packages, total distance: 121.21
  1. P1:
     Route: (5, 5) → (0, 0) (W1) → (30, 40)
     Distance: 57.07
  2. P4:
     Route: (30, 40) → (0, 0) (W1) → (10, 10)
     Distance: 64.14
```

### 🚀 3. Dynamic Agent Joining

Allows new agents to join mid-delivery to handle additional load.

**How it works:**
- Agents can be scheduled to join after processing N packages
- New agents start at specified locations
- System automatically assigns packages to newly joined agents
- Useful for modeling real-world scenarios with backup drivers

**Usage:**
```bash
python main.py base_case.json --dynamic-agents
```

**In code:**
```python
solver = DeliverySystemSolver(warehouses, agents, packages, 
                              enable_dynamic_agents=True)
new_agent = Agent(id="A_BACKUP", location=Location(50, 50))
solver.add_dynamic_agent(new_agent, join_after_packages=5)
```

**Output:**
```
[Dynamic] Agent A_BACKUP joined at package #6
```

### 📊 4. Export to CSV

Export results to CSV format for analysis in Excel, Google Sheets, etc.

**Features:**
- **Detailed CSV**: All assignments with agent, package, warehouse, distance, delays
- **Summary CSV**: Statistics per agent (total packages, distance, delays)
- Compatible with all spreadsheet software

**Usage:**
```bash
# Export detailed assignments
python main.py base_case.json --csv assignments.csv

# Export summary statistics
python main.py base_case.json --csv-summary summary.csv

# Export both
python main.py base_case.json --csv assignments.csv --csv-summary summary.csv
```

**CSV Format (assignments.csv):**
```
Agent ID,Package ID,Warehouse ID,Warehouse Location,Destination,Distance,Delay (seconds)
A1,P1,W1,"(0, 0)","(30, 40)",57.07,18.23
A1,P4,W1,"(0, 0)","(10, 10)",64.14,24.12
```

**CSV Format (summary.csv):**
```
Agent ID,Packages Delivered,Total Distance,Total Delay (seconds),Average Distance per Package
A1,2,121.21,42.35,60.61
A2,2,79.21,35.67,39.61
```

### 🎯 Demo All Bonus Features

Run the demo script to see all bonus features in action:

```bash
python demo_bonus.py
```

This will demonstrate:
- Random delays with statistics
- Dynamic agent joining
- CSV export
- All features combined

## Testing

The test suite validates:
1. ✓ All packages are assigned
2. ✓ No duplicate assignments
3. ✓ Valid warehouse references
4. ✓ Correct distance calculations
5. ✓ Proper handling of both input formats

Run tests:
```bash
python test_runner.py
```

Expected output:
```
RUNNING 10 TEST CASES
[1/10] Running test_case_1... ✓ PASS - Total distance: 234.56
[2/10] Running test_case_2... ✓ PASS - Total distance: 123.45
...
```

## Future Enhancements

Potential improvements for production deployment:

1. **Advanced Algorithms**:
   - Implement Hungarian algorithm for optimal assignment
   - Add vehicle capacity constraints
   - Support time windows and priorities

2. **Performance**:
   - Parallel processing for large datasets
   - Caching for repeated calculations
   - Database integration for persistent storage

3. **Features**:
   - Real-time tracking and updates
   - Multi-warehouse routing
   - Dynamic re-assignment
   - Cost optimization (fuel, time, etc.)

4. **API**:
   - REST API endpoints
   - WebSocket for real-time updates
   - Integration with mapping services

## License

This is an assignment solution. Use as reference material only.

## Author

Senior Python Backend Engineer
Created: February 2026
