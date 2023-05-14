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

def execute_custom_query():
    query = custom_query_entry.get("1.0", "end-1c")
    results = execute_sparql(query)
    treeview.delete(*treeview.get_children())
    for result in results:
        for var_name, var_value in result.items():
            treeview.insert("", "end", values=(var_name, var_value["value"]))

# Create the main window
window = Tk()
window.title("Country Explorer")

# Create and place widgets for country search
country_label = Label(window, text="Entrez le nom du pays:")
country_label.pack()
country_entry = Entry(window)
country_entry.pack()
search_button = Button(window, text="Recherche", command=search_country)
search_button.pack()

# Create and place widgets for custom query
custom_query_label = Label(window, text="Entrez une requête SPARQL personnalisée:")
custom_query_label.pack()
custom_query_entry = Text(window, height=5)
custom_query_entry.pack()
execute_query_button = Button(window, text="Exécuter la requête", command=execute_custom_query)
execute_query_button.pack()

# Create a treeview to display the properties and their values
treeview = ttk.Treeview(window, columns=("Variable", "Valeur"), show="headings")
treeview.heading("Variable", text="Variable")
treeview.heading("Valeur", text="Valeur")
treeview.pack()

# Start the Tkinter event loop
window.mainloop()