import tkinter as tk
from tkinter import *
import tkinter
from SPARQLWrapper import SPARQLWrapper, JSON

# SPARQL endpoint URL
SPARQL_ENDPOINTS = {
    "DBpedia": "https://dbpedia.org/sparql",
    "Other Database": "http://example.com/sparql"  # Add more databases and their endpoints here
}

def execute_sparql(endpoint, query):
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results["results"]["bindings"]

def get_resource_info(endpoint, resource):
    query = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        SELECT ?property ?value
        WHERE {{
            <http://dbpedia.org/resource/{resource}> ?property ?value
        }}
    """
    results = execute_sparql(endpoint, query)
    resource_info = {}
    for result in results:
        property_name = result["property"]["value"].split("/")[-1]
        property_value = result["value"]["value"]
        resource_info[property_name] = property_value
    return resource_info

def search_resource():
    endpoint = endpoint_var.get()
    resource = resource_entry.get()
    resource_info = get_resource_info(endpoint, resource)
    resource_info_text.delete("1.0", END)
    if resource_info:
        for property_name, property_value in resource_info.items():
            resource_info_text.insert(END, f"{property_name}: {property_value}\n")
    else:
        resource_info_text.insert(END, "No information found for the resource.")

# Create the main window
window = Tk()
window.title("Resource Explorer")

# Create and place widgets
endpoint_label = Label(window, text="Select database:")
endpoint_label.pack()
endpoint_var = StringVar()
endpoint_options = OptionMenu(window, endpoint_var, *SPARQL_ENDPOINTS.keys())
endpoint_options.pack()

resource_label = Label(window, text="Enter the resource name:")
resource_label.pack()
resource_entry = Entry(window)
resource_entry.pack()

search_button = Button(window, text="Search", command=search_resource)
search_button.pack()

resource_info_text = Text(window)
resource_info_text.pack()

# Start the Tkinter event loop
window.mainloop()
