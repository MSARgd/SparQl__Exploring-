import tkinter as tk
from tkinter import *
from SPARQLWrapper import SPARQLWrapper, JSON

# SPARQL endpoint URL
DBPEDIA_ENDPOINT = "https://dbpedia.org/sparql"

def execute_sparql(query):
    sparql = SPARQLWrapper(DBPEDIA_ENDPOINT)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results["results"]["bindings"]

def get_country_info(country):
    query = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        SELECT ?property ?value
        WHERE {{
            <http://dbpedia.org/resource/{country}> ?property ?value
        }}
    """
    results = execute_sparql(query)
    country_info = {}
    for result in results:
        property_name = result["property"]["value"].split("/")[-1]
        property_value = result["value"]["value"]
        country_info[property_name] = property_value
    return country_info

def search_country():
    country = country_entry.get()
    country_info = get_country_info(country)
    country_info_text.delete("1.0", END)
    if country_info:
        for property_name, property_value in country_info.items():
            country_info_text.insert(END, f"{property_name}: {property_value}\n")
    else:
        country_info_text.insert(END, "Aucune information n’a été trouvée pour le pays.")

# Create the main window
window = Tk()
window.title("Country Explorer")

# Create and place widgets
country_label = Label(window, text="Entrez le nom du pays:")
country_label.pack()
country_entry = Entry(window)
country_entry.pack()

search_button = Button(window, text="Search", command=search_country)
search_button.pack()

country_info_text = Text(window)
country_info_text.pack()

# Configure the widget placement
window.columnconfigure(0, weight=1)
window.rowconfigure(3, weight=1)

# Start the Tkinter event loop
window.mainloop()
