#!/usr/bin/python3

"""Script that reads stdin line by line and computes metrics"""

import sys
import signal

def print_stats(status_counts, total_size):
    """Prints accumulated statistics"""
    print("File size: {:d}".format(total_size))
    for code in sorted(status_counts.keys()):
        if status_counts[code] != 0:
            print("{}: {:d}".format(code, status_counts[code]))

def signal_handler(sig, frame):
    """Handles keyboard interruption signal"""
    print_stats(status_counts, total_file_size)
    sys.exit(0)

# Initialize counters and storage for statistics
status_counts = {
    "200": 0, "301": 0, "400": 0, "401": 0,
    "403": 0, "404": 0, "405": 0, "500": 0
}
total_file_size = 0
line_count = 0

# Set up signal handler for CTRL+C
signal.signal(signal.SIGINT, signal_handler)

try:
    for line in sys.stdin:
        line = line.strip()
        parts = line.split()
        
        # Check if line has the expected number of parts
        if len(parts) != 9:
            continue
        
        ip, dash1, dash2, date, request, quote, status_code, file_size = parts[0], parts[1], parts[2], parts[3], parts[4], parts[5], parts[7], parts[8]
        
        # Verify the request format
        if not request.startswith('"GET /projects/260 HTTP/1.1"'):
            continue

        # Update total file size
        try:
            total_file_size += int(file_size)
        except ValueError:
            continue

        # Update status code count
        if status_code in status_counts:
            status_counts[status_code] += 1

        line_count += 1

        # Print stats every 10 lines
        if line_count % 10 == 0:
            print_stats(status_counts, total_file_size)

    # Print final stats if input ends without interruption
    print_stats(status_counts, total_file_size)

except KeyboardInterrupt:
    print_stats(status_counts, total_file_size)
    raise
