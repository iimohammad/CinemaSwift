 <H1>CinemaSwift</H1> 

<h3>Introuction</h3>
<p>This project manages online cinema reservations, incorporating several noteworthy features such as the ability to rate films and make reservations. Users can score their favorite movies and easily book seats for upcoming screenings, enhancing the overall cinema-going experience.</p>

## Installation Guid 

<p>Follow these steps to set up the project:</p>

<h4>1- Clone the repository to your local machine:<h4>

```bash
git clone https://github.com/your-username/CinemaManagement.git

```

<p>2- Create a virtual environment py this command in terminal: </p>

```bash
py -m venv venv
```
<p>3- Active the virtual environment by this command:</p>

- For Windows :
```bash
\venv\Scripts\activate
```

- for Unix or MaxOS:

```bash
source venv/bin\activate
```

<p>4- now use this command to install all of the requirements:</p>

```bash
pip install -r requirements.txt
```

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

<p>To run the project, execute the following command:</p>

```bash
python main.py
```

<p>Follow the on-screen instructions to navigate through the application, perform actions, and experience the functionalities offered by CinemaManagement.</p>
