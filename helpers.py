from functools import wraps
from flask import g, request, redirect, url_for, session
import re

# Make a regular expression for validating an Email 
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

def check(email):    
    # pass the regular expression and the string in search() method 
    if (re.search(regex,email)):  
        return True     
    else:  
        return False 



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("person_id") is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function