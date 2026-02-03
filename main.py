"""
Main entry point for the Delivery System Solver.

Usage:
    python main.py <input_file.json> [options]
    
Example:
    python main.py base_case.json
    python main.py base_case.json --output output.json
    python main.py base_case.json --delays --csv results.csv
    python main.py base_case.json --delays --dynamic-agents
    
Options:
    --output FILE       Save JSON output to FILE
    --csv FILE          Export results to CSV file (BONUS TASK)
    --csv-summary FILE  Export summary statistics to CSV
    --delays            Enable random delivery delays (BONUS TASK)
    --dynamic-agents    Enable dynamic agent joining (BONUS TASK)
"""
import sys
import json
import argparse
from pathlib import Path

from utils import load_input_data, save_output_data
from solver import DeliverySystemSolver, format_output
from csv_exporter import export_assignments_to_csv, export_summary_to_csv
from models import Agent, Location


def main(input_file: str, output_file: str = None, csv_file: str = None, 
         csv_summary_file: str = None, enable_delays: bool = False, 
         enable_dynamic_agents: bool = False) -> dict:
    """
    Main execution function for the delivery system solver.
    
    Args:
        input_file: Path to input JSON file
        output_file: Optional path to save output JSON
        csv_file: Optional path to export CSV (BONUS TASK)
        csv_summary_file: Optional path to export summary CSV
        enable_delays: Enable random delivery delays (BONUS TASK)
        enable_dynamic_agents: Enable dynamic agent joining (BONUS TASK)
        
    Returns:
        Dictionary containing the solution
    """
    try:
        # Load input data
        print(f"Loading input from: {input_file}")
        warehouses, agents, packages = load_input_data(input_file)
        
        print(f"Loaded: {len(warehouses)} warehouses, {len(agents)} agents, {len(packages)} packages")
        
        # BONUS TASKS: Display enabled features
        features = []
        if enable_delays:
            features.append("Random Delays")
        if enable_dynamic_agents:
            features.append("Dynamic Agents")
        if features:
            print(f"Bonus Features Enabled: {', '.join(features)}")
        
        # Create solver with bonus features
        solver = DeliverySystemSolver(
            warehouses, 
            agents, 
            packages,
            enable_delays=enable_delays,
            enable_dynamic_agents=enable_dynamic_agents
        )
        
        # BONUS TASK: Add dynamic agents (example - adds agent after 50% of packages)
        if enable_dynamic_agents and len(packages) > 3:
            join_point = len(packages) // 2
            # Add a new agent at the center of the map
            locations = [a.location for a in agents.values()]
            avg_x = sum(loc.x for loc in locations) / len(locations)
            avg_y = sum(loc.y for loc in locations) / len(locations)
            
            new_agent = Agent(
                id=f"A{len(agents) + 1}_DYNAMIC",
                location=Location(x=avg_x, y=avg_y)
            )
            solver.add_dynamic_agent(new_agent, join_after_packages=join_point)
        
        print("Solving delivery assignment problem...")
        assignments = solver.solve()
        
        # Format output
        output = format_output(assignments, warehouses, agents, packages)
        
        # Calculate total delay if enabled
        total_delay = sum(a.delay for a in assignments) if enable_delays else 0
        
        # Display results
        print(f"\n{'='*60}")
        print("SOLUTION SUMMARY")
        print(f"{'='*60}")
        print(f"Total Distance: {output['total_distance']:.2f} units")
        print(f"Average Distance per Package: {output['statistics']['average_distance_per_package']:.2f} units")
        
        if enable_delays:
            print(f"Total Delivery Delays: {total_delay:.2f} seconds")
            print(f"Average Delay per Package: {total_delay / len(packages):.2f} seconds")
        
        print(f"\nAssignments by Agent:")
        
        for agent_id, agent_packages in output['assignments'].items():
            if agent_packages:
                agent_distance = sum(p['distance'] for p in agent_packages)
                agent_delay = sum(p.get('delay', 0) for p in agent_packages)
                
                delay_str = f", delay: {agent_delay:.2f}s" if enable_delays else ""
                dynamic_str = " (DYNAMIC)" if "DYNAMIC" in agent_id else ""
                
                print(f"\n  {agent_id}{dynamic_str}: {len(agent_packages)} package(s), distance: {agent_distance:.2f}{delay_str}")
                for pkg in agent_packages:
                    delay_info = f", delay: {pkg.get('delay', 0):.2f}s" if enable_delays else ""
                    print(f"    - {pkg['package_id']} from {pkg['warehouse_id']}, distance: {pkg['distance']:.2f}{delay_info}")
            else:
                print(f"\n  {agent_id}: No packages assigned")
        
        print(f"\n{'='*60}\n")
        
        # Save output if file specified
        if output_file:
            save_output_data(output, output_file)
            print(f"JSON output saved to: {output_file}")
        
        # BONUS TASK: Export to CSV
        if csv_file:
            export_assignments_to_csv(assignments, warehouses, agents, packages, csv_file)
        
        if csv_summary_file:
            export_summary_to_csv(assignments, agents, csv_summary_file)
        
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
    parser = argparse.ArgumentParser(
        description='Delivery System Solver with Bonus Features',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py base_case.json
  python main.py base_case.json --output result.json
  python main.py base_case.json --csv results.csv --csv-summary summary.csv
  python main.py base_case.json --delays --dynamic-agents
  python main.py base_case.json --delays --csv results.csv
        """
    )
    
    parser.add_argument('input_file', help='Input JSON file with delivery data')
    parser.add_argument('--output', '-o', help='Output JSON file')
    parser.add_argument('--csv', help='Export assignments to CSV file (BONUS TASK)')
    parser.add_argument('--csv-summary', help='Export summary statistics to CSV')
    parser.add_argument('--delays', action='store_true', 
                       help='Enable random delivery delays (BONUS TASK)')
    parser.add_argument('--dynamic-agents', action='store_true',
                       help='Enable dynamic agent joining mid-delivery (BONUS TASK)')
    
    args = parser.parse_args()
    
    main(
        input_file=args.input_file,
        output_file=args.output,
        csv_file=args.csv,
        csv_summary_file=args.csv_summary,
        enable_delays=args.delays,
        enable_dynamic_agents=args.dynamic_agents
    )
