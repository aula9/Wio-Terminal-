import serial
import os
import glob
import time

SERIAL_PORT = "COM5"
BAUDRATE = 9600

def main():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
        print(f"[OK] Connected to {SERIAL_PORT} at {BAUDRATE} baud")
        print("[WAIT] Ready to receive data...")
        print("[INFO] Press B3 to change class, then B1 to start recording")
        print("-" * 50)
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")
        print("Check:")
        print("1. Port is correct (check Device Manager)")
        print("2. No other program (like Serial Monitor) is using the port")
        return

    current_file = None
    current_class = "UNKNOWN"
    file_counter = 0
    sample_counter = 0
    start_time = None

    while True:
        try:
            raw_line = ser.readline()
            if not raw_line:
                continue

            line = raw_line.decode('utf-8', errors='ignore').strip()
            if not line:
                continue

            print(f"[RECV] {line}")

            if line.startswith("START,"):
                current_class = line[6:]  
                if not current_class:
                    current_class = "UNKNOWN"

                folder_path = f"dataset/{current_class}"
                os.makedirs(folder_path, exist_ok=True)

                existing_files = glob.glob(f"{folder_path}/{current_class}_*.csv")
                file_counter = len(existing_files) + 1

                filename = f"{folder_path}/{current_class}_{file_counter:02d}.csv"
                current_file = open(filename, 'w')
                current_file.write("timestamp,value\n")
                
                sample_counter = 0
                start_time = time.time()
                
                print(f"[FILE] Recording started: {filename}")
                continue

            if line == "END":
                if current_file:
                    current_file.close()
                    
                    duration = time.time() - start_time if start_time else 0
                    
                    print(f"[SAVE] Saved successfully: {current_file.name}")
                    print(f"[DATA] Total samples: {sample_counter}")
                    print(f"[TIME] Duration: {duration:.1f} seconds")
                    print("-" * 50)
                    
                    current_file = None
                continue

            if current_file is not None and "," in line:
                current_file.write(line + "\n")
                sample_counter += 1

        except KeyboardInterrupt:
            print("\n[STOP] Program stopped by user.")
            if current_file:
                current_file.close()
                print("[SAVE] Last file saved before closing.")
            break
        except Exception as e:
            print(f"[WARN] Error: {e}")
            continue

if __name__ == "__main__":
    main()
