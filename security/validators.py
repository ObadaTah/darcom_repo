
import re

def validate_password(password):
    SpecialSymbol =['$', '@', '#', '%'] 
    val = True
      
    if len(password) < 8: 
       val = 'length should be at least 8'
        
          
    if len(password) > 20: 
        val = 'length should be not be greater than 8' 
          
    if not any(char.isdigit() for char in password): 
        val ='Password should have at least one numeral'
          
    if not any(char.isupper() for char in password): 
        val = 'Password should have at least one uppercase letter'
          
    if not any(char.islower() for char in password): 
        val = 'Password should have at least one lowercase letter' 
        
          
    if not any(char in SpecialSymbol for char in password): 
       val = 'Password should have at least one of the symbols $@#'
        
    return val

 
def validate_email(email):
    if(re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email)):
        return True
 
    else:
        return False
 