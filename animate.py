import time
import sys

def spinner(duration):
    spin_chars = ['-', '\\', '|', '/']
    start_time = time.time()
    
    while time.time() - start_time < duration:
        for char in spin_chars:
            sys.stdout.write('\r' + char)
            sys.stdout.flush()
            time.sleep(0.1)

if __name__ == "__main__":
    spinner(5)  # Replace 5 with the desired duration in seconds
