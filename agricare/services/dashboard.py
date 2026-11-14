from agricare.database.db import get_connection


def get_dashboard_data(user_id):

    with get_connection() as conn:

        farm_data = conn.execute("""
            SELECT
                COUNT(*) AS total_farms,
                COALESCE(SUM(area_acres), 0) AS total_area
            FROM farms
            WHERE user_id = ?
        """, (user_id,)).fetchone()

        scan_data = conn.execute("""
            SELECT
                COUNT(*) AS total_scans,
                SUM(
                    CASE
                        WHEN predicted_class = 'Potato___healthy'
                        THEN 1 ELSE 0
                    END
                ) AS healthy_scans,
                SUM(
                    CASE
                        WHEN predicted_class != 'Potato___healthy'
                        THEN 1 ELSE 0
                    END
                ) AS disease_scans
            FROM scans
            WHERE user_id = ?
        """, (user_id,)).fetchone()

        recent_scans = conn.execute("""
            SELECT
                predicted_class,
                confidence,
                created_at
            FROM scans
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT 5
        """, (user_id,)).fetchall()

    return {
        "total_farms": farm_data["total_farms"],
        "total_area": float(farm_data["total_area"]),
        "total_scans": scan_data["total_scans"] or 0,
        "healthy_scans": scan_data["healthy_scans"] or 0,
        "disease_scans": scan_data["disease_scans"] or 0,
        "recent_scans": [dict(row) for row in recent_scans]
    }