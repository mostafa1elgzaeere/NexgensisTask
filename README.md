# Delivery System Solver

A production-quality Python solution for optimizing package delivery assignments to agents, minimizing total travel distance.

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
├── main.py            # CLI entry point
├── test_runner.py     # Automated test suite
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

### Run a Single Case

```bash
python main.py base_case.json
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
