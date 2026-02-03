"""
Delivery system solver implementing package-to-agent assignment optimization.

This module contains the core business logic for assigning packages to agents
to minimize total delivery distance.
"""
from typing import Dict, List, Tuple
from models import Warehouse, Agent, Package, Assignment
from utils import calculate_trip_distance


class DeliverySystemSolver:
    """
    Solves the delivery optimization problem.
    
    Assigns packages to agents to minimize total travel distance.
    Uses a greedy algorithm that iteratively assigns each package to the agent
    that can deliver it with minimum additional distance.
    
    Assumptions:
    1. Each package is assigned to exactly one agent
    2. Each agent can deliver multiple packages
    3. Agents travel: current_location -> warehouse -> destination for each package
    4. The goal is to minimize total distance traveled by all agents
    5. No capacity constraints on agents
    6. No time windows or priority constraints
    """
    
    def __init__(self, warehouses: Dict[str, Warehouse], 
                 agents: Dict[str, Agent], 
                 packages: List[Package]):
        """
        Initialize the solver with problem data.
        
        Args:
            warehouses: Dictionary mapping warehouse IDs to Warehouse objects
            agents: Dictionary mapping agent IDs to Agent objects
            packages: List of Package objects to be delivered
        """
        self.warehouses = warehouses
        self.agents = agents
        self.packages = packages
        
    def solve(self) -> List[Assignment]:
        """
        Solve the delivery assignment problem using a greedy algorithm.
        
        Algorithm:
        For each package:
            1. Calculate the delivery distance for each agent
            2. Assign the package to the agent with minimum distance
            3. Update agent's location to the package destination
        
        This is a greedy approach that provides a good approximate solution
        in O(n * m) time where n = packages, m = agents.
        
        Returns:
            List of Assignment objects representing optimal assignments
            
        Raises:
            ValueError: If warehouse for a package doesn't exist
        """
        assignments = []
        # Track current location of each agent (updated as they get assigned packages)
        agent_locations = {aid: agent.location for aid, agent in self.agents.items()}
        
        for package in self.packages:
            # Get warehouse location for this package
            if package.warehouse_id not in self.warehouses:
                raise ValueError(f"Warehouse {package.warehouse_id} not found for package {package.id}")
            
            warehouse = self.warehouses[package.warehouse_id]
            
            # Find the best agent for this package
            best_agent_id = None
            min_distance = float('inf')
            
            for agent_id, current_location in agent_locations.items():
                # Calculate total distance if this agent delivers this package
                distance = calculate_trip_distance(
                    current_location,
                    warehouse.location,
                    package.destination
                )
                
                if distance < min_distance:
                    min_distance = distance
                    best_agent_id = agent_id
            
            # Create assignment
            assignment = Assignment(
                agent_id=best_agent_id,
                package_id=package.id,
                warehouse_id=package.warehouse_id,
                total_distance=min_distance
            )
            assignments.append(assignment)
            
            # Update agent's location to the package destination
            # Assumption: After delivering a package, the agent is at the destination
            agent_locations[best_agent_id] = package.destination
        
        return assignments
    
    def calculate_total_distance(self, assignments: List[Assignment]) -> float:
        """
        Calculate total distance for all assignments.
        
        Args:
            assignments: List of Assignment objects
            
        Returns:
            Sum of all assignment distances
        """
        return sum(a.total_distance for a in assignments)
    
    def get_assignments_by_agent(self, assignments: List[Assignment]) -> Dict[str, List[Assignment]]:
        """
        Group assignments by agent.
        
        Args:
            assignments: List of Assignment objects
            
        Returns:
            Dictionary mapping agent IDs to their list of assignments
        """
        result = {agent_id: [] for agent_id in self.agents.keys()}
        for assignment in assignments:
            result[assignment.agent_id].append(assignment)
        return result


def format_output(assignments: List[Assignment], 
                  warehouses: Dict[str, Warehouse],
                  agents: Dict[str, Agent],
                  packages: List[Package]) -> dict:
    """
    Format the solution output in a structured way.
    
    Args:
        assignments: List of Assignment objects
        warehouses: Dictionary of warehouses
        agents: Dictionary of agents
        packages: List of packages
        
    Returns:
        Dictionary with formatted output data
    """
    # Group assignments by agent
    agent_assignments = {}
    for agent_id in agents.keys():
        agent_assignments[agent_id] = []
    
    for assignment in assignments:
        agent_assignments[assignment.agent_id].append({
            'package_id': assignment.package_id,
            'warehouse_id': assignment.warehouse_id,
            'distance': round(assignment.total_distance, 2)
        })
    
    # Calculate total distance
    total_distance = sum(a.total_distance for a in assignments)
    
    # Build output structure
    output = {
        'total_distance': round(total_distance, 2),
        'assignments': agent_assignments,
        'statistics': {
            'total_packages': len(packages),
            'total_agents': len(agents),
            'total_warehouses': len(warehouses),
            'average_distance_per_package': round(total_distance / len(packages), 2) if packages else 0
        }
    }
    
    return output
