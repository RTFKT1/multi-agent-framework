import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from state import DisasterState
from datetime import datetime

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

def reporter_agent(state: DisasterState) -> DisasterState:
    print("📝 Reporter Agent running...")

    prompt = f"""
    You are a disaster response communications officer. Based on all the data below, write a clear and concise situation report (SITREP) that can be shared with senior officials and the public.

    The SITREP should have these sections:
    1. INCIDENT SUMMARY
    2. CURRENT SITUATION
    3. CASUALTIES & AFFECTED POPULATION
    4. RESPONSE ACTIONS TAKEN
    5. RESOURCES DEPLOYED
    6. CRITICAL RISKS & GAPS
    7. NEXT STEPS & ESTIMATED RESOLUTION

    Write in clear, professional language. Be factual and concise.

    Full Incident Data:
    - Disaster Type: {state.get("disaster_type")}
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
    - Actions Taken: {state.get("actions_taken")}
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