from typing import TypedDict, List, Optional, Annotated
import operator

class AgentLog(TypedDict):
    agent: str
    timestamp: str
    summary: str

class DisasterState(TypedDict):
    # Input
    raw_report: str

    #Past Incidents
    past_incidents: Optional[str]
    
    # Triage
    disaster_type: Optional[str]
    severity: Optional[str]
    location: Optional[str]
    affected_population: Optional[int]
    casualties: Optional[int]        # ← fixed spelling
    injuries: Optional[int]
    # Environmental
    weather_conditions: Optional[str]
    infrastructure_damage: Optional[List[str]]   # ← added
    # Resources
    resources_needed: Optional[List[str]]        # ← added
    resources_available: Optional[List[str]]
    # Coordination
    teams_dispatched: Optional[List[str]]
    resource_gaps: Optional[List[str]]
    actions_taken: Optional[List[str]]
    estimated_response_time: Optional[str]       # ← renamed from response_time
    # Reporting
    situation_report: Optional[str]
    # Control and Audit
    current_agent: Optional[str]
    agent_logs: Annotated[List, operator.add]
    errors: Optional[List[str]]
    started_at: Optional[str]
    completed_at: Optional[str]