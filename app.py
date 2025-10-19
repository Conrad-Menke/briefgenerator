#!/usr/bin/env python3
"""
Brief-Generator Web-App
Flask-Webanwendung zum Erstellen von Briefen als PDF

Installation:
pip install flask reportlab pillow

Starten:
python app.py

Dann öffne: http://localhost:8888
"""

from flask import Flask, render_template_string, request, send_file, jsonify
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from datetime import date
import os
import io
import base64
import config
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / config.ORDNER_STATIC
WAPPEN_FARBE = STATIC_DIR / config.DATEI_WAPPEN_FARBE
WAPPEN_SW = STATIC_DIR / config.DATEI_WAPPEN_SW

ABSENDER_STRASSE = config.STRASSE
ABSENDER_PLZ_ORT = f"{config.PLZ} {config.ORT}"

STATIC_DIR.mkdir(exist_ok=True)

def get_wappen_base64(pfad):
    if os.path.exists(pfad):
        with open(pfad, 'rb') as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    return None

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Brief-Generator - Familie Menke</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Montserrat:wght@300;400;600&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Montserrat', sans-serif;
            background: #45663C;
            min-height: 100vh;
            padding: 40px 20px;
            position: relative;
            overflow-x: hidden;
        }
        
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 20% 50%, rgba(255,255,255,0.05) 0%, transparent 50%),
                radial-gradient(circle at 80% 50%, rgba(255,255,255,0.03) 0%, transparent 50%);
            pointer-events: none;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            border-radius: 30px;
            padding: 60px;
            box-shadow: 
                0 30px 100px rgba(0,0,0,0.3),
                0 10px 30px rgba(0,0,0,0.2);
            position: relative;
            backdrop-filter: blur(10px);
        }
        
        .container::before {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
            border-radius: 30px;
            z-index: -1;
            opacity: 0.5;
            filter: blur(20px);
        }
        
        .header-section {
            text-align: center;
            margin-bottom: 50px;
            position: relative;
        }
        
        .wappen-container {
            width: 120px;
            height: 120px;
            margin: 0 auto 30px;
            position: relative;
            animation: float 3s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        .wappen-img {
            width: 100%;
            height: 100%;
            object-fit: contain;
            filter: drop-shadow(0 10px 20px rgba(0,0,0,0.2));
        }
        
        .wappen-placeholder {
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 3em;
            font-weight: bold;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }
        
        h1 {
            font-family: 'Playfair Display', serif;
            color: #1a1a2e;
            margin-bottom: 10px;
            font-size: 3em;
            font-weight: 700;
            letter-spacing: -1px;
        }
        
        .subtitle {
            color: #6c757d;
            margin-bottom: 10px;
            font-size: 1.2em;
            font-weight: 300;
            letter-spacing: 2px;
            text-transform: uppercase;
        }
        
        .decorative-line {
            width: 100px;
            height: 3px;
            background: linear-gradient(90deg, #667eea, #764ba2);
            margin: 20px auto 40px;
            border-radius: 2px;
        }
        
        .form-group {
            margin-bottom: 30px;
        }
        
        label {
            display: block;
            margin-bottom: 10px;
            color: #2c3e50;
            font-weight: 600;
            font-size: 0.95em;
            letter-spacing: 0.5px;
        }
        
        input[type="text"],
        textarea,
        select {
            width: 100%;
            padding: 15px 20px;
            border: 2px solid #e1e8ed;
            border-radius: 12px;
            font-size: 16px;
            transition: all 0.3s ease;
            background: #ffffff;
            font-family: 'Montserrat', sans-serif;
        }
        
        input[type="text"]:focus,
        textarea:focus,
        select:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
            transform: translateY(-2px);
        }
        
        textarea {
            resize: vertical;
            min-height: 180px;
            line-height: 1.6;
        }
        
        .radio-group {
            display: flex;
            gap: 40px;
            margin-top: 15px;
        }
        
        .radio-option {
            display: flex;
            align-items: center;
            gap: 12px;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        .radio-option:hover {
            transform: translateX(5px);
        }
        
        .radio-option input[type="radio"] {
            width: 22px;
            height: 22px;
            cursor: pointer;
            accent-color: #667eea;
        }
        
        .radio-option label {
            cursor: pointer;
            margin-bottom: 0;
            font-weight: 400;
        }
        
        button {
            background: #AC3224;
            color: white;
            border: none;
            padding: 18px 50px;
            font-size: 18px;
            font-weight: 600;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
            position: relative;
            overflow: hidden;
            letter-spacing: 0.5px;
        }

        button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }
        
        button:hover::before {
            left: 100%;
        }
        
        button:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
        }
        
        button:active {
            transform: translateY(-1px);
        }
        
        .section-title {
            color: #2c3e50;
            font-size: 1.4em;
            margin-top: 40px;
            margin-bottom: 20px;
            padding-bottom: 12px;
            border-bottom: 2px solid #e1e8ed;
            font-family: 'Playfair Display', serif;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .section-title::before {
            content: '';
            width: 4px;
            height: 24px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 2px;
        }
        
        .hint {
            font-size: 0.85em;
            color: #95a5a6;
            font-style: italic;
            margin-left: 5px;
            font-weight: 300;
        }
        
        .logo-preview {
            display: flex;
            gap: 30px;
            margin-top: 20px;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        .logo-option {
            text-align: center;
            padding: 15px;
            border-radius: 12px;
            transition: all 0.3s;
            cursor: pointer;
            border: 2px solid transparent;
        }
        
        .logo-option:hover {
            background: #f8f9fa;
            transform: translateY(-5px);
        }
        
        .logo-option.selected {
            border-color: #667eea;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.05), rgba(118, 75, 162, 0.05));
        }
        
        .logo-option img {
            width: 80px;
            height: 80px;
            object-fit: contain;
            margin-bottom: 10px;
        }
        
        .logo-option .no-logo-placeholder {
            width: 80px;
            height: 80px;
            margin: 0 auto 10px;
            border: 3px dashed #ccc;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #999;
            font-size: 2em;
        }
        
        .success-message {
            position: fixed;
            top: 20px;
            right: -400px;
            background: linear-gradient(135deg, #00b09b, #96c93d);
            color: white;
            padding: 20px 30px;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,176,155,0.3);
            transition: right 0.5s ease;
            z-index: 1000;
        }
        
        .success-message.show {
            right: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header-section">
            <div class="wappen-container">
                {% if wappen_base64 %}
                <img src="data:image/png;base64,{{ wappen_base64 }}" alt="Familie Menke Wappen" class="wappen-img">
                {% else %}
                <div class="wappen-placeholder">M</div>
                {% endif %}
            </div>
            <h1>Brief-Generator</h1>
            <p class="subtitle">Familie {{familienname}}</p>
            <div class="decorative-line"></div>
        </div>
        
        <form method="POST" action="/generate" id="briefForm">
            
            <div class="section-title">Logo-Auswahl</div>
            <div class="form-group">
                <div class="logo-preview">
                    <div class="logo-option selected" onclick="selectLogo(this, '1')">
                        {% if wappen_farbe_base64 %}
                        <img src="data:image/png;base64,{{ wappen_farbe_base64 }}" alt="Farbiges Wappen">
                        {% else %}
                        <div style="width: 80px; height: 80px; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 50%; margin: 0 auto 10px;"></div>
                        {% endif %}
                        <input type="radio" id="logo1" name="logo" value="1" checked style="display: none;">
                        <label for="logo1">Farbiges Wappen</label>
                    </div>
                    <div class="logo-option" onclick="selectLogo(this, '2')">
                        {% if wappen_sw_base64 %}
                        <img src="data:image/png;base64,{{ wappen_sw_base64 }}" alt="Schwarz-Weiß Wappen">
                        {% else %}
                        <div style="width: 80px; height: 80px; background: #2c3e50; border-radius: 50%; margin: 0 auto 10px;"></div>
                        {% endif %}
                        <input type="radio" id="logo2" name="logo" value="2" style="display: none;">
                        <label for="logo2">Schwarz-Weiß</label>
                    </div>
                    <div class="logo-option" onclick="selectLogo(this, '3')">
                        <div class="no-logo-placeholder">∅</div>
                        <input type="radio" id="logo3" name="logo" value="3" style="display: none;">
                        <label for="logo3">Kein Wappen</label>
                    </div>
                </div>
            </div>

            <div class="section-title">Absender</div>
            <div class="form-group">
                <label>Wer schreibt den Brief?</label>
                <div class="radio-group">
                    <div class="radio-option">
                        <input type="radio" id="{{vorname_1}}" name="absender" value="s" checked>
                        <label for="{{vorname_1}}">{{vorname_1}} {{nachname_1}}</label>
                    </div>
                    <div class="radio-option">
                        <input type="radio" id="{{vorname_2}}" name="absender" value="c">
                        <label for="{{vorname_2}}">{{vorname_2}} {{nachname_2}}</label>
                    </div>
                    <div class="radio-option">
                        <input type="radio" id="beide" name="absender" value="b">
                        <label for="beide">Beide</label>
                    </div>
                </div>
            </div>

            <div class="section-title">Empfänger</div>
            <div class="radio-group">
                <div class="radio-option">
                    <input type="radio" id="anrede_none" name="emp_anrede" value="" checked>
                    <label for="anrede_none">Keine Anrede</label>
                </div>
                <div class="radio-option">
                    <input type="radio" id="anrede_herr" name="emp_anrede" value="Herr">
                    <label for="anrede_herr">Herr</label>
                </div>
                <div class="radio-option">
                    <input type="radio" id="anrede_frau" name="emp_anrede" value="Frau">
                    <label for="anrede_frau">Frau</label>
                </div>
            </div>
            <div class="form-group">
                <label for="emp_name">Name</label>
                <input type="text" id="emp_name" name="emp_name" required placeholder="Max Mustermann GmbH">
            </div>
            <div class="form-group">
                <label for="emp_strasse">Straße und Hausnummer</label>
                <input type="text" id="emp_strasse" name="emp_strasse" required placeholder="Beispielstraße 123">
            </div>
            <div class="form-group">
                <label for="emp_plz_ort">PLZ und Ort</label>
                <input type="text" id="emp_plz_ort" name="emp_plz_ort" required placeholder="12345 Musterstadt">
            </div>

            <div class="section-title">Briefinhalt</div>
            <div class="form-group">
                <label for="betreff">Betreff</label>
                <input type="text" id="betreff" name="betreff" required placeholder="Betreffzeile des Briefes">
            </div>
            <div class="form-group">
                <label for="anrede">Anrede <span class="hint">(Standard: "Sehr geehrter Herr/ geehrte Frau XYZ,")</span></label>
                <input type="text" id="anrede" name="anrede" placeholder="Sehr geehrte Damen und Herren,">
            </div>
            <div class="form-group">
                <label for="brieftext">Brieftext</label>
                <textarea id="brieftext" name="brieftext" required placeholder="Hier den Haupttext des Briefes eingeben..."></textarea>
            </div>
            <div class="form-group">
                <label for="grußformel">Grußformel <span class="hint">(Standard: "Mit freundlichen Grüßen,")</span></label>
                <input type="text" id="grußformel" name="grußformel" placeholder="Mit freundlichen Grüßen,">
            </div>

            <button type="submit">Brief als PDF herunterladen</button>
        </form>
    </div>
    
    <div class="success-message" id="successMessage">
        ✓ PDF wird erstellt und heruntergeladen...
    </div>
    
    <script>
        function selectLogo(element, value) {
            document.querySelectorAll('.logo-option').forEach(opt => {
                opt.classList.remove('selected');
            });
            element.classList.add('selected');
            document.getElementById('logo' + value).checked = true;
        }
        
        document.getElementById('briefForm').addEventListener('submit', function() {
            const successMsg = document.getElementById('successMessage');
            successMsg.classList.add('show');
            setTimeout(() => {
                successMsg.classList.remove('show');
            }, 3000);
        });
    </script>
</body>
</html>
"""

def zeichne_fusszeile(c, seite, breite, hoehe):
    y_pos = 1.5 * cm
    x_pos = breite / 2
    fuss_text = f"Seite {seite}"
    c.setFont("Helvetica", 9)
    c.drawCentredString(x_pos, y_pos, fuss_text)

def erstelle_brief_pdf(daten):
    buffer = io.BytesIO()
    breite, hoehe = A4
    c = canvas.Canvas(buffer, pagesize=A4)
    brieftext = daten['brieftext'].replace('\r\n', '\n').replace('\r', '\n')
    
    def zeichne_kopfzeile(c, mit_adresse=True):
        wappen_pfad = daten.get('wappen_pfad')
        hat_wappen = wappen_pfad and os.path.exists(wappen_pfad)
        
        if hat_wappen:
            wappen_hoehe_pos = hoehe - 3.5*cm
            wappen_breite = 3*cm
            
            try:
                c.drawImage(wappen_pfad, 
                           (breite - wappen_breite) / 2, wappen_hoehe_pos,
                           width=wappen_breite, height=wappen_breite,
                           preserveAspectRatio=True,
                           mask='auto')
            except:
                pass
            
            linie_y = wappen_hoehe_pos + (wappen_breite / 2)
            
            linke_linie_start = 1*cm
            linke_linie_ende = (breite - wappen_breite) / 2 - 0.5*cm
            c.line(linke_linie_start, linie_y, linke_linie_ende, linie_y)
            
            rechte_linie_start = (breite + wappen_breite) / 2 + 0.5*cm
            rechte_linie_ende = breite - 1*cm
            c.line(rechte_linie_start, linie_y, rechte_linie_ende, linie_y)
            
            # PERSÖNLICHE DATEN - Familienname ändern:
            c.setFont("Helvetica-Bold", 11)
            familie_text = "Familie " + config.FAMILIENNAME
            text_breite_familie = c.stringWidth(familie_text, "Helvetica-Bold", 11)
            c.drawString(rechte_linie_ende - text_breite_familie, linie_y + 0.3*cm, familie_text)
        
        if mit_adresse:
            anschrift_x = 2.5*cm
            anschrift_y_start = hoehe - 4.8*cm
            
            c.setFont("Helvetica", 8)
            absender_zeile = f"{daten['absender']['name']}, {daten['absender']['strasse']}, {daten['absender']['plz_ort']}"
            c.drawString(anschrift_x, anschrift_y_start, absender_zeile)
            
            c.setFont("Helvetica", 11)
            y_pos = anschrift_y_start - 0.6*cm
            
            if daten['empfaenger'].get('anrede'):
                c.drawString(anschrift_x, y_pos, daten['empfaenger']['anrede'])
                y_pos -= 0.5*cm
            
            c.drawString(anschrift_x, y_pos, daten['empfaenger']['name'])
            y_pos -= 0.5*cm
            
            c.drawString(anschrift_x, y_pos, daten['empfaenger']['strasse'])
            y_pos -= 0.5*cm
            
            c.drawString(anschrift_x, y_pos, daten['empfaenger']['plz_ort'])
            
            # PERSÖNLICHE DATEN - Ort im Datum ändern:
            datum_y = hoehe - 9*cm
            heute = date.today().strftime("%d.%m.%Y")
            datum_text = config.ORT + ", den " + heute
            datum_breite = c.stringWidth(datum_text, "Helvetica", 11)
            c.drawString(breite - 2.5*cm - datum_breite, datum_y, datum_text)
            
            betreff_y = hoehe - 11*cm
            c.setFont("Helvetica-Bold", 12)

            betreff_max_width = breite - 5*cm
            betreff_text = daten['betreff']
            betreff_woerter = betreff_text.split()
            betreff_zeilen = []
            aktuelle_zeile = ""

            for wort in betreff_woerter:
                test_zeile = aktuelle_zeile + " " + wort if aktuelle_zeile else wort
                if stringWidth(test_zeile, "Helvetica-Bold", 12) <= betreff_max_width:
                    aktuelle_zeile = test_zeile
                else:
                    if aktuelle_zeile:
                        betreff_zeilen.append(aktuelle_zeile)
                    aktuelle_zeile = wort

            if aktuelle_zeile:
                betreff_zeilen.append(aktuelle_zeile)

            for zeile in betreff_zeilen:
                c.drawString(2.5*cm, betreff_y, zeile)
                betreff_y -= 0.5*cm

            anrede_y = betreff_y - 0.5*cm
            c.setFont("Helvetica", 11)
            c.drawString(2.5*cm, anrede_y, daten['anrede'])

            return anrede_y - 1*cm
        else:
            return hoehe - 5*cm
    
    y_pos = zeichne_kopfzeile(c, mit_adresse=True)
    zeichne_fusszeile(c, c.getPageNumber(), breite, hoehe)
    
    c.setFont("Helvetica", 11)
    left_margin = 2.5*cm
    right_margin = breite - 2.5*cm
    max_width = right_margin - left_margin
    line_height = 0.5*cm
    
    def text_in_zeilen_aufteilen(text, font, font_size, max_width):
        zeilen = []
        absaetze = text.split('\n')
        
        for i, absatz in enumerate(absaetze):
            if i > 0:
                zeilen.append("")
            
            if not absatz.strip():
                continue
            
            stripped = absatz.strip()
            is_bullet = stripped.startswith(("•", "-", "*"))
            if is_bullet:
                absatz = stripped[1:].strip()
            
            woerter = absatz.split()
            aktuelle_zeile = ""
            
            for wort in woerter:
                test_zeile = aktuelle_zeile + " " + wort if aktuelle_zeile else wort
                if stringWidth(test_zeile, font, font_size) <= max_width:
                    aktuelle_zeile = test_zeile
                else:
                    if aktuelle_zeile:
                        zeilen.append(('bullet' if is_bullet else 'normal', aktuelle_zeile))
                        is_bullet = False
                    aktuelle_zeile = wort
            
            if aktuelle_zeile:
                zeilen.append(('bullet' if is_bullet else 'normal', aktuelle_zeile))
        
        return zeilen
    
    zeilen = text_in_zeilen_aufteilen(brieftext, "Helvetica", 11, max_width)
    
    for zeile_info in zeilen:
        if y_pos < 4*cm:
            c.showPage()
            y_pos = zeichne_kopfzeile(c, mit_adresse=False)
            zeichne_fusszeile(c, c.getPageNumber(), breite, hoehe)
            c.setFont("Helvetica", 11)
        
        if zeile_info == "":
            y_pos -= line_height
            continue
        
        zeilen_typ, zeilen_text = zeile_info
        
        if zeilen_typ == 'bullet':
            einrueckung = 0.8 * cm
            c.setFillColorRGB(0, 0, 0)
            bullet_radius = 0.07 * cm
            bullet_offset_x = 0.2 * cm
            bullet_offset_y = line_height / 2.8
            c.circle(left_margin + einrueckung + bullet_offset_x, y_pos + bullet_offset_y, bullet_radius, fill=1)
            c.drawString(left_margin + einrueckung + 0.5*cm, y_pos, zeilen_text)
        else:
            c.drawString(left_margin, y_pos, zeilen_text)
        y_pos -= line_height
    
    if y_pos < 5*cm:
        c.showPage()
        y_pos = zeichne_kopfzeile(c, mit_adresse=False)
        zeichne_fusszeile(c, c.getPageNumber(), breite, hoehe)
        c.setFont("Helvetica", 11)

    y_pos -= 1*cm
    c.drawString(left_margin, y_pos, daten.get('grußformel', 'Mit freundlichen Grüßen,'))
    y_pos -= 0.5*cm
    
    absender_auswahl = daten['absender'].get('auswahl', 's')
    
    # PERSÖNLICHE DATEN - Unterschriftsdateien anpassen. Vielleicht Pfade ändern:
    if absender_auswahl == 'b':
        unterschrift_sophia = STATIC_DIR / config.DATEI_UNTERSCHRIFT_1
        unterschrift_conrad = STATIC_DIR / config.DATEI_UNTERSCHRIFT_2
        
        unterschrift_hoehe = 2.5*cm
        unterschrift_breite = 5*cm
        y_pos -= 2.2*cm
        
        if unterschrift_sophia.exists():
            try:
                c.drawImage(
                    str(unterschrift_sophia),
                    left_margin,
                    y_pos,
                    width=unterschrift_breite,
                    height=unterschrift_hoehe,
                    preserveAspectRatio=True,
                    mask='auto'
                )
            except:
                pass
        
        rechte_position = breite / 2 + 1*cm
        if unterschrift_conrad.exists():
            try:
                c.drawImage(
                    str(unterschrift_conrad),
                    rechte_position,
                    y_pos,
                    width=unterschrift_breite,
                    height=unterschrift_hoehe,
                    preserveAspectRatio=True,
                    mask='auto'
                )
            except:
                pass
        
        y_pos -= 0.5*cm
        c.drawString(left_margin, y_pos, config.ABSENDER_VORNAME_1 + " " + config.ABSENDER_NACHNAME_1)
        c.drawString(rechte_position, y_pos, config.ABSENDER_VORNAME_2 + " " + config.ABSENDER_NACHNAME_2)
    
    else:
        unterschrift_datei = None
        if absender_auswahl == 's':
            unterschrift_datei = STATIC_DIR / config.DATEI_UNTERSCHRIFT_1
        elif absender_auswahl == 'c':
            unterschrift_datei = STATIC_DIR / config.DATEI_UNTERSCHRIFT_2
        
        if unterschrift_datei and unterschrift_datei.exists():
            try:
                unterschrift_hoehe = 2.5*cm
                unterschrift_breite = 5*cm
                y_pos -= 2.2*cm
                c.drawImage(
                    str(unterschrift_datei),
                    left_margin,
                    y_pos,
                    width=unterschrift_breite,
                    height=unterschrift_hoehe,
                    preserveAspectRatio=True,
                    mask='auto'
                )
                y_pos -= 0.5*cm
            except:
                pass
        else:
            y_pos -= 2*cm
        
        c.drawString(left_margin, y_pos, daten['absender']['name'])
    
    c.save()
    buffer.seek(0)
    return buffer

@app.route('/')
def index():
    wappen_farbe_b64 = get_wappen_base64(WAPPEN_FARBE)
    wappen_sw_b64 = get_wappen_base64(WAPPEN_SW)
    
    return render_template_string(
        HTML_TEMPLATE,
        wappen_base64=wappen_farbe_b64,
        wappen_farbe_base64=wappen_farbe_b64,
        wappen_sw_base64=wappen_sw_b64,
        familienname=config.FAMILIENNAME,
        vorname_1=config.ABSENDER_VORNAME_1,
        vorname_2=config.ABSENDER_VORNAME_2,
        nachname_1=config.ABSENDER_NACHNAME_1,
        nachname_2=config.ABSENDER_NACHNAME_2
    )

@app.route('/generate', methods=['POST'])
def generate():
    logo_auswahl = request.form.get('logo')
    if logo_auswahl == '1':
        wappen_pfad = str(WAPPEN_FARBE)
    elif logo_auswahl == '2':
        wappen_pfad = str(WAPPEN_SW)
    else:
        wappen_pfad = None
    
    # PERSÖNLICHE DATEN - Namen der Absender anpassen:
    absender_auswahl = request.form.get('absender')
    if absender_auswahl == 's':
        absender_name = config.ABSENDER_VORNAME_1 + " " + config.ABSENDER_NACHNAME_1
    elif absender_auswahl == 'c':
        absender_name = config.ABSENDER_VORNAME_2 + " " + config.ABSENDER_NACHNAME_2
    else:
        absender_name = f"{config.ABSENDER_VORNAME_1} {config.ABSENDER_NACHNAME_1} und {config.ABSENDER_VORNAME_2} {config.ABSENDER_NACHNAME_2}"
    
    anrede_manuell = request.form.get('anrede', '').strip()
    
    if anrede_manuell:
        anrede = anrede_manuell
    else:
        emp_anrede = request.form.get('emp_anrede', '')
        emp_name = request.form.get('emp_name', '')
        
        if emp_anrede == 'Herr':
            nachname = emp_name.split()[-1] if emp_name else ''
            anrede = f"Sehr geehrter Herr {nachname}," if nachname else "Sehr geehrter Herr,"
        elif emp_anrede == 'Frau':
            nachname = emp_name.split()[-1] if emp_name else ''
            anrede = f"Sehr geehrte Frau {nachname}," if nachname else "Sehr geehrte Frau,"
        else:
            anrede = "Sehr geehrte Damen und Herren,"
    
    grußformel = request.form.get('grußformel', '').strip()
    if not grußformel:
        grußformel = "Mit freundlichen Grüßen,"

    daten = {
        'absender': {
            'name': absender_name,
            'strasse': ABSENDER_STRASSE,
            'plz_ort': ABSENDER_PLZ_ORT,
            'auswahl': absender_auswahl
        },
        'empfaenger': {
            'anrede': request.form.get('emp_anrede', ''),
            'name': request.form.get('emp_name'),
            'strasse': request.form.get('emp_strasse'),
            'plz_ort': request.form.get('emp_plz_ort')
        },
        'anrede': anrede,
        'betreff': request.form.get('betreff'),
        'brieftext': request.form.get('brieftext'),
        'grußformel': grußformel,
        'wappen_pfad': wappen_pfad
    }
    
    try:
        pdf_buffer = erstelle_brief_pdf(daten)
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'brief_{date.today().strftime("%Y%m%d")}_{absender_auswahl}.pdf'
        )
    except Exception as e:
        return jsonify({"error": "Fehler beim Erstellen des PDFs"}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("✨ Brief-Generator - Familie" + " " + config.FAMILIENNAME)
    print("="*60)
    print("\n📍 Öffne in deinem Browser:")
    print("   http://localhost:8888")
    print("\n⏹️  Zum Beenden: Strg+C drücken\n")
    
    app.run(host='0.0.0.0', port=8888)