import requests
from bs4 import BeautifulSoup
import csv
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# Fungsi untuk melakukan scraping game berdasarkan genre
def scrape_steam_games_by_genres(genres, genre_mapping):
    base_url = "https://store.steampowered.com/search/?tags="
    games_list = []

    for genre in genres:
        url = base_url + str(genre)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        games = soup.find_all('a', class_='search_result_row')

        for game in games:
            title = game.find('span', class_='title').text
            
            # Cek apakah elemen harga ada
            price_element = game.find('div', class_='search_price')
            price = price_element.text.strip() if price_element else "Price Not Available"
            
            # Bersihkan harga dari spasi berlebih atau karakter yang tidak diinginkan
            price = ' '.join(price.split())  # Menghapus spasi berlebih

            # Cek apakah elemen tanggal rilis ada
            release_date_element = game.find('div', class_='search_released')
            release_date = release_date_element.text.strip() if release_date_element else "Release Date Not Available"

            # Ambil nama genre dari genre_mapping
            genre_name = genre_mapping.get(genre, "Unknown Genre")

            games_list.append({
                'title': title,
                'price': price,
                'release_date': release_date,
                'genre': genre_name  # Gunakan nama genre, bukan ID
            })

    return games_list

# Mapping ID genre ke nama genre
genre_mapping = {
    19: "Action",
    18: "Adventure",
    21: "RPG",
    9: "Strategy",
    22: "Simulation",
    29: "Sports",
    1: "Racing",
    23: "Casual",
    492: "Indie",
    8: "Puzzle",
    1774: "Arcade",
    1625: "Platformer",
    1773: "Shooter",
    4: "Fighting",
    1667: "Horror",
    1662: "Survival",
    1695: "Open World",
    3859: "Multiplayer",
    4182: "Singleplayer",
    1685: "Co-op",
    31: "VR",
    4085: "Anime",
    3942: "Sci-fi",
    1775: "Fantasy",
    1743: "Story Rich",
    1676: "Turn-Based",
    1677: "Real-Time",
    1684: "Tactical",
    599: "Sandbox",
    4181: "Retro",
    3964: "Pixel Graphics",
    3871: "2D",
    3872: "3D",
    1664: "First-Person",
    1665: "Third-Person",
    1666: "Top-Down",
    1668: "Side-Scroller",
}

# Fungsi untuk menangani tombol "Scrape"
def on_scrape():
    selected_genres = [genre_ids[genre] for genre in genre_combobox.get().split(', ')]
    games = scrape_steam_games_by_genres(selected_genres, genre_mapping)
    
    if games:
        csv_filename = "steam_games.csv"
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['title', 'price', 'release_date', 'genre'])
            writer.writeheader()
            for game in games:
                writer.writerow(game)
        messagebox.showinfo("Success", f"Data telah disimpan ke dalam file {csv_filename}")
    else:
        messagebox.showwarning("No Data", "Tidak ada data yang ditemukan untuk genre yang dipilih.")

# Membuat GUI dengan tkinter
root = tk.Tk()
root.title("Steam Game Scraper")
root.geometry("800x600")  # Ukuran window
root.configure(bg="#1e1e1e")  # Warna latar belakang gelap

# Load gambar latar belakang
try:
    bg_image = Image.open("gaming_background.jpg")  # Ganti dengan path gambar Anda
    bg_image = bg_image.resize((800, 600), Image.ANTIALIAS)
    bg_image = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)
except FileNotFoundError:
    bg_label = tk.Label(root, bg="#1e1e1e")  # Fallback jika gambar tidak ditemukan
    bg_label.place(relwidth=1, relheight=1)

# Frame untuk konten dengan efek transparansi
content_frame = tk.Frame(root, bg="#2d2d2d", bd=5, relief="ridge")
content_frame.place(relx=0.5, rely=0.5, anchor="center", width=700, height=500)

# Judul aplikasi
title_label = tk.Label(content_frame, text="Steam Game Scraper", font=("Poppins", 24, "bold"), fg="#00ff00", bg="#2d2d2d")
title_label.pack(pady=(20, 10))

# Dropdown untuk memilih genre
genre_ids = {v: k for k, v in genre_mapping.items()}
genre_list = list(genre_mapping.values())

genre_label = tk.Label(content_frame, text="Pilih Genre:", font=("Poppins", 12), fg="white", bg="#2d2d2d")
genre_label.pack(pady=(10, 5))

# Custom Combobox Style
style = ttk.Style()
style.theme_use("clam")
style.configure("TCombobox", fieldbackground="#2d2d2d", background="#2d2d2d", foreground="white", 
                font=("Poppins", 12), borderwidth=0, focuscolor="#2d2d2d", lightcolor="#2d2d2d", 
                darkcolor="#2d2d2d", selectbackground="#00ff00", selectforeground="black")
style.map("TCombobox", fieldbackground=[("readonly", "#2d2d2d")], background=[("readonly", "#2d2d2d")])

genre_combobox = ttk.Combobox(content_frame, values=genre_list, state="readonly", style="TCombobox")
genre_combobox.pack(pady=5)
genre_combobox.set(genre_list[0])  # Set default value

# Tombol untuk memulai scraping dengan ikon
try:
    scrape_icon = Image.open("scrape_icon.png")  # Ganti dengan path ikon Anda
    scrape_icon = scrape_icon.resize((20, 20), Image.ANTIALIAS)
    scrape_icon = ImageTk.PhotoImage(scrape_icon)
except FileNotFoundError:
    scrape_icon = None

scrape_button = tk.Button(content_frame, text="Scrape", font=("Poppins", 12, "bold"), bg="#00ff00", fg="black", 
                          activebackground="#00cc00", activeforeground="white", bd=0, padx=20, pady=10, 
                          image=scrape_icon, compound="left", command=on_scrape)
scrape_button.pack(pady=20)

# Efek hover pada tombol
def on_enter(e):
    scrape_button.config(bg="#00cc00", fg="white")

def on_leave(e):
    scrape_button.config(bg="#00ff00", fg="black")

scrape_button.bind("<Enter>", on_enter)
scrape_button.bind("<Leave>", on_leave)

# Menjalankan aplikasi
root.mainloop()