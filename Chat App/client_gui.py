import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog

HOST = '127.0.0.1'  # Server's IP address
PORT = 12345        # Same port as the server

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

class ChatClient:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Chat Application")

        self.chat_area = scrolledtext.ScrolledText(self.window)
        self.chat_area.pack(padx=20, pady=5, expand=True, fill="both")
        self.chat_area.config(state="disabled")

        self.message_entry = tk.Entry(self.window)
        self.message_entry.pack(padx=20, pady=5, expand=True, fill="x")
        self.message_entry.bind("<Return>", self.write)

        self.send_button = tk.Button(self.window, text="Send", command=self.write)
        self.send_button.pack(padx=20, pady=5)

        self.nickname = simpledialog.askstring("Nickname", "Choose your nickname")
        if not self.nickname:
            self.window.destroy()
            return

        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

    def receive(self):
        """Receive messages from the server."""
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if message == "NICK":
                    client.send(self.nickname.encode('utf-8'))
                else:
                    self.display_message(message)
            except:
                self.display_message("An error occurred! Closing connection.")
                client.close()
                break

    def write(self, event=None):
        """Send a message to the server."""
        message = self.message_entry.get()
        if message:
            client.send(f"{self.nickname}: {message}".encode('utf-8'))
            self.message_entry.delete(0, tk.END)

    def display_message(self, message):
        """Display a message in the chat area."""
        self.chat_area.config(state="normal")
        self.chat_area.insert(tk.END, f"{message}\n")
        self.chat_area.yview(tk.END)
        self.chat_area.config(state="disabled")

    def on_close(self):
        """Handle window closing."""
        client.close()
        self.window.destroy()

    def run(self):
        """Run the main GUI loop."""
        self.window.mainloop()


if __name__ == "__main__":
    client_app = ChatClient()
    client_app.run()
