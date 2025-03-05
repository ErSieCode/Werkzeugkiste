
---

Dokumentation der Funktionen in Importus3.py

Überblick

Die Datei Importus3.py besteht aus mehreren Klassen, die zusammen die Funktionalität eines Python Module Explorers realisieren. Neben der Verwaltung von Moduldaten und der Überprüfung von Modulimporten gibt es umfangreiche GUI-Komponenten, die mit Tkinter umgesetzt wurden. Außerdem werden Konfigurationen persistiert und diverse Hilfsfunktionen (z. B. zum Speichern von Diagrammen) bereitgestellt.


---

Klassen

ModuleData

Beschreibung:
Verwaltet eine modulare Datenbank, die Module nach Kategorien (wie Frontend, Backend, Web, Tooling etc.) gruppiert. Die Klasse stellt Methoden zur Abfrage von Kategorien, Modulen und Suchfunktionen zur Verfügung.

Methoden

__init__(self)
Initialisiert die Datenbank mit vordefinierten Kategorien und Modulinformationen.

get_categories(self) -> List[str]
Gibt die Liste aller verfügbaren Kategorien zurück.

get_modules_by_category(self, category: str) -> List[Dict[str, str]]
Liefert alle Module, die zu einer bestimmten Kategorie gehören.
Parameter:

category: Name der Kategorie
Rückgabewert:
Liste von Dictionaries mit Modulnamen, Beschreibungen und Dokumentations-URLs.


get_module_names(self) -> List[str]
Erzeugt eine Liste aller Modulnamen aus allen Kategorien.

search_modules(self, query: str) -> List[Dict[str, Any]]
Sucht nach Modulen anhand einer Suchanfrage im Namen oder in der Beschreibung.
Parameter:

query: Suchbegriff
Rückgabewert:
Liste der Module, denen das Suchkriterium entspricht, jeweils ergänzt um das Kategoriefeld.


get_module_popularity(self, category: str) -> Dict[str, int]
Simuliert ein Popularitätsranking für Module einer Kategorie (zum Beispiel basierend auf zufällig generierten Werten).
Parameter:

category: Name der Kategorie
Rückgabewert:
Dictionary, das Modulnamen und zugehörige Popularitätswerte enthält.




---

ModuleChecker

Beschreibung:
Bietet statische Methoden zur Überprüfung, ob Module importiert werden können, zur Ermittlung der Modulversionen sowie zur Generierung von Installationsbefehlen.

Statische Methoden

check_importable(module_names: List[str]) -> Dict[str, bool]
Überprüft, ob die in der Liste angegebenen Module importierbar sind.
Parameter:

module_names: Liste der zu testenden Modulnamen
Rückgabewert:
Dictionary, in dem jedem Modulname ein Boolean-Wert zugeordnet ist (True bei erfolgreichem Import, sonst False).


get_module_version(module_name: str) -> str
Versucht, die Version eines Moduls zu ermitteln, indem unterschiedliche Attributnamen sowie pkg_resources abgefragt werden.
Parameter:

module_name: Name des Moduls
Rückgabewert:
Versionsnummer als String oder "N/A", falls keine Version ermittelt werden kann.


get_module_install_command(module_name: str, platform_name: str = None) -> str
Generiert einen Befehl zum Installieren eines Moduls, wobei die Plattform (Windows, Linux, macOS) berücksichtigt wird.
Parameter:

module_name: Name des Moduls

platform_name (optional): Plattformname; falls nicht angegeben, wird der aktuelle Plattformname ermittelt.
Rückgabewert:
Installationsbefehl als String.




---

ConfigManager

Beschreibung:
Verwaltet die Anwendungskonfiguration, speichert und lädt ausgewählte Module sowie Einstellungen wie Theme, Sprache und Fenstergröße.

Methoden

__init__(self)
Initialisiert den Konfigurationsmanager, erstellt bei Bedarf den Konfigurationsordner und lädt die Standard- bzw. gespeicherte Konfiguration.

load_config(self) -> Dict[str, Any]
Lädt die Konfiguration aus einer JSON-Datei und aktualisiert dabei die Standardkonfiguration.
Rückgabewert:
Konfigurations-Dictionary.

save_config(self) -> bool
Speichert die aktuelle Konfiguration in der Datei.
Rückgabewert:
True, falls das Speichern erfolgreich war, ansonsten False.

get_selected_modules(self) -> List[str]
Gibt die aktuell ausgewählten Module zurück.

set_selected_modules(self, modules: List[str]) -> None
Aktualisiert die Liste der ausgewählten Module und speichert die Konfiguration.

get_theme(self) -> str
Gibt das aktuell konfigurierte Theme ("light" oder "dark") zurück.

set_theme(self, theme: str) -> None
Setzt das Theme, sofern ein gültiger Wert übergeben wird, und speichert die Änderung.
Parameter:

theme: "light" oder "dark"


get_language(self) -> str
Gibt die konfigurierte Sprache ("de" oder "en") zurück.

set_language(self, language: str) -> None
Setzt die Sprache, sofern ein gültiger Wert übergeben wird, und speichert die Änderung.
Parameter:

language: "de" oder "en"


get_window_size(self) -> str
Gibt die gespeicherte Fenstergröße im Format "BreitexHöhe" zurück.

set_window_size(self, size: str) -> None
Aktualisiert die Fenstergröße in der Konfiguration.
Parameter:

size: Fenstergröße als String (z. B. "900x700").




---

ModuleExplorerApp

Beschreibung:
Implementiert die Hauptanwendung des Module Explorers mit sämtlichen GUI-Komponenten. Diese Klasse koordiniert die Darstellung, die Interaktion und die Datenverwaltung.

Methoden (Auswahl)

__init__(self, root)
Initialisiert die Anwendung: Konfiguriert das Hauptfenster, lädt die Konfiguration, setzt Farben und Styles und erstellt alle Widgets.
Parameter:

root: Haupt-Tkinter-Fenster.


_configure_styles(self)
Definiert und passt die Tkinter-Styles (wie TFrame, TButton, TLabel usw.) basierend auf dem aktuellen Farbschema an.

on_window_resize(self, event)
Wird beim Ändern der Fenstergröße aufgerufen und speichert die neue Größe nach einer kurzen Verzögerung.

_save_window_size(self)
Speichert die aktuelle Fenstergröße in der Konfiguration (nur im Normalzustand).

create_widgets(self)
Baut die Benutzeroberfläche auf – von Header, Beschreibungen und Einstellungsbereichen bis hin zu den Kategorie-Buttons und Listen der ausgewählten Module.

_create_category_buttons(self)
Erstellt ein scrollbares Raster mit Buttons für jede Modul-Kategorie, inklusive Hover-Effekten und Klick-Events, die zum Anzeigen der entsprechenden Module führen.

change_theme(self, theme)
Wechselt das Theme (Farbschema) der Anwendung und aktualisiert die UI entsprechend.
Parameter:

theme: "light" oder "dark".


add_missing_imports(self)
Analysiert einen Eingabetext, extrahiert mögliche Modulnamen und fügt diese, sofern sie nicht zu den Standardbibliotheken oder Schlüsselwörtern gehören, der Auswahlliste hinzu.

_normalize_to_pypi_name(self, module_name)
Normalisiert einen Modulnamen zu einem PyPI-Paketnamen anhand eines Mappings bekannter Abweichungen.
Parameter:

module_name: Ursprünglicher Modulname.
Rückgabewert:
Normalisierter Name (oder unverändert, falls keine Abweichung vorliegt).


on_module_select(self, event)
Reagiert auf Klicks in der Modul-Tabelle, um Module zur Auswahlliste hinzuzufügen oder daraus zu entfernen, und aktualisiert den entsprechenden Status in der UI.

show_pypi_info(self, module_name)
Öffnet ein neues Fenster, in dem Informationen zu einem Modul (abgerufen von PyPI) angezeigt werden.
Parameter:

module_name: Name des Moduls.


update_import_code(self, text_widget, module_list, include_tests)
Generiert und aktualisiert den angezeigten Import-Code für die ausgewählten Module. Optional wird ein Test-Code eingebaut, um die Importfähigkeit zu überprüfen.
Parameter:

text_widget: Das Textfeld, in dem der Code dargestellt wird.

module_list: Liste der Module, für die der Code erstellt werden soll.

include_tests: Boolean, ob Test-Code hinzugefügt wird.


copy_to_clipboard(self, text)
Kopiert den übergebenen Text in die Zwischenablage und zeigt eine Bestätigung an.
Parameter:

text: Zu kopierender Text.


show_popularity_chart(self, category: str)
Zeigt ein Balkendiagramm, das die simulierte Popularität der Module in der angegebenen Kategorie darstellt.
Parameter:

category: Name der Kategorie.


run_import_test(self)
Führt einen Import-Test für die im Eingabefeld angegebenen Module durch, zeigt die Ergebnisse (erfolgreiche und fehlgeschlagene Importe) an und fügt Module ggf. der Auswahlliste hinzu.


Hinweis: Weitere Methoden zur Interaktion mit der Benutzeroberfläche (z. B. zum Kopieren von Befehlen, Speichern von Diagrammen, Öffnen von Dokumentationen) sind ebenfalls vorhanden, wurden aber hier nur exemplarisch aufgeführt.


---

Globale Funktionen

check_python_version() -> bool
Überprüft, ob die aktuell verwendete Python-Version mindestens 3.6 beträgt.
Rückgabewert:
True bei kompatibler Version, ansonsten wird ein Fehlerdialog angezeigt und False zurückgegeben.

main()
Hauptfunktion, die die Anwendung startet.
Führt zunächst die Versionsprüfung durch, initialisiert das Tkinter-Fenster (inklusive Icon-Einstellungen) und startet anschließend die Hauptschleife der GUI.

if __name__ == "__main__": main()
Stellt sicher, dass die Anwendung gestartet wird, wenn das Skript direkt ausgeführt wird.



---

Zusammenfassung

Die Datei Importus3.py kombiniert verschiedene Funktionalitäten:

Datenmanagement: Mit der Klasse ModuleData werden Modulinformationen kategorisiert und Suchfunktionen bereitgestellt.

Modulprüfung: ModuleChecker übernimmt die Überprüfung der Importfähigkeit und Versionsermittlung.

Konfigurationsverwaltung: ConfigManager sorgt für das Speichern und Laden von Benutzereinstellungen.

Benutzeroberfläche: ModuleExplorerApp integriert alle GUI-Elemente, ermöglicht die Interaktion (z. B. Importtests, Anzeige von PyPI-Informationen, Diagrammen) und stellt die Verbindung zu den darunterliegenden Funktionen her.

Globale Funktionen: check_python_version und main starten und sichern den reibungslosen Ablauf der Anwendung.


Diese Dokumentation bietet einen schnellen Überblick über die Architektur und die wichtigsten Funktionen der Anwendung. Für weitere Details und zur Anpassung der Anwendung können die Quellcode-Kommentare und Docstrings direkt im Code nachgelesen werden , .


---

Diese Funktionsdokumentation in Markdown dient als Referenz und Leitfaden zur Nutzung und Erweiterung des Python Module Explorers. Falls weitere Informationen oder Anpassungen benötigt werden, kann der Code entsprechend ergänzt werden.


