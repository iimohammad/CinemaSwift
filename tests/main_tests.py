import unittest
import threading
import socket
import time
import json
from unittest.mock import patch
from io import StringIO
from main import TCPServer, configDB, UserDatabase, ClientThread

class TestServer(unittest.TestCase):
    def setUp(self):
        self.server = TCPServer(host='localhost', port=12345)
        self.server_thread = threading.Thread(target=self.server.run_server)
        self.server_thread.start()
        time.sleep(1)

    def tearDown(self):
        self.server.server_socket.close()
        self.server_thread.join()

    def test_configDB(self):
        with patch('db.initialize_all_module.run') as mock_initialize:
            configDB()
            mock_initialize.assert_called_once()

    def test_check_credentials(self):
        UserDatabase.users = {'user1': 'password1', 'user2': 'password2'}
        self.assertTrue(UserDatabase.check_credentials('user1', 'password1'))
        self.assertFalse(UserDatabase.check_credentials('user1', 'wrong_password'))
        self.assertFalse(UserDatabase.check_credentials('nonexistent_user', 'password'))

    def test_parse_data_signup(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 12345))
        data = {'action': 'signup', 'username': 'test_user', 'password': 'test_password', 'email': 'test@example.com', 'phone': '1234567890', 'birthday': '2000-01-01'}
        client_socket.sendall(json.dumps(data).encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        self.assertEqual(response, "Signup successful!")

    def test_parse_data_login_success(self):
        UserDatabase.users = {'test_user': 'test_password'}
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 12345))
        data = {'action': 'login', 'username': 'test_user', 'password': 'test_password'}
        client_socket.sendall(json.dumps(data).encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        self.assertIn("Login successful", response)

    def test_parse_data_login_failure(self):
        UserDatabase.users = {'test_user': 'test_password'}
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 12345))
        data = {'action': 'login', 'username': 'test_user', 'password': 'wrong_password'}
        client_socket.sendall(json.dumps(data).encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        self.assertEqual(response, "Login failed. Check your credentials.")

    def test_ClientThread_run(self):
        client_socket_mock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_mock = TCPServer()
        server_mock.parse_data = lambda x, y: None 
        with patch.object(client_socket_mock, 'recv') as mock_recv, \
             patch.object(client_socket_mock, 'close') as mock_close:
            mock_recv.return_value = json.dumps({'action': 'dummy_action'}).encode('utf-8')
            client_thread = ClientThread(client_socket_mock, server_mock)
            client_thread.run()
            mock_recv.assert_called_once()
            mock_close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
