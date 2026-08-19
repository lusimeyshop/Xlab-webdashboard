import pandas as pd
import mysql.connector

bestand = r"Ticketsysteem mockdata (1).xlsx"

df = pd.read_excel(bestand)

print("Aantal regels in Excel:", len(df))
print("Kolommen:", df.columns.tolist())

db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="@Shayparmo24518",
    database="xlab_webdashboard"
)

cursor = db.cursor()

sql = """
INSERT INTO tickets (
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
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s)
"""

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

data = df[kolommen].copy()

for kolom in ["Gewijzigd", "Datum", "created_at", "modified_at"]:
    data[kolom] = pd.to_datetime(data[kolom], errors="coerce")

data = data.astype(object).where(pd.notna(data), None)

waarden = list(data.itertuples(index=False, name=None))

cursor.executemany(sql, waarden)
db.commit()

print("Geïmporteerd:", cursor.rowcount)

cursor.close()
db.close()