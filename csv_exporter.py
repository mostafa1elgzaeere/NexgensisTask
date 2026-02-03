"""
CSV Export functionality for delivery system results.
BONUS TASK: Export to CSV
"""
import csv
from pathlib import Path
from typing import List, Dict
from models import Assignment, Warehouse, Agent, Package


def export_assignments_to_csv(assignments: List[Assignment], 
                              warehouses: Dict[str, Warehouse],
                              agents: Dict[str, Agent],
                              packages: List[Package],
                              output_file: str) -> None:
    """
    Export delivery assignments to CSV format.
    
    Args:
        assignments: List of Assignment objects
        warehouses: Dictionary of warehouses
        agents: Dictionary of agents
        packages: List of packages
        output_file: Path to output CSV file
    """
    path = Path(output_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Header
        writer.writerow([
            'Agent ID', 
            'Package ID', 
            'Warehouse ID', 
            'Warehouse Location', 
            'Destination',
            'Distance',
            'Delay (seconds)'
        ])
        
        # Data rows
        for assignment in assignments:
            warehouse = warehouses[assignment.warehouse_id]
            package = next(p for p in packages if p.id == assignment.package_id)
            
            delay = getattr(assignment, 'delay', 0)
            
            writer.writerow([
                assignment.agent_id,
                assignment.package_id,
                assignment.warehouse_id,
                f"({warehouse.location.x}, {warehouse.location.y})",
                f"({package.destination.x}, {package.destination.y})",
                f"{assignment.total_distance:.2f}",
                f"{delay:.2f}"
            ])
    
    print(f"CSV exported to: {output_file}")


def export_summary_to_csv(assignments: List[Assignment],
                         agents: Dict[str, Agent],
                         output_file: str) -> None:
    """
    Export summary statistics by agent to CSV.
    
    Args:
        assignments: List of Assignment objects
        agents: Dictionary of agents
        output_file: Path to output CSV file
    """
    path = Path(output_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    # Group by agent
    agent_stats = {}
    for agent_id in agents.keys():
        agent_assignments = [a for a in assignments if a.agent_id == agent_id]
        total_distance = sum(a.total_distance for a in agent_assignments)
        total_delay = sum(getattr(a, 'delay', 0) for a in agent_assignments)
        
        agent_stats[agent_id] = {
            'packages': len(agent_assignments),
            'distance': total_distance,
            'delay': total_delay
        }
    
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Header
        writer.writerow([
            'Agent ID',
            'Packages Delivered',
            'Total Distance',
            'Total Delay (seconds)',
            'Average Distance per Package'
        ])
        
        # Data rows
        for agent_id, stats in sorted(agent_stats.items()):
            avg_distance = stats['distance'] / stats['packages'] if stats['packages'] > 0 else 0
            
            writer.writerow([
                agent_id,
                stats['packages'],
                f"{stats['distance']:.2f}",
                f"{stats['delay']:.2f}",
                f"{avg_distance:.2f}"
            ])
    
    print(f"Summary CSV exported to: {output_file}")
