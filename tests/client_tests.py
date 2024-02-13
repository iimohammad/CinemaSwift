# Import necessary modules
import getpass
from client import TCPClient, clientSettings, main, show_services

# Initialize client and settings
client = TCPClient()
client_settings = clientSettings()

# Test connect
try:
    client.connect()
    print("Connection successful.")
except Exception as e:
    print(f"Connection failed. Error: {e}")

# Test send_dict_to_server
try:
    data_dict = {"key": "value"}
    response = client.send_dict_to_server(data_dict)
    print(f"Server response: {response.decode('utf-8')}")
except Exception as e:
    print(f"Sending data to server failed. Error: {e}")

# Test show_services
print("Available services:")
show_services()

# Test main
try:
    # Test signup functionality
    print("Testing signup functionality:")
    args_signup = argparse.Namespace(action='signup', username='testuser')
    main(args_signup)
    
    # Test login functionality
    print("Testing login functionality:")
    args_login = argparse.Namespace(action='login', username='testuser')
    main(args_login)
    
    # Test admin login functionality
    print("Testing admin login functionality:")
    args_admin_login = argparse.Namespace(action='login', username='admin')
    main(args_admin_login)
    
    # Test invalid action
    print("Testing invalid action:")
    args_invalid_action = argparse.Namespace(action='invalid_action')
    main(args_invalid_action)
    
    print("Main function executed successfully.")
except Exception as e:
    print(f"Error executing main function: {e}")
finally:
    # Close connection
    client.close_connection()
