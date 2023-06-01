import tkinter as tk
from tkinter import *
from tkinter import ttk
from SPARQLWrapper import SPARQLWrapper, JSON
import urllib.request
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

DBPEDIA_ENDPOINT = "https://dbpedia.org/sparql"

def execute_sparql(query):
    sparql = SPARQLWrapper(DBPEDIA_ENDPOINT)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results["results"]["bindings"]

def get_info(object):
    query = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        SELECT ?property ?value
        WHERE {{
            <http://dbpedia.org/resource/{object}> ?property ?value
        }}
    """
    results = execute_sparql(query)
    object_info = {}
    for result in results :
        property_name = result["property"]["value"].split("/")[-1]
        property_value = result["value"]["value"]
        object_info[property_name] = property_value
    return object_info

def search_object() :
    object = object_entry.get()
    object_info = get_info(object)
    treeview.delete(*treeview.get_children())
    if object_info:
        for property_name, property_value in object_info.items():
            treeview.insert("", "end", values=(property_name, property_value))


        image_url = object_info.get('thumbnail')
        if image_url:
            urllib.request.urlretrieve(image_url, "test/object_image.jpg")
            image = Image.open("test/object_image.jpg")
            image = image.resize((200, 200), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(image)
            image_label.configure(image=photo)
            image_label.image = photo
        else:
            image_label.configure(image='')
    else:
        treeview.insert("", "end", values=("Aucune information n’a été trouvée pour le pays.", ""))
        image_label.configure(image='')

def execute_custom_query():
    query = custom_query_entry.get("1.0", "end-1c")
    results = execute_sparql(query)
    treeview.delete(*treeview.get_children())
    for result in results:
        for var_name, var_value in result.items():
            treeview.insert("", "end", values=(var_name, var_value["value"]))




window = Tk()
window.title("Explorer")


object_label = Label(window, text="Entrez ")
object_label.pack()
object_entry = Entry(window)
object_entry.pack()
search_button = Button(window, text="Recherche", command=search_object)
search_button.pack()


custom_query_label = Label(window, text="Entrez une requête SPARQL personnalisée:")
custom_query_label.pack()
custom_query_entry = Text(window, height=5)
custom_query_entry.pack()
execute_query_button = Button(window, text="Exécuter la requête", command=execute_custom_query)
execute_query_button.pack()


treeview = ttk.Treeview(window, columns=("Variable", "Valeur"), show="headings")
treeview.heading("Variable", text="Variable")
treeview.heading("Valeur", text="Valeur")
treeview.column("Valeur", width=400)
treeview.pack()

image_label = Label(window)
image_label.pack()




window.mainloop()