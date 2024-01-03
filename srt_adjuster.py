import argparse
import re
import sys


def parse_args():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Adjust the timing of subtitles in an SRT file.")
    parser.add_argument('file', type=str, help="Path to the SRT file.")
    parser.add_argument('-t', '--time', type=str, required=True,
                        help="Time adjustment in format [A/D]HH:MM:SS,MS or [A/D]SS,MS. A is for advance, D is for delay.")
    parser.add_argument('-o', '--output', type=str,
                        help="Output file name. If not specified, overwrite the original file.")

    return parser.parse_args()


def read_srt_file(file_path):
    """
    Read an SRT file and return its contents.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.readlines()
    except FileNotFoundError:
        sys.exit(f"Error: The file {file_path} was not found.")
    except IOError:
        sys.exit(f"Error: Could not read file {file_path}.")


def write_srt_file(file_path, content):
    """
    Write content to an SRT file.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(content)


def adjust_time_code(time_code, adjustment):
    """
    Adjust a time code by a specified time adjustment.
    """
    match = re.match(r'(\d+):(\d+):(\d+),(\d+)', time_code)
    if match:
        hours, minutes, seconds, milliseconds =  list(map(int, match.groups()))
    else:
        sys.exit(f"Error: Invalid time format '{time_code}'.")

    # Convert everything to milliseconds for easier calculation
    total_ms = (hours * 3600000) + (minutes * 60000) + (seconds * 1000) + milliseconds
    total_ms += adjustment

    if total_ms < 0:
        sys.exit("Error: Adjusted time results in negative time.")

    # Convert back to hours, minutes, seconds, and milliseconds
    hours, remainder = divmod(total_ms, 3600000)
    minutes, remainder = divmod(remainder, 60000)
    seconds, milliseconds = divmod(remainder, 1000)

    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"


def calculate_adjustment_milliseconds(adjustment_str):
    """
    Convert the adjustment string to milliseconds.
    """
    sign = 1
    if adjustment_str.startswith(('A', 'D')):
        sign = 1 if adjustment_str[0] == 'A' else -1
        adjustment_str = adjustment_str[1:]

    hours, minutes, seconds, milliseconds = 0, 0, 0, 0

    parts = adjustment_str.split(':')
    if len(parts) == 3:
        hours, minutes, seconds_with_ms = parts
        hours, minutes = int(hours), int(minutes)
        if ',' in seconds_with_ms:
            seconds, milliseconds = map(int, seconds_with_ms.split(','))
        else:
            seconds = int(seconds_with_ms)
    elif len(parts) == 2:
        minutes, seconds_with_ms = parts
        minutes = int(minutes)
        if ',' in seconds_with_ms:
            seconds, milliseconds = map(int, seconds_with_ms.split(','))
        else:
            seconds = int(seconds_with_ms)
    elif ',' in adjustment_str:
        seconds, milliseconds = map(int, adjustment_str.split(','))
    else:
        seconds = int(adjustment_str)

    total_ms = (hours * 3600000 + minutes * 60000 + seconds * 1000 + milliseconds) * sign
    return total_ms


def process_srt_file(lines, adjustment):
    """
    Process the lines of an SRT file, applying the time adjustment.
    """
    time_code_pattern = re.compile(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})')
    adjusted_lines = []

    for line in lines:
        match = time_code_pattern.match(line)
        if match:
            start_time, end_time = match.groups()
            adjusted_start = adjust_time_code(start_time, adjustment)
            adjusted_end = adjust_time_code(end_time, adjustment)
            adjusted_line = f"{adjusted_start} --> {adjusted_end}\n"
            adjusted_lines.append(adjusted_line)
        else:
            adjusted_lines.append(line)

    return adjusted_lines


def main():
    args = parse_args()
    adjustment_ms = calculate_adjustment_milliseconds(args.time)
    srt_content = read_srt_file(args.file)
    adjusted_srt_content = process_srt_file(srt_content, adjustment_ms)
    output_file = args.output if args.output else args.file
    write_srt_file(output_file, adjusted_srt_content)
    print(f"Subtitle timings adjusted and saved to '{output_file}'.")


if __name__ == "__main__":
    main()
