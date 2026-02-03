"""
Data models for the delivery system.
Defines core entities: Location, Warehouse, Agent, Package, and Assignment.
"""
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Location:
    """Represents a 2D coordinate location."""
    x: float
    y: float
    
    def to_tuple(self) -> Tuple[float, float]:
        """Convert location to tuple format."""
        return (self.x, self.y)
    
    @staticmethod
    def from_list(coords: List[float]) -> 'Location':
        """Create Location from a list [x, y]."""
        return Location(x=coords[0], y=coords[1])
    
    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"


@dataclass
class Warehouse:
    """Represents a warehouse with an ID and location."""
    id: str
    location: Location
    
    def __repr__(self) -> str:
        return f"Warehouse({self.id} at {self.location})"


@dataclass
class Agent:
    """Represents a delivery agent with an ID and current location."""
    id: str
    location: Location
    
    def __repr__(self) -> str:
        return f"Agent({self.id} at {self.location})"


@dataclass
class Package:
    """Represents a package that needs to be delivered."""
    id: str
    warehouse_id: str
    destination: Location
    
    def __repr__(self) -> str:
        return f"Package({self.id} from {self.warehouse_id} to {self.destination})"


@dataclass
class Assignment:
    """
    Represents an assignment of a package to an agent.
    
    Attributes:
        agent_id: ID of the assigned agent
        package_id: ID of the package to deliver
        total_distance: Total distance the agent needs to travel
                       (agent location -> warehouse -> destination)
        delay: Random delivery delay in seconds (for simulation)
        timestamp: When this assignment was made (for dynamic agents)
    """
    agent_id: str
    package_id: str
    warehouse_id: str
    total_distance: float
    delay: float = 0.0
    timestamp: int = 0
    
    def __repr__(self) -> str:
        return (f"Assignment({self.agent_id} delivers {self.package_id} "
                f"from {self.warehouse_id}, distance: {self.total_distance:.2f}, "
                f"delay: {self.delay:.2f}s)")
