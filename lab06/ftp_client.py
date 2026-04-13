import os
from ftplib import FTP, error_perm
import sys


class FTPClient:
    def __init__(self):
        self.ftp = FTP()
        self.connected = False

    def connect(self, host, port=21, username="anonymous", password=""):
        try:
            print(f"Connecting to {host}:{port}...")
            self.ftp.connect(host, port)
            self.ftp.login(username, password)
            self.connected = True
            print(f"Successfully connected to {host}")
            print(f"Welcome message: {self.ftp.getwelcome()}")
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def disconnect(self):
        if self.connected:
            try:
                self.ftp.quit()
            except:
                self.ftp.close()
            self.connected = False
            print("Disconnected from server")

    def list_directory(self, path=""):
        if not self.connected:
            print("Not connected to server")
            return []

        try:
            print(f"\n--- Directory contents: {path or '/'} ---")
            print(f"{'Type':<6} {'Size':<12} {'Name':<30} {'Modified'}")
            print("-" * 70)

            files = []
            dirs = []

            def parse_line(line):
                parts = line.split()
                if len(parts) < 9:
                    return

                item_type = "DIR" if line.startswith('d') else "FILE"
                size = parts[4] if item_type == "FILE" else "-"
                name = " ".join(parts[8:])
                date = f"{parts[5]} {parts[6]} {parts[7]}"

                if item_type == "DIR":
                    dirs.append(name)
                    print(f"{'[DIR]':<6} {'-':<12} {name:<30} {date}")
                else:
                    files.append(name)
                    print(f"{'[FILE]':<6} {size:<12} {name:<30} {date}")

            self.ftp.retrlines(f"LIST {path}", parse_line)

            print(f"\nTotal: {len(dirs)} folders, {len(files)} files")

            return dirs + files

        except error_perm as e:
            print(f"Access error: {e}")
        except Exception as e:
            print(f"Error getting listing: {e}")
        return []

    def upload_file(self, local_path, remote_name=None):
        if not self.connected:
            print("Not connected to server")
            return False

        if not os.path.exists(local_path):
            print(f"File not found: {local_path}")
            return False

        if remote_name is None:
            remote_name = os.path.basename(local_path)

        try:
            file_size = os.path.getsize(local_path)
            print(f"Uploading: {local_path} -> {remote_name}")
            print(f"Size: {file_size} bytes")

            with open(local_path, 'rb') as f:
                self.ftp.storbinary(f"STOR {remote_name}", f, callback=self._progress_callback)

            print(f"\nFile successfully uploaded to server")
            return True

        except Exception as e:
            print(f"\nUpload error: {e}")
            return False

    def download_file(self, remote_name, local_path=None):
        if not self.connected:
            print("Not connected to server")
            return False

        if local_path is None:
            local_path = remote_name

        try:
            size = self.ftp.size(remote_name)
            print(f"Downloading: {remote_name} -> {local_path}")
            print(f"Size: {size} bytes")

            with open(local_path, 'wb') as f:
                self.ftp.retrbinary(f"RETR {remote_name}", f.write)

            print(f"\nFile successfully saved as: {local_path}")
            return True

        except Exception as e:
            print(f"\nDownload error: {e}")
            return False

    def _progress_callback(self, block):
        print(".", end="", flush=True)

    def change_directory(self, path):
        try:
            self.ftp.cwd(path)
            print(f"Current directory: {self.ftp.pwd()}")
            return True
        except Exception as e:
            print(f"Error changing directory: {e}")
            return False

    def current_directory(self):
        try:
            print(f"Current directory: {self.ftp.pwd()}")
        except Exception as e:
            print(f"Error: {e}")


def print_menu():
    print("FTP CLIENT MENU")
    print("=" * 50)
    print("1. Connect to server")
    print("2. Disconnect from server")
    print("3. Show file list")
    print("4. Change directory")
    print("5. Upload file to server")
    print("6. Download file from server")
    print("7. Show current directory")
    print("0. Exit")
    print("=" * 50)


if __name__ == "__main__":
    try:
        client = FTPClient()

        test_servers = {
            "1": {"name": "Local server", "host": "127.0.0.1", "port": 21,
                  "user": "TestUser", "pass": "12345"},
            "2": {"name": "DLP Test FTP", "host": "ftp.dlptest.com", "port": 21,
                  "user": "dlpuser", "pass": "rNrKYTX9g7z3RgJRmxWuGHbeu"}
        }

        while True:
            print_menu()

            if client.connected:
                print("\nStatus: connected")
            else:
                print("\nStatus: not connected")

            choice = input("\nChoose action: ").strip()

            if choice == "0":
                if client.connected:
                    client.disconnect()
                    print("Goodbye!")
                else:
                    print("Already disconnected")
                continue

            elif choice == "1":
                if client.connected:
                    print("Already connected")
                    continue

                print("\nChoose server")
                print("1. Local FileZilla Server (127.0.0.1)")
                print("2. Public test FTP (ftp.dlptest.com)")

                server_choice = input("Choice: ").strip()

                if server_choice in test_servers:
                    server = test_servers[server_choice]
                    host = server["host"]
                    port = server["port"]
                    user = server["user"]
                    pwd = server["pass"]
                    print(f"Selected: {server['name']}")

                    client.connect(host, port, user, pwd)
                else:
                    print("Invalid choice")

            elif choice == "2":
                client.disconnect()

            elif choice == "3":
                if client.connected:
                    client.list_directory()
                else:
                    print("You are not connected!")

            elif choice == "4":
                if client.connected:
                    path = input("Enter directory path: ").strip()
                    if path:
                        client.change_directory(path)
                    else:
                        print("Path can't be empty")
                else:
                    print("You are not connected!")

            elif choice == "5":
                if client.connected:
                    local_path = input("Local file path: ").strip()
                    remote_name = input("Remote file name: ").strip()
                    if remote_name == "":
                        remote_name = None
                    client.upload_file(local_path, remote_name)
                else:
                    print("You are not connected!")

            elif choice == "6":
                if client.connected:
                    remote_name = input("Remote file name: ").strip()
                    local_path = input("Save as: ").strip()
                    if local_path == "":
                        local_path = None
                    client.download_file(remote_name, local_path)
                else:
                    print("You are not connected!")

            elif choice == "7":
                if client.connected:
                    client.current_directory()
                else:
                    print("You are not connected!")

            else:
                print("Invalid choice!")

    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nCritical error: {e}")
        sys.exit(1)