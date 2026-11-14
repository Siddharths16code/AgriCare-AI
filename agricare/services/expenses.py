
from agricare.database.db import get_connection


def add_expense(user_id, farm_id, category, amount, description, expense_date):
    try:
        with get_connection() as conn:

            # Verify that the selected farm belongs to this user
            if farm_id is not None:
                farm = conn.execute(
                    "SELECT id FROM farms WHERE id = ? AND user_id = ?",
                    (farm_id, user_id)
                ).fetchone()

                if farm is None:
                    return False, "Invalid farm selected."

            conn.execute(
                """
                INSERT INTO expenses (
                    user_id, farm_id, category,
                    amount, description, expense_date
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id, farm_id, category,
                    amount, description, expense_date
                )
            )

        return True, "Expense added successfully!"

    except Exception as error:
        return False, f"Could not add expense: {error}"


def get_user_expenses(user_id):
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT e.id, e.farm_id, e.category, e.amount,
                   e.description, e.expense_date, e.created_at,
                   f.farm_name
            FROM expenses e
            LEFT JOIN farms f ON e.farm_id = f.id
            WHERE e.user_id = ?
            ORDER BY e.expense_date DESC, e.id DESC
            """,
            (user_id,)
        ).fetchall()

    return [dict(row) for row in rows]


def get_expense_summary(user_id):
    with get_connection() as conn:
        total = conn.execute(
            """
            SELECT COALESCE(SUM(amount), 0)
            FROM expenses
            WHERE user_id = ?
            """,
            (user_id,)
        ).fetchone()[0]

        categories = conn.execute(
            """
            SELECT category, SUM(amount) AS total_amount
            FROM expenses
            WHERE user_id = ?
            GROUP BY category
            ORDER BY total_amount DESC
            """,
            (user_id,)
        ).fetchall()

    return {
        "total_expenses": float(total),
        "category_breakdown": [dict(row) for row in categories]
    }


def delete_expense(user_id, expense_id):
    with get_connection() as conn:
        cursor = conn.execute(
            """
            DELETE FROM expenses
            WHERE id = ? AND user_id = ?
            """,
            (expense_id, user_id)
        )

        if cursor.rowcount == 0:
            return False, "Expense not found."

    return True, "Expense deleted successfully!"
