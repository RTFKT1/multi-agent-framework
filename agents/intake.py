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

llm = ChatOllama(model = "llama3.2", temperature = 0)

def intake_agent(state: DisasterState) -> DisasterState:
    print("🚨 Intake Agent is Running...")

    prompt = f"""
    You are a disaster response intake officer. Read the following incident report and extract key information.

    Respond ONLY with a valid JSON object with these exact fields:
    {{
    "disaster_type": "flood/fire/earthquake/hurricane/other",
    "location": "extracted location string",
    "severity": "critical/high/medium/low",
    "affected_population": <integer — total number of people impacted, displaced, trapped, or at risk. Look for any population figure in the report>,
    "casualties": <integer or null>,
    "injuries": <integer or null>,
    "weather_conditions": "description or null",
    "infrastructure_damage": ["list", "of", "damaged", "infrastructure"]
    }}

    Incident Report:
    {state["raw_report"]}
    """

    response = llm.invoke([HumanMessage(content = prompt)])
    print("Raw intake response:", response.content)
    try:
        extracted = parse_llm_json(response.content)
    except json.JSONDecodeError as e:
        print(f"❌ JSON parse error: {e}")
        print(f"Raw response: {response.content}")
        extracted = {}

    #LogEntry
    log_entry = {
        "agent" : "intake",
        "timestamp" : datetime.now().isoformat(),
        "summary": f"Extracted {extracted.get('disaster_type')} in {extracted.get('location')}, severity: {extracted.get('severity')}"
    }

    return {
        **state,
        "disaster_type": extracted.get("disaster_type"),
        "location": extracted.get("location"),
        "severity": extracted.get("severity"),
        "affected_population": extracted.get("affected_population"),
        "casualties": extracted.get("casualties"),
        "injuries": extracted.get("injuries"),
        "weather_conditions": extracted.get("weather_conditions"),
        "infrastructure_damage": extracted.get("infrastructure_damage", []),
        "current_agent": "intake",
        "agent_logs": (state.get("agent_logs") or []) + [log_entry],
        "started_at": state.get("started_at") or datetime.now().isoformat(),
    }
