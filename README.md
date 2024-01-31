# CinemaSwift 
## Introuction 
This project handles online cinema reservations, incorporating several noteworthy features such as the ability to rate films and make reservations. Users can score their favorite movies and easily book seats for upcoming screenings, enhancing the overall cinema-going experience

## Installation Guid 
Create a virtual environment py this command in terminal: 
```bash
py -m venv venv
```
Active the virtual environment by this command:
```bash
\venv\Scripts\activate
```
now use this command to install all of the requirements:
```bash
pip install -r requirements.txt
```

## Project Details 
In this project, the backend development follows the MVC (Model-View-Controller) architecture, where the backend is separated into different parts. Each of these parts will be explained in detail here to provide a comprehensive understanding of the project's structural design and organization.

### db -> Database Management
"The models in this section encapsulate the essential structural components of each database table, providing a clear and organized representation of the data schema. Meanwhile, the database manager, following a singleton design pattern, plays a pivotal role in database interactions. It establishes and maintains connections to the database, ensures data is regularly refreshed, and employs caching mechanisms to optimize data retrieval and storage performance. By effectively managing the interplay between models and the database, this project establishes a robust foundation for data storage and retrieval within the MVC architecture."
