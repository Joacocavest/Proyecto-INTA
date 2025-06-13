import socket

def start_server(host='10.130.1.205', port=65432, node_red_host='10.130.1.211', node_red_port=1880):
    # Crear socket UDP para enviar datos a Node-RED
    node_red_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Crear socket TCP y permitir la reutilización de la dirección
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen()
        print(f'Servidor TCP en marcha en {host}:{port}. Esperando conexiones...')

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f'Conexión establecida con {addr}')
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    print(f'Datos recibidos: {data.decode("utf-8")}')
                    
                    # Retransmitir datos a Node-RED
                    node_red_socket.sendto(data, (node_red_host, node_red_port))
                    print(f'Datos enviados a Node-RED en {node_red_host}:{node_red_port}')

if __name__ == "__main__":
    start_server()

