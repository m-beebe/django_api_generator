# Django REST API Generator
Automatically generate an API built with Django Rest Framework based on a Python class.

\
Requirements:
- Django
- djangorestframework

\
Recommendations for use:
- For more complex classes, create an interface class on which you call the APIGenerator
- always pass an instantiated class to the APIGenerator
- for best results, type your method parameters! otherwise, account for strings in your methods

Example Use:
```
from api_generator import APIGenerator

class SampleClass:
    def adder(self, num1: int, num2: int):
        return num1 + num2

    def multiplier(self, num1: int, num2: int):
        return num1 * num2

    def add_list(self, num_list: list):
        num_list = [int(x) for x in num_list]
        added_up = 0
        for i in num_list:
            added_up += i
        return num_list


if __name__ == '__main__':
    APIGenerator(SampleClass())
```
This will generate a Django project with the Django Rest Framework based on the methods above.

Next, in the commandline:
```
py manage.py runserver
```
Navigate to http://127.0.0.1:8000/adder/?num1=12&num2=30

# TO-DO:
- automatically generate a front page with documentation of all methods callable from API
- account for more types in methods
- account for more complex classes than one file

