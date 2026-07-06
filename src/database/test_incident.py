from src.database.incidents import create_incident, fetch_incidents

create_incident(1)

incidents = fetch_incidents()

for incident in incidents:
    print(incident)