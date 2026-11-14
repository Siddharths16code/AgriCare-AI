
import sqlite3
from agricare.database.db import get_connection


def add_farm(user_id, farm_name, area_acres, soil_type,
             irrigation_method, potato_variety, sowing_date, crop_stage):

    farm_name = farm_name.strip()

    if not farm_name:
        return False, "Please enter a farm name."

    if area_acres <= 0:
        return False, "Farm area must be greater than zero."

    try:
        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO farms (
                    user_id, farm_name, area_acres, soil_type,
                    irrigation_method, potato_variety, sowing_date,
                    crop_stage
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id, farm_name, area_acres, soil_type,
                    irrigation_method, potato_variety, sowing_date,
                    crop_stage
                )
            )

        return True, "Farm added successfully!"

    except sqlite3.Error as error:
        return False, f"Could not add farm: {error}"


def get_user_farms(user_id):

    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM farms
            WHERE user_id = ?
            ORDER BY rowid DESC
            """,
            (user_id,)
        ).fetchall()

    return [dict(row) for row in rows]


def delete_farm(user_id, farm_id):

    with get_connection() as conn:
        cursor = conn.execute(
            """
            DELETE FROM farms
            WHERE id = ? AND user_id = ?
            """,
            (farm_id, user_id)
        )

        if cursor.rowcount == 0:
            return False, "Farm not found."

    return True, "Farm deleted successfully!"
