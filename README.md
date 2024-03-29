![](https://img.shields.io/badge/Programming_Language-Python-blue.svg)
[![Supported Versions](https://img.shields.io/pypi/pyversions/requests.svg)](https://pypi.org/project/requests)
[![PyPI](https://img.shields.io/pypi/v/py-mdb.svg)](https://pypi.org/project/py-mdb/)
[![License](https://img.shields.io/pypi/l/py-mdb.svg)](https://github.com/zembrodt/pymdb/blob/master/LICENSE)
[![mysql_licesnce](https://img.shields.io/pypi/l/py-mdb.svg)](https://github.com/zembrodt/pymdb/blob/master/LICENSE)

 
 <H1>CinemaSwift</H1> 

## Introuction
<p>This project manages online cinema reservations, incorporating several noteworthy features such as the ability to rate films and make reservations. Users can score their favorite movies and easily book seats for upcoming screenings, enhancing the overall cinema-going experience.</p>

## Features
-  Add / Update / Delete Movies

-  Add / Update / Delete cinema

-  Add / Update / Delete Showtimes

-  Add / Update / Delete users



## Installation Guid 

<p>Follow these steps to set up the project:</p>

<h4>1- From PyPI using pip:<h4>

```bash
pip install CinemaSwift
```

<h3>Development version from GitHub:</h3>

<h4>2- Clone the repository to your local machine:<h4>

```bash
git clone https://github.com/CinemaSwift.git
```

<p> 3- To run the project, execute the following command:</p>

```bash
python main.py
```

<p>4- To start the TCP server, use the following command:: </p>

```bash
python main.py --runserver
```
<p>5- To configure the database, execute the following command: </p>

```bash
python main.py --configDB
```
<p>6- Active the virtual environment by this command:</p>

- For windows :
```bash
\venv\Scripts\activate
```

- for Unix or MaxOS:

```bash
source venv/bin\activate
```

<p>7-This command adds an admin user to the system:</p>

- For windows :
```bash
python main.py --show-user-manual
```

<p>8- Displays the user manual with available commands and usage.:</p>

- For windows :
```bash
python main.py --show-user-manual

```
<p>9- Prompts for a username and changes the specified user to an admin.:</p>

- For windows :
```bash
python main.py --change-to-admin
```
<p>10- now use this command to install all of the requirements:</p>

```bash
pip install -r requirements.txt
```

## File Structure

main.py: The main file that contains the TCP server and various commands.

users_module : User management module.

db: The module related to the connection with the database.

intractions: The module contains various commands and interactions with the server.

settings: Holds local settings, such as network configurations.

## Project Details 
<p>In this project, the backend development follows the MVC (Model-View-Controller) architecture, where the backend is separated into different parts. Each of these parts will be explained in detail here to provide a comprehensive understanding of the project's structural design and organization.</P>

### db -> Database Management
<p>"The models in this section encapsulate the essential structural components of each database table, providing a clear and organized representation of the data schema. Meanwhile, the database manager, following a singleton design pattern, plays a pivotal role in database interactions. It establishes and maintains connections to the database, ensures data is regularly refreshed, and employs caching mechanisms to optimize data retrieval and storage performance. By effectively managing the interplay between models and the database, this project establishes a robust foundation for data storage and retrieval within the MVC architecture."</p>


### users.py -> User Module :

<p>"The user module is responsible for defining user profiles with unique attributes, including usernames, emails, phone numbers, passwords, and user IDs. It enforces validation rules for each attribute, such as unique usernames and proper email formats. Additionally, it tracks user registration and login dates, ensuring accurate user activity logs."</p>


### main.py -> main Model :

<p>"The main module acts as the central hub of the application, orchestrating the flow of user interactions and coordinating the various components of the backend. It houses the core functionalities, including user authentication, cinema session management, and transaction processing. By leveraging a loop that continually awaits and processes user requests, the main module ensures seamless communication with multiple users simultaneously. Additionally, it employs an event-driven model to handle asynchronous tasks efficiently, allowing for real-time updates and responsiveness in user interactions."</p>



### client.py -> client Model:

<p>The client module simulates a user interacting with the system. Users can log in, perform various actions, and log out. The client module ensures concurrent user interactions without interference.</p>

### Usage

```bash
BUFFOR_SIZE_DATA = 65507 - UDP max packet size to avoid this use TCP instead of UDP
```

```bash
host_ip_adress = '' - localhost by default(127.0.0.1)
```

```bash
host_port = 1024 - free PORT
```

### Report

<p>The CinemaSwift project successfully implements an online cinema reservation system with user authentication, film rating, and reservation functionalities. The MVC architecture ensures a well-organized and modular codebase, promoting code reusability and maintainability. The project's main execution module, users module, and client interaction module work in harmony to provide users with a smooth and efficient experience.

The installation guide facilitates the setup process, ensuring that users can quickly deploy the system on their local machines. By following the outlined steps, users can create a virtual environment, install necessary dependencies, and start exploring the functionalities of CinemaSwift.

Overall, the project showcases effective backend development practices, encapsulating database management, user models, and client interactions in a cohesive structure. The modular design allows for easy extension and modification, making it an excellent foundation for future enhancements and feature additions.</p>

### Project Link

<a href='https://github.com/iimohammad/CinemaSwift'>Visit my github  project!</a>

<p>Note: The specific details of individual files are omitted as per your request. The emphasis is on providing guidance for setting up and running the project along with a general overview of its features.</p>

### Conclusion

<p>This readme file is primarily intended for project setup and usage. It does not include detailed explanations of individual files. For specific file functionalities, refer to the relevant sections in this readme.</p>

