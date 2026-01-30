import requests

# Mapping sederhana untuk weathercode (berdasarkan Open-Meteo docs)
WEATHER_CODES = {
    0: "Cerah",
    1: "Sebagian Berawan",
    2: "Berawan",
    3: "Mendung",
    45: "Kabut",
    48: "Kabut Beku",
    51: "Gerimis Ringan",
    53: "Gerimis",
    55: "Gerimis Lebat",
    56: "Gerimis Beku Ringan",
    57: "Gerimis Beku",
    61: "Hujan Ringan",
    63: "Hujan",
    65: "Hujan Lebat",
    66: "Hujan Beku Ringan",
    67: "Hujan Beku",
    71: "Salju Ringan",
    73: "Salju",
    75: "Salju Lebat",
    77: "Butiran Salju",
    80: "Hujan Badai Ringan",
    81: "Hujan Badai",
    82: "Hujan Badai Lebat",
    85: "Salju Badai Ringan",
    86: "Salju Badai",
    95: "Badai Petir",
    96: "Badai Petir dengan Hujan Es",
    99: "Badai Petir dengan Hujan Es Lebat"
}

def get_weather(city_name, lat, lon):
    print(f"\n--- Mengambil Data Cuaca untuk {city_name} ---")

    # Validasi koordinat sederhana
    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        print("[ERROR] Koordinat latitude dan longitude harus berupa angka!")
        return

    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': lat,
        'longitude': lon,
        'current_weather': 'true',
        'timezone': 'auto'
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)  # Tambah timeout untuk menghindari hang

        if response.status_code == 200:
            data = response.json()
            current = data['current_weather']
            suhu = current['temperature']
            kecepatan_angin = current['windspeed']
            weathercode = current.get('weathercode', 'Tidak tersedia')  # Default jika tidak ada
            deskripsi_cuaca = WEATHER_CODES.get(weathercode, "Tidak diketahui")

            print(f"🌡️  Suhu Saat Ini: {suhu}°C")
            print(f"💨 Kecepatan Angin: {kecepatan_angin} km/h")
            print(f"🌤️  Kondisi Cuaca: {deskripsi_cuaca} (Kode: {weathercode})")
            print(f"🌍 Koordinat: {lat}, {lon}")
        else:
            print(f"[ERROR] Gagal mengambil data. Status: {response.status_code} - {response.text}")

    except requests.exceptions.Timeout:
        print("[ERROR] Request timeout! Coba lagi nanti.")
    except requests.exceptions.ConnectionError:
        print("[ERROR] Tidak ada koneksi internet!")
    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan: {e}")

if __name__ == "__main__":
    # Loop untuk input berulang
    while True:
        city = input("Masukkan nama kota (atau 'exit' untuk keluar): ").strip()
        if city.lower() == 'exit':
            print("Terima kasih telah menggunakan aplikasi cuaca!")
            break
        
        # Hardcode koordinat untuk demo (dalam aplikasi nyata, gunakan geocoding API)
        coords = {
            "jakarta": (-6.2088, 106.8456),
            "makassar": (-5.1477, 119.4327),
            # Tambah kota lain jika perlu
        }
        
        if city.lower() in coords:
            lat, lon = coords[city.lower()]
            get_weather(city, lat, lon)
        else:
            print(f"[ERROR] Kota '{city}' tidak ditemukan dalam daftar. Tambahkan koordinat manual atau gunakan geocoding.")
            # Opsi untuk input manual koordinat
            try:
                lat = input("Masukkan latitude: ").strip()
                lon = input("Masukkan longitude: ").strip()
                get_weather(city, lat, lon)
            except KeyboardInterrupt:
                print("\nKeluar dari aplikasi.")
                break