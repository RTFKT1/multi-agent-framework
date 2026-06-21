from graph import build_graph
from datetime import datetime

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
    print(f"Report received at: {datetime.now().isoformat()}")
    print()

    # Build and run the graph
    graph = build_graph()
    
    final_state = graph.invoke({
        "raw_report": raw_report,
        "agent_logs": [],
        "errors": [],
    })

        # Add this temporarily in main.py after graph.invoke
    print("\n--- DEBUG STATE ---")
    print("Casualties:", final_state.get("casualties"))
    print("Affected Population:", final_state.get("affected_population"))
    print("Severity:", final_state.get("severity"))
    print("Disaster Type:", final_state.get("disaster_type"))

    # Print agent trail
    print()
    print("=" * 60)
    print("📋 AGENT TRAIL")
    print("=" * 60)
    for log in final_state.get("agent_logs", []):
        print(f"[{log['timestamp']}] {log['agent'].upper()}: {log['summary']}")

    print()
    print("=" * 60)
    print("📄 FINAL SITUATION REPORT")
    print("=" * 60)
    print(final_state.get("situation_report"))

if __name__ == "__main__":
    main()