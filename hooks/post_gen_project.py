from venv import EnvBuilder

if "{{ cookiecutter.create_virtualenv }}" == "y":
    EnvBuilder().create("{{ cookiecutter.app_name }}")

