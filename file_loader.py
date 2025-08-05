import pandas as pd
from models.property import Property

def load_properties_from_excel(file_path):
    df = pd.read_excel(file_path)

    properties = []
    for _, row in df.iterrows():
        city = row.get("city", "")
        street = row.get("street", "")
        number = row.get("number", "")
        price = row.get("price", None)

        property_obj = Property(city, street, number, price)
        properties.append(property_obj)

    return properties