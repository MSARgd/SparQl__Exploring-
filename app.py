import tkinter as tk
from tkinter import *
from tkinter import ttk
from SPARQLWrapper import SPARQLWrapper, JSON

# SPARQL endpoint URL
DBPEDIA_ENDPOINT = "https://dbpedia.org/sparql"

# Function to execute SPARQL queries
def execute_sparql(query):
    sparql = SPARQLWrapper(DBPEDIA_ENDPOINT)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results["results"]["bindings"]

# Function to retrieve entity information from selected category
def get_entity_info(category, entity):
    # Modify the query to include the selected category
    query = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        SELECT ?property ?value
        WHERE {{
            dbr:{entity} dbo:category ?category.
           ?category rdfs:label "{category_combobox.get()}"@en.
            dbr:{entity} ?property ?value.
        }}
    """
    results = execute_sparql(query)
    entity_info = {}
    for result in results:
        property_name = result["property"]["value"].split("/")[-1]
        property_value = result["value"]["value"]
        entity_info[property_name] = property_value
    return entity_info

# Function to handle the search button click
def search_entity():
    category = category_combobox.get()
    entity = entity_entry.get()
    entity_info = get_entity_info(category, entity)
    entity_info_text.delete("1.0", END)
    if entity_info:
        for property_name, property_value in entity_info.items():
            entity_info_text.insert(END, f"{property_name}: {property_value}\n")
    else:
        entity_info_text.insert(END, "No information found for the entity.")

# Create the main window
window = Tk()
window.title("DBpedia Explorer")

# Create and place widgets
category_label = Label(window, text="Select a category:")
category_label.pack()
category_combobox = ttk.Combobox(window, values=["books", "countries", "films", "scientists"])
category_combobox.pack()

entity_label = Label(window, text="Enter the entity name:")
entity_label.pack()
entity_entry = Entry(window)
entity_entry.pack()

search_button = Button(window, text="Search", command=search_entity)
search_button.pack()

entity_info_text = Text(window)
entity_info_text.pack()

# Start the Tkinter event loop
window.mainloop()


# ============================================================
# import tkinter as tk
# from tkinter import *
# from tkinter import ttk
# from SPARQLWrapper import SPARQLWrapper, JSON
#
# # SPARQL endpoint URL
# DBPEDIA_ENDPOINT = "https://dbpedia.org/sparql"
#
# # Function to execute SPARQL queries
# def execute_sparql(query):
#     sparql = SPARQLWrapper(DBPEDIA_ENDPOINT)
#     sparql.setQuery(query)
#     sparql.setReturnFormat(JSON)
#     results = sparql.query().convert()
#     return results["results"]["bindings"]
#
# # Function to retrieve entity information from selected category
# def get_entity_info(category, entity):
#     # Modify the query to include the selected category
#     query = f"""
#         PREFIX dbo: <http://dbpedia.org/ontology/>
#         PREFIX dbr: <http://dbpedia.org/resource/>
#         SELECT ?property ?value
#         WHERE {{
#             dbr:{entity} dbo:category dbr:{category}.
#             dbr:{entity} ?property ?value
#         }}
#     """
#     results = execute_sparql(query)
#     entity_info = {}
#     for result in results:
#         property_name = result["property"]["value"].split("/")[-1]
#         property_value = result["value"]["value"]
#         entity_info[property_name] = property_value
#     return entity_info
#
# # Function to handle the search button click
# def search_entity():
#     category = category_combobox.get()
#     entity = entity_entry.get()
#     entity_info = get_entity_info(category, entity)
#     entity_info_text.delete("1.0", END)
#     if entity_info:
#         for property_name, property_value in entity_info.items():
#             entity_info_text.insert(END, f"{property_name}: {property_value}\n")
#     else:
#         entity_info_text.insert(END, "No information found for the entity.")
#
# # Create the main window
# window = Tk()
# window.title("DBpedia Explorer")
#
# # Create and place widgets
# category_label = Label(window, text="Select a category:")
# category_label.pack()
# category_combobox = ttk.Combobox(window, values=["books", "countries", "films", "scientists"])
# category_combobox.pack()
#
# entity_label = Label(window, text="Enter the entity name:")
# entity_label.pack()
# entity_entry = Entry(window)
# entity_entry.pack()
#
# search_button = Button(window, text="Search", command=search_entity)
# search_button.pack()
#
# entity_info_text = Text(window)
# entity_info_text.pack()
#
# # Start the Tkinter event loop
# window.mainloop()

























# ====================

