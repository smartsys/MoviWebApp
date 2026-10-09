# MoviWebApp

Webanwendung zum Verwalten von Lieblingsfilmen. Jeder Nutzer wählt seinen Namen
aus einer Liste und pflegt dort seine eigene Filmsammlung. Beim Hinzufügen eines
Films werden Regisseur, Erscheinungsjahr und Poster automatisch über die
[OMDb API](https://www.omdbapi.com/) ergänzt.

## Funktionen

- Nutzer anlegen und aus einer Liste auswählen
- Lieblingsfilme eines Nutzers als Posterraster anzeigen
- Film über Titel und optionales Jahr hinzufügen, Details kommen von OMDb
- Filmtitel ändern
- Film löschen
- Eigene Fehlerseiten für 404 und 500

## Technik

- Python mit Flask
- Flask-SQLAlchemy mit SQLite (`data/data.db`)
- requests für den Abruf der OMDb API
- python-dotenv für die Konfiguration
- HTML-Templates mit Jinja, eigenes CSS, Icons von Tabler Icons

## Installation

1. Repository klonen und in den Projektordner wechseln.
2. Virtuelle Umgebung anlegen und aktivieren:

   ```
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   Unter Windows: `.venv\Scripts\activate`

3. Abhängigkeiten installieren:

   ```
   pip install -r requirements.txt
   ```

4. Konfiguration anlegen: `.env.example` nach `.env` kopieren und den eigenen
   OMDb-API-Key eintragen. Einen kostenlosen Key gibt es unter
   https://www.omdbapi.com/apikey.aspx.

   ```
   OMDB_API_KEY=your_api_key
   OMDB_URL=https://www.omdbapi.com/
   ```

## Starten

```
python app.py
```

Die Anwendung läuft danach unter http://localhost:5000. Fehlende Tabellen werden
beim Start automatisch angelegt.

## Projektstruktur

```
MoviWebApp/
|-- app.py              Flask-Anwendung mit Routen und OMDb-Abruf
|-- models.py           SQLAlchemy-Modelle User und Movie
|-- data_manager.py     DataManager mit allen Datenbankoperationen
|-- requirements.txt
|-- .env.example        Vorlage für die Konfiguration
|-- data/
    |-- data.db         SQLite-Datenbank
|-- static/
    |-- style.css
|-- templates/
    |-- base.html       Grundlayout mit Navigation
    |-- icons.html      Makro für die Tabler Icons
    |-- index.html      Startseite mit Nutzerliste
    |-- movies.html     Filme eines Nutzers
    |-- 404.html
    |-- 500.html
```

## Routen

| Route | Methode | Zweck |
|---|---|---|
| `/` | GET | Startseite mit allen Nutzern und Formular für neue Nutzer |
| `/users` | POST | Neuen Nutzer anlegen |
| `/users/<user_id>/movies` | GET | Filme eines Nutzers anzeigen |
| `/users/<user_id>/movies` | POST | Film hinzufügen (mit OMDb-Abruf) |
| `/users/<user_id>/movies/<movie_id>/update` | POST | Titel eines Films ändern |
| `/users/<user_id>/movies/<movie_id>/delete` | POST | Film löschen |

## Datenmodell

**users**

| Spalte | Typ | Beschreibung |
|---|---|---|
| `id` | Integer | Primärschlüssel |
| `name` | String | Name des Nutzers |

**movies**

| Spalte | Typ | Beschreibung |
|---|---|---|
| `id` | Integer | Primärschlüssel |
| `name` | String | Filmtitel |
| `director` | String | Regisseur |
| `year` | Integer | Erscheinungsjahr |
| `poster_url` | String | URL des Posters |
| `user_id` | Integer | Fremdschlüssel auf `users.id` |

Jeder Film gehört genau einem Nutzer.

## Hinweise

- OMDb führt Filme unter dem Jahr ihres US-Starts. Wird ein Film mit Jahr nicht
  gefunden, hilft es, ihn ohne Jahr hinzuzufügen.
- Findet OMDb einen Film nicht oder ist der Dienst nicht erreichbar, wird der
  Film nur mit Titel und Jahr gespeichert.
- Die Anwendung ist für den lokalen Betrieb gedacht.
