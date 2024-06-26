import subprocess
import sqlite3
import os

# Constants
LINES = "-----------------------------------------"
WHITE_SPACE = "     "
CURRENT_USER = os.popen('echo -n "$USER"').read()
BYE_MESSAGE = "\n" + "\033[91m {}\033[00m".format("-------- Good Bye! ---------------------")

def get_db_connection():
    try:
        connection = sqlite3.connect('database_DriverMounter.db')
        return connection
    except sqlite3.Error as error:
        print(f"Error occurred - {error}")
        return None

def fetch_mount_info(cursor):
    cursor.execute("""SELECT * FROM Info""")
    rows = cursor.fetchall()
    if rows:
        return rows[-1][0], rows[-1][1]
    return "", ""

def mount(def_mount_loc, mount_fol, cursor, connection):
    try:
        print("  " + WHITE_SPACE, end='')
        print("\033[94m {}\033[00m".format("Use Ctrl + C to Go back!"))
        print(LINES)
        print("  " + WHITE_SPACE, end='')
        print("\033[91m {}\033[00m".format("Choose a Mount Point"))
        print(LINES)

        subprocess.run("lsblk")

        input1 = input("\n" + "\033[91m {}\033[00m".format("Mount Point (sdb1,sda3 ...) : ")).strip()

        if not mount_fol:
            input4 = input("\033[91m {}\033[00m".format("Name For The Mounted Folder : ")).strip()
            subprocess.run(["sudo", "mkdir", f"{def_mount_loc}/{input4}"])
            cursor.execute('''INSERT INTO Info (DefaultMountLocation, MountFolder) VALUES (?, ?)''', (def_mount_loc, input4))
            connection.commit()
            print_mount_message(input1, def_mount_loc, input4)
        else:
            input3 = input("\033[91m {}\033[00m".format(f"Use the name ***{mount_fol}*** (y/n)? ")).strip().lower()
            if input3 == "y":
                subprocess.run(["sudo", "mkdir", f"{def_mount_loc}/{mount_fol}"])
                print_mount_message(input1, def_mount_loc, mount_fol)
            elif input3 == "n":
                input4 = input("\033[91m {}\033[00m".format("Enter a New Name For The Mounted Folder : ")).strip()
                subprocess.run(["sudo", "mkdir", f"{def_mount_loc}/{input4}"])
                cursor.execute('''INSERT INTO Info (DefaultMountLocation, MountFolder) VALUES (?, ?)''', (def_mount_loc, input4))
                connection.commit()
                print_mount_message(input1, def_mount_loc, input4)

        input("\033[91m {}\033[00m".format("Done! Press Any Key To continue! "))
    except KeyboardInterrupt:
        print(BYE_MESSAGE)

def print_mount_message(mount_point, def_mount_loc, folder):
    print()
    print(LINES)
    print("\n" + "\033[91m {}\033[00m".format(f"Mounting /dev/{mount_point} to --> {def_mount_loc}/{folder}\n"))
    print(LINES)
    subprocess.run(["sudo", "mount", f"/dev/{mount_point}", f"{def_mount_loc}/{folder}"])

def unmount():
    try:
        print("  " + WHITE_SPACE, end='')
        print("\033[94m {}\033[00m".format("Use Ctrl + C to Go back!"))
        print(LINES)
        print("  " + WHITE_SPACE, end='')
        print("\033[91m {}\033[00m".format("Choose a Path to Unmount"))
        print(LINES)

        subprocess.run("lsblk")

        input1 = input("\n" + "\033[91m {}\033[00m".format("Enter The Full Path : ")).strip()

        print()
        print(LINES)
        print("\n" + "\033[91m {}\033[00m".format(f"Unmounting {input1}\n"))
        print(LINES)

        subprocess.run(["sudo", "umount", f"{input1}"])

        input("\033[91m {}\033[00m".format("Done! Press Any Key To continue! "))
    except KeyboardInterrupt:
        print(BYE_MESSAGE)

def disk_poweroff():
    try:
        print("  " + WHITE_SPACE, end='')
        print("\033[94m {}\033[00m".format("Use Ctrl + C to Go back!"))
        print(LINES)
        print("  " + WHITE_SPACE, end='')
        print("\033[91m {}\033[00m".format("Choose a Drive to Poweroff"))
        print(LINES)

        subprocess.run("lsblk")

        input1 = input("\n" + "\033[91m {}\033[00m".format("Enter The drive's name (sdb,sda ...) : ")).strip()

        print()
        print(LINES)
        print("\n" + "\033[91m {}\033[00m".format(f"Turning Off ... {input1}\n"))
        print(LINES)

        subprocess.run(["sudo", "udisksctl", "power-off", "-b", f"/dev/{input1}"])

        input("\033[91m {}\033[00m".format("Done! Press Any Key To continue! "))
    except KeyboardInterrupt:
        print(BYE_MESSAGE)

def change_default_mount_location(mount_location, cursor, connection):
    try:
        print("  " + WHITE_SPACE, end='')
        print("\033[94m {}\033[00m".format("Use Ctrl + C to Go back!"))
        print(LINES)
        if mount_location != "":
            print("\033[91m {}\033[00m".format("The Default Location is : " + mount_location))
            print(LINES)

            input3 = input("\033[94m {}\033[00m".format("Do you want to change it? : (y/n) ")).strip().lower()
            if input3 == "y":
                input4 = input("\033[91m {}\033[00m".format("Enter a new Location (Full Path) : ")).strip()
                cursor.execute('''INSERT INTO Info (DefaultMountLocation) VALUES (?)''', (input4,))
                connection.commit()

        if mount_location == "":
            input4 = input("\033[91m {}\033[00m".format("Enter a new Location (Full Path) : ")).strip()
            cursor.execute('''INSERT INTO Info (DefaultMountLocation) VALUES (?)''', (input4,))
            connection.commit()

        DefaultMountLocation, _ = fetch_mount_info(cursor)

        print()
        print(LINES)
        print("\n" + "\033[91m {}\033[00m".format(f"Current location is {DefaultMountLocation}\n"))
        print(LINES)

        input("\033[91m {}\033[00m".format("Done! Press Any Key To continue! "))
    except KeyboardInterrupt:
        print(BYE_MESSAGE)

def delete_database():
    try:
        print()
        print(LINES)
        print("\n" + "\033[91m {}\033[00m".format("Deleting ... database_DriverMounter.db\n"))
        print(LINES)

        subprocess.run(["rm", "database_DriverMounter.db"])

        input("\033[91m {}\033[00m".format("Done! Press Any Key To continue! "))
    except KeyboardInterrupt:
        print(BYE_MESSAGE)

def main():
    while True:
        try:
            subprocess.run("clear")
            print(LINES)
            print("\033[93m {}\033[00m".format(WHITE_SPACE + f"Welcome {CURRENT_USER} To Drive Mounter!"))
            print("\033[93m {}\033[00m".format(WHITE_SPACE + "By github.com/stking68"))
            print(LINES)

            with get_db_connection() as sqliteConnection:
                cursor = sqliteConnection.cursor()
                cursor.execute('''CREATE TABLE IF NOT EXISTS Info
                    (
                    DefaultMountLocation TEXT,
                    MountFolder TEXT
                    );''')
                DefaultMountLocation, mountFolderName = fetch_mount_info(cursor)

                print("\033[96m {}\033[00m".format(WHITE_SPACE + "Choose an Option"))
                if DefaultMountLocation:
                    print("\033[96m {}\033[00m".format(WHITE_SPACE + f"Default Location is : {DefaultMountLocation}"))
                else:
                    print()
                    print("\033[91m {}\033[00m".format(WHITE_SPACE + "Please Enter a Default \n" + WHITE_SPACE + " Mount Location Using [4] !"))
                print(LINES)

                print()
                print("\033[95m {}\033[00m".format(WHITE_SPACE + "[1] Mount"))
                print("\033[95m {}\033[00m".format(WHITE_SPACE + "[2] Unmount"))
                print("\033[95m {}\033[00m".format(WHITE_SPACE + "[3] Poweroff Disk"))
                print("\033[95m {}\033[00m".format(WHITE_SPACE + "[4] Change Default Mount Location"))
                print("\033[95m {}\033[00m".format(WHITE_SPACE + "[5] Delete Database"))
                print("\033[95m {}\033[00m".format(WHITE_SPACE + "[6] Exit"))
                input_text = "\033[91m {}\033[00m".format("Option : ")

                print()
                print(LINES)

                choice = input(input_text).strip()
                print(LINES)

                if choice == "1" and DefaultMountLocation:
                    mount(DefaultMountLocation, mountFolderName, cursor, sqliteConnection)
                elif choice == "2":
                    unmount()
                elif choice == "3":
                    disk_poweroff()
                elif choice == "4":
                    change_default_mount_location(DefaultMountLocation, cursor, sqliteConnection)
                elif choice == "5":
                    delete_database()
                elif choice == "6":
                    print(BYE_MESSAGE)
                    break
                else:
                    print("\033[91m {}\033[00m".format("Please Enter a Valid Option!"))
                    input("\033[91m {}\033[00m".format("Press Any Key To continue! "))
        except KeyboardInterrupt:
            print(BYE_MESSAGE)
            break

if __name__ == "__main__":
    main()
