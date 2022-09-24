import polars as pl


def test_sql_groupby(foods_ipc: str) -> None:
    c = pl.SQLContext()

    lf = pl.scan_ipc(foods_ipc)
    c.register("foods", lf)

    out = c.query(
        """
    SELECT
        category,
        count(category) as count,
        max(calories),
        min(fats_g)
    FROM foods
    GROUP BY category
    ORDER BY count, category DESC
    LIMIT 2
    """
    )

    assert out.to_dict(False) == {
        "category": ["meat", "vegetables"],
        "count": [5, 7],
        "calories": [120, 45],
        "fats_g": [5.0, 0.0],
    }


def test_sql_join(foods_ipc: str) -> None:
    c = pl.SQLContext()

    lf = pl.scan_ipc(foods_ipc)
    c.register("foods1", lf)
    c.register("foods2", lf)

    out = c.query(
        """
    SELECT * FROM
    foods1 INNER JOIN foods2 ON category = category
    LIMIT 2
    """
    )
    assert out.to_dict(False) == {
        "category": ["vegetables", "vegetables"],
        "calories": [45, 20],
        "fats_g": [0.5, 0.0],
        "sugars_g": [2, 2],
        "calories_right": [45, 45],
        "fats_g_right": [0.5, 0.5],
        "sugars_g_right": [2, 2],
    }