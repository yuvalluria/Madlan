class Property:
    def __init__(self, city, street, number, price):
        self.city = city
        self.street = street
        self.number = number
        self.price = price
        self.latitude = None
        self.longitude = None
        self.distance = None  # for calculated distances

    def __str__(self):
        return f"{self.street} {self.number}, {self.city}"

    def full_address(self):
        return f"{self.street} {self.number}, {self.city}, Israel"
