
from utils.file_loader import load_properties_from_excel
from services.geocoding_service import geocode_address
from services.distance_calculator import sort_by_distance
from models.property import Property

EXCEL_PATH = "data/100 listings haifa.xlsx"

# Define target locations
clinic_location = (32.807, 35.043)
school_location = (32.802, 35.048)

def main():
    properties = load_properties_from_excel(EXCEL_PATH)

    print("🔍 Geocoding addresses...")
    for prop in properties:
        geocode_address(prop)

    print("\n🏥 Closest to Clinic:")
    closest_to_clinic = sort_by_distance(properties, clinic_location)
    for prop in closest_to_clinic:
        print(f"{prop} - {prop.distance:.2f} meters")

    print("\n🏫 Closest to School:")
    closest_to_school = sort_by_distance(properties, school_location)
    for prop in closest_to_school:
        print(f"{prop} - {prop.distance:.2f} meters")

if __name__ == "__main__":
    main()
