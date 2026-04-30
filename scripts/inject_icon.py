#!/usr/bin/env python3
"""
inject_icon.py
Resize icon foreground & background lalu inject ke semua density di APK.
"""

import os
import glob
import shutil
import zipfile
from PIL import Image

# ── Konfigurasi density ──────────────────────────────────────────────────────
DENSITIES = {
    'mdpi':    48,
    'hdpi':    72,
    'xhdpi':   96,
    'xxhdpi':  144,
    'xxxhdpi': 192,
}

INPUT_DIR  = 'input'
OUTPUT_DIR = 'output'
TEMP_DIR   = 'temp_apk'

# ── Helper ───────────────────────────────────────────────────────────────────

def find_file(pattern):
    """Cari file di input/ berdasarkan glob pattern."""
    results = glob.glob(os.path.join(INPUT_DIR, pattern))
    return results[0] if results else None


def find_icon_files_in_apk(apk_path):
    """
    Scan APK dan return mapping:
      { 'background': ['res/mipmap-hdpi-v4/ic_background.png', ...],
        'foreground': ['res/mipmap-hdpi-v4/ic_foreground.png', ...] }
    Mendukung nama file apapun selama ada kata 'background'/'foreground' di path.
    """
    result = {'background': [], 'foreground': []}
    with zipfile.ZipFile(apk_path, 'r') as zf:
        for name in zf.namelist():
            lower = name.lower()
            if lower.startswith('res/mipmap') and lower.endswith('.png'):
                if 'background' in lower:
                    result['background'].append(name)
                elif 'foreground' in lower:
                    result['foreground'].append(name)
    return result


def resize_icon(src_path, size):
    """Resize icon ke ukuran size x size, return bytes PNG."""
    img = Image.open(src_path).convert('RGBA')
    img = img.resize((size, size), Image.LANCZOS)
    import io
    buf = io.BytesIO()
    img.save(buf, 'PNG')
    return buf.getvalue()


def density_from_path(zip_path):
    """
    Ekstrak density string dari path zip.
    Contoh: 'res/mipmap-xxhdpi-v4/ic_background.png' → 'xxhdpi'
    """
    # ambil nama folder mipmap-*
    parts = zip_path.split('/')
    for part in parts:
        if part.startswith('mipmap-'):
            # mipmap-xxhdpi-v4  →  xxhdpi
            tokens = part.split('-')
            if len(tokens) >= 2:
                return tokens[1]
    return None


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 1. Temukan file input
    apk_path = find_file('*.apk')
    fg_path  = find_file('*foreground*')
    bg_path  = find_file('*background*')

    if not apk_path:
        raise FileNotFoundError("Tidak ada .apk di folder input/")
    if not fg_path:
        raise FileNotFoundError("Tidak ada file *foreground* di folder input/")
    if not bg_path:
        raise FileNotFoundError("Tidak ada file *background* di folder input/")

    apk_name = os.path.basename(apk_path)
    print(f"APK      : {apk_name}")
    print(f"FG Icon  : {os.path.basename(fg_path)}")
    print(f"BG Icon  : {os.path.basename(bg_path)}")

    # 2. Scan APK untuk temukan semua icon paths
    icon_map = find_icon_files_in_apk(apk_path)
    print(f"\nIcon paths ditemukan di APK:")
    for kind, paths in icon_map.items():
        for p in paths:
            print(f"  [{kind}] {p}")

    if not icon_map['background'] and not icon_map['foreground']:
        raise ValueError("Tidak ditemukan ic_background/ic_foreground di APK. "
                         "Cek apakah APK punya adaptive icon.")

    # 3. Extract APK
    print(f"\nExtracting APK...")
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    os.makedirs(TEMP_DIR)

    with zipfile.ZipFile(apk_path, 'r') as zf:
        zf.extractall(TEMP_DIR)

    # 4. Resize dan replace tiap icon
    print("\nReplacing icons...")
    for kind, paths in icon_map.items():
        src_icon = fg_path if kind == 'foreground' else bg_path
        for zip_path in paths:
            density = density_from_path(zip_path)
            size    = DENSITIES.get(density, 192)  # fallback ke xxxhdpi
            dest    = os.path.join(TEMP_DIR, zip_path)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            img_bytes = resize_icon(src_icon, size)
            with open(dest, 'wb') as f:
                f.write(img_bytes)
            print(f"  ✓ {zip_path} ({size}x{size})")

    # 5. Repack APK
    output_apk = os.path.join(OUTPUT_DIR, apk_name)
    print(f"\nRepacking → {output_apk}")
    with zipfile.ZipFile(output_apk, 'w', zipfile.ZIP_DEFLATED) as zf_out:
        for root, dirs, files in os.walk(TEMP_DIR):
            for file in files:
                file_path  = os.path.join(root, file)
                arcname    = os.path.relpath(file_path, TEMP_DIR)
                # .so dan .dex lebih baik STORED (tidak di-compress)
                if arcname.endswith(('.so', '.dex')):
                    zf_out.write(file_path, arcname, zipfile.ZIP_STORED)
                else:
                    zf_out.write(file_path, arcname, zipfile.ZIP_DEFLATED)

    # 6. Cleanup
    shutil.rmtree(TEMP_DIR)

    size_kb = os.path.getsize(output_apk) / 1024
    print(f"\nDone! Output: {output_apk} ({size_kb:.1f} KB)")


if __name__ == '__main__':
    main()
