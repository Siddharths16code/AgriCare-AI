
from agricare.database.db import get_connection


def add_activity(user_id, farm_id, activity_name, description, scheduled_date):

    try:
        with get_connection() as conn:

            if farm_id is not None:
                farm = conn.execute(
                    "SELECT id FROM farms WHERE id = ? AND user_id = ?",
                    (farm_id, user_id)
                ).fetchone()

                if farm is None:
                    return False, "Invalid farm selected."

            conn.execute(
                """
                INSERT INTO activities (
                    user_id, farm_id, activity_name,
                    description, scheduled_date
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    farm_id,
                    activity_name,
                    description,
                    scheduled_date
                )
            )

        return True, "Activity added successfully!"

    except Exception as error:
        return False, f"Could not add activity: {error}"


def get_user_activities(user_id):

    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT a.id, a.farm_id, a.activity_name,
                   a.description, a.scheduled_date,
                   a.status, a.created_at, f.farm_name
            FROM activities a
            LEFT JOIN farms f ON a.farm_id = f.id
            WHERE a.user_id = ?
            ORDER BY a.scheduled_date ASC, a.id DESC
            """,
            (user_id,)
        ).fetchall()

    return [dict(row) for row in rows]


def update_activity_status(user_id, activity_id, status):

    if status not in ["Pending", "Completed"]:
        return False, "Invalid activity status."

    with get_connection() as conn:
        cursor = conn.execute(
            """
            UPDATE activities
            SET status = ?
            WHERE id = ? AND user_id = ?
            """,
            (status, activity_id, user_id)
        )

        if cursor.rowcount == 0:
            return False, "Activity not found."

    return True, "Activity status updated successfully!"


def delete_activity(user_id, activity_id):

    with get_connection() as conn:
        cursor = conn.execute(
            """
            DELETE FROM activities
            WHERE id = ? AND user_id = ?
            """,
            (activity_id, user_id)
        )

        if cursor.rowcount == 0:
            return False, "Activity not found."

    return True, "Activity deleted successfully!"
