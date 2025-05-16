import socket

def start_client(host='10.130.1.205', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        print(f'Conectado al servidor en {host}:{port}')

        while True:
            message = input("Escribe un mensaje para enviar al servidor ('salir' para terminar): ")
            if message.lower() == 'salir':
                print('Cerrando conexión...')
                break
            
            client_socket.sendall(message.encode('utf-8'))
            print(f'Mensaje enviado: {message}')

if __name__ == "__main__":
    start_client()

