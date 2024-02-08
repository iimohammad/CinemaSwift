from db import models
from db.database_manager import DatabaseManager
from enum import Enum
from users_module import personalized_exceptions
from datetime import datetime
from screen_module import queryset


class SeatType(Enum):
    FREE = "FREE"
    RESERVED = "RESERVED"


class Screens:
    @staticmethod
    def create_screen(screen: models.screen_model):
        queryset.create_screen_query(screen.film_id, screen.number_of_screens)
        return True

    @staticmethod
    def remove_screen(screen_id: int):
        r = queryset.find_session_id_query(screen_id=screen_id)
        if len(r) > 0:
            raise personalized_exceptions.RemoveScreenNotPossible()

        queryset.remove_screen_query(screen_id)

        return True

    @staticmethod
    def update_screen(screen: models.screen_model):
        r = queryset.count_session_query(screen.id)

        if r[0][0] > screen.number_of_screens:
            raise personalized_exceptions.UpdateScreenNotPossible()

        queryset.update_screen_query(screen.film_id, screen.number_of_screens, screen.id)

        return True

    @staticmethod
    def get_screens_list():
        r = queryset.get_screen_list_query()
        return r

    @staticmethod
    def get_screens_list_for_a_film(film_id: int):
        r = queryset.get_screens_list_for_a_film_query(film_id)
        return r


class Session:
    database_manager = DatabaseManager()

    @staticmethod
    def create_session(session: models.session_model):
        defined_session = queryset.count_session_query(session.screen_id)

        if session.capacity < 1:
            raise personalized_exceptions.CreateSessionNotPossibleCapacity()

        defined_session = defined_session[0][0]
        total_allowed_sessions = queryset.number_sans_query(session.screen_id)

        total_allowed_sessions = total_allowed_sessions[0][0]

        if defined_session == total_allowed_sessions:
            raise personalized_exceptions.CreateSessionNotPossibleMaxNumber()

        time = session.start_time
        timestamp_str = f"{time.year}-{time.month:02d}-{time.day:02d} {time.hour:02d}:{time.minute:02d}"

        r = queryset.find_by_start_time_query(timestamp_str)

        if len(r) > 0:
            raise personalized_exceptions.CreateSessionNotPossible()

        queryset.insert_session_query(session.screen_id, timestamp_str, session.capacity, session.ticket_price)

        session_id = queryset.find_by_time_and_screen_id_query(timestamp_str, session.screen_id)

        session_id = session_id[0][0]
        Seats.create_seat(models.seat_model(-1, session_id, SeatType.FREE.value), session.capacity)

        return True

    @staticmethod
    def remove_session(session_id: int):
        total_seats = queryset.find_total_seats_query(session_id)
        free_seats = Seats.get_number_of_free_seats(session_id)

        if total_seats != free_seats:
            raise personalized_exceptions.RemoveSessionNotPossible()
        queryset.delete_session_query(session_id)
        return True

    @staticmethod
    def get_number_of_remain_sessions(screen_id: int):
        r = queryset.find_remain_session(screen_id)
        counted = 0
        for i in r:
            session_id = i[0]
            start_time = i[2]
            if start_time < datetime.now():
                continue
            if Seats.get_number_of_free_seats(session_id) == 0:
                continue
            counted += 1
        return counted


class Seats:
    database_manager = DatabaseManager()

    @staticmethod
    def create_seat(seat: models.seat_model, number: int):
        queryset.create_seat_query(seat.session_id, seat.status, number)

        return True

    @staticmethod
    def update_seat(seat_id: int, status: SeatType):
        queryset.update_seat_query(seat_id, status)
        return True

    @staticmethod
    def get_seats_of_a_session(session_id: int):
        r = queryset.get_seats_of_a_session_query(session_id)

        return r

    @staticmethod
    def get_number_of_free_seats(session_id: int):
        r = queryset.get_number_of_free_seats_query(session_id, SeatType.FREE.value)
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
