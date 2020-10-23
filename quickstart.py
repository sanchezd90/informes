from pydrive.auth import GoogleAuth

gauth = GoogleAuth()
gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.

from pydrive.drive import GoogleDrive

drive = GoogleDrive(gauth)

"""
#buscar archivos que el titulo contiene ENPS y .xlsx
for file_list in drive.ListFile({'q': "title contains 'ENPS' and title contains '.xlsx' and trashed=false", 'maxResults': 10}):
  print('Received %s files from Files.list()' % len(file_list)) # <= 10
  for file1 in file_list:
      print('title: %s, id: %s' % (file1['title'], file1['id']))
"""

#descargar archivos encontrados
for file_list in drive.ListFile({'q': "title contains 'ENPS' and title contains 'csv' and trashed=false"}):
    print('Received %s files from Files.list()' % len(file_list)) # <= 10
    for file1 in file_list:   
        file_id= file1['id']
        file_title= file1['title']  
        file_d = drive.CreateFile({'id': file_id})
        file_d.GetContentFile(file_title)

