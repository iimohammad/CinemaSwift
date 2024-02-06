from db import models
from db.database_manager import DatabaseManager
import personalized_exceptions
class Films:
    """
    A class representing operations related to films in the database.
    """
    database_manager = DatabaseManager()
    @staticmethod
    def add_film(film:models.film_model):
        """
        Adds a new film to the database.

        Args:
            film (models.film_model): The film object to be added.

        Returns:
            bool: True if the film is added successfully, False otherwise.
        """
        query = f"""INSERT INTO `cinemaswift`.`films` (`name`, `age_rating`, `duration`, `point`) 
                VALUES 
                ('{film.name}', '{film.age_rating}', '{film.duration}', '0');"""
        Films.database_manager.execute_query(query)
        return True
    
    @staticmethod
    def get_film(film_id:int)-> models.film_model:
        """
        Retrieves information about a film based on its ID.

        Args:
            film_id (int): The ID of the film to retrieve.

        Returns:
            models.film_model: The film object containing information about the film.
        
        Raises:
            personalized_exceptions.FilmNotFount: If the film with the given ID is not found.
        """
        query = f"SELECT id,name,age_rating,duration,point FROM films WHERE id = '{film_id}'"
        r = Films.database_manager.execute_query_select(query)
        if len(r)==0:
            raise personalized_exceptions.FilmNotFount()
        return models.film_model(r[0][0],r[0][1],r[0][2],r[0][3],r[0][4],)
    @staticmethod
    def remove_film(film_id:int)->bool:
        """
        Removes a film from the database.

        Args:
            film_id (int): The ID of the film to remove.

        Returns:
            bool: True if the film is removed successfully, False otherwise.
        
        Raises:
            personalized_exceptions.RemoveFilmNotPossible: If the film cannot be removed.
        """
        query = f"""SELECT id FROM screens WHERE id = '{film_id}';"""
        r = Films.database_manager.execute_query_select(query)
        if len(r)>0:
            raise personalized_exceptions.RemoveFilmNotPossible()
        query = f"""DELETE FROM films WHERE id = '{film_id}';"""
        Films.database_manager.execute_query(query)
        return True
    @staticmethod
    def _calculate_point(film_id:int):
        """
        Calculates the average point for a film.

        Args:
            film_id (int): The ID of the film.

        Returns:
            bool: True if the calculation is successful, False otherwise.
        """
        #query : calculate film rate base on rate table
        query = f"""UPDATE films set point = (select avg(point) as av from filmspoints  
                where film_id='{film_id}') 
                where id = '{film_id}'"""
        Films.database_manager.execute_query(query)
        return True
    @staticmethod
    def update_film(film:models.film_model):
        """
        Updates information about a film in the database.

        Args:
            film (models.film_model): The updated film object.

        Returns:
            bool: True if the film information is updated successfully, False otherwise.
        """
        query = f"""UPDATE films set 
        name = '{film.name}' AND age_rating = '{film.age_rating}' AND duration = '{film.duration}'
        WHERE id = '{film.id}'"""
        Films.database_manager.execute_query(query)
        return True
class FilmsPoints:
    """
    A class representing operations related to film ratings in the database.
    """
    database_manager = DatabaseManager()
    @staticmethod
    def add_point(user_id:str,film_id:int,point:int):
        """
        Adds a rating point for a film by a user.

        Args:
            user_id (str): The ID of the user.
            film_id (int): The ID of the film.
            point (int): The rating point to be added.

        Returns:
            bool: True if the point is added successfully, False otherwise.
        """
        query = f"SELECT point FROM filmspoints WHERE client_id='{user_id}' AND film_id='{film_id}'"
        r = FilmsPoints.database_manager.execute_query_select(query)
        if len(r)>0:
            query = f"""UPDATE `cinemaswift`.`filmspoints` SET `point` = '{point}' 
                    WHERE 
                    (`film_id` = '{film_id}') and (`user_id` = '{user_id}');"""
            FilmsPoints.database_manager.execute_query(query)
        else :
            query = f"""INSERT INTO `cinemaswift`.`filmspoints` (`{film_id}`, `{user_id}`, `{point}`)
                VALUES
                ('{film_id}', '{user_id}', '{point}');"""
            FilmsPoints.database_manager.execute_query(query)
        Films._calculate_point(film_id)
        return True
    @staticmethod
    def remove_point(client_id:str,film_id:int):
        """
        Removes a rating point for a film by a user.

        Args:
            client_id (str): The ID of the client.
            film_id (int): The ID of the film.

        Returns:
            bool: True if the point is removed successfully, False otherwise.
        """
        query = f"""DELETE FROM filmspoints WHERE user_id = '{client_id}' AND film_id = '{film_id}';""" 
        FilmsPoints.database_manager.execute_query(query)
        Films._calculate_point(film_id)
        return True
    
class Comments:
    """
    A class representing operations related to comments on films in the database.
    """
    database_manager = DatabaseManager()
    @staticmethod
    def add_comment(comment:models.comment_model):
        """
        Adds a comment to a film in the database.

        Args:
            comment (models.comment_model): The comment object to be added.

        Returns:
            bool: True if the comment is added successfully, False otherwise.
        """
        query = f"""INSERT INTO `cinemaswift`.`comments` 
        (`film_id`,`user_id`, `text` , `parent_comment`) 
        VALUES 
        ('{comment.film_id}', '{comment.user_id}', '{comment.text}',{comment.parent_comments_id});"""
        
        Comments.database_manager.execute_query(query)
        return True
    @staticmethod
    def remove_comment(comment_id:int):
        """
        Removes a comment from the database.

        Args:
            comment_id (int): The ID of the comment to remove.

        Returns:
            bool: True if the comment is removed successfully, False otherwise.
        """
        query = f"""DELETE FROM comments WHERE id = '{comment_id}';"""
        Comments.database_manager.execute_query(query)
        return True
    
    @staticmethod
    def update_comment(comment:models.comment_model):
        """
        Updates information about a comment in the database.

        Args:
            comment (models.comment_model): The updated comment object.

        Returns:
            bool: True if the comment information is updated successfully, False otherwise.
        """
        query = f"""UPDATE `cinemaswift`.`comments` 
            SET 
            `film_id` = '{comment.film_id}', `user_id` = '{comment.user_id}', 
            `text` = '{comment.text}', `parent_comment` = {comment.parent_comments_id}
            WHERE (`id` = '{comment.id}');"""
        Comments.database_manager.execute_query(query)
        return True
    @staticmethod
    def get_comments_of_film(film_id:int):
        """
        Retrieves comments of a film from the database.

        Args:
            film_id (int): The ID of the film.

        Returns:
            list: A list of comments related to the specified film.
        """
        query = f"""SELECT users.user_name,comments.id,comments.text,comments.created_at,comments.parent_comment 
                FROM cinemaswift.comments
                left join cinemaswift.users
                ON users.id = comments.user_id
                where comments.film_id = '{film_id}'"""
        r = Comments.database_manager.execute_query_select(query)
        return r