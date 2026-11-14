
from agricare.database.db import get_connection


def add_harvest(user_id, farm_id, harvest_date, quantity_kg, selling_price, notes):

    try:
        with get_connection() as conn:

            if farm_id is not None:
                farm = conn.execute(
                    "SELECT id, area_acres FROM farms WHERE id = ? AND user_id = ?",
                    (farm_id, user_id)
                ).fetchone()

                if farm is None:
                    return False, "Invalid farm selected."

            conn.execute(
                """
                INSERT INTO harvest_records (
                    user_id, farm_id, harvest_date,
                    quantity_kg, selling_price, notes
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    farm_id,
                    harvest_date,
                    quantity_kg,
                    selling_price,
                    notes
                )
            )

        return True, "Harvest record added successfully!"

    except Exception as error:
        return False, f"Could not add harvest record: {error}"


def get_harvest_records(user_id):

    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT h.id, h.farm_id, h.harvest_date,
                   h.quantity_kg, h.selling_price,
                   h.notes, h.created_at,
                   f.farm_name, f.area_acres
            FROM harvest_records h
            LEFT JOIN farms f ON h.farm_id = f.id
            WHERE h.user_id = ?
            ORDER BY h.harvest_date DESC, h.id DESC
            """,
            (user_id,)
        ).fetchall()

    return [dict(row) for row in rows]


def get_harvest_summary(user_id):

    with get_connection() as conn:
        result = conn.execute(
            """
            SELECT
                COALESCE(SUM(quantity_kg), 0) AS total_quantity,
                COALESCE(SUM(quantity_kg * selling_price), 0) AS total_revenue,
                COUNT(*) AS total_records
            FROM harvest_records
            WHERE user_id = ?
            """,
            (user_id,)
        ).fetchone()

    return {
        "total_quantity": float(result["total_quantity"]),
        "total_revenue": float(result["total_revenue"]),
        "total_records": result["total_records"]
    }


def delete_harvest_record(user_id, harvest_id):

    with get_connection() as conn:
        cursor = conn.execute(
            """
            DELETE FROM harvest_records
            WHERE id = ? AND user_id = ?
            """,
            (harvest_id, user_id)
        )

        if cursor.rowcount == 0:
            return False, "Harvest record not found."

    return True, "Harvest record deleted successfully!"
