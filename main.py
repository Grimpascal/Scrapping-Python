import requests
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate

respon = requests.get('https://www.scrapethissite.com/pages/forms/?per_page=500')
soup = BeautifulSoup(respon.text, "html.parser")

mentah = soup.find_all("tr", class_="team")

Hasil = []
for block in mentah:
    namaElement = block.find('td', class_='name')
    namaTim = namaElement.get_text(strip=True)

    tahunElement = block.find('td', class_='year')
    tahunTim = tahunElement.get_text(strip=True)

    menangElement = block.find('td', class_='wins')
    menangTim = menangElement.get_text(strip=True)

    kalahElement = block.find('td', class_='losses')
    kalahTim = kalahElement.get_text(strip=True)

    Hasil.append({'nama' : namaTim, 'tahun' : tahunTim, 'menang' : menangTim, 'kalah' : kalahTim})

data = pd.DataFrame(Hasil)
data.index = data.index + 1
print(tabulate(data, headers='keys', tablefmt='grid'))
