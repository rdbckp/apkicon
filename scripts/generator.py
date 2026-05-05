import os
import sys

def generate():
    # 1. Lokasi file yang benar (menggunakan path absolut)
    base_dir = os.getcwd()
    template_path = os.path.join(base_dir, 'templates', 'template_nisan.svg')
    output_dir = os.path.join(base_dir, 'output')
    
    # 2. Cek apakah file template ada
    if not os.path.exists(template_path):
        print(f"ERROR: File template tidak ditemukan di {template_path}")
        sys.exit(1)

    # 3. Ambil data dari Environment Variables
    data = {
        "{{NAMA}}": os.getenv("INPUT_NAMA", "NAMA PEMESAN"),
        "{{BIN}}": os.getenv("INPUT_BIN", "Bin"),
        "{{AYAH}}": os.getenv("INPUT_AYAH", "NAMA AYAH"),
        "{{LAHIR}}": os.getenv("INPUT_LAHIR", "00-00-0000"),
        "{{WAFAT}}": os.getenv("INPUT_WAFAT", "00-00-2026"),
    }

    # 4. Baca template
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Debug: Pastikan text placeholder ada di file
    if "{{NAMA}}" not in content:
        print("WARNING: Placeholder {{NAMA}} tidak ditemukan di file SVG!")
        print("Pastikan kamu save file SVG sebagai 'Plain SVG' dari CorelDraw.")

    # 5. Ganti teks
    for key, value in data.items():
        content = content.replace(key, value)

    # 6. Simpan hasil
    os.makedirs(output_dir, exist_ok=True)
    output_filename = f"nisan_{data['{{NAMA}}'].replace(' ', '_')}.svg"
    output_path = os.path.join(output_dir, output_filename)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"SUCCESS: File berhasil dibuat di {output_path}")

if __name__ == "__main__":
    generate()
