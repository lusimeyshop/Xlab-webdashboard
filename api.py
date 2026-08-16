from fastapi import FastAPI
from fastapi.responses import FileResponse
import mysql.connector

app = FastAPI()


def get_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="@Shayparmo24518",
        database="xlab_webdashboard"
    )

@app.get("/")
def home():
    return FileResponse(
        "templates/index.html",
        media_type="text/html"
    )


@app.get("/tickets")
def get_tickets():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM tickets")
    tickets = cursor.fetchall()

    cursor.close()
    db.close()

    return tickets
@app.get("/tickets/search")
def search_tickets(
    status: str | None = None,
    organisatie: str | None = None,
    zoekterm: str | None = None
):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    query = "SELECT * FROM tickets WHERE 1=1"
    waarden = []

    if status:
        query += " AND status = %s"
        waarden.append(status)

    if organisatie:
        query += " AND organisatie = %s"
        waarden.append(organisatie)

    if zoekterm:
        query += """
            AND (
                ticketnr LIKE %s
                OR onderwerp LIKE %s
                OR toelichting LIKE %s
            )
        """

        zoek = f"%{zoekterm}%"
        waarden.extend([zoek, zoek, zoek])

    query += " ORDER BY id DESC"

    cursor.execute(query, tuple(waarden))
    tickets = cursor.fetchall()

    cursor.close()
    db.close()

    return tickets


@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM tickets WHERE id = %s",
        (ticket_id,)
    )

    ticket = cursor.fetchone()

    cursor.close()
    db.close()

    if ticket is None:
        return {"message": "Ticket niet gevonden"}

    return ticket

from pydantic import BaseModel
from datetime import date

class TicketCreate(BaseModel):
    dossier_id: str
    status: str
    ticketnr:str
    soort_ticket: str
    aangemeld_door: str
    onderwerp: str
    omgeving: str
    prioriteit: str
    impact: str
    datum: date
    toelichting: str
    organisatie: str
    created_by: str
    modified_by: str


@app.post("/tickets")
def create_ticket(ticket: TicketCreate):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO tickets (
            dossier_id,
            status,
            ticketnr,
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
            modified_by
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            ticket.dossier_id,
            ticket.status,
            ticket.ticketnr,
            ticket.soort_ticket,
            ticket.aangemeld_door,
            ticket.onderwerp,
            ticket.omgeving,
            ticket.prioriteit,
            ticket.impact,
            ticket.datum,
            ticket.toelichting,
            ticket.organisatie,
            ticket.created_by,
            ticket.modified_by
        )
    )

    db.commit()

    new_id = cursor.lastrowid

    cursor.close()
    db.close()

    return {
        "message": "Ticket succesvol aangemaakt",
        "id": new_id
    }
class TicketUpdate(BaseModel):
    dossier_id: str
    status: str
    ticketnr: str
    soort_ticket: str
    aangemeld_door: str
    onderwerp: str
    omgeving: str
    prioriteit: str
    impact: str
    datum: date
    toelichting: str
    organisatie: str
    created_by: str
    modified_by: str


@app.put("/tickets/{ticket_id}")
def update_ticket(ticket_id: int, ticket: TicketUpdate):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        UPDATE tickets
        SET
            dossier_id = %s,
            status = %s,
            ticketnr = %s,
            soort_ticket = %s,
            aangemeld_door = %s,
            onderwerp = %s,
            omgeving = %s,
            prio = %s,
            impact = %s,
            datum = %s,
            toelichting = %s,
            organisatie = %s,
            created_by = %s,
            modified_by = %s
        WHERE id = %s
        """,
        (
            ticket.dossier_id,
            ticket.status,
            ticket.ticketnr,
            ticket.soort_ticket,
            ticket.aangemeld_door,
            ticket.onderwerp,
            ticket.omgeving,
            ticket.prioriteit,
            ticket.impact,
            ticket.datum,
            ticket.toelichting,
            ticket.organisatie,
            ticket.created_by,
            ticket.modified_by,
            ticket_id
        )
    )

    db.commit()

    if cursor.rowcount == 0:
        cursor.close()
        db.close()
        return {"message": "Ticket niet gevonden"}

    cursor.close()
    db.close()

    return {
        "message": "Ticket succesvol gewijzigd",
        "id": ticket_id
    }
@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: int):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM tickets WHERE id = %s",
        (ticket_id,)
    )

    db.commit()

    if cursor.rowcount == 0:
        cursor.close()
        db.close()
        return {"message": "Ticket niet gevonden"}

    cursor.close()
    db.close()

    return {
        "message": "Ticket succesvol verwijderd",
        "id": ticket_id
    }
