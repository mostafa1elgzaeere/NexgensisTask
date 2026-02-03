"""
Utility functions for the delivery system.
Provides distance calculations, JSON parsing, and data loading.
"""
import json
import math
from pathlib import Path
from typing import Dict, List, Tuple

from models import Location, Warehouse, Agent, Package


def euclidean_distance(loc1: Location, loc2: Location) -> float:
    """
    Calculate Euclidean distance between two locations.
    
    Args:
        loc1: First location
        loc2: Second location
        
    Returns:
        Euclidean distance as a float
    """
    return math.sqrt((loc1.x - loc2.x) ** 2 + (loc1.y - loc2.y) ** 2)


def calculate_trip_distance(agent_loc: Location, warehouse_loc: Location, 
                           destination: Location) -> float:
    """
    Calculate total distance for a delivery trip.
    Trip: agent location -> warehouse -> destination
    
    Args:
        agent_loc: Starting location of the agent
        warehouse_loc: Warehouse location to pick up package
        destination: Final delivery destination
        
    Returns:
        Total distance for the complete trip
    """
    dist_to_warehouse = euclidean_distance(agent_loc, warehouse_loc)
    dist_to_destination = euclidean_distance(warehouse_loc, destination)
    return dist_to_warehouse + dist_to_destination


def load_input_data(file_path: str) -> Tuple[Dict[str, Warehouse], 
                                              Dict[str, Agent], 
                                              List[Package]]:
    """
    Load and parse input JSON file.
    
    Handles both formats:
    - Format 1: warehouses/agents as list of dicts with 'id' and 'location'
    - Format 2: warehouses/agents as dict with id as key and location as value
    
    Args:
        file_path: Path to the JSON input file
        
    Returns:
        Tuple of (warehouses dict, agents dict, packages list)
        
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If JSON is malformed
        KeyError: If required fields are missing
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Parse warehouses
    warehouses = {}
    warehouse_data = data.get('warehouses', {})
    
    if isinstance(warehouse_data, list):
        # Format 1: List of objects with 'id' and 'location'
        for w in warehouse_data:
            wid = w['id']
            loc = Location.from_list(w['location'])
            warehouses[wid] = Warehouse(id=wid, location=loc)
    else:
        # Format 2: Dict with id as key, location as value
        for wid, coords in warehouse_data.items():
            loc = Location.from_list(coords)
            warehouses[wid] = Warehouse(id=wid, location=loc)
    
    # Parse agents
    agents = {}
    agent_data = data.get('agents', {})
    
    if isinstance(agent_data, list):
        # Format 1: List of objects with 'id' and 'location'
        for a in agent_data:
            aid = a['id']
            loc = Location.from_list(a['location'])
            agents[aid] = Agent(id=aid, location=loc)
    else:
        # Format 2: Dict with id as key, location as value
        for aid, coords in agent_data.items():
            loc = Location.from_list(coords)
            agents[aid] = Agent(id=aid, location=loc)
    
    # Parse packages
    packages = []
    package_data = data.get('packages', [])
    
    for p in package_data:
        pid = p['id']
        # Handle both 'warehouse' and 'warehouse_id' field names
        wid = p.get('warehouse', p.get('warehouse_id'))
        dest = Location.from_list(p['destination'])
        packages.append(Package(id=pid, warehouse_id=wid, destination=dest))
    
    return warehouses, agents, packages


def save_output_data(output_data: dict, file_path: str) -> None:
    """
    Save output data to JSON file.
    
    Args:
        output_data: Dictionary containing the output data
        file_path: Path where to save the output
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
