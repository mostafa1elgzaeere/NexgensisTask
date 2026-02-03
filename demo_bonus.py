"""
Demo script showcasing all BONUS TASKS implemented.

Run this script to see all bonus features in action:
1. Random Delivery Delays
2. ASCII Route Visualization (already in visualize.py)
3. Dynamic Agent Joining
4. Export to CSV
"""
import sys
from utils import load_input_data
from solver import DeliverySystemSolver
from csv_exporter import export_assignments_to_csv, export_summary_to_csv
from models import Agent, Location


def demo_all_bonus_features():
    """Demonstrate all bonus tasks with the base case."""
    
    print("=" * 80)
    print("BONUS TASKS DEMONSTRATION")
    print("=" * 80)
    print()
    
    # Load base case
    warehouses, agents, packages = load_input_data("base_case.json")
    
    print(f"Initial Setup: {len(warehouses)} warehouses, {len(agents)} agents, {len(packages)} packages\n")
    
    # ===================================================================
    # BONUS TASK 1: Random Delivery Delays
    # ===================================================================
    print("🎲 BONUS TASK 1: Random Delivery Delays")
    print("-" * 80)
    
    solver_with_delays = DeliverySystemSolver(
        warehouses, agents, packages,
        enable_delays=True,
        min_delay=5.0,
        max_delay=30.0
    )
    
    assignments_with_delays = solver_with_delays.solve()
    total_delay = sum(a.delay for a in assignments_with_delays)
    
    print(f"✓ Delays enabled: 5-30 seconds per delivery")
    print(f"✓ Total delivery time: {total_delay:.2f} seconds")
    print(f"✓ Average delay per package: {total_delay / len(packages):.2f} seconds")
    
    # Show first 3 assignments with delays
    print("\nSample assignments with delays:")
    for i, assignment in enumerate(assignments_with_delays[:3], 1):
        print(f"  {i}. {assignment.agent_id} → {assignment.package_id}: "
              f"{assignment.total_distance:.2f} units, delay: {assignment.delay:.2f}s")
    print()
    
    # ===================================================================
    # BONUS TASK 2: ASCII Route Visualization
    # ===================================================================
    print("🗺️  BONUS TASK 2: ASCII Route Visualization")
    print("-" * 80)
    print("✓ Implemented in visualize.py")
    print("✓ Run: python visualize.py base_case.json")
    print("✓ Shows step-by-step routes with locations and distances")
    print()
    
    # ===================================================================
    # BONUS TASK 3: Dynamic Agent Joining
    # ===================================================================
    print("🚀 BONUS TASK 3: Dynamic Agent Joining")
    print("-" * 80)
    
    solver_with_dynamic = DeliverySystemSolver(
        warehouses, agents, packages,
        enable_dynamic_agents=True
    )
    
    # Add a dynamic agent that joins after 2 packages
    new_agent = Agent(
        id="A_DYNAMIC_BACKUP",
        location=Location(x=50, y=50)  # Central location
    )
    solver_with_dynamic.add_dynamic_agent(new_agent, join_after_packages=2)
    
    print(f"✓ Dynamic agents enabled")
    print(f"✓ Agent {new_agent.id} will join after 2 packages")
    print("\nSolving with dynamic agent...")
    
    assignments_dynamic = solver_with_dynamic.solve()
    
    # Count how many packages the dynamic agent got
    dynamic_assignments = [a for a in assignments_dynamic if "DYNAMIC" in a.agent_id]
    print(f"✓ Dynamic agent received {len(dynamic_assignments)} package(s)")
    print()
    
    # ===================================================================
    # BONUS TASK 4: Export to CSV
    # ===================================================================
    print("📊 BONUS TASK 4: Export to CSV")
    print("-" * 80)
    
    # Export to CSV
    csv_file = "demo_assignments.csv"
    csv_summary_file = "demo_summary.csv"
    
    export_assignments_to_csv(
        assignments_with_delays,
        warehouses,
        agents,
        packages,
        csv_file
    )
    
    export_summary_to_csv(
        assignments_with_delays,
        agents,
        csv_summary_file
    )
    
    print(f"✓ Detailed assignments exported to: {csv_file}")
    print(f"✓ Summary statistics exported to: {csv_summary_file}")
    print()
    
    # ===================================================================
    # ALL TOGETHER
    # ===================================================================
    print("🎯 ALL BONUS TASKS TOGETHER")
    print("-" * 80)
    
    solver_all = DeliverySystemSolver(
        warehouses, agents, packages,
        enable_delays=True,
        enable_dynamic_agents=True,
        min_delay=10.0,
        max_delay=25.0
    )
    
    # Add dynamic agent
    agent_all = Agent(id="A_SUPER", location=Location(x=25, y=25))
    solver_all.add_dynamic_agent(agent_all, join_after_packages=1)
    
    print("Solving with ALL bonus features enabled...")
    assignments_all = solver_all.solve()
    
    total_distance = sum(a.total_distance for a in assignments_all)
    total_delay = sum(a.delay for a in assignments_all)
    
    print(f"\n✓ Total distance: {total_distance:.2f} units")
    print(f"✓ Total delays: {total_delay:.2f} seconds")
    print(f"✓ Packages: {len(assignments_all)}")
    print(f"✓ Active agents: {len(set(a.agent_id for a in assignments_all))}")
    
    # Export combined results
    export_assignments_to_csv(
        assignments_all,
        warehouses,
        agents,
        packages,
        "demo_all_features.csv"
    )
    print(f"✓ Combined results exported to: demo_all_features.csv")
    
    print("\n" + "=" * 80)
    print("🎉 ALL BONUS TASKS SUCCESSFULLY DEMONSTRATED!")
    print("=" * 80)
    print("\nTo use in main.py:")
    print("  python main.py base_case.json --delays --dynamic-agents --csv results.csv")


if __name__ == "__main__":
    demo_all_bonus_features()
