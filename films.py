from db import models

class Films:
    @staticmethod
    def calculate_rate(film_id:int):
        #query : calculate film rate base on rate table
        pass
    @staticmethod
    def add_film(film:models.films_model):
        # query : add film
        pass
    
    @staticmethod
    def get_film(film_id)-> models.films_model:
        r = models.films_model(-1,"test",15,120,5)
        # query : get a film object
        return r
    @staticmethod
    def remove_film(film_id)->bool:
        # query
        
        return True
    @staticmethod
    def update_film(film:models.films_model):
        pass
    
class FilmRates:
    @staticmethod
    def add_rate(client_id:str,film_id:int,rate:int):
        # query : if already client_id give a rate for film_id, need to update rate
        # otherwise add
        Films.calculate_rate(film_id)
        return True
    @staticmethod
    def remove_rate(client_id:str,film_id:int):
        # query : remove rate from client_id for film_id
        Films.calculate_rate(film_id)
        return True
    
class Comments:
    @staticmethod
    def add_comment(comment:models.comments_model):
        #query : add comment
        return True
    
    @staticmethod
    def remove_comment(comment_id):
        # query
        return True
    
    @staticmethod
    def update_comment(comment:models.comments_model):
        # query
        return True