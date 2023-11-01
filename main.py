# import the flask package for making rest apis.
from flask import Flask
from flask import *
from flask import request 
from logger import *
import uuid

# create an instance of a Flask object.
app = Flask(__name__)
movies = []

@app.route("/", methods=["GET"])
def hello_world():
    '''
    This is our base route. When visited, we get the text "Hello, world!"
    '''
    return "Hello, world!"

@app.route("/api/movies", methods=["GET", "POST"])
def handle_movies():
    if request.method == "GET":
        response_body = movies

        titles = request.args.getlist("title")

        # only get the movies that have the same title as the query parameter.
        if titles != []:
            response_body = [movie for movie in movies if movie["title"] in titles]

        # use logger class to log query to log file
        log(request.method + " " + request.url, log_file)

        return jsonify(response_body)
    
    elif request.method == "POST":
        request_body = request.get_json()
        
        #checks if request body is empty or title is missing
        if request_body == None or request_body["title"] == None:
            return Response("Bad request", 400)
        #checks if movie already exists in the list
        for movie in movies:
            if movie["title"] == request_body["title"]:
                return Response("Already Exists", 409)
        #creates dictionary object with movie info from request_body
        new_movie= {"uuid": str(uuid.uuid4()), "title": request_body["title"], "review": []}
        movies.append(new_movie)
        return Response("Created", 201)
        

@app.route("/api/movies/<mid>", methods=["GET", "DELETE"])
def handle_movie(mid: str) -> Response:
    if request.method == "GET":
        count = 0
        if movies == []:
            return Response("Not Found", 404)
        for movie in movies:
            if mid in movie.values():
                count += 1
        if count == 0:
            return Response("Not Found", 404)
        #finds movie with uuid equal to mid and returns it
        for movie in movies:
            if movie["uuid"] == mid:
                return jsonify(movie)
    elif request.method == "DELETE":
        count = 0
        if movies == []:
            return Response("Not Found", 404)
        for movie in movies:
            if mid in movie.values():
                count += 1
        if count == 0:
            return Response("Not Found", 404)
        for movie in movies:
            if movie["uuid"] == mid:
                movies.remove(movie)
                return Response("No content", 204)
        
@app.route("/api/movies/<mid>/reviews", methods=["GET", "POST"])
def handle_reviews(mid: str) -> Response:
    if request.method == "GET":
        count = 0
        if movies == []:
            return Response("Not Found", 404)
        for movie in movies:
            if mid in movie.values():
                count += 1
        if count == 0:
            return Response("Not Found", 404)
        else:
            reviews = []
            for movie in movies:
                if movie["uuid"] == mid:
                    reviews = movie["reviews"]
            return jsonify(reviews)
    elif request.method == "POST":
        request_body = request.get_json()
        
        count = 0
        if movies == []:
            return Response("Not Found", 404)
        for movie in movies:
            if mid in movie.values():
                count += 1
        if count == 0:
            return Response("Not Found", 404)

        #check if request body is invalid
        if request_body == None or request_body == {}:
            return Response("Bad request", 400)
        if "username" not in request_body or "score" not in request_body or "review" not in request_body:
            return Response("Bad request", 400)
        if request_body["username"] == None or request_body["score"] == None or request_body["review"] == None:
            return Response("Bad request", 400)
        elif type(request_body["username"]) != str or type(request_body["score"]) != float or type(request_body["review"]) != str:
            return Response("Bad request", 400)
        elif request_body["score"] < 0.0 or request_body["score"] > 10.0:
            return Response("Bad request", 400)
        review = {
            "uuid": uuid.uuid4(),
            "username": request.get_json()["username"],
            "score": request.get_json()["score"],
            "review": request.get_json()["review"]
        }
        for movie in movies:
            if movie["uuid"] == mid:
                movie["reviews"].append(review)
                return Response("Created", 201)


@app.route("/api/movies/<mid>/reviews/<rid>", methods=["GET", "DELETE"])
def handle_review(mid: str, rid: str) -> Response:
    if request.method == "GET":
        count = 0
        r_count = 0
        if movies == []:
            return Response("Not Found", 404)
        for movie in movies:
            if mid in movie.values():
                count += 1
                for review in movie["reviews"]:
                    if rid in review.values():
                        r_count +=1
        if count == 0 or r_count == 0:
            return Response("Not Found", 404)
        else:
            for movie in movies:
                for review in movie["reviews"]:
                    if rid in review.values():
                        return jsonify(review)
        
    elif request.method == "DELETE":
        count = 0
        r_count = 0
        if movies == []:
            return Response("Not Found", 404)
        for movie in movies:
            if mid == movie["uuid"]:
                count += 1
                for review in movie["reviews"]:
                    if rid == review["uuid"]:
                        r_count += 1
                        movie["reviews"].remove(review)
                        break
    if count == 0 or r_count == 0:
        return Response("Not Found", 404)
    if r_count > 0:
        return Response("No Content", 204)
    else:
        return Response("Review Not Found", 404)

# run our application
if __name__ == '__main__':
    app.run()



