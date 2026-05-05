import os

# Data input dari Environment Variable GitHub Actions
data = {
    "{{NAMA}}": os.getenv("INPUT_NAMA", "NAMA PEMESAN"),
    "{{BIN}}": os.getenv("INPUT_BIN", "Bin"),
    "{{AYAH}}": os.getenv("INPUT_AYAH", "NAMA AYAH"),
    "{{LAHIR}}": os.getenv("INPUT_LAHIR", "00-00-0000"),
    "{{WAFAT}}": os.getenv("INPUT_WAFAT", "00-00-2026"),
}

template_path = 'templates/template_nisan.svg'
output_path = f"output/nisan_{data['{{NAMA}}'].replace(' ', '_')}.svg"

# Buat folder output jika belum ada
os.makedirs('output', exist_ok=True)

with open(template_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Proses penggantian teks
for key, value in data.items():
    content = content.replace(key, value)

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ Sukses! File dibuat di: {output_path}")
