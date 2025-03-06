from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import importlib
import subprocess
import sys
import json
import os
import platform
import requests
from typing import List, Dict, Any, Set, Optional
import pkg_resources

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for all routes


# Class to manage module data (based on original ModuleData class)
class ModuleData:
    """Class to manage the module database"""

    def __init__(self):
        # Dictionary with module information, categorized
        self.modules_by_category = {
            "Frontend": [
                {"name": "Tkinter", "description": "Builtin GUI Toolkit",
                 "doc_url": "https://docs.python.org/3/library/tkinter.html"},
                {"name": "PyQt5", "description": "Python-Bindings für Qt5",
                 "doc_url": "https://www.riverbankcomputing.com/static/Docs/PyQt5/"},
                # ... other modules
            ],
            "Backend": [
                {"name": "Django", "description": "High-Level Webframework",
                 "doc_url": "https://docs.djangoproject.com/en/stable/"},
                {"name": "Flask", "description": "Lightweight web framework",
                 "doc_url": "https://flask.palletsprojects.com/"},
                # ... other modules
            ],
            # ... other categories
        }

    def get_categories(self) -> List[str]:
        """Returns the list of all available categories"""
        return list(self.modules_by_category.keys())

    def get_modules_by_category(self, category: str) -> List[Dict[str, str]]:
        """Returns the modules of a specific category"""
        if category in self.modules_by_category:
            return self.modules_by_category[category]
        return []

    def get_module_names(self) -> List[str]:
        """Returns a list of all module names"""
        all_modules = []
        for category_modules in self.modules_by_category.values():
            all_modules.extend([module["name"] for module in category_modules])
        return all_modules

    def search_modules(self, query: str) -> List[Dict[str, Any]]:
        """
        Searches for modules that match the query

        Args:
            query: The search query

        Returns:
            List of found modules with additional category field
        """
        if not query:
            return []

        query = query.lower()
        results = []

        for category, modules in self.modules_by_category.items():
            for module in modules:
                # Search in name
                if query in module["name"].lower():
                    # Add category to module
                    module_with_category = module.copy()
                    module_with_category["category"] = category
                    results.append(module_with_category)
                # Search in description
                elif query in module["description"].lower():
                    module_with_category = module.copy()
                    module_with_category["category"] = category
                    results.append(module_with_category)

        return results

    def get_module_popularity(self, category: str) -> Dict[str, int]:
        """
        Creates a simulated popularity ranking for modules of a category
        (In a real application, this would be based on real data like PyPI downloads)
        """
        import random
        modules = self.get_modules_by_category(category)
        popularity = {}
        for i, module in enumerate(modules):
            # Creates simulated popularity values that roughly correspond to the order
            # (with some randomness for variation)
            popularity[module["name"]] = 10000 - (i * 800) + random.randint(-300, 300)
        return popularity


# Class to check module imports (based on original ModuleChecker class)
class ModuleChecker:
    """Class to check module imports"""

    @staticmethod
    def check_importable(module_names: List[str]) -> Dict[str, bool]:
        """
        Checks if the specified modules can be imported.

        Args:
            module_names: List of module names to check

        Returns:
            Dictionary with module names as keys and
            Boolean values indicating whether the import was successful
        """
        results = {}
        for module_name in module_names:
            try:
                # Normalize the module name for import
                import_name = module_name.lower().replace('-', '_')
                # Try to import the module
                importlib.import_module(import_name)
                results[module_name] = True
            except (ImportError, ModuleNotFoundError):
                results[module_name] = False
        return results

    @staticmethod
    def get_module_version(module_name: str) -> str:
        """
        Attempts to determine the version of a module

        Args:
            module_name: Name of the module

        Returns:
            Version number as string or "N/A" if not available
        """
        try:
            # Normalize the module name for import
            import_name = module_name.lower().replace('-', '_')
            # Try to import the module
            module = importlib.import_module(import_name)

            # Try to find various attributes for the version
            if hasattr(module, "__version__"):
                return module.__version__
            if hasattr(module, "VERSION"):
                return str(module.VERSION)
            if hasattr(module, "version"):
                return str(module.version)

            # If no direct attribute is found, try pkg_resources
            try:
                return pkg_resources.get_distribution(module_name).version
            except (pkg_resources.DistributionNotFound, AttributeError):
                pass

            return "N/A"
        except (ImportError, ModuleNotFoundError):
            return "N/A"

    @staticmethod
    def get_module_install_command(module_name: str, platform_name: str = None) -> str:
        """
        Returns the command to install a module, based on the platform

        Args:
            module_name: Name of the module
            platform_name: Name of the platform (Windows, Linux, macOS)

        Returns:
            Command to install the module
        """
        if platform_name is None:
            platform_name = platform.system()

        if platform_name == "Windows":
            return f"pip install {module_name}"
        elif platform_name == "Linux":
            return f"python3 -m pip install {module_name}"
        elif platform_name == "Darwin":  # macOS
            return f"python3 -m pip install {module_name}"
        else:
            return f"pip install {module_name}"


# Initialize the module data
module_data = ModuleData()


# API Routes
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/api/categories')
def get_categories():
    """Returns all module categories"""
    return jsonify(module_data.get_categories())


@app.route('/api/modules/<category>')
def get_modules(category):
    """Returns modules for a specific category"""
    modules = module_data.get_modules_by_category(category)
    return jsonify(modules)


@app.route('/api/search')
def search_modules():
    """Searches for modules"""
    query = request.args.get('q', '')
    results = module_data.search_modules(query)
    return jsonify(results)


@app.route('/api/check_imports', methods=['POST'])
def check_imports():
    """Checks if modules can be imported"""
    data = request.json
    module_names = data.get('modules', [])

    if not module_names:
        return jsonify({'error': 'No modules provided'}), 400

    results = ModuleChecker.check_importable(module_names)
    return jsonify(results)


@app.route('/api/module_version/<module_name>')
def get_module_version(module_name):
    """Gets the version of a module"""
    version = ModuleChecker.get_module_version(module_name)
    return jsonify({'module': module_name, 'version': version})


@app.route('/api/install_command/<module_name>')
def get_install_command(module_name):
    """Gets the installation command for a module"""
    platform_name = request.args.get('platform', platform.system())
    command = ModuleChecker.get_module_install_command(module_name, platform_name)
    return jsonify({'module': module_name, 'command': command})


@app.route('/api/popularity/<category>')
def get_popularity(category):
    """Gets the popularity data for modules in a category"""
    popularity = module_data.get_module_popularity(category)
    return jsonify(popularity)


@app.route('/api/pypi_info/<module_name>')
def get_pypi_info(module_name):
    """Gets information about a module from PyPI"""
    try:
        # Make a request to the PyPI JSON API
        response = requests.get(f"https://pypi.org/pypi/{module_name}/json", timeout=5)

        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': f'Error loading information: Status code {response.status_code}'}), 404
    except Exception as e:
        return jsonify({'error': f'Error loading information: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)