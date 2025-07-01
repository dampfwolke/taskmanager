from datetime import datetime

def timestamp(time_type: int) -> str:
    """
    Gibt die aktuelle Zeit und/oder Datum aus.
    Je nach integer wird dann folgendes ausgegeben.
    1 = nur Zeit hh:mm:ss
    2 = nur Datum YYYY-MM-DD
    3 = Datum und Uhrzeit YYYY-MM-DD hh:mm:ss"""
    if time_type == 1:
        current_time = datetime.now()
        current_timestamp = current_time.strftime("%H:%M:%S")
        return current_timestamp

    if time_type == 2:
        current_time = datetime.now()
        current_timestamp = current_time.date()
        return str(current_timestamp)

    if time_type == 3:
        current_time = datetime.now()
        current_timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
        return str(current_timestamp)
    return "Keine passender 'time_type(1,2 oder 3)' ausgewählt"

if __name__ == "__main__":
    print(timestamp(5))