# 🏠 Madlan Property Finder

This project is a Minimal Command Processor (MCP) Server built for a take-home challenge. It finds the **top 3 real estate listings** closest to a **clinic** or **elementary school**, based on a dataset of 100 properties.

Built with a clean architecture in mind, this tool demonstrates smart spatial querying, user-defined filters (like price and number of rooms), and easy Claude Desktop integration.

---

## 🚀 Features

- 🔍 Filter listings by:
  - Max price
  - Minimum number of rooms
  - Target proximity (clinic or school)
- 📍 Calculates Haversine distance to target
- 🧠 Claude Desktop ready
- 🧪 Unit-tested & modular

---

## 🧠 Using with Claude Desktop

To enable this tool inside **Claude Desktop**, follow these steps:

### 1. Add to `claude_desktop_config.json`

Paste the following into your Claude Desktop config file:

```json
{
  "name": "madlan_property_finder",
  "entry_point": "Madlan.py",
  "description": "Find top 3 listings below 2M NIS, 3+ rooms, closest to clinic or school",
  "inputs": {
    "max_price": 2000000,
    "min_rooms": 3,
    "target": "clinic"
  }
}
2. Ask Claude:

Using madlan_property_finder, provide me with the top 3 listings, below 2 million NIS, that have 3+ rooms and that also have the minimal distances from a health clinic.
The tool will return the best 3 listings based on your criteria.

🏗️ Project Structure

madlan_project/
├── data/
│   └── properties.csv
├── Madlan.py
├── distance_utils.py
├── filters.py
├── mcp_server.py
├── test_distance_utils.py
├── test_filters.py
└── README.md
🧪 How to Run

# Run the main tool
python Madlan.py --target clinic --max_price 2000000 --min_rooms 3

# Run tests
pytest
🧩 Dependencies
Python 3.10+

pandas

numpy

argparse

math

Install them with:
pip install


📍 Example Output

Top 3 matching listings:
1. Property ID 24 - 1.2 km from clinic - 3.5 rooms - 1.8M NIS
2. Property ID 76 - 1.6 km from clinic - 4 rooms - 1.9M NIS
3. Property ID 42 - 1.9 km from clinic - 3.5 rooms - 1.85M NIS