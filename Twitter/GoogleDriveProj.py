from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from docs.Google import Create_Service


class GoogleDriveProj:
    def __init__(self):
        """Creates the GoogleDrive object which will host the artworks created by the creator."""
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        self.drive = GoogleDrive(gauth)

    def upload_file(self, filename):
        gfile = self.drive.CreateFile({'parents': [{'id': '118fLfsoSmGZCg9ISKrNbiieQSQPTpi7F'}]})
        # Read file and set it as the content of PROJH402 folder.ù
        print("Uploading...")
        gfile.SetContentFile(filename)
        gfile.Upload()  # Upload the file.
        new_permission = {
            'id': 'anyoneWithLink',
            'type': 'anyone',
            'value': 'anyoneWithLink',
            'withLink': True,
            'role': 'reader'
        }
        permission = gfile.auth.service.permissions().insert(
            fileId=gfile['id'], body=new_permission, supportsTeamDrives=True).execute(http=gfile.http)

    def createService(self):
        CLIENT_SECRET_FILE = '../client_secrets.json'
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
            {'q': "'{}' in parents and trashed=false".format('118fLfsoSmGZCg9ISKrNbiieQSQPTpi7F')}).GetList()
        for file in file_list:
            print('title: %s, id: %s' % (file['title'], file['id']))
            print(self.share_link(file['id']))

    def get_id_from_name(self, filename):
        file_list = self.drive.ListFile({'q': "'{}' in parents and trashed=false".format('118fLfsoSmGZCg9ISKrNbiieQSQPTpi7F')}).GetList()
        for file in file_list:
            if file['title'] == filename:
                return file['id']
        return "None"
