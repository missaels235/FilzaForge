import os
import sys
import shutil
import urllib.request
import tarfile
import tempfile
from pathlib import Path

DEFAULT_DEB_URL = "https://tigisoftware.com/cydia/com.tigisoftware.filza_4.0.1-2_iphoneos-arm.deb"
IPA_NAME = "FilzaForge-Jailed.ipa"

def get_windows_desktop():
    """Obtiene la ruta real del escritorio en Windows."""
    return Path(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'))

def progress_bar(block_num, block_size, total_size):
    """Barra de progreso visual."""
    downloaded = block_num * block_size
    if total_size > 0:
        percent = (downloaded / total_size) * 100
        percent = min(100, percent)
        bar_length = 40
        filled_length = int(bar_length * percent // 100)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        sys.stdout.write(f'\r[⬇] Descargando: |{bar}| {percent:.1f}%')
        sys.stdout.flush()
    else:
        sys.stdout.write(f'\r[⬇] Descargando: {downloaded / (1024*1024):.2f} MB')
        sys.stdout.flush()

def download_file(url, dest_path):
    print(f"[ i ] Conectando a: {url}")
    try:
        urllib.request.urlretrieve(url, dest_path, progress_bar)
        print()
        print("[ + ] Descarga completada.")
    except Exception as e:
        print(f"\n[ ! ] Error en la descarga: {e}")
        sys.exit(1)

def extract_deb(deb_path, extract_dir):
    print(f"[ i ] Analizando estructura DEB: {deb_path.name}")
    try:
        with open(deb_path, 'rb') as f:
            content = f.read()
            extensions = {b'data.tar.xz': '.tar.xz', b'data.tar.gz': '.tar.gz', b'data.tar.bz2': '.tar.bz2', b'data.tar': '.tar'}
            found_archive = None
            
            for signature, ext in extensions.items():
                index = content.find(signature)
                if index != -1:
                    f.seek(0)
                    if f.read(8) != b'!<arch>\n': break
                    
                    while True:
                        header = f.read(60)
                        if not header or len(header) < 60: break
                        try:
                            name = header[:16].strip().decode('ascii', errors='ignore')
                            size = int(header[48:58].strip())
                        except: break
                        
                        if name.startswith("data.tar"):
                            print(f"[ i ] Extrayendo núcleo (Forge Core): {name}")
                            data_content = f.read(size)
                            temp_tar_path = Path(extract_dir) / ("internal_data" + ext)
                            with open(temp_tar_path, 'wb') as out_tar:
                                out_tar.write(data_content)
                            found_archive = temp_tar_path
                            break
                        f.seek(size + (size % 2), 1)
                    if found_archive: break
        
        if not found_archive:
            print("[ ! ] No se encontró 'data.tar' dentro del paquete.")
            sys.exit(1)

        print(f"[ i ] Descomprimiendo binarios...")
        try:
            with tarfile.open(found_archive, 'r:*') as tar:
                tar.extractall(path=extract_dir)
        except tarfile.ReadError:
            print("[ ! ] Error descomprimiendo el TAR interno.")
            sys.exit(1)
    except Exception as e:
        print(f"\n[ ! ] Error procesando DEB: {e}")
        sys.exit(1)

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== FilzaForge (Windows Edition) by Missaels235 ===\n")

    # 1. Rutas
    work_dir = Path(tempfile.mkdtemp())
    desktop_dir = get_windows_desktop()
    deb_local = work_dir / "filza.deb"
    target_url = DEFAULT_DEB_URL
    
    if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
        print(f"[ i ] Modo Forge Local: {sys.argv[1]}")
        shutil.copy(sys.argv[1], deb_local)
        target_url = None
    
    # 2. Descargar
    if target_url: download_file(target_url, deb_local)
        
    # 3. Extraer
    extract_dir = work_dir / "extracted"
    extract_dir.mkdir()
    extract_deb(deb_local, extract_dir)
    
    # 4. Buscar App
    filza_path = next(extract_dir.rglob("Filza.app"), None)
    if not filza_path:
        print("[ ! ] Error: Filza.app no encontrado.")
        sys.exit(1)
        
    # 5. Payload
    payload_dir = work_dir / "Payload"
    payload_dir.mkdir()
    destination_app = payload_dir / "Filza.app"
    print(f"[ i ] Forjando estructura Payload...")
    shutil.copytree(filza_path, destination_app)
    
    # 6. Limpieza firmas
    shutil.rmtree(destination_app / "_CodeSignature", ignore_errors=True)
    try: os.remove(destination_app / "embedded.mobileprovision")
    except: pass
            
    # 7. Comprimir IPA
    print(f"[ i ] Empaquetando {IPA_NAME}...")
    
    ipa_output_path = work_dir / IPA_NAME
    base_name = str(ipa_output_path.with_suffix('')) 
    
    shutil.make_archive(base_name, 'zip', work_dir, "Payload")
    
    zip_created = Path(base_name + ".zip")
    
    if not zip_created.exists():
        print(f"[ ! ] Error crítico: Fallo en la forja del ZIP.")
        sys.exit(1)
        
    if ipa_output_path.exists():
        os.remove(ipa_output_path)
    os.rename(zip_created, ipa_output_path)
        
    # 8. Mover al escritorio
    final_path = desktop_dir / IPA_NAME
    print(f"[ i ] Entregando producto a: {final_path}")
    
    if final_path.exists():
        os.remove(final_path)
        
    if not ipa_output_path.exists():
        print(f"[ ! ] Error: El archivo IPA desapareció.")
        sys.exit(1)

    shutil.move(ipa_output_path, final_path)
    
    # 9. Limpiar
    try: shutil.rmtree(work_dir, ignore_errors=True)
    except: pass 
    
    print("\n" + "█"*60)
    print(f"[ v ] FORJA COMPLETADA")
    print(f"[ + ] Archivo listo: {final_path}")
    print("█"*60)
    input("\nPresiona ENTER para salir...")

if __name__ == "__main__":
    main()