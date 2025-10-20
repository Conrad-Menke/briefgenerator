# 📬 Brief-Generator

Eine elegante Flask-Webanwendung zum Erstellen professioneller Briefe als PDF mit persönlichem Wappen und Unterschriften.

## ✨ Features

- 🎨 Moderne, responsive Web-Oberfläche
- 📄 Automatische PDF-Generierung mit korrekter Formatierung
- 🖼️ Unterstützung für Firmenlogos oder Familienwappen (farbig/schwarz-weiß)
- ✍️ Digitale Unterschriften
- 📝 Mehrseitige Briefe mit automatischem Seitenumbruch
- 🎯 Bullet-Points und Absätze werden korrekt formatiert

## 🚀 Installation

### Voraussetzungen

- Python 3.7 oder höher
- pip (Python Package Installer)

### Schritt 1: Repository klonen

```bash
git clone https://github.com/Conrad-Menke/briefgenerator/
cd brief-generator
```

### Schritt 2: Abhängigkeiten installieren

```bash
pip install flask reportlab pillow
```

### Schritt 3: Konfiguration einrichten

1. Kopiere `config.example.py` zu `config.py`:
   ```bash
   cp config.example.py config.py
   ```

2. Öffne `config.py` und trage deine persönlichen Daten ein:
   ```python
   ABSENDER_VORNAME_1 = "Dein Vorname"
   ABSENDER_NACHNAME_1 = "Dein Nachname"
   # ... weitere Anpassungen
   ```

### Schritt 4: Static-Ordner vorbereiten

Erstelle den `static/` Ordner und füge folgende Dateien hinzu:
- `logo.png` - Farbiges Logo
- `logosw.png` - Schwarz-Weiß Logo
- `Unterschrift_<Name1>.png` - Unterschrift Person 1
- `Unterschrift_<Name2>.png` - Unterschrift Person 2

**Hinweis:** Die Dateinamen müssen mit den Namen in `config.py` übereinstimmen!

## 🎯 Verwendung

### Starten der Anwendung

```bash
python app.py
```

Die Anwendung startet auf Port 8888. Öffne in deinem Browser:
```
http://localhost:8888
```

### Brief erstellen

1. **Logo auswählen**: Wähle zwischen farbigem Logo, Schwarz-Weiß oder keinem Logo
2. **Absender**: Wähle wer den Brief schreibt (Person 1, Person 2 oder beide)
3. **Empfänger**: Trage die Empfängerdaten ein
4. **Briefinhalt**: Fülle Betreff, Anrede, Text und Grußformel aus
5. **Generieren**: Klicke auf "Brief als PDF herunterladen"

Das PDF wird automatisch heruntergeladen und enthält:
- Professionellen Briefkopf mit Wappen
- Korrekte Anschrift nach DIN 5008
- Automatische Seitennummerierung
- Digitale Unterschrift(en)

## 📁 Projektstruktur

```
brief-generator/
├── app.py                 # Hauptanwendung
├── config.py              # Persönliche Konfiguration (nicht in Git!)
├── config.example.py      # Konfigurations-Vorlage
├── .gitignore            # Git-Ausschlüsse
├── README.md             # Diese Datei
└── static/               # Persönliche Dateien (nicht in Git!)
    ├── logo.png
    ├── logosw.png
    ├── Unterschrift_<Name1>.png
    └── Unterschrift_<Name2>.png
```

## 🔒 Sicherheitshinweise

- Die Datei `config.py` enthält persönliche Daten und wird **nicht** ins Git-Repository übertragen
- Der `static/` Ordner mit Logos und Unterschriften ist ebenfalls geschützt
- Denn in `config.py` und auch `static/` stehen deine persönliche Anschrift und deine privaten Logos/Wappen...

## 🛠️ Anpassungen

### Farben ändern

Die Farben können im HTML-Template in `app.py` angepasst werden:
- Hintergrundfarbe: `body { background: #45663C; }`
- Button-Farbe: `button { background: #AC3224; }`

### Port ändern

Ändere den Port in Zeile 417 von `app.py`:
```python
app.run(host='0.0.0.0', port=8888)  # Ändere 8888 zu deinem Wunsch-Port
```

## 🐛 Fehlerbehebung

### "Datei nicht gefunden" Fehler
- Prüfe ob alle Dateien im `static/` Ordner vorhanden sind
- Vergleiche Dateinamen in `config.py` mit tatsächlichen Dateien

### PDF wird nicht generiert
- Stelle sicher, dass alle Pflichtfelder ausgefüllt sind
- Prüfe die Browser-Konsole auf Fehlermeldungen

### Port bereits belegt
- Ändere den Port in `app.py` (siehe Anpassungen)
- Oder beende die andere Anwendung auf Port 8888

## 📝 Lizenz

Privates Projekt - Alle Rechte vorbehalten

**Hinweis:** Diese Anwendung ist für den privaten Gebrauch konzipiert.
