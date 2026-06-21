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
    print("DEBUG past_incidents in reporter:", state.get("past_incidents"))

    prompt = f"""
    You are a disaster response communications officer. Write a SITREP for the CURRENT incident ONLY.

    STRICT RULES — VIOLATIONS ARE NOT ACCEPTABLE:
    - The CURRENT INCIDENT DATA below is your ONLY source for facts, numbers, and location.
    - NEVER use any location, date, casualties, or population figures from past incidents.
    - Past incidents are provided ONLY to inform resource and strategy decisions.
    - Current Location is: {state.get("location")} — use this, nothing else.
    - Current Casualties are: {state.get("casualties")} dead — use this exact number.
    - Current Injuries are: {state.get("injuries")} injured — use this exact number.
    - Current Affected Population: {state.get("affected_population")} — use this exact number.
    - If a value is None, write "Not yet confirmed".

    The SITREP should have these sections:
    1. INCIDENT SUMMARY
    2. CURRENT SITUATION
    3. CASUALTIES & AFFECTED POPULATION
    4. RESPONSE ACTIONS TAKEN
    5. RESOURCES DEPLOYED
    6. CRITICAL RISKS & GAPS
    7. NEXT STEPS & ESTIMATED RESOLUTION
    8. LESSONS FROM SIMILAR INCIDENTS (use past incidents here ONLY)

    After section 7, you MUST include this section:

    **LESSONS FROM SIMILAR INCIDENTS**
    Based on the past similar incidents provided, list 2-3 specific lessons or strategies 
    that should be applied to this response. Reference the past incident location and type explicitly.
    If no similar incidents were found, write "No historical precedent available."

    CURRENT INCIDENT DATA:
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

    PAST SIMILAR INCIDENTS (for section 8 ONLY):
    {state.get("past_incidents") or "No similar past incidents found."}
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
        "agent_logs": [log_entry],
    }