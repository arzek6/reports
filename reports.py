from statistics import median


def median_coffee(rows):
    spending = {}
    for row in rows:
        student = row["student"]
        spending.setdefault(student, []).append(float(row["coffee_spent"]))

    result = [
        {"student": student, "median_coffee": median(values)}
        for student, values in spending.items()
    ]
    result.sort(key=lambda r: r["median_coffee"], reverse=True)
    return result


REPORTS = {
    "median-coffee": median_coffee,
}
