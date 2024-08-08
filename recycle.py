import os
import sys
import subprocess


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def overwrite_file(file_path, overwrite_passes=1):
    try:
        with open(file_path, 'r+b') as f:
            length = os.path.getsize(file_path)
            for _ in range(overwrite_passes):
                f.seek(0)
                f.write(os.urandom(length))
                f.flush()
                os.fsync(f.fileno())
    except Exception as error_overwrite:
        print(f"\033[91;1m Error overwriting file {file_path}: {error_overwrite}\033[0m")
        return False

    try:
        os.remove(file_path)
    except Exception as error_delete:
        print(f"\033[91;1m Error removing file {file_path}: {error_delete}\033[0m")
        return False

    if os.path.exists(file_path):
        print(f"\033[91;1m File {file_path} was not successfully removed.\033[0m")
        return False

    print(f"\n\033[1;92m Success, \033[1;93m{file_path}\033[1;92m file nuked!\033[0m\n")
    return True


def secure_erase_folder(folder_path, overwrite_passes=1, dry_run=False):

    if not os.path.exists(folder_path):
        print(f"\033[91;1m Error: {folder_path} does not exist.\033[0m")
        return

    files_found = False

    for root, dirs, files in os.walk(folder_path, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            files_found = True
            if dry_run:
                print(f"        {file_path}")
            else:
                if not overwrite_file(file_path, overwrite_passes):
                    print(f"\033[91;1m Failed to securely erase {file_path}\033[0m")
        for name in dirs:
            dir_path = os.path.join(root, name)
            if dry_run:
                print(f"        {dir_path} (directory)")
            else:
                try:
                    os.rmdir(dir_path)
                    print(f"\033[1;92m Success, \033[1;93m{dir_path}\033[1;92m directory removed!\033[0m\n")
                except Exception as error_rmdir:
                    print(f"\033[91;1m Error removing directory {dir_path}: {error_rmdir}\033[0m")

    if not files_found and not dry_run:
        print("\033[93;1m No files or directories found in the Trash. Exiting...\033[0m")
        exit(0)


if __name__ == '__main__':
    try:
        clear_console()
        folder_to_erase = os.path.expanduser("~/.local/share/Trash/files/")
        overwrite_passes = 1
        dry_run = True
        print("\n\033[1;97m Finding files & folders in the bin...\033[1;93m\n")
        secure_erase_folder(folder_to_erase, overwrite_passes=overwrite_passes, dry_run=dry_run)

        confirm = input("\n\033[91;1m WARNING!\n\033[1;97m"
                        " This will erase the files listed above & cannot be undone, proceed?\n"
                        " Enter \033[1;93my\033[1;97m or \033[1;93mn\033[0m: ")
        if confirm.lower() == 'y':
            dry_run = False
            secure_erase_folder(folder_to_erase, overwrite_passes=overwrite_passes, dry_run=dry_run)

        if confirm.lower() == 'n':
            print("\n\033[1;92m Aborted!\033[0m")
    except KeyboardInterrupt:
        print("\n")
        exit(0)
