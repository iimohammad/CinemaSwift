
# Import necessary modules
import unittest
from unittest.mock import patch
from io import StringIO
import argparse
from client import TCPClient, clientSettings,main

# Initialize client and settings
client = TCPClient()
client_settings = clientSettings()


# Test connect
class TCPClient(unittest.TestCase):
    def connect(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.client.connect()
            self.assertIn("Connected to", mock_stdout.getvalue().strip())

# Test send_dict_to_server
    def send_dict_to_server(self):
        data_dict = {"key": "value"}
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout, \
             patch.object(self.client.client_socket, 'recv', return_value=b'MockResponse'):
            response = self.client.send_dict_to_server(data_dict)
            self.assertEqual(response, b'MockResponse')
            self.assertIn("Sent dictionary to the server", mock_stdout.getvalue().strip())
            self.assertIn("Received response from the server", mock_stdout.getvalue().strip())

# Test main
    def main(self , mock_input, mock_getpass):
    
        # Test signup functionality
         with patch('client.TCPClient.send_dict_to_server', return_value=b"Signup successful!") as mock_send:
            args_signup = {'action': 'signup', 'username': 'testuser'}
            main(args_signup)
            mock_send.assert_called_once_with({
                'action': 'signup',
                'username': 'testuser',
                'password': 'password',
                'email': 'test@example.com',
                'phone': '1234567890',
                'birthday': '2000-01-01'
            })

        
        # Test login functionality
         with patch('client.TCPClient.send_dict_to_server', return_value=b"Login successful!") as mock_send:
            args_login = {'action': 'login', 'username': 'testuser'}
            main(args_login)
            mock_send.assert_called_once_with({
                'action': 'login',
                'username': 'testuser',
                'password': 'password'
         })
        # Test admin login functionality
         with patch('client.TCPClient.send_dict_to_server', return_value=b"Login successful!") as mock_send:
            args_admin_login = {'action': 'login', 'username': 'admin'}
            main(args_admin_login)
            mock_send.assert_called_once_with({
                'action': 'login',
                'username': 'admin',
                'password': 'password'
            })