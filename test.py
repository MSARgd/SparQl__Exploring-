
from tkinter import Tk, Label, Entry, Button
from tkinter import ttk
from SPARQLWrapper import SPARQLWrapper, JSON

def query_sparql(endpoint, query):
    with SPARQLWrapper(endpoint) as sparql:
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return results["results"]["bindings"]

def get_country_info(country):
    endpoint = "https://dbpedia.org/sparql"
    query = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        SELECT ?property ?value
        WHERE {{
            <http://dbpedia.org/resource/{country}> ?property ?value
        }}
    """
    results = query_sparql(endpoint, query)
    country_info = {}
    for result in results:
        property_name = result["property"]["value"].rsplit('/', 1)[-1]
        property_value = result["value"]["value"]
        country_info[property_name] = property_value
    return country_info

def search_country():
    country = country_entry.get()
    country_info = get_country_info(country)
    country_info_text.delete(*country_info_text.get_children())
    if country_info:
        for property_name, property_value in country_info.items():
            country_info_text.insert("", "end", values=(property_name, property_value))
    else:
        country_info_text.insert("", "end", values=("No information found for the country.", ""))

# Create the main window
window = Tk()
window.title("Country Explorer")

# Create and place widgets
country_label = Label(window, text="Enter country name:")
country_label.pack()
country_entry = Entry(window)
country_entry.pack()

search_button = Button(window, text="Search", command=search_country)
search_button.pack()

country_info_text = ttk.Treeview(window, columns=("Property", "Value"), show="headings")
country_info_text.column("Property", width=200)
country_info_text.column("Value", width=200)
country_info_text.heading("Property", text="Property")
country_info_text.heading("Value", text="Value")
country_info_text.pack()

# Start the Tkinter event loop
window.mainloop()
