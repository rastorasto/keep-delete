import os
import subprocess

def open_with_specific_app(file_path, file_type=None):
    if file_type == 'image':
        subprocess.call(['open', '-a', 'Preview', file_path])
    elif file_type == 'video':
        subprocess.call(['open', '-a', 'VLC', file_path])
    else:
        subprocess.call(['open', file_path])  # Open with default system app

def close_app(app_name):
    subprocess.call(['osascript', '-e', f'tell application "{app_name}" to quit'])

def prompt_for_action(file_path):
    action = input(f"Do you want to keep {file_path}? (y/n, Enter for yes): ")
    return action.lower() in ('y', '')  # Treat empty input as 'yes'

def prompt_for_folder_action(folder_path):
    action = input(f"Do you want to process files in folder {folder_path}? (y/n): ")
    return action.lower() == 'y'

def process_file(file_path):
    file_name = os.path.basename(file_path)
    
    if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        open_with_specific_app(file_path, 'image')
        if not prompt_for_action(file_path):
            os.remove(file_path)
            print(f"{file_name} deleted.")
        else:
            print(f"{file_name} kept.")
        close_app('Preview')
    elif file_name.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        open_with_specific_app(file_path, 'video')
        if not prompt_for_action(file_path):
            os.remove(file_path)
            print(f"{file_name} deleted.")
        else:
            print(f"{file_name} kept.")
        close_app('VLC')
    else:
        open_with_specific_app(file_path)  # Open other file types with default app
        if not prompt_for_action(file_path):
            os.remove(file_path)
            print(f"{file_name} deleted.")
        else:
            print(f"{file_name} kept.")

def main():
    folder_path = input("Enter the folder path (leave empty for current directory): ")
    
    if not folder_path:
        folder_path = os.getcwd()

    try:
        for root, dirs, files in os.walk(folder_path):
            # Prompt the user for each directory
            if not prompt_for_folder_action(root):
                print(f"Skipping folder: {root}")
                continue  # Skip processing this folder

            for file_name in files:
                file_path = os.path.join(root, file_name)
                process_file(file_path)
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting...")

if __name__ == "__main__":
    main()
