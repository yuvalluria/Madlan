# 🏠 Madlan Property Finder

This project helps find the **top 3 property listings** in Haifa that are **closest to a clinic or school**, using geographic coordinates.

## 🔧 What the Code Does

1. **Loads property listings** from an Excel file.
2. **Geocodes** the addresses (gets latitude & longitude).
3. **Calculates distances** to:
   - A nearby health clinic
   - A nearby elementary school
4. **Sorts the listings** by distance.
5. Supports filtering by price, number of rooms, and distance.

## 📁 Project Structure

Madlan/
│
├── data/
│ └── 100 listings haifa.xlsx # Your input data
│
├── models/
│ └── property.py # Property object definition
│
├── services/
│ ├── geocoding_service.py # Address-to-coordinate service
│ └── distance_calculator.py # Distance calculator & sorting
│
├── utils/
│ └── file_loader.py # Excel loader
│
├── Madlan.py # Main runner script
└── README.md # This file


## 🧑‍💻 How to Install & Run

### Requirements

- Python 3.8+
- Install dependencies:

Run the project

python Madlan.py
You’ll see two lists printed:

🏥 Closest properties to the health clinic

🏫 Closest properties to the elementary school
