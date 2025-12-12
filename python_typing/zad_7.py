"""Stworzyć skrypt pythonowy, który połączy się z API, które zawiera informacje
o browarach (dokumentacja https://www.openbrewerydb.org/documentation).
Należy w pythonie zrobić klasę
Brewery , która będzie zawierała takie atrybuty jakich dostarcza API wraz z
odpowiednim typowaniem.
W klasie należy zaimplementować magiczną metodę
__str__ która będzie opisywała dane przechowywane w obiekcie.
Skrypt ma się połączyć do API i pobrać 20 pierwszych obiektów, a następnie
utworzyć listę 20 instancji klasy
Brewery , którą przeiteruje i wyświetli każdy obiekt z osobna."""

import requests


class Brewery:
    def __init__(
        self,
        id: str,
        name: str,
        brewery_type: str,
        street: str,
        city: str,
        state: str,
        postal_code: str,
        country: str,
        phone: str,
        website_url: str,
    ) -> None:
        self.id = id
        self.name = name
        self.brewery_type = brewery_type
        self.street = street
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.country = country
        self.phone = phone
        self.website_url = website_url

    def __str__(self) -> str:
        return (
            f"Brewery ID: {self.id}\n"
            f"Name: {self.name}\n"
            f"Type: {self.brewery_type}\n"
            f"Address: {self.street}, {self.city}, {self.state}, "
            f"{self.postal_code}, {self.country}\n"
            f"Phone: {self.phone}\n"
            f"Website: {self.website_url}\n"
        )


if __name__ == "__main__":
    response = requests.get("https://api.openbrewerydb.org/v1/breweries?per_page=20")
    breweries_data = response.json()

    breweries = []
    for data in breweries_data:
        brewery = Brewery(
            id=data.get("id", ""),
            name=data.get("name", ""),
            brewery_type=data.get("brewery_type", ""),
            street=data.get("street", ""),
            city=data.get("city", ""),
            state=data.get("state", ""),
            postal_code=data.get("postal_code", ""),
            country=data.get("country", ""),
            phone=data.get("phone", ""),
            website_url=data.get("website_url", ""),
        )
        breweries.append(brewery)

    for brewery in breweries:
        print(brewery)
