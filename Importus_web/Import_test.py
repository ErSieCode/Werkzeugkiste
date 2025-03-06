# Python Import-Anweisungen

# Liste für fehlgeschlagene Importe
fehlende_module = []

print("Überprüfe Module...")

try:
    import Kivy
    print("✅ Kivy erfolgreich importiert")
except ImportError:
    print("❌ Kivy nicht gefunden")
    fehlende_module.append("Kivy")

try:
    import PyQt5
    print("✅ PyQt5 erfolgreich importiert")
except ImportError:
    print("❌ PyQt5 nicht gefunden")
    fehlende_module.append("PyQt5")

# Zeige Installationsanweisungen für fehlende Module
if fehlende_module:
    print("\nFolgende Module müssen installiert werden:")
    for modul in fehlende_module:
        print(f"  - {modul}")
    print("\nInstallationsbefehl:")
    print(f"pip install {' '.join(fehlende_module)}")
else:
    print("\nAlle Module wurden erfolgreich importiert!")
