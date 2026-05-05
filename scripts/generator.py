import xml.etree.ElementTree as ET

def update_nisan():
    # Load file SVG
    tree = ET.parse('templates/sv.svg')
    root = tree.getroot()
    
    # Data kamu
    data = {
        "NAMA_SARIP": "SARIP",
        "BIN_TEXT": "BIN",
        "AYAH_TEXT": "H. ANEN",
        "LAHIR_VAL": "02 – 07 – 1970",
        "WAFAT_VAL": "28 – 05 – 2025"
    }

    # Fungsi untuk cari teks dan update
    # Di Corel/Inkscape, teks yang mau diganti harus punya ID atau diisi placeholder
    # Pastikan di SVG lo, teksnya sudah diisi placeholder: {{NAMA}}, {{BIN}}, dll.
    for element in root.iter('{http://www.w3.org/2000/svg}text'):
        text = element.text
        if text:
            if "{{NAMA}}" in text: element.text = text.replace("{{NAMA}}", data["NAMA_SARIP"])
            if "{{BIN}}" in text: element.text = text.replace("{{BIN}}", data["BIN_TEXT"])
            if "{{AYAH}}" in text: element.text = text.replace("{{AYAH}}", data["AYAH_TEXT"])
            if "{{LAHIR}}" in text: element.text = text.replace("{{LAHIR}}", data["LAHIR_VAL"])
            if "{{WAFAT}}" in text: element.text = text.replace("{{WAFAT}}", data["WAFAT_VAL"])

    # Simpan hasil
    tree.write('output/nisan_SARIP.svg', encoding='utf-8', xml_declaration=True)
    print("File nisan_SARIP.svg berhasil dibuat!")

if __name__ == "__main__":
    update_nisan()
