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

def resource_agent(state: DisasterState) -> DisasterState:
    print("📦 Resource Agent running...")

    prompt = f"""
    You are a disaster resource planning specialist. Based on the incident and triage data below, determine what resources are needed and what teams should be dispatched.

    Respond ONLY with a valid JSON object with these exact fields:
    {{
    "resources_needed": ["list", "of", "required", "resources"],
    "resources_available": ["list", "of", "typically", "available", "resources"],
    "teams_dispatched": ["list", "of", "teams", "to", "dispatch"],
    "resource_gaps": ["resources", "that", "may", "be", "unavailable"],
    "notes": "any additional resource observations"
    }}

    Incident Data:
    - Disaster Type: {state.get("disaster_type")}
    - Location: {state.get("location")}
    - Severity: {state.get("severity")}
    - Affected Population: {state.get("affected_population")}
    - Casualties: {state.get("casualties")}
    - Injuries: {state.get("injuries")}
    - Infrastructure Damage: {state.get("infrastructure_damage")}
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
        "agent": "resource",
        "timestamp": datetime.now().isoformat(),
        "summary": f"Resources identified: {len(extracted.get('resources_needed', []))} needed, {len(extracted.get('teams_dispatched', []))} teams dispatched"
    }

    return {
        **state,
        "resources_needed": extracted.get("resources_needed", []),
        "resources_available": extracted.get("resources_available", []),
        "teams_dispatched": extracted.get("teams_dispatched", []),
        "current_agent": "resource",
        "agent_logs": (state.get("agent_logs") or []) + [log_entry],
    }