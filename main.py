import pandas as pd
import mysql.connector

bestand = '"Ticketsysteem mockdata (1).xlsx"'

df = pd.read_excel(bestand)

print("Aantal tickets:", len(df))
print("Kolommen:")
print(df.columns.tolist())

db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="@Shayparmo24518",
    database="xlab_webdashboard"
)
print("Verbonden met MySQL!")
# Tickets importeren naar MySQL
cursor = db.cursor()

sql = """
INSERT IGNORE INTO tickets (
    dossier_id,
    status,
    ticketnr,
    gewijzigd,
    soort_ticket,
    aangemeld_door,
    onderwerp,
    omgeving,
    prio,
    impact,
    datum,
    toelichting,
    organisatie,
    created_by,
    created_at,
    modified_by,
    modified_at
)
VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s
)
"""

# Excel-kolommen koppelen aan MySQL-kolommen
kolommen = [
    "dossier_id",
    "Status",
    "Ticketnr",
    "Gewijzigd",
    "Soort ticket",
    "Aangemeld door",
    "Onderwerp",
    "Omgeving",
    "Prio",
    "Impact",
    "Datum",
    "Toelichting",
    "Organisatie",
    "created_by",
    "created_at",
    "modified_by",
    "modified_at"
]

# Lege Excel-waarden omzetten naar None
data = df[kolommen].where(df[kolommen].notna(), None)

# Datums goed verwerken
for kolom in ["Gewijzigd", "Datum", "created_at", "modified_at"]:
    data[kolom] = pd.to_datetime(data[kolom], errors="coerce")

data = data.where(data.notna(), None)

# Data naar MySQL
waarden = [tuple(row) for row in data.itertuples(index=False, name=None)]

cursor.executemany(sql, waarden)
db.commit()

print("Aantal geïmporteerde tickets:", cursor.rowcount)

cursor.close()
db.close()
