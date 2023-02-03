from datetime import datetime
from typing import Optional, Tuple

import pandas as pd
import tabula


class Colors():
    OKCYAN  = "\033[96m"
    OKGREEN = "\033[92m"
    BOLD    = "\033[1m"
    WARNING = "\033[93m"
    FAIL    = "\033[91m"
    ENDC    = "\033[0m"

def get_weekday_and_time() -> Tuple[str, datetime.time]:
    current_datetime = datetime.now()
    weekday = get_weekday(current_datetime)
    current_time = current_datetime.time()
    return weekday, current_time

def get_weekday(current_datetime: datetime) -> str:
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    number_to_weekday = {index: day for index, day in zip(range(7), days)}

    weekday_number = current_datetime.weekday()
    weekday = number_to_weekday[weekday_number]
    return weekday

def get_table_from_pdf(file_name: str) -> pd.DataFrame:
    pdf_dataframes = tabula.read_pdf(file_name, pages="all")
    schedule_df = list(pdf_dataframes)[0]
    return pd.DataFrame(schedule_df)

def display_time_message(weekday: str, time: datetime.time):
    time = str(time)[0:5]
    message = "\n\tDay of the week is "
    message += highlight(weekday, Colors.OKGREEN)
    message += ". Current time is "
    message += highlight(time, Colors.OKCYAN)
    print(f"{message}.")

def load_and_process_dataframe(pdf_name: str) -> pd.DataFrame:
    df = get_table_from_pdf(pdf_name)
    split_time_windows(df)
    df["start_time"] = convert_to_datetime(df, "start_time")
    df["end_time"] = convert_to_datetime(df, "end_time")
    return df

def split_time_windows(df: pd.DataFrame):
    time_column = df.columns[0]
    df[["start_time", "end_time"]] = df[time_column].str.split(" - ", expand=True)

def convert_to_datetime(df: pd.DataFrame, column: str) -> pd.Series:
    return pd.to_datetime(df[column], format="%H:%M").dt.time

def find_time_row(df: pd.DataFrame, time: datetime.time) -> Optional[pd.Series]:
    selected_rows = df.loc[(df["start_time"] <= time) & (df["end_time"] >= time)]
    if selected_rows.empty:
        return None
    return selected_rows

def query_dataframe(df: pd.DataFrame, time: datetime.time, weekday: str) -> Optional[str]:
    selected_rows = find_time_row(df, time)
    if selected_rows is None:
        return selected_rows
    query_result = selected_rows[weekday]
    processed_output = str(query_result.values[0])
    processed_output = processed_output.replace("\r", " ")
    if processed_output:
        return None
    return processed_output

def display_location_message(processed_output: Optional[str], object_of_limerence: str):
    if processed_output is None:
        message = highlight(object_of_limerence, Colors.FAIL)
        message += highlight(" not found.", Colors.WARNING)
        print(f"\t{message}\n")
        exit()
    message = highlight(object_of_limerence, Colors.OKGREEN)
    message += " is currently in: "
    message += highlight(processed_output, Colors.OKCYAN)
    print(f"\t{message}.\n")

def highlight(text: str, color: str) -> str:
    return f"{color}{Colors.BOLD}{text}{Colors.ENDC}"

def main():
    object_of_limerence = "Mari"

    weekday, current_time = get_weekday_and_time()
    schedule_df = load_and_process_dataframe("schedule.pdf")
    location = query_dataframe(schedule_df, current_time, weekday)
    
    display_time_message(weekday, current_time)
    display_location_message(location, object_of_limerence)

if __name__ == "__main__":
    main()
