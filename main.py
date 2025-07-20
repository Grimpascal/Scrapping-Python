import requests
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate
import os
import time

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"}

def utama():
    while True:
        os.system('cls')
        print('Ingin melihat data apa')
        print('''1. Data tim hockey
2. Daftar project github
3. Daftar harga Tokopedia''')
        pilihan = input('Masukkan pilihan : ')
        if pilihan == '1':
            hockey()
        elif pilihan == '2':
            github()
        elif pilihan == '3':
            tokopedia()
        else:
            print('Tidak ada dipilihan!')
            time.sleep(1)
            continue

def hockey():
    os.system('cls')
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
    input('ENTER UNTUK KEMBALI >>>')
    utama()

def github():
    os.system('cls')
    print('=====GITHUB=====')
    user = input('Masukkan Username : ')
    url = f'https://github.com/{user}?tab=repositories'
    
    try:
        respon = requests.get(url, headers=headers)
        soup = BeautifulSoup(respon.text, 'html.parser')

        mentah = soup.find_all('div', class_='col-10 col-lg-9 d-inline-block')
        hasil = []
        
        for block in mentah:
            namaRepo = "N/A"
            bahasaRepo = "Not Specified"

            namaRepoE = block.find('h3', class_='wb-break-all').find('a')
            if namaRepoE:
                namaRepo = namaRepoE.get_text(strip=True)

            statusRepoE = block.find('span', class_='Label Label--secondary v-align-middle ml-1 mb-1')
            if statusRepoE:
                statusRepo = statusRepoE.get_text(strip=True)

            bahasaRepoE = block.find('span', itemprop='programmingLanguage')
            if bahasaRepoE:
                bahasaRepo = bahasaRepoE.get_text(strip=True)

            hasil.append({
                'Nama Repository': namaRepo,
                'Status': statusRepo,
                'Bahasa': bahasaRepo
            })

        os.system('cls')
        data = pd.DataFrame(hasil)
        data.index = data.index + 1
        print(tabulate(data, headers='keys', tablefmt='grid'))
        
    except requests.exceptions.RequestException as e:
        print(f"Error saat mengakses GitHub: {e}")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    
    input('TEKAN ENTER UNTUK KEMBALI>>>')
    utama()

def tokopedia():
    os.system('cls')
    print('=====TOKOPEDIA NAMA SCRAPPING=====')
    namaBarang = input('Masukkan Nama Barang : ')
    namaBarangSpasi = namaBarang.replace(' ', '%20')
    os.system('cls')
    url = f'https://www.tokopedia.com/search?st=&q={namaBarangSpasi}&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource='
    respon = requests.get(url, headers=headers)
    soup = BeautifulSoup(respon.text, 'html.parser')

    mentah = soup.find_all('div', class_='gG1uA844gIiB2+C3QWiaKA==')

    hasil = []
    for block in mentah:
        namaProdukE = block.find('span', class_='+tnoqZhn89+NHUA43BpiJg==')
        namaProduk = namaProdukE.get_text(strip=True)

        ratingE = block.find('span', class_='_2NfJxPu4JC-55aCJ8bEsyw==')
        rating = ratingE.get_text(strip=True)

        hasil.append({'nama' : namaProduk, 'rating' : rating})
    
    data = pd.DataFrame(hasil)
    data.index = data.index + 1
    print(tabulate(data, headers='keys', tablefmt='grid'))
    input('ENTER UNTUK KEMBALI >>>')
    utama()

utama()