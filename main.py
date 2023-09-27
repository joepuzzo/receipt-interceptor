import serial
import threading
import time

# Define the serial port settings
SERIAL_PORT = '/dev/ttyUSB0'  # Change this to the correct port for your setup
BAUD_RATE = 9600  # Change this to the correct baud rate for your setup


def process_buffer(buffer):
    # Initialize variables
    text_buffer = []
    is_text_mode = True

    # Iterate over the buffer
    i = 0
    while i < len(buffer):
        byte = buffer[i]

        if is_text_mode:
            if byte == 0x1B:  # ESC
                # Switch to command mode
                is_text_mode = False
                # Append the accumulated text to the text buffer
                if text_buffer:
                    print("Text:", ''.join(text_buffer))
                    text_buffer.clear()
            else:
                # Append the byte as a character to the text buffer
                text_buffer.append(chr(byte))
        else:
            # Interpret ESC/POS command
            if byte == 0x45:  # 'E' - Emphasized mode
                print("Command: Emphasized mode")
                i += 1  # Skip the parameter byte
            elif byte == 0x61:  # 'a' - Alignment
                print("Command: Alignment")
                i += 1  # Skip the parameter byte
            elif byte == 0x0A:  # 'LF' - Print and line feed
                print("Command: Print and line feed")
            elif byte == 0x1D:  # 'GS' - Group Separator, used for various commands
                i += 1  # Move to the next byte to interpret the command
                next_byte = buffer[i]
                if next_byte == 0x56:  # 'V' - Full cut or partial cut
                    print("Command: Paper Cut")
                elif next_byte == 0x6B:  # 'k' - Print bar code
                    print("Command: Print Bar Code")
                # Add more GS subcommands as needed
            # Add more command interpretations as needed

            # Switch back to text mode
            is_text_mode = True

        i += 1

    # Print any remaining text in the text buffer
    if text_buffer:
        print("Text:", ''.join(text_buffer))


def read_from_pos(ser):
    buffer = []
    while True:
        byte = ser.read(1)
        if byte:
            buffer.append(byte[0])
            process_buffer(buffer)
            buffer.clear()  # Clear the buffer after processing


def emulate_printer_responses(ser):
    while True:
        command = ser.read(1)
        if command:
            print("Received command from POS:", command)
            if command == b'\x10\x04':  # DLE EOT - Transmit status
                print("Sending printer status")
                # DLE SYN - Printer is online and has no errors
                ser.write(b'\x16')
            elif command == b'\x1D(r':  # GS (r - Transmit parameter settings
                print("Sending parameter settings")
                ser.write(b'\x1D(r\x05\x00\x01\x02\x03\x04')
            # Add more command processing and response logic as needed
        time.sleep(0.01)


def emulate_esc_pos_printer():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    except serial.SerialException as e:
        print(f"Error opening serial port {SERIAL_PORT}: {e}")
        return

    # Start the threads to read from POS and emulate printer responses
    read_thread = threading.Thread(target=read_from_pos, args=(ser,))
    response_thread = threading.Thread(
        target=emulate_printer_responses, args=(ser,))

    read_thread.start()
    response_thread.start()

    try:
        # Wait for the threads to finish (they won't, in this case, since they have infinite loops)
        read_thread.join()
        response_thread.join()
    except KeyboardInterrupt:
        print("Terminating...")
        ser.close()  # Close the serial port when terminating the program


if __name__ == "__main__":
    emulate_esc_pos_printer()
