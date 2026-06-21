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
