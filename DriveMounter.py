import subprocess
import sqlite3
import os

while True:
    ### Var's ###
    lines1 = "-----------------------------------------"
    white_space = "     "
    current_user = os.popen('echo -n "$USER"').read()
    DefaultMountLocation = str()
    mountFolderName = str()
    Bye_Message = "\n" + "\033[91m {}\033[00m".format("-------- Good Bye! ---------------------")

    ################## Sqlite Connection #################
    try:
        sqliteConnection = sqlite3.connect('database_DriverMounter.db')
        cursor = sqliteConnection.cursor()

    except sqlite3.Error as error:
        terminal.run_command(f"echo 'Error occurred - {error}'")


    sqliteConnection.execute('''CREATE TABLE IF NOT EXISTS Info
        (
        DefaultMountLocation TEXT ,
        MountFolder TEXT
        );''')
    ######################################################

    ######## Fetching Data From SQL Table ################
    cursor.execute("""SELECT * FROM Info""")
    rows = cursor.fetchall()
    for row in rows:
        DefaultMountLocation = row[0]
        mountFolderName = row[1]
    ######################################################

    try:
        def Mount(def_mount_loc,MountFol):
            print("  " + white_space,end='')
            print("\033[94m {}\033[00m".format("Use Ctrl + C to Go back!"))
            print(lines1)
            print("  " + white_space,end='')
            print("\033[91m {}\033[00m".format("Choose a Mount Point"))
            print(lines1)

            subprocess.run("lsblk")

            input1 = input("\n" + "\033[91m {}\033[00m".format("Mount Point (sdb1,sda3 ...) : "))

            if not MountFol:
                input4 = input("\033[91m {}\033[00m".format("Name For The Mounted Folder : "))
                subprocess.run(["sudo","mkdir",f"{def_mount_loc}/{input4}"])
                sql_2 = f'''INSERT INTO Info (DefaultMountLocation,MountFolder) VALUES ("{def_mount_loc}","{input4}")'''
                cursor.execute(sql_2)
                sqliteConnection.commit()
                print()
                print(lines1)
                print("\n" + "\033[91m {}\033[00m".format(f"Mounting /dev/{input1} to --> {def_mount_loc}/{input4}" + "\n"))
                print(lines1)
            else:
                input3 = input("\033[91m {}\033[00m".format("Use the name " +"***"+str(MountFol)+"***"+ " (y/n)? "))
                if input3.lower() == "y":
                    subprocess.run(["sudo","mkdir",f"{def_mount_loc}/{MountFol}"])
                    print()
                    print(lines1)
                    print("\n" + "\033[91m {}\033[00m".format(f"Mounting /dev/{input1} to --> {def_mount_loc}/{MountFol}" + "\n"))
                    print(lines1)

                elif input3.lower() == "n":
                    input4 = input("\033[91m {}\033[00m".format("Enter a New Name For The Mounted Folder : "))
                    subprocess.run(["sudo","mkdir",f"{def_mount_loc}/{input4}"])
                    sql_2 = f'''INSERT INTO Info (DefaultMountLocation,MountFolder) VALUES ("{def_mount_loc}","{input4}")'''
                    cursor.execute(sql_2)
                    sqliteConnection.commit()
                    print()
                    print(lines1)
                    print("\n" + "\033[91m {}\033[00m".format(f"Mounting /dev/{input1} to --> {def_mount_loc}/{input4}" + "\n"))
                    print(lines1)
                    subprocess.run(["sudo","mount",f"/dev/{input1}",f"{def_mount_loc}/{input4}"])

            input3 = input("\033[91m {}\033[00m".format("Done! Press Any Key To continue! "))
            if input3:
                pass
    except KeyboardInterrupt:
        print(Bye_Message)

    try:
        def Unmount():
            print("  " + white_space,end='')
            print("\033[94m {}\033[00m".format("Use Ctrl + C to Go back!"))
            print(lines1)
            print("  " + white_space,end='')
            print("\033[91m {}\033[00m".format("Choose a Path to Unmount"))
            print(lines1)

            subprocess.run("lsblk")

            input1 = input("\n" + "\033[91m {}\033[00m".format("Enter The Full Path : "))

            print()
            print(lines1)
            print("\n" + "\033[91m {}\033[00m".format(f"Unmounting {input1}" + "\n"))
            print(lines1)

            subprocess.run(["sudo","umount",f"{input1}"])

            input3 = input("\033[91m {}\033[00m".format("Done! Press Any Key To continue! "))
            if input3:
                pass
    except KeyboardInterrupt:
        print(Bye_Message)

    try:
        def Disk_poweroff():
            print("  " + white_space,end='')
            print("\033[94m {}\033[00m".format("Use Ctrl + C to Go back!"))
            print(lines1)
            print("  " + white_space,end='')
            print("\033[91m {}\033[00m".format("Choose a Drive to Poweroff"))
            print(lines1)

            subprocess.run("lsblk")

            input1 = input("\n" + "\033[91m {}\033[00m".format("Enter The drive's name (sdb,sda ...) : "))

            print()
            print(lines1)
            print("\n" + "\033[91m {}\033[00m".format(f"Turning Off ... {input1}" + "\n"))
            print(lines1)

            subprocess.run(["sudo","udisksctl","power-off","-b",f"/dev/{input1}"])

            input3 = input("\033[91m {}\033[00m".format("Done! Press Any Key To continue! "))
            if input3:
                pass
    except KeyboardInterrupt:
        print(Bye_Message)

    try:
        def Change_default_mount_location(mount_location):
            print("  " + white_space,end='')
            print("\033[94m {}\033[00m".format("Use Ctrl + C to Go back!"))
            print(lines1)
            if mount_location != "":
                print("\033[91m {}\033[00m".format("The Default Location is : " + mount_location))
                print(lines1)

                input3 = input("\033[94m {}\033[00m".format("Do you want to change it? : (y/n) "))
                if input3.lower() == "y":
                    input4 = input("\033[91m {}\033[00m".format("Enter a new Location (Full Path) : "))
                    sql_3 = f'''INSERT INTO Info (DefaultMountLocation) VALUES ('{input4}')'''
                    cursor.execute(sql_3)
                    sqliteConnection.commit()

                cursor.execute("""SELECT * FROM Info""")
                rows = cursor.fetchall()
                for row in rows:
                    DefaultMountLocation = row[0]
                    mountFolderName = row[1]
            
            if mount_location == "":
                input4 = input("\033[91m {}\033[00m".format("Enter a new Location (Full Path) : "))
                sql_3 = f'''INSERT INTO Info (DefaultMountLocation) VALUES ('{input4}')'''
                cursor.execute(sql_3)
                sqliteConnection.commit()

                cursor.execute("""SELECT * FROM Info""")
                rows = cursor.fetchall()
                for row in rows:
                    DefaultMountLocation = row[0]
                    mountFolderName = row[1]

            print()
            print(lines1)
            print("\n" + "\033[91m {}\033[00m".format(f"Current location is {DefaultMountLocation}" + "\n"))
            print(lines1)

            input3 = input("\033[91m {}\033[00m".format("Done! Press Any Key To continue! "))
            if input3:
                pass
    except KeyboardInterrupt:
        print(Bye_Message)

    try:
        def Delete_Database():
            print()
            print(lines1)
            print("\n" + "\033[91m {}\033[00m".format("Deleting ... database_DriverMounter.db" + "\n"))
            print(lines1)

            #subprocess.run(["sudo","rm","database_DriverMounter.db"])
            subprocess.run(["rm","database_DriverMounter.db"])


            input3 = input("\033[91m {}\033[00m".format("Done! Press Any Key To continue! "))
            if input3:
                pass
    except KeyboardInterrupt:
        print(Bye_Message)


    #Welcome Screen
    try:
            subprocess.run("clear")
            print(lines1)
            print("\033[93m {}\033[00m".format(white_space + f"Welcome {current_user} To Drive Mounter!"))
            print("\033[93m {}\033[00m".format(white_space + "By github.com/stking68"))
            print(lines1)

            print("\033[96m {}\033[00m".format(white_space + "Choose an Option"))

            if DefaultMountLocation != "":
                print("\033[96m {}\033[00m".format(white_space + f"Default Location is : {DefaultMountLocation}"))
            else:
                print()
                print("\033[91m {}\033[00m".format(white_space + f"Please Enter a Default \n"+ white_space +" Mount Location Using [4] !"))
            print(lines1)

            print()
            print("\033[95m {}\033[00m".format(white_space + "[1]Mount"))
            print("\033[95m {}\033[00m".format(white_space + "[2]Unmount"))
            print("\033[95m {}\033[00m".format(white_space + "[3]Poweroff Disk"))
            print("\033[95m {}\033[00m".format(white_space + "[4]Change Default Mount Location"))
            print("\033[95m {}\033[00m".format(white_space + "[5]Delete Database"))
            print("\033[95m {}\033[00m".format(white_space + "[6]Exit"))
            input_text = "\033[91m {}\033[00m".format(white_space + "----> ")
            input4 = str(input(input_text))
            if input4.lower() == "1":
                subprocess.run("clear")
                Mount(DefaultMountLocation,mountFolderName)
            elif input4.lower() == "2":
                subprocess.run("clear")
                Unmount()
            elif input4.lower() == "3":
                subprocess.run("clear")
                Disk_poweroff()
            elif input4.lower() == "4":
                subprocess.run("clear")
                Change_default_mount_location(DefaultMountLocation)
            elif input4.lower() == "5":
                Delete_Database()
            elif input4.lower() == "6":
                print(Bye_Message)
                break
            else:
                print("Wrong input try again!")
    except KeyboardInterrupt:
        pass
