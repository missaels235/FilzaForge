# ⚒️ FilzaForge (Windows Edition)

[![Python](https://img.shields.io/badge/Language-Python%203-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows-win)](https://github.com/missaels235)
[![iOS Support](https://img.shields.io/badge/iOS-15%20--%2018%2B-black)]()
[![Author](https://img.shields.io/badge/Forged%20By-Missaels235-orange)](https://github.com/missaels235)

**Forja tu propio Filza Jailed directamente en Windows.**

**FilzaForge** es una utilidad de ingeniería inversa escrita 100% en Python por **Missaels235**. Su objetivo es automatizar la conversión del paquete oficial `.deb` de Filza File Manager en un archivo `.ipa` instalable en dispositivos sin Jailbreak (Jailed).

A diferencia de otros métodos que requieren Linux, macOS o subsistemas pesados (WSL), **FilzaForge** opera nativamente en Windows utilizando algoritmos propios para desensamblar los binarios AR/DEB.

---

## 🔥 Características de la Forja

* **Nativo y Ligero:** Cero dependencias externas. No necesitas instalar binarios de Unix (`ar`, `tar`, `dpkg`). Todo se maneja con librerías estándar de Python.
* **Algoritmo de Extracción Inteligente:** El script analiza byte a byte la estructura del `.deb` para extraer el contenido `data.tar` sin importar si está comprimido en `.xz`, `.gz` o `.lzma`.
* **Automatización Total:**
    * ⬇️ **Descarga:** Obtiene la última versión oficial desde los servidores de TiGi Software.
    * 📦 **Conversión:** Extrae, limpia firmas digitales y reestructura el Payload.
    * 🔨 **Empaquetado:** Genera un `.ipa` limpio listo para firmar.
* **Modo Drag & Drop:** ¿Ya tienes el deb? Arrástralo sobre el script y FilzaForge lo procesará localmente.

## ⚙️ Requisitos

* **Sistema:** Windows 10 u 11.
* **Motor:** [Python 3.8 o superior](https://www.python.org/downloads/) (Asegúrate de marcar "Add to PATH" al instalar).

## 🚀 Cómo usar FilzaForge

1.  **Descarga el repositorio:**
    ```bash
    git clone [https://github.com/missaels235/FilzaForge.git](https://github.com/missaels235/FilzaForge.git)
    cd FilzaForge
    ```

2.  **Ejecuta la herramienta:**
    Haz doble clic en `filza_forge.py` o corre el comando:
    ```bash
    python filza_forge.py
    ```

3.  **¡Listo!**
    El script trabajará y dejará el archivo `FilzaForge-Jailed.ipa` en tu **Escritorio**.

---

## 📱 Instalación en iOS (15 - 18+)

El archivo IPA generado es "Jailed" (sin acceso root completo), pero funcional. Para instalarlo, usa tu herramienta de firma favorita:

* **Sideloadly** (Recomendado - Gratuito).
* **AltStore / SideStore**.
* **Certificados Empresariales** (ESign, Scarlet, GBox).

> **Nota del Desarrollador:** Al no tener Jailbreak, FilzaForge te dará acceso a la gestión de archivos dentro del sandbox (/var/mobile/Containers/Data/Application/...), ideal para importar/exportar archivos, gestionar descargas y modificar datos de apps.

## 👨‍💻 Créditos

* **Desarrollado por:** [Missaels235](https://github.com/missaels235)
    * *Creación del script, lógica de extracción binaria en Python y port para Windows.*
* **Filza File Manager:** Propiedad intelectual de TiGi Software.

---
<div align="center">
  <sub>Hecho con código y martillazos por Missaels235</sub>
</div>
