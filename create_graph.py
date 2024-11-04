import spacy
import json
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
import pandas as pd

nlp = spacy.load("en_core_web_sm")

def extract_entities(transcript):
    doc = nlp(transcript)
    relationships = []

    all_politicians = []
    all_organizations = []
    politicians = []
    organizations = []
    locations = []
    nationalities = []
    money = []
    dates = []
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            politicians.append(ent.text)
        elif ent.label_ == "ORG":
            organizations.append(ent.text)
        elif ent.label_ == "GPE":
            locations.append(ent.text)
        elif ent.label_ == "NORP":
            nationalities.append(ent.text)
        elif ent.label_ == "MONEY":
            money.append(ent.text)
        elif ent.label_ == "DATE":
            dates.append(ent.text)

    # Remove duplicates and add to overall lists
    politicians = list(set(politicians))
    organizations = list(set(organizations))
    locations = list(set(locations))
    nationalities = list(set(nationalities))
    money = list(set(money))
    dates = list(set(dates))
    all_politicians.extend(politicians)
    all_organizations.extend(organizations)



    for sent in doc.sents:
    # Check for relevant entities in the sentence
        sentence_politicians = [ent.text for ent in sent.ents if ent.label_ == "PERSON"]
        sentence_organizations = [ent.text for ent in sent.ents if ent.label_ == "ORG"]
        sentence_locations = [ent.text for ent in sent.ents if ent.label_ == "GPE"]
        sentence_nationalities = [ent.text for ent in sent.ents if ent.label_ == "NORP"]
        sentence_money = [ent.text for ent in sent.ents if ent.label_ == "MONEY"]
        sentence_dates = [ent.text for ent in sent.ents if ent.label_ == "DATE"]

        if sentence_politicians and sentence_organizations:
            for politician in sentence_politicians:
                for organization in sentence_organizations:
                    relationships.append((politician, organization, "works_with", sent.text))

        if sentence_politicians and sentence_locations:
            for politician in sentence_politicians:
                for location in sentence_locations:
                    relationships.append((politician, location, "located_in", sent.text))

        if sentence_politicians and sentence_nationalities:
            for politician in sentence_politicians:
                for nationality in sentence_nationalities:
                    relationships.append((politician, nationality, "is", sent.text))

        if sentence_politicians and sentence_money:
            for politician in sentence_politicians:
                for money in sentence_money:
                    relationships.append((politician, money, "received", sent.text))

        if sentence_politicians and sentence_dates:
            for politician in sentence_politicians:
                for date in sentence_dates:
                    relationships.append((politician, date, "active_on", sent.text))

        if sentence_organizations and sentence_locations:
            for organization in sentence_organizations:
                for location in sentence_locations:
                    relationships.append((organization, location, "operates_in", sent.text))

        if sentence_organizations and sentence_nationalities:
            for organization in sentence_organizations:
                for nationality in sentence_nationalities:
                    relationships.append((organization, nationality, "associated_with", sent.text))

        if sentence_organizations and sentence_money:
            for organization in sentence_organizations:
                for money in sentence_money:
                    relationships.append((organization, money, "funding", sent.text))

        if sentence_locations and sentence_dates:
            for location in sentence_locations:
                for date in sentence_dates:
                    relationships.append((location, date, "relevant_date", sent.text))

        if sentence_nationalities and sentence_dates:
            for nationality in sentence_nationalities:
                for date in sentence_dates:
                    relationships.append((nationality, date, "observed_on", sent.text))

    # Convert relationships to DataFrame
    df_relationships = pd.DataFrame(relationships, columns=['Entity1', 'Entity2', 'Relationship', 'Context'])  
    return df_relationships

G = nx.Graph()
video_data_list = []
with open('recorder_channel_videos.jsonl', 'r', encoding='utf-8') as file:
    for line in tqdm(file):
        video_data = json.loads(line)
        data =  video_data['transcript']
        df_relationships = extract_entities(data)

        for _, row in df_relationships.iterrows():
            G.add_edge(row['Entity1'], row['Entity2'], relationship=row['Relationship'], context=row['Context'])

# Draw the graph
largest_component = max(nx.connected_components(G), key=len)
subgraph = G.subgraph(largest_component)
plt.figure(figsize=(40, 23), dpi=430)
pos = nx.spring_layout(subgraph, seed=16)
nx.draw(subgraph, pos, with_labels=True, node_size=400, node_color='yellow', font_size=3, font_color='black', font_weight='bold', edge_color='red')

# Add title
plt.title("Graficul persoanelor, scandalurilor și instituțiilor")
plt.savefig('graph_people_scandals_institutions.png', format='png', dpi=430)
plt.close()