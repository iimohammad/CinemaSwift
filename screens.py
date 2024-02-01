from db import models
from enum import Enum

class SeatType(Enum):
    Free = "Free"
    Reserved = "Reserved"
class Screens:
    @staticmethod
    def create_screen(screen:models.screens_mode):
        # query
        return True
    
    @staticmethod
    def remove_screen(screen_id:int):
        # if there was't any sans for this screen then remove
        return True
    
    @staticmethod
    def update_screen(screen:models.screens_mode):
        # if number of sans is more than new screen_sansed, return false
        # update_screen
        return True

class Seats:
    @staticmethod
    def create_seat(seat:models.seats_showtimes_model):
        # add to seat table
        return True
    
    @staticmethod
    def update_seat(seat:models.seats_showtimes_model):
        # not possible to change the sans, only can change status
        # update
        return True
    @staticmethod
    def remove_seat(reat_id):
        # remove
        return True
    
    @staticmethod
    def get_seats_of_sans(sans_id:int):
        pass
    @staticmethod
    def get_free_seats_of_sans(sans_id:int):
        pass
class Sans:
    @staticmethod
    def create_sans(sans:models.sans_model):
        # create sans of a screen
        for i in range(sans.capacity):
            Seats.create_seat(models.seats_showtimes_model(-1,sans.id,SeatType.Free))
        return True
    
    
    @staticmethod
    def remove_sanse(sans:models.sans_model):
        # if all the seat are free we can remove sans
        return True
    
    
    @staticmethod
    def get_number_of_remain_sanses(screen_id:int):
        pass

    