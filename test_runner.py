"""
Test runner for the Delivery System Solver.

Runs all test cases in the specified directory and validates the solution.
"""
import json
from pathlib import Path
from typing import List, Tuple
import sys

from utils import load_input_data
from solver import DeliverySystemSolver, format_output


class TestRunner:
    """Manages running and validating test cases."""
    
    def __init__(self, test_dir: str = "Python Assignment(Delivery System Test Cases)"):
        """
        Initialize test runner.
        
        Args:
            test_dir: Directory containing test case JSON files
        """
        self.test_dir = Path(test_dir)
        if not self.test_dir.exists():
            raise FileNotFoundError(f"Test directory not found: {test_dir}")
    
    def find_test_cases(self) -> List[Path]:
        """
        Find all test case JSON files in the test directory.
        
        Returns:
            Sorted list of test case file paths
        """
        test_files = list(self.test_dir.glob("test_case_*.json"))
        # Sort by test case number
        test_files.sort(key=lambda p: int(p.stem.split('_')[-1]))
        return test_files
    
    def run_test_case(self, test_file: Path) -> Tuple[bool, dict, str]:
        """
        Run a single test case.
        
        Args:
            test_file: Path to test case JSON file
            
        Returns:
            Tuple of (success: bool, output: dict, message: str)
        """
        try:
            # Load input
            warehouses, agents, packages = load_input_data(str(test_file))
            
            # Validate input
            if not warehouses:
                return False, {}, "No warehouses found"
            if not agents:
                return False, {}, "No agents found"
            if not packages:
                return False, {}, "No packages found"
            
            # Solve
            solver = DeliverySystemSolver(warehouses, agents, packages)
            assignments = solver.solve()
            
            # Validate solution
            if len(assignments) != len(packages):
                return False, {}, f"Expected {len(packages)} assignments, got {len(assignments)}"
            
            # Check all packages assigned
            assigned_packages = {a.package_id for a in assignments}
            expected_packages = {p.id for p in packages}
            if assigned_packages != expected_packages:
                return False, {}, "Not all packages were assigned"
            
            # Format output
            output = format_output(assignments, warehouses, agents, packages)
            
            return True, output, f"Total distance: {output['total_distance']:.2f}"
            
        except Exception as e:
            return False, {}, f"Error: {str(e)}"
    
    def run_all_tests(self) -> None:
        """Run all test cases and print results."""
        test_files = self.find_test_cases()
        
        if not test_files:
            print("No test cases found!")
            return
        
        print(f"{'='*80}")
        print(f"RUNNING {len(test_files)} TEST CASES")
        print(f"{'='*80}\n")
        
        results = []
        passed = 0
        failed = 0
        
        for i, test_file in enumerate(test_files, 1):
            test_name = test_file.stem
            print(f"[{i}/{len(test_files)}] Running {test_name}...", end=" ")
            
            success, output, message = self.run_test_case(test_file)
            
            if success:
                print(f"✓ PASS - {message}")
                passed += 1
            else:
                print(f"✗ FAIL - {message}")
                failed += 1
            
            results.append({
                'test': test_name,
                'passed': success,
                'message': message,
                'output': output
            })
        
        # Print summary
        print(f"\n{'='*80}")
        print(f"TEST SUMMARY")
        print(f"{'='*80}")
        print(f"Total Tests: {len(test_files)}")
        print(f"Passed: {passed} ✓")
        print(f"Failed: {failed} ✗")
        print(f"Success Rate: {(passed/len(test_files)*100):.1f}%")
        print(f"{'='*80}\n")
        
        # Save detailed results
        results_file = Path("test_results.json")
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        print(f"Detailed results saved to: {results_file}")
        
        return passed == len(test_files)


def run_base_case():
    """Run the base case as a demonstration."""
    base_case_file = Path("base_case.json")
    
    if not base_case_file.exists():
        print("base_case.json not found!")
        return
    
    print(f"{'='*80}")
    print("RUNNING BASE CASE")
    print(f"{'='*80}\n")
    
    try:
        warehouses, agents, packages = load_input_data(str(base_case_file))
        solver = DeliverySystemSolver(warehouses, agents, packages)
        assignments = solver.solve()
        output = format_output(assignments, warehouses, agents, packages)
        
        print(f"Total Distance: {output['total_distance']:.2f} units")
        print(f"Packages: {len(packages)}, Agents: {len(agents)}, Warehouses: {len(warehouses)}")
        print("\nAssignments:")
        for agent_id, pkgs in output['assignments'].items():
            if pkgs:
                print(f"  {agent_id}: {[p['package_id'] for p in pkgs]}")
        
        print(f"\n{'='*80}\n")
        
    except Exception as e:
        print(f"Error running base case: {e}")


if __name__ == "__main__":
    # Run base case first
    run_base_case()
    
    # Then run all test cases
    test_dir = "Python Assignment(Delivery System Test Cases)"
    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
    
    try:
        runner = TestRunner(test_dir)
        all_passed = runner.run_all_tests()
        sys.exit(0 if all_passed else 1)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
