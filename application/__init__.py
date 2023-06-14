# Imports from Flask
from flask import Flask, send_from_directory, request, jsonify, make_response, g

# Function to create the app


def create_app():
    # Initialize the Flask app
    app = Flask(__name__)

    # initialize an empty dictionary for the resume
    app.config['resume'] = {}

    # Define the route for the index page
    @app.route('/')
    # when this route is called, the function will be executed
    def hello_world():
        # basic route
        return 'Hello, World!'

    # Function to validate the resume data
    def validate_resume(new_resume):
        # define the required fields
        keys = ['name', 'tagline', 'email', 'phone', 'address',
                'socialLinks', 'objective', 'education', 'experience', 'skills']
        # check if the resume has all the required fields
        for key in keys:
            if key not in new_resume:
                return False
        return True

# Defining routes for handling the resume data


    @app.route('/resume', methods=['GET', 'POST', 'PUT', 'DELETE'])
    # Function to handle the resume data
    def handle_resume():
        # switch case to handle the request method
        match request.method:
            # if the request method is GET
            case 'GET':
                # check if the resume exists
                if app.config['resume']:
                    # return the resume
                    return jsonify(app.config['resume']), 200
                else:
                    # return an error message
                    return make_response(jsonify({'error': 'Resume not found'}), 404)

            case 'POST':
                # get the resume data from the request
                new_resume = request.get_json()
                # validate the resume data
                if not validate_resume(new_resume):
                    # return an error message
                    return make_response(jsonify({'error': 'Invalid resume'}), 400)
                # save the resume if it is valid and does not exist
                app.config['resume'] = new_resume
                # return a success message
                return make_response(jsonify({'message': 'Resume created'}), 201)

            case 'PUT':
                # if no resume exists return an error message
                if not app.config['resume']:
                    return make_response(jsonify({'error': 'Resume not found'}), 404)
                # get the resume data from the request
                new_resume = request.get_json()
                # validate the resume data
                if not validate_resume(new_resume):
                    # if resume is invalid return an error message
                    return make_response(jsonify({'error': 'Invalid resume'}), 400)
                # update the resume
                app.config['resume'] = new_resume
                # return a success message
                return jsonify(app.config['resume']), 200

            case 'DELETE':
                # if no resume exists return an error message
                if not app.config['resume']:
                    return make_response(jsonify({'error': 'Resume not found'}), 404)
                # delete the resume
                app.config['resume'] = {}
                # return a success message
                return make_response(jsonify({'message': 'Resume deleted'}), 204)

            case _:
                # if the request method is not supported return an error message
                return make_response(jsonify({'error': 'Method not allowed'}), 405)

    # return the app
    return app
