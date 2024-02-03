from db import models
from db.database_manager import DatabaseManager
import personalized_exceptions
class Films:
    database_manager = DatabaseManager()
    @staticmethod
    def add_film(film:models.film_model):
        query = f"""INSERT INTO `cinemaswift`.`films` (`name`, `age_rating`, `duration`, `point`) 
                VALUES 
                ('{film.name}', '{film.age_rating}', '{film.duration}', '0');"""
        Films.database_manager.execute_query(query)
        return True
    
    @staticmethod
    def get_film(film_id:int)-> models.film_model:
        query = f"SELECT id,name,age_rating,duration,point FROM films WHERE id = '{film_id}'"
        r = Films.database_manager.execute_query_select(query)
        if len(r)==0:
            raise personalized_exceptions.FilmNotFount()
        return models.film_model(r[0][0],r[0][1],r[0][2],r[0][3],r[0][4],)
    @staticmethod
    def remove_film(film_id:int)->bool:
        query = f"""SELECT id FROM screens WHERE id = '{film_id}';"""
        r = Films.database_manager.execute_query_select(query)
        if len(r)>0:
            raise personalized_exceptions.RemoveFilmNotPossible()
        query = f"""DELETE FROM films WHERE id = '{film_id}';"""
        Films.database_manager.execute_query(query)
        return True
    @staticmethod
    def _calculate_point(film_id:int):
        #query : calculate film rate base on rate table
        query = f"""UPDATE films set point = (select avg(point) as av from filmspoints  
                where film_id='{film_id}') 
                where id = '{film_id}'"""
        Films.database_manager.execute_query(query)
        return True
    @staticmethod
    def update_film(film:models.film_model):
        query = f"""UPDATE films set 
        name = '{film.name}' AND age_rating = '{film.age_rating}' AND duration = '{film.duration}'
        WHERE id = '{film.id}'"""
        Films.database_manager.execute_query(query)
        return True
class FilmsPoints:
    database_manager = DatabaseManager()
    @staticmethod
    def add_point(user_id:str,film_id:int,point:int):
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
        query = f"""DELETE FROM filmspoints WHERE user_id = '{client_id}' AND film_id = '{film_id}';""" 
        FilmsPoints.database_manager.execute_query(query)
        Films._calculate_point(film_id)
        return True
    
class Comments:
    database_manager = DatabaseManager()
    @staticmethod
    def add_comment(comment:models.comment_model):
        query = f"""INSERT INTO `cinemaswift`.`comments` 
        (`film_id`,`user_id`, `text` , `parent_comment`) 
        VALUES 
        ('{comment.film_id}', '{comment.user_id}', '{comment.text}',{comment.parent_comments_id});"""
        
        Comments.database_manager.execute_query(query)
        return True
    @staticmethod
    def remove_comment(comment_id:int):
        query = f"""DELETE FROM comments WHERE id = '{comment_id}';"""
        Comments.database_manager.execute_query(query)
        return True
    
    @staticmethod
    def update_comment(comment:models.comment_model):
        query = f"""UPDATE `cinemaswift`.`comments` 
            SET 
            `film_id` = '{comment.film_id}', `user_id` = '{comment.user_id}', 
            `text` = '{comment.text}', `parent_comment` = {comment.parent_comments_id}
            WHERE (`id` = '{comment.id}');"""
        Comments.database_manager.execute_query(query)
        return True
    @staticmethod
    def get_comments_of_film(film_id:int):
        query = f"""SELECT users.user_name,comments.id,comments.text,comments.created_at,comments.parent_comment 
                FROM cinemaswift.comments
                left join cinemaswift.users
                ON users.id = comments.user_id
                where comments.film_id = '{film_id}'"""
        r = Comments.database_manager.execute_query_select(query)
        return r