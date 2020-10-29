from pydrive.auth import GoogleAuth

gauth = GoogleAuth()
gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.

from pydrive.drive import GoogleDrive
drive = GoogleDrive(gauth)

def get_drivefiles():
    #Paso1: abro la lista de los que ya fueron descargados
    dloads=[]
    new_dloads=[]
    with open("filedloads.txt","r") as f:
        for entry in f:
            entry=entry.rstrip("\n")
            dloads.append(entry)
    
    #Paso 2: descargar csv encontrados aún no descargados
    for file_list in drive.ListFile({'q': " '11doEjeqBMrPXpk_I3hho95WYU5YzDZ-5' in parents and trashed=false"}):
        for file1 in file_list:
            file_id= file1['id']
            q_value=f" '{file_id}' in parents and title contains 'ENPS' and title contains 'csv' and trashed=false"
            for f_list in drive.ListFile({'q': q_value}):
                for f in f_list:
                    file_title= f['title']
                    if file_title not in dloads:   
                        file_id= f['id'] 
                        file_d = drive.CreateFile({'id': file_id})
                        file_d.GetContentFile(file_title)
                        new_dloads.append(file_title)
    
    #Paso 3: descargar docs encontrados aún no descargados
    for file_list in drive.ListFile({'q': " '11doEjeqBMrPXpk_I3hho95WYU5YzDZ-5' in parents and trashed=false"}):
        for file1 in file_list:
            file_id= file1['id']
            q_value=f" '{file_id}' in parents and title contains 'ENPS' and title contains 'docx' and not title contains 'cuestionario' and trashed=false"
            for f_list in drive.ListFile({'q': q_value}):
                for f in f_list:
                    file_title= f['title']
                    if file_title not in dloads:   
                        file_id= f['id'] 
                        file_d = drive.CreateFile({'id': file_id})
                        file_d.GetContentFile(file_title)
                        new_dloads.append(file_title)
    
    #Paso 4: agregar nuevos archivos a la lista de descargados
    with open("filedloads.txt","a") as f:
        for x in new_dloads:
            f.write("\n")
            f.write(x)

get_drivefiles()

