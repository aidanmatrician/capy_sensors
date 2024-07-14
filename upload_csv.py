import os
import glob
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def authenticate_drive():
    """Authenticate and create Google Drive instance."""
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Creates local webserver and automatically handles authentication
    drive = GoogleDrive(gauth)
    return drive

def upload_csv_files(drive, directory='.'):
    """Upload all CSV files in the specified directory to Google Drive and delete them after upload."""
    csv_files = glob.glob(os.path.join(directory, '*.csv'))
    for file_path in csv_files:
        try:
            file_name = os.path.basename(file_path)
            file_drive = drive.CreateFile({'title': file_name})
            file_drive.SetContentFile(file_path)
            file_drive.Upload()
            print(f'Uploaded {file_name} to Google Drive')

            # Verify the file was uploaded by checking its presence in the drive
            uploaded_file_list = drive.ListFile({'q': f"title='{file_name}'"}).GetList()
            if any(uploaded_file['title'] == file_name for uploaded_file in uploaded_file_list):
                os.remove(file_path)
                print(f'Deleted {file_name} from local disk')
            else:
                print(f'Failed to verify upload for {file_name}')

        except Exception as e:
            print(f'An error occurred: {e}')

if __name__ == '__main__':
    drive = authenticate_drive()
    upload_csv_files(drive)
