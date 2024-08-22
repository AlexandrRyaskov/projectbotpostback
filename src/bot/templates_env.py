from jinja2 import Environment, FileSystemLoader

jinja_env = Environment(loader=FileSystemLoader(searchpath="./src/bot/templates"))
