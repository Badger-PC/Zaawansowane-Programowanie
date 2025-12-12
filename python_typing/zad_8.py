"""Rozszerzyć skrypt z punktu 7 o przyjmowanie parametru city , który może
być przekazywany w wierszu poleceń podczas wykonywania (np. python
main.py --city=Berlin ). Należy wykorzystać moduł argparse do wczytywania
przekazywanych parametrów, a w razie przekazania wartości ograniczyć
pobierane browary do miasta, które zostało wskazane."""

import requests
import argparse


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
            f"CITY: {self.city}\n"
            f"Address: {self.street}, {self.state}, "
            f"{self.postal_code}, {self.country}\n"
            f"Phone: {self.phone}\n"
            f"Website: {self.website_url}\n"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Sprawdzanie browarów z określonego miasta"
    )
    parser.add_argument("--city", type=str, help="Nazwa miasta do filtrowania browarów")
    args = parser.parse_args()

    url = "https://api.openbrewerydb.org/v1/breweries?per_page=20"
    if args.city:
        url += f"&by_city={args.city}"

    response = requests.get(url)
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
