from db import models
from films import Films, FilmsPoints, Comments
import queryset , films 
from users_module import personalized_exceptions


# Test add_film
<<<<<<< Updated upstream
new_film = models.film_model(name="  Test Film  ", age_rating="PG", duration=120)
=======
new_film = models.film_model(name="Test Film", age_rating="PG", duration=120)
>>>>>>> Stashed changes
Films.add_film(new_film)
print("Film added successfully.")

# Test get_film
try:
    retrieved_film = Films.get_film(film_id=1)
    print(f"Retrieved Film: {retrieved_film}")
except personalized_exceptions.FilmNotFount:
    print("Film not found!")

# Test remove_film
try:
    Films.remove_film(film_id=1)
    print("Film removed successfully.")
except personalized_exceptions.RemoveFilmNotPossible:
    print("Unable to remove the film.")

# Test calculate_point
Films.calculate_point(film_id=2)
print("Point calculated successfully.")


# Test update_film
updated_film = models.film_model(id=2, name="Updated Film", age_rating="R", duration=150)
Films.update_film(updated_film)
print("Film updated successfully.")


# Test add_point
try:
    FilmsPoints.add_point(user_id="user123", film_id=2, point=4)
    print("Point added successfully.")
except personalized_exceptions.FilmNotFount:
    print("Film not found!")


# Test remove_point
FilmsPoints.remove_point(client_id="user123", film_id=2)
print("Point removed successfully.")


# Test add_point
try:
    FilmsPoints.add_point(user_id="user123", film_id=2, point=4)
    print("Point added successfully.")
except personalized_exceptions.FilmNotFount:
    print("Film not found!")


# Test remove_point
FilmsPoints.remove_point(client_id="user123", film_id=2)
print("Point removed successfully.")

# Test add_comment
new_comment = models.comment_model(film_id=2, user_id="user123", text="Great movie!")
Comments.add_comment(new_comment)
print("Comment added successfully.")

# Test remove_comment
try:
    Comments.remove_comment(comment_id=1)
    print("Comment removed successfully.")
except personalized_exceptions.CommentNotFound:
    print("Comment not found!")

# Test update_comment
updated_comment = models.comment_model(id=2, film_id=2, user_id="user123", text="Updated comment!")
Comments.update_comment(updated_comment)
print("Comment updated successfully.")

# Test get_comments_of_film
film_comments = Comments.get_comments_of_film(film_id=2)
print("Comments for Film:")
for comment in film_comments:
    print(f"- {comment}")



