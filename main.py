from graph import build_graph
from memory import save_incident, get_similar_incidents, format_past_incidents
from datetime import datetime
import uuid

raw_report = """
On the morning of June 21, 2026, a 6.8 magnitude earthquake struck the city of 
Karachi, Pakistan. Initial reports indicate widespread structural damage across 
residential and commercial areas. The Lyari and Korangi districts are the most 
affected with buildings collapsed trapping an estimated 2,000 residents. 

Casualties are reported at 150 dead and over 600 injured. Major roads including 
Shahrae Faisal and the Northern Bypass are blocked due to debris. The city hospital 
has sustained partial damage and is operating at limited capacity. Power is out 
across 60% of the city. Weather conditions show strong winds at 45km/h with 
temperatures at 38°C making rescue operations difficult.
"""

def main():
    print("=" * 60)
    print("🚨 DISASTER RESPONSE SYSTEM ACTIVATED")
    print("=" * 60)

    # Unique ID for this run
    thread_id = str(uuid.uuid4())
    print(f"Thread ID: {thread_id}")
    print(f"Report received at: {datetime.now().isoformat()}")
    print()

    # Get similar past incidents before running
    # We do a quick pre-scan using just the raw report
    similar = get_similar_incidents({"disaster_type": None, "location": None,
                                     "severity": None, "casualties": None,
                                     "infrastructure_damage": []},
                                     n_results=3)
    past_incidents_text = format_past_incidents(similar)

    # Build and run the graph
    graph = build_graph()

    final_state = graph.invoke({
        "raw_report": raw_report,
        "past_incidents": past_incidents_text,   # ← injected into state
        "agent_logs": [],
        "errors": [],
    })

    # Print agent trail
    print()
    print("=" * 60)
    print("📋 AGENT TRAIL")
    print("=" * 60)
    for log in final_state.get("agent_logs", []):
        print(f"[{log['timestamp']}] {log['agent'].upper()}: {log['summary']}")

    # Print final SITREP
    print()
    print("=" * 60)
    print("📄 FINAL SITUATION REPORT")
    print("=" * 60)
    print(final_state.get("situation_report"))

    # Save this incident to memory
    save_incident(final_state, thread_id)

if __name__ == "__main__":
    main()