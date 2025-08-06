

"""
MCP Server for Madlan Property Finder
Provides tools to find properties closest to clinics and schools in Haifa
"""

import asyncio
import json
from typing import Any, Dict, List, Optional
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)
import mcp.types as types

# Fixed file loader with rooms column
import pandas as pd

from services.distance_calculator import sort_by_distance
from services.geocoding_service import geocode_address

class Property:
    def __init__(self, city, street, number, price, rooms=None):
        self.city = city
        self.street = street
        self.number = number
        self.price = price
        self.rooms = rooms
        self.latitude = None
        self.longitude = None
        self.distance = None

    def __str__(self):
        room_info = f", {self.rooms} rooms" if self.rooms else ""
        price_info = f", ₪{self.price:,}" if self.price else ""
        return f"{self.street} {self.number}, {self.city}{room_info}{price_info}"

    def full_address(self):
        return f"{self.street} {self.number}, {self.city}, Israel"

def load_properties_from_excel(file_path):
    df = pd.read_excel(file_path)
    
    properties = []
    for _, row in df.iterrows():
        city = row.get("city", "")
        street = row.get("street", "")
        number = row.get("number", "")
        price = row.get("price", None)
        rooms = row.get("property_rooms", None)  # Using property_rooms column
        
        property_obj = Property(city, street, number, price, rooms)
        properties.append(property_obj)
    
    return properties

# Configuration
EXCEL_PATH = "data/100 listings haifa.xlsx"
CLINIC_LOCATION = (32.807, 35.043)
SCHOOL_LOCATION = (32.802, 35.048)

# Global cache for properties (loaded once)
_properties_cache = None

server = Server("madlan-property-finder")

async def load_properties():
    """Load and cache properties from Excel file"""
    global _properties_cache
    if _properties_cache is None:
        print("Loading properties from Excel...")
        _properties_cache = load_properties_from_excel(EXCEL_PATH)
        
        # Geocode all addresses
        print("Geocoding addresses...")
        for prop in _properties_cache:
            geocode_address(prop)
    
    return _properties_cache

@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available tools"""
    return [
        Tool(
            name="find_closest_properties",
            description="Find the 3 closest properties to a clinic, school, or both",
            inputSchema={
                "type": "object",
                "properties": {
                    "location_type": {
                        "type": "string",
                        "enum": ["clinic", "school", "both"],
                        "description": "Type of target location to calculate distances from",
                        "default": "both"
                    },
                    "max_price": {
                        "type": "number",
                        "description": "Maximum price in NIS",
                        "default": 2000000
                    },
                    "min_rooms": {
                        "type": "number", 
                        "description": "Minimum number of rooms",
                        "default": 3
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="property_statistics",
            description="Get statistics about properties in the dataset",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle tool calls"""
    
    if name == "find_closest_properties":
        # Load properties
        properties = await load_properties()
        
        # Get parameters
        location_type = arguments.get("location_type", "both")
        max_price = arguments.get("max_price", 2000000)
        min_rooms = arguments.get("min_rooms", 3)
        
        # Filter properties by criteria
        filtered_properties = [
            prop for prop in properties 
            if (prop.price <= max_price if prop.price else True) and 
               (prop.rooms >= min_rooms if prop.rooms else True)
        ]
        
        results = []
        
        if location_type in ["clinic", "both"]:
            clinic_closest = sort_by_distance(filtered_properties, CLINIC_LOCATION)[:3]
            results.append("🏥 **Closest to Clinic:**")
            for i, prop in enumerate(clinic_closest, 1):
                results.append(f"{i}. {prop} - {prop.distance:.0f}m away")
            results.append("")
        
        if location_type in ["school", "both"]:
            school_closest = sort_by_distance(filtered_properties, SCHOOL_LOCATION)[:3]
            results.append("🏫 **Closest to School:**")
            for i, prop in enumerate(school_closest, 1):
                results.append(f"{i}. {prop} - {prop.distance:.0f}m away")
        
        if not results:
            results = ["No properties found matching your criteria."]
        
        # Add filter info
        filter_info = f"\n📊 **Filters applied:** Max price: ₪{max_price:,}, Min rooms: {min_rooms}"
        filter_info += f"\n📈 **Found {len(filtered_properties)} properties** out of {len(properties)} total"
        
        return [types.TextContent(
            type="text",
            text="\n".join(results) + filter_info
        )]
    
    elif name == "property_statistics":
        properties = await load_properties()
        
        # Calculate statistics
        total_props = len(properties)
        prices = [prop.price for prop in properties if prop.price]
        rooms = [prop.rooms for prop in properties if prop.rooms]
        
        stats = []
        stats.append(f"📊 **Property Dataset Statistics**")
        stats.append(f"Total properties: {total_props}")
        
        if prices:
            avg_price = sum(prices) / len(prices)
            min_price = min(prices)
            max_price = max(prices)
            stats.append(f"\n💰 **Prices:**")
            stats.append(f"Average: ₪{avg_price:,.0f}")
            stats.append(f"Range: ₪{min_price:,} - ₪{max_price:,}")
        
        if rooms:
            avg_rooms = sum(rooms) / len(rooms)
            min_rooms = min(rooms)
            max_rooms = max(rooms)
            stats.append(f"\n🏠 **Rooms:**")
            stats.append(f"Average: {avg_rooms:.1f}")
            stats.append(f"Range: {min_rooms} - {max_rooms}")
        
        return [types.TextContent(
            type="text",
            text="\n".join(stats)
        )]
    
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    """Main entry point for the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="madlan-property-finder",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())


