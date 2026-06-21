import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from state import DisasterState
from datetime import datetime
import json

import re

def parse_llm_json(content: str) -> dict:
    content = content.strip()
    content = re.sub(r"```json|```", "", content).strip()
    
    match = re.search(r"\{.*", content, re.DOTALL)
    if match:
        content = match.group(0)
    
    # Fix trailing commas
    content = re.sub(r",\s*}", "}", content)
    content = re.sub(r",\s*]", "]", content)
    
    # Add missing closing brace if needed
    open_braces = content.count("{")
    close_braces = content.count("}")
    if open_braces > close_braces:
        content += "}" * (open_braces - close_braces)

    return json.loads(content)

llm = ChatOllama(model="llama3.2", temperature=0)

def coordinator_agent(state: DisasterState) -> DisasterState:
    print("🎯 Coordinator Agent running...")

    prompt = f"""
    You are a disaster response coordinator. Based on all available data, create a coordinated action plan assigning teams and sequencing response efforts.

    Respond ONLY with a valid JSON object with these exact fields:
    {{
    "coordinated_actions": ["First action to take", "Second action to take"],
    "team_assignments": {{
        "team_name": "assigned_task"
    }},
    "escalation_required": true/false,
    "escalation_reason": "reason if escalation needed or null",
    "estimated_resolution_time": "e.g. 12 hours, 3 days",
    "resource_gaps": ["Resource that is missing", "Another gap"],
    "notes": "any additional coordination notes"
    }}

    Full Incident Data:
    - Disaster Type: {state.get("disaster_type")}
    - Past Similar Incidents:{state.get("past_incidents") or "No similar past incidents found."}
    Use the past incidents above to inform your coordination decisions — 
    what worked before, what resource gaps occurred, and what to avoid.
    - Location: {state.get("location")}
    - Severity: {state.get("severity")}
    - Affected Population: {state.get("affected_population")}
    - Casualties: {state.get("casualties")}
    - Injuries: {state.get("injuries")}
    - Weather Conditions: {state.get("weather_conditions")}
    - Infrastructure Damage: {state.get("infrastructure_damage")}
    - Resources Needed: {state.get("resources_needed")}
    - Resources Available: {state.get("resources_available")}
    - Teams Dispatched: {state.get("teams_dispatched")}
    - Priority Actions: {state.get("actions_taken")}
    - Estimated Response Time: {state.get("estimated_response_time")}
    """

    response = llm.invoke([HumanMessage(content=prompt)])

    try:
        extracted = parse_llm_json(response.content)
    except json.JSONDecodeError as e:
        print(f"❌ JSON parse error: {e}")
        print(f"Raw response: {response.content}")
        extracted = {}

    log_entry = {
        "agent": "coordinator",
        "timestamp": datetime.now().isoformat(),
        "summary": f"Action plan created, escalation required: {extracted.get('escalation_required')}, ERT: {extracted.get('estimated_resolution_time')}"
    }

    return {
        **state,
        "actions_taken": extracted.get("coordinated_actions", []),
        "current_agent": "coordinator",
        "resource_gaps": extracted.get("resource_gaps", []), 
        "agent_logs": [log_entry],
    }