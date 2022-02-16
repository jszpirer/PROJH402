from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

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