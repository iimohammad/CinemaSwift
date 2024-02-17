from db import models
from db.database_manager import DatabaseManager
from users_module import personalized_exceptions, users
from comments_module import queryset


class Films:
    """
    A class representing operations related to films in the database.
    """

    @staticmethod
    def add_film(film: models.film_model):
        """
        Adds a new film to the database.
        Args:
            film (models.film_model): The film object to be added.
        Returns:
            bool: True if the film is added successfully, False otherwise.
        """
        queryset.add_film_query(film.name, film.age_rating, film.duration)
        return True

    @staticmethod
    def get_film(film_id: int) -> models.film_model:
        """
        Retrieves information about a film based on its ID.
        Args:
            film_id (int): The ID of the film to retrieve.
        Returns:
            models.film_model: The film object containing information about the film.
        Raises:
            personalized_exceptions.FilmNotFount: If the film with the given ID is not found.
        """
        r = queryset.get_film_query(film_id=film_id)
        if len(r) == 0:
            raise personalized_exceptions.FilmNotFount()
        return models.film_model(r[0][0], r[0][1], r[0][2], r[0][3], r[0][4], r[0][5])

    @staticmethod
    def get_films_list() -> list:
        films = []
        r = queryset.get_films_list_query()
        for i in r:
            film = models.film_model(i[0], i[1], i[2], i[3], i[4], i[5])
            films.append(film)

        return films

    @staticmethod
    def get_filmid_by_name(film_name: str):
        r = queryset.get_filmid_by_name_query(film_name)
        if len(r) == 0:
            return None
        return r[0][0]

    @staticmethod
    def remove_film(film_id: int) -> bool:
        """
        Removes a film from the database.
        Args:
            film_id (int): The ID of the film to remove.
        Returns:
            bool: True if the film is removed successfully, False otherwise.
        Raises:
            personalized_exceptions.RemoveFilmNotPossible: If the film cannot be removed.
        """
        r = queryset.remove_film_screen_query(film_id=film_id)
        if len(r) > 0:
            raise personalized_exceptions.RemoveFilmNotPossible()
        queryset.remove_film_films_query(film_id=film_id)
        return True

    @staticmethod
    def calculate_point(film_id: int):
        """
        Calculates the average point for a film.
        Args:
            film_id (int): The ID of the film.
        Returns:
            bool: True if the calculation is successful, False otherwise.
        """
        queryset.calculate_point_query(film_id=film_id)
        return True

    @staticmethod
    def update_film(film: models.film_model):
        """
        Updates information about a film in the database.
        Args:
            film (models.film_model): The updated film object.
        Returns:
            bool: True if the film information is updated successfully, False otherwise.
        """
        queryset.update_film_query(film.name, film.id, film.age_rating, film.duration)
        return True


class FilmsPoints:
    """
    A class representing operations related to film ratings in the database.
    """
    database_manager = DatabaseManager()

    @staticmethod
    def add_point(user_id: str, film_id: int, point: int):
        """
        Adds a rating point for a film by a user.
        Args:
            user_id (str): The ID of the user.
            film_id (int): The ID of the film.
            point (int): The rating point to be added.

        Returns:
            bool: True if the point is added successfully, False otherwise.
        """
        if int(point)<1 or int(point)>5:
            raise personalized_exceptions.InvalidPointError()
        user_type = users.Subscriptions.get_subscription_type_name(user_id)
        coefficient = 1
        if (user_type == 'Golden'):
            coefficient = 3
        elif (user_type == 'Silver'):
            coefficient = 2
        r = queryset.select_point_query(user_id=user_id, film_id=film_id)
        if len(r) > 0:
            queryset.update_point_film(user_id=user_id, film_id=film_id, point=point, coefficient=coefficient)
        else:
            queryset.insert_films_point(film_id=film_id, user_id=user_id, point=point, coefficient=coefficient)
        Films.calculate_point(film_id)
        return True

    @staticmethod
    def remove_point(client_id: str, film_id: int):
        """
        Removes a rating point for a film by a user.
        Args:
            client_id (str): The ID of the client.
            film_id (int): The ID of the film.
        Returns:
            bool: True if the point is removed successfully, False otherwise.
        """
        queryset.remove_point_query(client_id, film_id)
        Films.calculate_point(film_id)
        return True


class Comments:
    """
    A class representing operations related to comments on films in the database.
    """

    @staticmethod
    def add_comment(comment: models.comment_model):
        """
        Adds a comment to a film in the database.
        Args:
            comment (models.comment_model): The comment object to be added.
        Returns:
            bool: True if the comment is added successfully, False otherwise.
        """
        parrent = comment.parent_comments_id
        if parrent<0:
            parrent = None
        queryset.add_comment_query(comment.film_id, comment.user_id, comment.text,parrent )
        return True

    @staticmethod
    def remove_comment(comment_id: int):
        """
        Removes a comment from the database.
        Args:
            comment_id (int): The ID of the comment to remove.
        Returns:
            bool: True if the comment is removed successfully, False otherwise.
        """
        queryset.remove_comment_query(comment_id=comment_id)
        return True

    @staticmethod
    def update_comment(comment: models.comment_model):
        """
        Updates information about a comment in the database.
        Args:
            comment (models.comment_model): The updated comment object.
        Returns:
            bool: True if the comment information is updated successfully, False otherwise.
        """
        queryset.update_comment_query(comment.film_id, comment.user_id, comment.text, comment.parent_comments_id,
                                      comment.id)
        return True

    @staticmethod
    def get_comments_of_film(film_id: int):
        """
        Retrieves comments of a film from the database.
        Args:
            film_id (int): The ID of the film.
        Returns:
            list: A list of comments related to the specified film.
        """
        resault_list = []
        r = queryset.get_comments_of_film_query(film_id)
        for i in r:
            resault_list.append([i[0],i[1],i[2],i[3],i[4]])
        return resault_list