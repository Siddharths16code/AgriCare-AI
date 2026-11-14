import json
from agricare.database.db import get_connection


def get_scan_history(user_id):
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT
                s.id,
                s.farm_id,
                s.image_path,
                s.predicted_class,
                s.confidence,
                s.probabilities_json,
                s.created_at,
                f.farm_name
            FROM scans s
            LEFT JOIN farms f ON s.farm_id = f.id
            WHERE s.user_id = ?
            ORDER BY s.created_at DESC
        """, (user_id,)).fetchall()

    return [dict(row) for row in rows]


def get_scan_analytics(user_id):
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT predicted_class, COUNT(*) AS total
            FROM scans
            WHERE user_id = ?
            GROUP BY predicted_class
        """, (user_id,)).fetchall()

    return [dict(row) for row in rows]