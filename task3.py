import sys


LOG_LEVELS = ("INFO", "DEBUG", "ERROR", "WARNING")


def parse_log_line(line: str) -> dict:
    parts = line.strip().split(maxsplit=3)
    if len(parts) != 4:
        raise ValueError(f"Invalid log line format: {line.strip()}")

    date, time, level, message = parts
    level = level.upper()
    if level not in LOG_LEVELS:
        raise ValueError(f"Unknown log level: {level}")

    return {
        "date": date,
        "time": time,
        "level": level,
        "message": message,
    }


def load_logs(file_path: str) -> list:
    logs = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                if not line.strip():
                    continue

                try:
                    logs.append(parse_log_line(line))
                except ValueError as error:
                    print(f"Skipping line {line_number}: {error}", file=sys.stderr)
    except FileNotFoundError as error:
        raise FileNotFoundError(f"Log file not found: {file_path}") from error
    except OSError as error:
        raise OSError(f"Unable to read log file: {file_path}") from error

    return logs


def filter_logs_by_level(logs: list, level: str) -> list:
    normalized_level = level.upper()
    return list(filter(lambda log: log["level"] == normalized_level, logs))


def count_logs_by_level(logs: list) -> dict:
    counts = {level: 0 for level in LOG_LEVELS}

    for log in logs:
        counts[log["level"]] += 1

    return counts


def display_log_counts(counts: dict) -> None:
    print("Рівень логування | Кількість")
    print("-----------------|----------")
    for level in LOG_LEVELS:
        print(f"{level:<16} | {counts.get(level, 0)}")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python task3.py <log_file_path> [log_level]")
        sys.exit(1)

    file_path = sys.argv[1]
    selected_level = sys.argv[2].upper() if len(sys.argv) > 2 else None

    try:
        logs = load_logs(file_path)
    except (FileNotFoundError, OSError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)

    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if selected_level:
        if selected_level not in LOG_LEVELS:
            print(f"Unknown log level: {selected_level}", file=sys.stderr)
            sys.exit(1)

        filtered_logs = filter_logs_by_level(logs, selected_level)
        print(f"\nДеталі логів для рівня '{selected_level}':")
        for log in filtered_logs:
            print(f"{log['date']} {log['time']} - {log['message']}")


if __name__ == "__main__":
    main()