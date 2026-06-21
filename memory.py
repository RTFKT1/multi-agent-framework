import json
import chromadb
from chromadb.config import Settings
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model = "llama3.2")

client = chromadb.PersistentClient(path = "./chroma_db")
collection = client.get_or_create_collection(name = "incidents")

def save_incident(state: dict, thread_id: str):
    document = f"""
    Disaster Type: {state.get("disaster_type")}
    Location: {state.get("location")}
    Severity: {state.get("severity")}
    Casualties: {state.get("casualties")} dead, {state.get("injuries")} injured
    Affected Population: {state.get("affected_population")}
    Weather: {state.get("weather_conditions")}
    Infrastructure Damage: {', '.join(state.get("infrastructure_damage") or [])}
    Resources Needed: {', '.join(state.get("resources_needed") or [])}
    Resource Gaps: {', '.join(state.get("resource_gaps") or [])}
    Teams Dispatched: {', '.join(state.get("teams_dispatched") or [])}
    Actions Taken: {', '.join(state.get("actions_taken") or [])}
    Situation Report: {state.get("situation_report")}
    """

    #Create Embedding
    vector = embeddings.embed_query(document)

    #Upload Embedding
    collection.upsert(
        ids= [thread_id],
        documents = [document],
        embeddings = [vector],
        metadatas=[{
            "disaster_type": state.get("disaster_type") or "",
            "location": state.get("location") or "",
            "severity": state.get("severity") or "",
            "casualties": state.get("casualties") or 0,
            "completed_at": state.get("completed_at") or "",
        }]
    )
    print(f"Data point uploaded to database with thread_id: {thread_id}")

    #Retrieve
def get_similar_incidents(current_state: dict, n_results: int = 3) -> list:
    query = f"""
    Disaster Type: {current_state.get("disaster_type")}
    Location: {current_state.get("location")}
    Severity: {current_state.get("severity")}
    Casualties: {current_state.get("casualties")}
    Infrastructure Damage: {', '.join(current_state.get("infrastructure_damage") or [])}
    """
            
    query_vector = embeddings.embed_query(query_vector)

    results = collection.query(
    query_embeddings=[query_vector],
    n_results=n_results,
    )

    if not results or not results["documents"][0]:
        return []
    return results["documents"][0]

def format_past_incidents(incidents: list) -> str:
    if not incidents:
        return "No similar past incidents found."

    lines = ["SIMILAR PAST INCIDENTS FOR REFERENCE:"]
    for i, incident in enumerate(incidents, 1):
        lines.append(f"\n--- Similar Incident {i} ---")
        lines.append(incident)
    return "\n".join(lines)