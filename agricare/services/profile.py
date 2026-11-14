
import sqlite3

from agricare.database.db import get_connection


def get_user_profile(user_id):

    with get_connection() as conn:

        user = conn.execute(
            """
            SELECT
                id,
                full_name,
                email,
                phone,
                village,
                district,
                state,
                preferred_language,
                created_at
            FROM users
            WHERE id = ?
            """,
            (user_id,)
        ).fetchone()

    return dict(user) if user else None


def update_user_profile(
    user_id,
    full_name,
    phone,
    village,
    district,
    state,
    preferred_language
):

    full_name = full_name.strip()
    phone = phone.strip()

    if not full_name or not phone:
        return False, "Name and phone number are required."

    try:

        with get_connection() as conn:

            cursor = conn.execute(
                """
                UPDATE users
                SET
                    full_name = ?,
                    phone = ?,
                    village = ?,
                    district = ?,
                    state = ?,
                    preferred_language = ?
                WHERE id = ?
                """,
                (
                    full_name,
                    phone,
                    village.strip(),
                    district.strip(),
                    state.strip(),
                    preferred_language,
                    user_id
                )
            )

            if cursor.rowcount == 0:
                return False, "Farmer account not found."

        return True, "Profile updated successfully!"

    except sqlite3.IntegrityError:

        return False, "This phone number is already registered."
