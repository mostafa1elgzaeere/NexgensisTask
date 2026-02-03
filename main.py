"""
Main entry point for the Delivery System Solver.

Usage:
    python main.py <input_file.json> [output_file.json]
    
Example:
    python main.py base_case.json output.json
    python main.py test_case_1.json
"""
import sys
import json
from pathlib import Path

from utils import load_input_data, save_output_data
from solver import DeliverySystemSolver, format_output


def main(input_file: str, output_file: str = None) -> dict:
    """
    Main execution function for the delivery system solver.
    
    Args:
        input_file: Path to input JSON file
        output_file: Optional path to save output JSON
        
    Returns:
        Dictionary containing the solution
    """
    try:
        # Load input data
        print(f"Loading input from: {input_file}")
        warehouses, agents, packages = load_input_data(input_file)
        
        print(f"Loaded: {len(warehouses)} warehouses, {len(agents)} agents, {len(packages)} packages")
        
        # Create solver and solve
        solver = DeliverySystemSolver(warehouses, agents, packages)
        print("Solving delivery assignment problem...")
        assignments = solver.solve()
        
        # Format output
        output = format_output(assignments, warehouses, agents, packages)
        
        # Display results
        print(f"\n{'='*60}")
        print("SOLUTION SUMMARY")
        print(f"{'='*60}")
        print(f"Total Distance: {output['total_distance']:.2f} units")
        print(f"Average Distance per Package: {output['statistics']['average_distance_per_package']:.2f} units")
        print(f"\nAssignments by Agent:")
        
        for agent_id, agent_packages in output['assignments'].items():
            if agent_packages:
                print(f"\n  {agent_id}: {len(agent_packages)} package(s)")
                for pkg in agent_packages:
                    print(f"    - {pkg['package_id']} from {pkg['warehouse_id']}, distance: {pkg['distance']:.2f}")
            else:
                print(f"\n  {agent_id}: No packages assigned")
        
        print(f"\n{'='*60}\n")
        
        # Save output if file specified
        if output_file:
            save_output_data(output, output_file)
            print(f"Output saved to: {output_file}")
        
        return output
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in input file: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyError as e:
        print(f"Error: Missing required field in input: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_file.json> [output_file.json]")
        print("\nExample:")
        print("  python main.py base_case.json")
        print("  python main.py test_case_1.json output.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    main(input_file, output_file)
