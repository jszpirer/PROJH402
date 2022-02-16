from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from Google import Create_Service


class GoogleDriveProj:
    def __init__(self):
        """Creates the GoogleDrive object which will host the artworks created by the creator."""
        gauth = GoogleAuth()
        self.drive = GoogleDrive(gauth)

    def upload_file(self, filename):
        gfile = self.drive.CreateFile({'parents': [{'id': '1tRRGBtmj4PRvkPa03br7VSp06Hva-Z7f'}]})
        # Read file and set it as the content of PROJH402 folder.
        gfile.SetContentFile(filename)
        gfile.Upload()  # Upload the file.

    def createService(self):
        CLIENT_SECRET_FILE = 'client_secrets.json'
        API_NAME = 'drive'
        API_VERSION = 'v3'
        SCOPES = ['https://www.googleapis.com/auth/drive']

        service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
        return service

    def share_link(self, fileId):
        share_link = "https://drive.google.com/file/d/"+fileId+"/view?usp=sharing"
        return share_link

    def list_files_from_folder(self):
        file_list = self.drive.ListFile(
            {'q': "'{}' in parents and trashed=false".format('1tRRGBtmj4PRvkPa03br7VSp06Hva-Z7f')}).GetList()
        for file in file_list:
            print('title: %s, id: %s' % (file['title'], file['id']))
            print(self.share_link(file['id']))
