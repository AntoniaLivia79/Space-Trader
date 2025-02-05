import socket
import threading
from game import Player, galactic_exchange


def handle_client(client_socket):
    try:
        player = Player()
        client_socket.send(b"Welcome to Space Trader!\r\n")

        while player.age < 60:
            try:
                def mock_print(text, **kwargs):  # Allow other keyword args
                    try:
                        client_socket.send((str(text) + "\r\n").encode())
                    except Exception:
                        pass

                def mock_input(prompt):
                    try:
                        if not prompt.endswith('\r\n'):
                            prompt += ' '
                        client_socket.send(prompt.encode())
                        response = client_socket.recv(1024).decode().strip()
                        client_socket.send(f"{response}\r\n".encode())
                        return response
                    except Exception as e:
                        print(f"Error in mock_input: {e}")
                        return ""

                import builtins
                original_print = builtins.print
                original_input = builtins.input
                builtins.print = mock_print
                builtins.input = mock_input

                galactic_exchange(player)

                builtins.print = original_print
                builtins.input = original_input

            except Exception as e:
                try:
                    client_socket.send(f"Error: {str(e)}\n".encode())
                except:
                    break
                break

        client_socket.send(b"Game Over!\n")
    except:
        pass
    finally:
        try:
            client_socket.close()
        except:
            pass


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 3000))
    server.listen(5)
    print("Server started on port 3000")

    while True:
        try:
            client, addr = server.accept()
            print(f"New connection from {addr}")
            client_handler = threading.Thread(target=handle_client, args=(client,))
            client_handler.daemon = True
            client_handler.start()
        except Exception as e:
            print(f"Error accepting connection: {e}")


if __name__ == "__main__":
    start_server()
