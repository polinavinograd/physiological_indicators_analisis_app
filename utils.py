from datetime import datetime, timedelta
import os


def date_range(start_date, end_date):
    if isinstance(start_date, str) and isinstance(end_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

    current_date = start_date
    while current_date <= end_date:
        yield current_date.strftime("%Y-%m-%d")
        current_date += timedelta(days=1)


def get_all_files_from_directory(directory: str) -> list[str]:
    files = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            files.append(filename)
    return files
