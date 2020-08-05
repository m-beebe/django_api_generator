import os
import inspect
from inspect import Parameter
import shutil


class APIGenerator:
    def __init__(self, instance):
        """
        Build an API from an existing class instantiation.
        Creates a Django Project with the Rest Framework based on the instantiated class you provide it.
        Note that it is best to type your method parameters for best results!
        Example:
            import APIGenerator
            APIGenerator(ClassName())
        """
        self.instance = instance
        self.class_name = type(self.instance).__name__
        self.method_list = self.get_methods()
        self.signatures = self.get_method_signatures()
        self.run_generator()

    def run_generator(self):
        """
        Run the full suite of methods
        :return: None
        """
        self.start_django_project()
        self.augment_settings()
        self.create_views_dot_py()
        self.augment_urls()
        self.package_required_files()

    def start_django_project(self):
        """
        Create an initial django project to be augmented.
        :return: None
        """
        dirs = [x[0] for x in os.walk('../..')]
        if f".\\{self.class_name}" not in dirs:
            os.system(f"django-admin startproject {self.class_name}")

    def get_methods(self):
        """
        Retrieve the public methods in the class for use in get_method_signatures
        :return: list: method names
        """
        k = self.instance
        attrs = list(vars(k).keys())
        return [m for m in dir(k)
                if not m.startswith('_') and m not in attrs]

    def get_method_signatures(self):
        """
        Retrieve the method signatures from the called instance
        :return: dict() of Parameters objects
        """
        params = {}
        for meth in self.method_list:
            params[meth] = inspect.signature(getattr(self.instance, meth)).parameters
        return params

    def package_required_files(self):
        """
        Copy the calling class and place into /BackendClasses folder of the django project
        :return: None
        """
        be_classes = f"{self.class_name}/{self.class_name}/BackendClasses"
        if not os.path.exists(be_classes):
            os.makedirs(be_classes)
        t = type(self.instance)
        shutil.copy(
            src=inspect.getfile(t),
            dst=f"{be_classes}/{self.class_name.lower()}.py")

    def augment_settings(self):
        """
        Augment settings.py created when running django-admin startproject.
        Inserts additions to INSTALLED_APPS and MIDDLEWARE that are necessary for rest_framework
        :return: None
        """

        installed_apps_additions = ['rest_framework', 'corsheaders']
        middleware_addition = 'corsheaders.middleware.CorsMiddleware'

        with open(f"{self.class_name}/{self.class_name}/settings.py", "r+") as rewrite:
            a = rewrite.read()
            if "# ADDED FROM API GENERATOR" not in a:
                rewrite.write(f"\n\n# ADDED FROM API GENERATOR\n"
                              f"# it's fine to move it to the correct spot\n"
                              f"INSTALLED_APPS += {installed_apps_additions}\n"
                              f"MIDDLEWARE.insert(1, '{middleware_addition}')")

    def create_views_dot_py(self):
        """
        Creates the views.py file in the django app based on the methods provided in the class.
        Note: the more explicit your methods are, the better the generator is at determining
        how to handle parameter inputs. Seek to type your method parameters!
        :return: None
        """
        with open(f"{self.class_name}/{self.class_name}/views.py", "w") as testopen:
            pass
        with open(f"{self.class_name}/{self.class_name}/views.py", "r+") as viewwriter:
            checker = viewwriter.read()
            if "from rest_framework" not in checker:
                stringBuilder = ("from rest_framework.decorators import api_view, throttle_classes\n"
                                 "from rest_framework.response import Response\n"
                                 "from rest_framework.throttling import UserRateThrottle\n"
                                 "from rest_framework.exceptions import APIException\n")
                stringBuilder += f"from .BackendClasses.{self.class_name.lower()} import {self.class_name}\n\n\n"
                stringBuilder += "class CustomThrottle(UserRateThrottle):\n    rate = '100000/day'\n\n\n"
                stringBuilder += f"INSTANCE = {self.class_name}()\n"
                viewwriter.write(stringBuilder)

            for meth, attrs in self.signatures.items():
                if f"def {meth}(request):" not in checker:
                    stringBuilder = "\n\n@api_view(['GET'])\n"
                    stringBuilder += "@throttle_classes([CustomThrottle])\n"
                    stringBuilder += f"def {meth}(request):\n"
                    methodCallParams = []
                    for attr, par in dict(attrs).items():
                        name = par.name
                        default = f" or {par.default}" if par.default != Parameter.empty else ""
                        annotation = par.annotation
                        stringBuilder += f"    {name} = request.GET.get('{name}'){default}\n"
                        if annotation != Parameter.empty:
                            stringBuilder += self._convert_incoming_param(annotation, name)
                        methodCallParams.append(f"{name}={name}")
                    stringBuilder += f"    methodcall = INSTANCE.{meth}({', '.join(methodCallParams)})\n"
                    stringBuilder += f"    return Response(methodcall)\n"
                    viewwriter.write(stringBuilder)

    @staticmethod
    def _convert_incoming_param(annotation, name):
        """
        Based on a method's explicit typing, add a helper variable which converts the input
        :param annotation: the type as declared
        :param name: the name of the parameter
        :return: str: helper variable
        """
        if annotation == list:
            return f"    {name} = {name}.split(',')\n"
        elif annotation == int:
            return f"    {name} = int({name})\n"
        elif annotation == float:
            return f"    {name} = float({name})\n"

    def augment_urls(self):
        """
        Adds paths for calling each API method
        :return: None
        """
        with open(f"{self.class_name}/{self.class_name}/urls.py", "r+") as urlwriter:
            checker = urlwriter.read()
            if "from . import views" not in checker:
                urlwriter.write("\n\nfrom . import views")
            urlpatterns = []
            for meth in self.method_list:
                if f"path('{meth}/'," not in checker:
                    urlpatterns.append(
                        f"    path('{meth}/', views.{meth}),\n"
                    )
            if urlpatterns:
                urlwriter.write("\n\nurlpatterns += [\n")
                for path in urlpatterns:
                    urlwriter.write(path)
                urlwriter.write("]\n")
