import threading
import time

class FilmCachingManager:
    def __init__(self):
        self.lock = threading.Lock()
        self.cache = {}

    def get_film_info(self, film_id):
        with self.lock:
            if film_id in self.cache:
                print(f"Film info for film {film_id} retrieved from cache.")
                return self.cache[film_id]

        time.sleep(2)
        film_info = f"Details for film {film_id}"
        
        with self.lock:
            self.cache[film_id] = film_info

        return film_info

def worker(film_id):
    film_info = caching_manager.get_film_info(film_id)
    print(f"Worker {threading.current_thread().name} retrieved: {film_info}")

if __name__ == "__main__":
    caching_manager = FilmCachingManager()

    threads = []
    for i in range(5):
        thread = threading.Thread(target=worker, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("All threads have finished.")
