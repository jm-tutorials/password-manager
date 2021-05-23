

class Password:

    def __init__(self, params):
        self.website = params.get('website')
        self.name = params.get('name')
        self.username = params.get('username')
        self.password = params.get('password')
        self.notes = params.get('notes')

    def set_website(self,new_website):
        try:
            self.website = new_website
        except Exception as e:
            print(e)

    def set_username(self,new_username):
        try:
            self.username = new_username
        except Exception as e:
            print(e)   
    
    def set_password(self,new_password):
        try:
            self.password = new_password
        except Exception as e:
            print(e)   
      
    def set_notes(self,new_notes):
        try:
            self.notes = new_notes
        except Exception as e:
            print(e)
    
    