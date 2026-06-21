import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from state import DisasterState
from datetime import datetime


llm = ChatOllama(model="llama3.2", temperature=0)

def reporter_agent(state: DisasterState) -> DisasterState:
    print("📝 Reporter Agent running...")

    prompt = f"""
    You are a disaster response communications officer. Based on all the data below, write a clear and concise situation report (SITREP).

    CRITICAL RULES:
    - Use ONLY the exact numbers provided below. Do not say "None" if a number is provided.
    - If a value is None or null, write "Not yet confirmed" instead.
    - Never contradict the data provided.

    The SITREP should have these sections:
    1. INCIDENT SUMMARY
    2. CURRENT SITUATION
    3. CASUALTIES & AFFECTED POPULATION
    4. RESPONSE ACTIONS TAKEN
    5. RESOURCES DEPLOYED
    6. CRITICAL RISKS & GAPS
    7. NEXT STEPS & ESTIMATED RESOLUTION

    Full Incident Data:
    - Disaster Type: {state.get("disaster_type")}
    - Location: {state.get("location")}
    - Severity: {state.get("severity")}
    - Affected Population: {state.get("affected_population")}
    - Casualties: {state.get("casualties")} dead
    - Injuries: {state.get("injuries")} injured
    - Weather Conditions: {state.get("weather_conditions")}
    - Infrastructure Damage: {', '.join(state.get("infrastructure_damage") or [])}
    - Resources Needed: {', '.join(state.get("resources_needed") or [])}
    - Resources Available: {', '.join(state.get("resources_available") or [])}
    - Resource Gaps: {', '.join(state.get("resource_gaps") or [])}
    - Teams Dispatched: {', '.join(state.get("teams_dispatched") or [])}
    - Actions Taken: {', '.join(state.get("actions_taken") or [])}
    - Estimated Response Time: {state.get("estimated_response_time")}
    - Started At: {state.get("started_at")}
"""

    response = llm.invoke([HumanMessage(content=prompt)])
    
    log_entry = {
        "agent": "reporter",
        "timestamp": datetime.now().isoformat(),
        "summary": "Situation report generated"
    }

    return {
        **state,
        "situation_report": response.content,
        "current_agent": "reporter",
        "completed_at": datetime.now().isoformat(),
        "agent_logs": (state.get("agent_logs") or []) + [log_entry],
    }