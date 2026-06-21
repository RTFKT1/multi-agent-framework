from graph import build_graph
from memory import save_incident, get_similar_incidents, format_past_incidents
from datetime import datetime
import uuid

def main():
    print("📋 Paste the incident report below, then press Enter twice when done:")
    print()

    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)

    raw_report = "\n".join(lines)

    if not raw_report.strip():
        print("❌ No report provided. Exiting.")
        return
    
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