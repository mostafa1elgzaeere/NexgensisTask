"""
Optional: Simple visualization of the delivery system solution.
Generates a text-based representation of assignments.
"""
from pathlib import Path
from utils import load_input_data
from solver import DeliverySystemSolver


def visualize_solution(input_file: str) -> None:
    """
    Create a text visualization of the delivery solution.
    
    Args:
        input_file: Path to input JSON file
    """
    warehouses, agents, packages = load_input_data(input_file)
    solver = DeliverySystemSolver(warehouses, agents, packages)
    assignments = solver.solve()
    
    # Group by agent
    agent_assignments = {}
    for agent_id in agents.keys():
        agent_assignments[agent_id] = []
    
    for assignment in assignments:
        agent_assignments[assignment.agent_id].append(assignment)
    
    print(f"\n{'='*80}")
    print(f"DELIVERY VISUALIZATION: {Path(input_file).name}")
    print(f"{'='*80}\n")
    
    # Show initial state
    print("INITIAL STATE:")
    print("-" * 80)
    for agent_id, agent in agents.items():
        print(f"  {agent_id}: at location {agent.location}")
    print()
    
    for warehouse_id, warehouse in warehouses.items():
        pkgs = [p.id for p in packages if p.warehouse_id == warehouse_id]
        print(f"  {warehouse_id}: at {warehouse.location}, has packages {pkgs}")
    print()
    
    # Show assignments
    print("OPTIMAL ASSIGNMENTS:")
    print("-" * 80)
    
    total_distance = 0
    total_delay = 0
    has_delays = any(a.delay > 0 for a in assignments)
    
    for agent_id in sorted(agents.keys()):
        agent_pkgs = agent_assignments[agent_id]
        if not agent_pkgs:
            print(f"\n{agent_id}: No packages assigned")
            continue
        
        agent_distance = sum(a.total_distance for a in agent_pkgs)
        agent_delay = sum(a.delay for a in agent_pkgs)
        total_distance += agent_distance
        total_delay += agent_delay
        
        delay_str = f", total delay: {agent_delay:.2f}s" if has_delays else ""
        print(f"\n{agent_id}: {len(agent_pkgs)} package(s), total distance: {agent_distance:.2f}{delay_str}")
        
        current_loc = agents[agent_id].location
        for i, assignment in enumerate(agent_pkgs, 1):
            warehouse = warehouses[assignment.warehouse_id]
            package = next(p for p in packages if p.id == assignment.package_id)
            
            delay_info = f", delay: {assignment.delay:.2f}s" if has_delays else ""
            print(f"  {i}. {assignment.package_id}:")
            print(f"     Route: {current_loc} → {warehouse.location} ({assignment.warehouse_id}) → {package.destination}")
            print(f"     Distance: {assignment.total_distance:.2f}{delay_info}")
            
            current_loc = package.destination
    
    print(f"\n{'-'*80}")
    print(f"TOTAL DISTANCE: {total_distance:.2f} units")
    if has_delays:
        print(f"TOTAL DELAYS: {total_delay:.2f} seconds")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        # Default to base case
        input_file = "base_case.json"
    else:
        input_file = sys.argv[1]
    
    visualize_solution(input_file)
