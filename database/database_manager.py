import sqlite3
from pathlib import Path
from typing import Any

from config import DATABASE_PATH


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(
        str(DATABASE_PATH)
    )
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS reports (
                report_id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_type TEXT NOT NULL CHECK(report_type IN ('lost', 'found')),
                item_name TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                colour TEXT,
                brand TEXT,
                location TEXT NOT NULL,
                report_date TEXT NOT NULL,
                contact_name TEXT NOT NULL,
                contact_email TEXT NOT NULL,
                contact_phone TEXT,
                image_path TEXT,
                status TEXT NOT NULL DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS matches (
                match_id INTEGER PRIMARY KEY AUTOINCREMENT,
                lost_report_id INTEGER NOT NULL,
                found_report_id INTEGER NOT NULL,
                image_similarity REAL DEFAULT 0,
                text_similarity REAL DEFAULT 0,
                category_similarity REAL DEFAULT 0,
                colour_similarity REAL DEFAULT 0,
                brand_similarity REAL DEFAULT 0,
                location_similarity REAL DEFAULT 0,
                date_similarity REAL DEFAULT 0,
                final_probability REAL DEFAULT 0,
                match_status TEXT NOT NULL DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (lost_report_id) REFERENCES reports(report_id),
                FOREIGN KEY (found_report_id) REFERENCES reports(report_id)
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS feedback (
                feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
                match_id INTEGER NOT NULL,
                actual_match INTEGER NOT NULL CHECK(actual_match IN (0, 1)),
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (match_id) REFERENCES matches(match_id)
            )
            """
        )
        cursor.execute(
            """
            PRAGMA table_info(reports)
            """
        )

        report_columns = {
            row[1]
            for row in cursor.fetchall()
        }

        if "feature_path" not in report_columns:
            cursor.execute(
                """
                ALTER TABLE reports
                ADD COLUMN feature_path TEXT
                """
            )

        connection.commit()


def add_report(
    report_type: str,
    item_name: str,
    category: str,
    description: str,
    colour: str,
    brand: str,
    location: str,
    report_date: str,
    contact_name: str,
    contact_email: str,
    contact_phone: str,
    image_path: str | None,
) -> int:
    if report_type not in {"lost", "found"}:
        raise ValueError("report_type must be either 'lost' or 'found'")

    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO reports (
                report_type,
                item_name,
                category,
                description,
                colour,
                brand,
                location,
                report_date,
                contact_name,
                contact_email,
                contact_phone,
                image_path
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                report_type,
                item_name,
                category,
                description,
                colour,
                brand,
                location,
                report_date,
                contact_name,
                contact_email,
                contact_phone,
                image_path,
            ),
        )

        connection.commit()

        return int(cursor.lastrowid)


def get_all_reports() -> list[dict[str, Any]]:
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM reports
            ORDER BY created_at DESC
            """
        )

        rows = cursor.fetchall()

    return [dict(row) for row in rows]


def get_reports_by_type(report_type: str) -> list[dict[str, Any]]:
    if report_type not in {"lost", "found"}:
        raise ValueError("report_type must be either 'lost' or 'found'")

    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM reports
            WHERE report_type = ?
            ORDER BY created_at DESC
            """,
            (report_type,),
        )

        rows = cursor.fetchall()

    return [dict(row) for row in rows]


def get_report_by_id(report_id: int) -> dict[str, Any] | None:
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM reports
            WHERE report_id = ?
            """,
            (report_id,),
        )

        row = cursor.fetchone()

    return dict(row) if row else None


def update_report_status(report_id: int, status: str) -> None:
    valid_statuses = {"active", "matched", "closed"}

    if status not in valid_statuses:
        raise ValueError(
            f"status must be one of: {', '.join(sorted(valid_statuses))}"
        )

    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE reports
            SET status = ?
            WHERE report_id = ?
            """,
            (status, report_id),
        )

        connection.commit()


def add_match(
    lost_report_id: int,
    found_report_id: int,
    image_similarity: float,
    text_similarity: float,
    category_similarity: float,
    colour_similarity: float,
    brand_similarity: float,
    location_similarity: float,
    date_similarity: float,
    final_probability: float,
) -> int:
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO matches (
                lost_report_id,
                found_report_id,
                image_similarity,
                text_similarity,
                category_similarity,
                colour_similarity,
                brand_similarity,
                location_similarity,
                date_similarity,
                final_probability
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                lost_report_id,
                found_report_id,
                image_similarity,
                text_similarity,
                category_similarity,
                colour_similarity,
                brand_similarity,
                location_similarity,
                date_similarity,
                final_probability,
            ),
        )

        connection.commit()

        return int(cursor.lastrowid)


def get_all_matches() -> list[dict[str, Any]]:
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM matches
            ORDER BY final_probability DESC
            """
        )

        rows = cursor.fetchall()

    return [dict(row) for row in rows]


def update_match_status(match_id: int, match_status: str) -> None:
    valid_statuses = {"pending", "confirmed", "rejected"}

    if match_status not in valid_statuses:
        raise ValueError(
            f"match_status must be one of: {', '.join(sorted(valid_statuses))}"
        )

    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE matches
            SET match_status = ?
            WHERE match_id = ?
            """,
            (match_status, match_id),
        )

        connection.commit()


def add_feedback(
    match_id: int,
    actual_match: bool,
    notes: str = "",
) -> int:
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO feedback (
                match_id,
                actual_match,
                notes
            )
            VALUES (?, ?, ?)
            """,
            (
                match_id,
                int(actual_match),
                notes,
            ),
        )

        connection.commit()

        return int(cursor.lastrowid)
def get_opposite_reports(
    report_type: str,
) -> list[dict[str, Any]]:
    if report_type not in {"lost", "found"}:
        raise ValueError(
            "report_type must be either 'lost' or 'found'"
        )

    opposite_type = (
        "found"
        if report_type == "lost"
        else "lost"
    )

    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM reports
            WHERE report_type = ?
            AND status = 'active'
            ORDER BY created_at DESC
            """,
            (opposite_type,),
        )

        rows = cursor.fetchall()

    return [dict(row) for row in rows]

def update_report_feature_path(
    report_id: int,
    feature_path: str,
) -> None:
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE reports
            SET feature_path = ?
            WHERE report_id = ?
            """,
            (
                feature_path,
                report_id,
            ),
        )

        connection.commit()
        
def get_existing_match(
    lost_report_id: int,
    found_report_id: int,
) -> dict[str, Any] | None:
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM matches
            WHERE lost_report_id = ?
            AND found_report_id = ?
            ORDER BY created_at DESC
            LIMIT 1
            """,
            (
                lost_report_id,
                found_report_id,
            ),
        )

        row = cursor.fetchone()

    return dict(row) if row else None

def get_match_by_id(
    match_id: int,
) -> dict[str, Any] | None:
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM matches
            WHERE match_id = ?
            """,
            (match_id,),
        )

        row = cursor.fetchone()

    return dict(row) if row else None

def get_match_history() -> list[dict[str, Any]]:
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                m.match_id,
                m.lost_report_id,
                m.found_report_id,
                m.image_similarity,
                m.text_similarity,
                m.category_similarity,
                m.colour_similarity,
                m.brand_similarity,
                m.location_similarity,
                m.date_similarity,
                m.final_probability,
                m.match_status,
                m.created_at,

                lost.item_name AS lost_item_name,
                lost.image_path AS lost_image_path,
                lost.description AS lost_description,
                lost.location AS lost_location,
                lost.report_date AS lost_date,

                found.item_name AS found_item_name,
                found.image_path AS found_image_path,
                found.description AS found_description,
                found.location AS found_location,
                found.report_date AS found_date

            FROM matches AS m

            JOIN reports AS lost
                ON m.lost_report_id = lost.report_id

            JOIN reports AS found
                ON m.found_report_id = found.report_id

            ORDER BY m.created_at DESC
            """
        )

        rows = cursor.fetchall()

    return [dict(row) for row in rows]

def get_feedback_history() -> list[dict[str, Any]]:
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                feedback_id,
                match_id,
                actual_match,
                notes,
                created_at
            FROM feedback
            ORDER BY created_at DESC
            """
        )

        rows = cursor.fetchall()

    return [dict(row) for row in rows]

def process_match_decision(
    match_id: int,
    decision: str,
    notes: str = "",
) -> None:
    if decision not in {
        "confirmed",
        "rejected",
    }:
        raise ValueError(
            "Decision must be confirmed or rejected."
        )

    match_record = get_match_by_id(
        match_id
    )

    if match_record is None:
        raise ValueError(
            f"Match ID {match_id} was not found."
        )

    update_match_status(
        match_id=match_id,
        match_status=decision,
    )

    actual_match = (
        decision == "confirmed"
    )

    add_feedback(
        match_id=match_id,
        actual_match=actual_match,
        notes=notes,
    )

    if decision == "confirmed":
        update_report_status(
            report_id=match_record[
                "lost_report_id"
            ],
            status="matched",
        )

        update_report_status(
            report_id=match_record[
                "found_report_id"
            ],
            status="matched",
        )
def get_dashboard_statistics() -> dict[str, int | float]:
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM reports
            """
        )
        total_reports = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM reports
            WHERE report_type = 'lost'
            """
        )
        total_lost = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM reports
            WHERE report_type = 'found'
            """
        )
        total_found = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM reports
            WHERE status = 'active'
            """
        )
        active_reports = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM reports
            WHERE status = 'matched'
            """
        )
        matched_reports = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM matches
            """
        )
        total_matches = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM matches
            WHERE match_status = 'confirmed'
            """
        )
        confirmed_matches = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM matches
            WHERE match_status = 'rejected'
            """
        )
        rejected_matches = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM matches
            WHERE match_status = 'pending'
            """
        )
        pending_matches = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT AVG(final_probability)
            FROM matches
            """
        )
        average_probability = cursor.fetchone()[0]

    decided_matches = (
        confirmed_matches + rejected_matches
    )

    confirmation_rate = (
        confirmed_matches / decided_matches
        if decided_matches > 0
        else 0.0
    )

    return {
        "total_reports": int(total_reports),
        "total_lost": int(total_lost),
        "total_found": int(total_found),
        "active_reports": int(active_reports),
        "matched_reports": int(matched_reports),
        "total_matches": int(total_matches),
        "confirmed_matches": int(confirmed_matches),
        "rejected_matches": int(rejected_matches),
        "pending_matches": int(pending_matches),
        "average_probability": float(
            average_probability or 0.0
        ),
        "confirmation_rate": float(
            confirmation_rate
        ),
    }
def get_category_statistics() -> list[dict[str, Any]]:
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                category,
                COUNT(*) AS report_count
            FROM reports
            GROUP BY category
            ORDER BY report_count DESC
            """
        )

        rows = cursor.fetchall()

    return [dict(row) for row in rows]
def get_report_status_statistics() -> list[dict[str, Any]]:
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                status,
                COUNT(*) AS report_count
            FROM reports
            GROUP BY status
            ORDER BY report_count DESC
            """
        )

        rows = cursor.fetchall()

    return [dict(row) for row in rows]
def get_report_type_statistics() -> list[dict[str, Any]]:
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                report_type,
                COUNT(*) AS report_count
            FROM reports
            GROUP BY report_type
            ORDER BY report_count DESC
            """
        )

        rows = cursor.fetchall()

    return [dict(row) for row in rows]
def get_match_score_statistics() -> list[dict[str, Any]]:
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                match_id,
                lost_report_id,
                found_report_id,
                final_probability,
                match_status,
                created_at
            FROM matches
            ORDER BY created_at DESC
            """
        )

        rows = cursor.fetchall()

    return [dict(row) for row in rows]
