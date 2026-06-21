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

def triage_agent(state: DisasterState) -> DisasterState:
    print("🔍 Triage Agent running...")
    prompt = f"""
    You are a disaster triage specialist. Based on the extracted incident data below, assess the situation and determine response priorities.

    Respond ONLY with a valid JSON object with these exact fields:
    {{
    "severity": "critical/high/medium/low",
    "priority_actions": ["list", "of", "immediate", "actions"],
    "estimated_response_time": "e.g. 2 hours, 30 minutes",
    "critical_risks": ["list", "of", "risks", "if", "no", "action"],
    "notes": "any additional triage observations"
    }}

    Incident Data:
    - Disaster Type: {state.get("disaster_type")}
    - Location: {state.get("location")}
    - Severity: {state.get("severity")}
    - Affected Population: {state.get("affected_population")}
    - Casualties: {state.get("casualties")}
    - Injuries: {state.get("injuries")}
    - Weather Conditions: {state.get("weather_conditions")}
    - Infrastructure Damage: {state.get("infrastructure_damage")}
    """

    response = llm.invoke([HumanMessage(content=prompt)])

    try:
        extracted = parse_llm_json(response.content)
    except json.JSONDecodeError as e:
        print(f"❌ JSON parse error: {e}")
        print(f"Raw response: {response.content}")
        extracted = {}

    log_entry = {
        "agent": "triage",
        "timestamp": datetime.now().isoformat(),
        "summary": f"Severity confirmed: {extracted.get('severity')}, ETA: {extracted.get('estimated_response_time')}"
    }

    return {
        **state,
        "severity": extracted.get("severity"),
        "estimated_response_time": extracted.get("estimated_response_time"),
        "actions_taken": extracted.get("priority_actions", []),
        "current_agent": "triage",
        "agent_logs": (state.get("agent_logs") or []) + [log_entry],
    }