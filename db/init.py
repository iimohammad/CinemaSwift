import inspect
import models
class MyClass:
    def __init__(self, name: str, age: int, city: str):
        self.name = name
        self.age = age
        self.city = city
        self.dict = {
            'str': 'VARCHAR(255) NOT NULL',
            'int': 'INTEGER',
            'datetime': 'DATE'
        }

# Create a temporary instance of MyClass for type lookup


# Get the signature of the __init__ method
    def create_columns(self,model_name):
        init_signature = inspect.signature(model_name.__init__)
        init_params = {param.name: param.annotation for param in init_signature.parameters.values() if param.name != 'self'}
        person_model_columns = [(name, self.dict.get(param_type.__name__, 'UNKNOWN')) for name, param_type in init_params.items()]
        return person_model_columns

temp_instance = MyClass('', 0, '')
print(temp_instance.create_columns(model_name=models.person_model))