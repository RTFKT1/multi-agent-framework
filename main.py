from graph import build_graph
from agents.intake import intake_agent
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

    thread_id = str(uuid.uuid4())
    print(f"Thread ID: {thread_id}")
    print(f"Report received at: {datetime.now().isoformat()}\n")

    # PASS 1 — Run intake agent alone to extract key fields
    print("🔍 Pre-scanning report for memory search...")
    initial_state = {
        "raw_report": raw_report,
        "agent_logs": [],
        "errors": [],
    }
    intake_state = intake_agent(initial_state)

    # Query memory with real extracted values
    similar = get_similar_incidents(intake_state, n_results=3)
    past_incidents_text = format_past_incidents(similar)

    if similar:
        print(f"🧠 Found {len(similar)} similar past incident(s) — injecting into agents\n")
    else:
        print("🧠 No similar past incidents found\n")

    # PASS 2 — Run full graph starting from triage (intake already ran)
    graph = build_graph()
    final_state = graph.invoke({
        **intake_state,
        "past_incidents": past_incidents_text,
        "agent_logs": [],    # ← reset logs so intake doesn't appear twice
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

    # Save to memory
    save_incident(final_state, thread_id)
    print(f"\n✅ Incident saved to memory with thread ID: {thread_id}")

if __name__ == "__main__":
    main()