import tkinter as tk
from tkinter import *
from tkinter import ttk
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
    treeview.delete(*treeview.get_children())
    if country_info:
        for property_name, property_value in country_info.items():
            treeview.insert("", "end", values=(property_name, property_value))
    else:
        treeview.insert("", "end", values=("Aucune information n’a été trouvée pour le pays.", ""))

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

# Create a treeview to display the properties and their values
treeview = ttk.Treeview(window, columns=("Property", "Value"), show="headings")
treeview.heading("Property", text="Property")
treeview.heading("Value", text="Value")
treeview.pack()

# Start the Tkinter event loop
window.mainloop()
