class Property:
    def __init__(self, city, street, number, price, rooms=None):
        self.city = city
        self.street = street
        self.number = number
        self.price = price
        self.rooms = rooms  # Added rooms parameter
        self.latitude = None
        self.longitude = None
        self.distance = None  # for calculated distances

    def __str__(self):
        room_info = f", {self.rooms} rooms" if self.rooms else ""
        price_info = f", ₪{self.price:,}" if self.price else ""
        return f"{self.street} {self.number}, {self.city}{room_info}{price_info}"

    def full_address(self):
        return f"{self.street} {self.number}, {self.city}, Israel"
