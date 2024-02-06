from db import models
from db.database_manager import DatabaseManager
from enum import Enum
import personalized_exceptions
from datetime import datetime
class SeatType(Enum):
    """
    Enumeration class representing the status of a seat.
    """
    FREE = "FREE"
    RESERVED = "RESERVED"
class Screens:
    """
    A class for managing screen operations.

    Attributes:
        database_manager (DatabaseManager): Instance of the DatabaseManager class.
    """
    database_manager = DatabaseManager()
    @staticmethod
    def create_screen(screen:models.screen_model):
        """
        Create a new screen in the database.

        Args:
            screen (models.screen_model): Screen model containing information about the screen.

        Returns:
            bool: True if the screen creation is successful; otherwise, False.
        """
        query = f"""INSERT INTO `cinemaswift`.`screens` (`film_id`, `number_of_sans`) 
        VALUES 
        ('{screen.film_id}', '{screen.number_of_screens}');"""
        Screens.database_manager.execute_query(query)
        return True
    
    @staticmethod
    def remove_screen(screen_id:int):
        """
        Remove a screen from the database.

        Args:
            screen_id (int): The ID of the screen to be removed.

        Returns:
            bool: True if the screen removal is successful; otherwise, False.

        Raises:
            personalized_exceptions.RemoveScreenNotPossible: If the screen cannot be removed.
        """
        query = f"""SELECT id FROM cinemaswift.sessions WHERE screen_id = '{screen_id}';"""
        r = Screens.database_manager.execute_query_select(query)
        if len(r)>0:
            raise personalized_exceptions.RemoveScreenNotPossible()
        query = f"""DELETE FROM `cinemaswift`.`screens` WHERE (`id` = '{screen_id}');"""
        Screens.database_manager.execute_query(query)
        return True
    
    @staticmethod
    def update_screen(screen:models.screen_model):
        """
        Update information about a screen in the database.

        Args:
            screen (models.screen_model): Screen model containing updated information about the screen.

        Returns:
            bool: True if the screen update is successful; otherwise, False.

        Raises:
            personalized_exceptions.UpdateScreenNotPossible: If the screen update is not possible.
        """
        query = f"""SELECT count(id) FROM sessions WHERE screen_id = '{screen.id}'"""
        r = Screens.database_manager.execute_query_select(query)
        if r[0][0]>screen.number_of_screens:
            raise personalized_exceptions.UpdateScreenNotPossible()
        query = f"""UPDATE `cinemaswift`.`screens`
                SET `film_id` = '{screen.film_id}', `number_of_sans` = '{screen.number_of_screens}' 
                WHERE 
                (`id` = '{screen.id}');"""
        Screens.database_manager.execute_query(query)
        return True
    @staticmethod
    def get_screens_list():
        """
        Get a list of screens along with their associated films and number of seats.

        Returns:
            list: List of tuples containing screen information (film name, number of seats).
        """
        query = """SELECT cinemaswift.films.name , cinemaswift.screens.number_of_sans FROM cinemaswift.screens
                join films
                on  films.id = screens.film_id;"""
        r = Screens.database_manager.execute_query_select(query)
        return r
    
    @staticmethod
    def get_screens_list_for_a_film(film_id:int):
        """
        Get a list of screens for a specific film.

        Args:
            film_id (int): The ID of the film.

        Returns:
            list: List of tuples containing screen information (film name, number of seats).
        """
        query = f"""SELECT cinemaswift.films.name , cinemaswift.screens.number_of_sans FROM cinemaswift.screens
                join films
                on  films.id = screens.film_id
                WHERE cinemaswift.screens.film_id = '{film_id}';"""
        r = Screens.database_manager.execute_query_select(query)
        return r
class Session:
    """
    A class for managing session operations.

    Attributes:
        database_manager (DatabaseManager): Instance of the DatabaseManager class.
    """
    database_manager = DatabaseManager()
    @staticmethod
    def create_session(session:models.session_model):
        """
        Create a new session in the database.

        Args:
            session (models.session_model): Session model containing information about the session.

        Returns:
            bool: True if the session creation is successful; otherwise, False.

        Raises:
            personalized_exceptions.CreateSessionNotPossible: If the session creation is not possible.
        """
        if session.capacity < 1 :
            raise personalized_exceptions.CreateSessionNotPossibleCapacity()
        query = f"""SELECT count(id) FROM sessions 
                WHERE screen_id = '{session.screen_id}'"""
                
        defined_session = Session.database_manager.execute_query_select(query)
        defined_session = defined_session[0][0]
        query = f"""SELECT number_of_sans FROM screens 
                WHERE id = '{session.screen_id}'"""
        total_allowed_sessions = Session.database_manager.execute_query_select(query)
        total_allowed_sessions = total_allowed_sessions[0][0]
        
        if defined_session == total_allowed_sessions:
            raise personalized_exceptions.CreateSessionNotPossibleMaxNumber()
        
        time = session.start_time
        timestamp_str = f"{time.year}-{time.month:02d}-{time.day:02d} {time.hour:02d}:{time.minute:02d}"
        query = f"""SELECT id FROM cinemaswift.sessions
                 WHERE start_time = '{timestamp_str}';"""
        r = Session.database_manager.execute_query_select(query)
        
        if len(r)>0:
            raise personalized_exceptions.CreateSessionNotPossible()
        
        query = f"""INSERT INTO `cinemaswift`.`sessions` (`screen_id`, `start_time`, `capacity`) 
                    VALUES 
                    ('{session.screen_id}', '{timestamp_str}' , '{session.capacity}');"""
        Session.database_manager.execute_query(query)
        query = f"""SELECT id FROM sessions WHERE start_time = '{timestamp_str}' AND screen_id = '{session.screen_id}'"""
        session_id = Session.database_manager.execute_query_select(query)
        session_id = session_id[0][0]
        Seats.create_seat(models.seat_model(-1,session_id,SeatType.FREE.value),session.capacity)
        
        return True
    
    
    @staticmethod
    def remove_session(session_id:int):
        """
        Remove a session from the database.

        Args:
            session_id (int): The ID of the session to be removed.

        Returns:
            bool: True if the session removal is successful; otherwise, False.

        Raises:
            personalized_exceptions.RemoveSessionNotPossible: If the session cannot be removed.
        """
        query = f"""SELECT capacity FROM cinemaswift.sessions
                WHERE id = '{session_id}' ;"""
        total_seats = Seats.database_manager.execute_query_select(query)[0][0]
        free_seats = Seats.get_number_of_free_seats(session_id)
        
        if total_seats!=free_seats:
            raise personalized_exceptions.RemoveSessionNotPossible()
        query = f"""DELETE FROM `cinemaswift`.`sessions` WHERE (`id` = '{session_id}');"""
        Session.database_manager.execute_query(query)
        return True
    
    @staticmethod
    def get_number_of_remain_sessions(screen_id:int):
        """
        Get the number of remaining sessions for a screen.

        Args:
            screen_id (int): The ID of the screen.

        Returns:
            int: The number of remaining sessions.
        """
        query = f"""SELECT * FROM cinemaswift.sessions
                WHERE
                screen_id = '{screen_id}';"""
        r = Screens.database_manager.execute_query_select(query)
        counted = 0
        for i in r:
            session_id = i[0]
            start_time = i[2]
            if start_time < datetime.now():
                continue
            if Seats.get_number_of_free_seats(session_id)==0:
                continue
            counted+=1
        return counted
        
        
class Seats:
    """
    A class for managing seat operations.

    Attributes:
        database_manager (DatabaseManager): Instance of the DatabaseManager class.
    """
    database_manager = DatabaseManager()
    @staticmethod
    def create_seat(seat:models.seat_model,number:int):
        """
        Create seats for a session in the database.

        Args:
            seat (models.seat_model): Seat model containing information about the seat.
            number (int): The number of seats to create.

        Returns:
            bool: True if seat creation is successful; otherwise, False.
        """ 
        query = """INSERT INTO `cinemaswift`.`seats` (`session_id`, `status` , `number`) 
                VALUES """
        for i in range(number):
            query+=f"('{seat.session_id}' , '{seat.status}', '{i+1}'),"
        query=query[:-1]+';'
        Seats.database_manager.execute_query(query)
        return True
    
    @staticmethod
    def update_seat(seat_id:int,status:SeatType):
        """
        Update the status of a seat in the database.

        Args:
            seat_id (int): The ID of the seat to update.
            status (SeatType): The new status of the seat.

        Returns:
            bool: True if seat update is successful; otherwise, False.
        """
        query = f"""UPDATE `cinemaswift`.`seats` SET `status` = '{status.value}' WHERE (`id` = '{seat_id}');"""
        Seats.database_manager.execute_query(query)
        return True
    @staticmethod
    def get_seats_of_a_session(session_id:int):
        """
        Get seats for a session from the database.

        Args:
            session_id (int): The ID of the session.

        Returns:
            list: List of seats for the session.
        """
        query = f"""SELECT * FROM cinemaswift.seats WHERE session_id = '{session_id}';"""
        r= Seats.database_manager.execute_query_select(query)
        return r
    @staticmethod
    def get_number_of_free_seats(session_id:int):
        """
        Get the number of free seats for a session from the database.

        Args:
            session_id (int): The ID of the session.

        Returns:
            int: The number of free seats for the session.
        """
        query = f"""SELECT count(id) FROM cinemaswift.seats 
                WHERE 
                session_id = '{session_id}' AND status = '{SeatType.FREE.value}';"""
        r= Seats.database_manager.execute_query_select(query)
        r = r[0][0]
        return r
# Screens.create_screen(models.screen_model(-1,2,5))
# Screens.update_screen(models.screen_model(-1,2,6))
# print(Screens.get_screens_list())
# print(Screens.get_screens_list_for_a_film(2))
# Seats.update_seat(1,SeatType.RESERVED)
# print(Seats.get_number_of_free_seats(19))
# Session.remove_session(21)
# Session.create_session(models.session_model(-1,2,datetime.now(),30))
# print(Session.get_number_of_remain_sessions(2))
