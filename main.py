from website import create_app


app = create_app()  #create an instance of our flask app.This instance represents our flask app. 

#conditional statement to check if the program runs directy and not as a module. 
if __name__ == '__main__':
    app.run(debug=True)  #reloads the server when we make changes so that we dont have to restart every time


