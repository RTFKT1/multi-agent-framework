from typing import TypedDict, List, Optional
from datetime import datetime

class AgentLog(TypedDict):
    agent : str
    timestamp : str
    summary : str

class DisasterState(TypedDict):
    #Input
    raw_report : str

    #Triage
    disaster_type : Optional[str]
    severity : Optional[str]
    location : Optional[str]
    affected_population : Optional[str]
    casualities : Optional[str]
    injuries : Optional[str]

    #Environmental 
    weather_conditions : Optional[str]
    resources_available : Optional[List[str]]

    #Coordination
    teams_dispatched : Optional[List[str]]
    actions_taken : Optional[List[str]]
    response_time : Optional[str]

    #Reporting
    situation_report : Optional[str]

    #Control and Audit
    current_agent : Optional[str]
    agent_logs : Optional[List[AgentLog]]
    errors : Optional[List[str]]
    started_at : Optional[str]
    completed_at : Optional[str]
    

