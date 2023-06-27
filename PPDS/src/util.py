import re
import jinja2

from src.parse_err import PPDSParseError

# modified from:
# https://stackoverflow.com/questions/241327/remove-c-and-c-comments-using-python
# this preserves line numbers by inserting newlines
def remove_comments(text):
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return " " + "\n"*s.count("\n")
        else:
            return s
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, replacer, text)

def header_from_template(template_str, argdict, declare_site):
    try:
        return template_str.render(**argdict,declare_site=declare_site)+"\n\n"
    except jinja2.TemplateError as e:
        print(e)
        print(e.__dict__)
        raise PPDSParseError(f"{type(e).__name__} with message: {e.message}")