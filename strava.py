import socket
import xml.etree.ElementTree as ET
import datetime

def get_lunch():
    # Získání aktuálního data
    now = datetime.datetime.now()
    weekday = now.weekday()

    # URL XML souboru
    url = "/foxisapi/foxisapi.dll/istravne.istravne.process?xmljidelnickyA&zarizeni=1005"

    # Vytvoření socketu
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Připojení k serveru
    s.connect(("www.strava.cz", 80))

    # Odeslání HTTP požadavku
    request = f"GET {url} HTTP/1.1\r\nHost: www.strava.cz\r\n\r\n"
    s.send(request.encode())

    # Získání odpovědi
    response = b""
    while True:
        part = s.recv(8192)
        if not part:
            break  # Server ukončil spojení
        response += part

    # Odstranění HTTP hlavičky z odpovědi
    parts = response.decode('cp1250').split("\r\n\r\n", 1)
    xml_content = parts[1] if len(parts) > 1 else parts[0]

    # Převedení XML obsahu na strom elementů
    root = ET.fromstring(xml_content)

    # Nalezení požadovaných elementů
    elements = root.findall(".//pomjidelnic_xmljidelnic")

    # Výpis hodnot požadovaných elementů pro aktuální týden (bez víkendů)
    meals = []
    current_date = None

    for element in elements:
        date = datetime.datetime.strptime(element.find('datum').text, '%Y-%m-%d')
        if now <= date <= now + datetime.timedelta(days=6) and date.weekday() < 5:
            meal_type = element.find('druh_popis').text
            meal_name = element.find('nazev').text
            if meal_name and meal_type != None:
                if current_date != date:
                    meals.append(f"### {date.strftime('%d.%m.%Y')} \n")
                    current_date = date
                meals.append(f"{meal_type} - {meal_name} \n")

    s.close()
    return "".join(meals)