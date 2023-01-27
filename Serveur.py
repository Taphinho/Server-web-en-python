#coding:utf-8
import socket 
import argparse
import threading


parser = argparse.ArgumentParser()
parser.add_argument("--base","-b",required=True,help="Chemin du repertoire contenant le fichier index.html de votre site web (terminant toujours par un '/')")
parser.add_argument("--port","-p",required=True,help="Port a attribuer au serveur web")

args=parser.parse_args()

chemin = args.base
port = args.port

print(""" 

#######    #    ######  #     #   ###   #     # #     # #######
   #      # #   #     # #     #    #    ##    # #     # #     #
   #     #   #  #     # #     #    #    # #   # #     # #     #
   #    #     # ######  #######    #    #  #  # ####### #     #
   #    ####### #       #     #    #    #   # # #     # #     #
   #    #     # #       #     #    #    #    ## #     # #     #
   #    #     # #       #     #   ###   #     # #     # #######

 #####  ####### ######  #     # ####### ######
#     # #       #     # #     # #       #     #
#       #       #     # #     # #       #     #
 #####  #####   ######  #     # #####   ######
      # #       #   #    #   #  #       #   #
#     # #       #    #    # #   #       #    #
 #####  ####### #     #    #    ####### #     #



        """)
print("CE SERVEUR WEB A ETE CREE PAR MOUSTAPHA MADIOP NIANG,UN ETUDIANT DE L'ESP.IL A ETE OPTIMISER POUR MOZILLA FIREFOX\n\n")
if chemin[len(chemin)-1] !="/":
    print("DOSSIER NON TROUVER, ESSAYEZ AVEC UN '/' A LA FIN ")
else:    
    server_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #Creation du socket du server
    print("ctrl + c pour quitter le server\n\n")

    try :
        server_sock.bind(('',int(port)))
        server_sock.listen(5)
        print("EN ATTENTE DE CONNEXION ...")
        #attente de connexion
        #connexion_client,addresse_client=server_sock.accept()

        def handle(connexion_client) :
            
                request=connexion_client.recv(2048)
                print('REQUETE : \n'+request.decode())
                lines = request.split(b'\r\n')
                #Reception de la requete HTTP
                request_type,request_path,request_version = lines[0].decode().split(' ')
                if request_type == "GET" and request_path == "/" :
                        
                        path = chemin+"index.html"
                        with open(path,'r') as f :
                            response_body = f.read()
                            response_headers = 'HTTP/1.1 200 OK\nContent-Type:text/html;\nContent-Length:'+str(len(response_body))+';\nKeep-Alive:timeout=5,max=100;\nConnection: Keep-Alive;\n\n'
                            
                            connexion_client.sendall(response_headers.encode())
                            connexion_client.sendall(response_body.encode())
                            connexion_client.close()
                elif request_type == "GET" :
                    try :
                        path= chemin+str(request_path)
                        with open(path,'rb') as f :
                            response_body = f.read()
                            response_headers = 'HTTP/1.1 200 OK\nContent-Type:*/*;\nContent-Length:'+str(len(response_body))+';\nKeep-Alive:timeout=5,max=100;\nConnection: Keep-Alive;\n\n'
                            
                            connexion_client.sendall(response_headers.encode())
                            connexion_client.sendall(response_body)
                    except FileNotFoundError :
                            response_body ='404 ERROR\nPAGE INTROUVABLE!!!'
                            response_headers = 'HTTP/1.1 404 Not Found\nContent-Type:text/plain\n\n'
                            connexion_client.sendall(response_headers.encode())
                            connexion_client.sendall(response_body.encode())
                    finally :
                            connexion_client.close()
                        
                else :
                            
                        response_body =f'La requete '+request_type+' n\'est pas prise en compte'
                        response_headers = 'HTTP/1.1 501 Not implemented\nContent-Type:text/plain\n\n'
                        connexion_client.sendall(response_headers.encode())
                        connexion_client.sendall(response_body.encode())
                        connexion_client.close()

                    
            
                    
                        
            
                        
        while True :
                connexion_client,addresse_client=server_sock.accept()
                print(f"Connection de la part de {addresse_client}")
                client_thread = threading.Thread(target=handle,args=(connexion_client,)) 
                client_thread.start()



        
    except OSError :
        print("VEUILLEZ RESSAYER")
    except KeyboardInterrupt :
        server_sock.close()

    finally :
        server_sock.close()
