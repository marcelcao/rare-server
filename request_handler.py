from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs
from views import (
    create_user,
    login_user,
    get_single_user,
    get_all_users,
    update_user,
    delete_user
    )
from views import (
    create_post,
    update_post,
    delete_post,
    get_all_posts,
    get_posts_by_user_id,
    get_single_post,
)
from views import get_all_tags, get_single_tag, create_tag, delete_tag, update_tag
from views import get_all_post_tags, get_single_post_tag, create_post_tag, delete_post_tag, update_post_tag
from views import (
    get_all_reactions,
    get_single_reaction,
    get_all__post_reactions,
    get_single_post_reaction,
    delete_reaction,
    delete_post_reaction,
    create_reaction,
    create_post_reaction,
    update_reaction,
    update_post_reaction
)
from views.comment_requests import get_all_comments, get_single_comment, create_comment, delete_comment, update_comment

class HandleRequests(BaseHTTPRequestHandler):
    """Handles the requests to this server"""

    def parse_url(self):
        """Parse the url into the resource and id"""
        path_params = self.path.split("/")
        resource = path_params[1]
        if "?" in resource:
            param = resource.split("?")[1]
            resource = resource.split("?")[0]
            pair = param.split("=")
            key = pair[0]
            value = pair[1]
            return (resource, key, value)
        else:
            id = None
            try:
                id = int(path_params[2])
            except (IndexError, ValueError):
                pass
            return (resource, id)

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the OPTIONS headers"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")
        self.send_header(
            "Access-Control-Allow-Headers", "X-Requested-With, Content-Type, Accept"
        )
        self.end_headers()

    def do_GET(self):

        response = {}
        parsed = self.parse_url()
        if "?" not in self.path:
            (resource, id) = parsed
            
            if resource == 'users':
                if id is not None:
                    response = get_single_user(id)
                    self._set_headers(200)
                else:
                    response = get_all_users()
                    self._set_headers(200)    
            
            if resource == 'posts':
                if id is not None:
                    response = get_single_post(id)
                    self._set_headers(200)
                else:
                    response = get_all_posts()
                    self._set_headers(200)
            if resource == "tags":
                if id is not None:
                    response = get_single_tag(id)
                    self._set_headers(200)
                else:
                    response = get_all_tags()
                    self._set_headers(200)
            
            if resource == 'posttags':
                if id is not None:
                    response = get_single_post_tag(id)
                    self._set_headers(200)
                else:
                    response = get_all_post_tags()
                    self._set_headers(200)
                    
            if resource == "reactions":
                if id is not None:
                    response = get_single_reaction(id)
                    self._set_headers(200)

                else:
                    response = get_all_reactions()
                    self._set_headers(200)

            if resource == "postreactions":
                if id is not None:
                    response = get_single_post_reaction(id)
                    self._set_headers(200)

                else:
                    response = get_all__post_reactions()
                    self._set_headers(200)
                    
            if resource == "comments":
                if id is not None:
                    response = get_single_comment(id)
                    self._set_headers(200)
                else:
                    response = get_all_comments()
                    self._set_headers(200)
        else:
            (resource, key, value) = parsed
            if resource == "posts":
                if key == "user_id":
                    response = get_posts_by_user_id(value)
                    self._set_headers(200)

        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """Make a post request to the server"""
        self._set_headers(201)
        content_len = int(self.headers.get("content-length", 0))
        post_body = json.loads(self.rfile.read(content_len))
        response = ""
        resource, _ = self.parse_url()

        if resource == "login":
            response = login_user(post_body)
        if resource == "register":
            response = create_user(post_body)
        if resource == 'comments':
            response == create_comment(post_body)
        if resource == "posts":
            response = create_post(post_body)
        if resource == "tags":
            response = create_tag(post_body)
        if resource == 'posttags':
            response = create_post_tag(post_body)
        if resource == 'reactions':
            response = create_reaction(post_body)
        if resource == 'postreactions':
            response = create_post_reaction(post_body)

        self.wfile.write(json.dumps(response).encode())

    def do_PUT(self):
        """Handles PUT requests to the server"""
        content_len = int(self.headers.get("content-length", 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        (resource, id) = self.parse_url()
        success = False
        if resource == "users":
            success = update_user(id,post_body)
        if resource == "posts":
            success = update_post(id, post_body)
        if resource == "tags":
            success = update_tag(id, post_body)     
        if resource == 'posttags':
            success = update_post_tag(id, post_body)
        if resource == "reactions":
            success = update_reaction(id, post_body)
        if resource == "postreactions":
            success = update_post_reaction(id, post_body)
        if resource == "comments":
            success = update_comment(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

    def do_DELETE(self):
        """Handle DELETE Requests"""
        (resource, id) = self.parse_url()

        if resource == "users":
            delete_user(id)
            self._set_headers(204)
        if resource == "posts":
            delete_post(id)
            self._set_headers(204)
        if resource == "tags":
            delete_tag(id)
            self._set_headers(204)
        if resource == "posttags":
            delete_post_tag(id)
            self._set_headers(204)
        if resource == "reactions":
            delete_reaction(id)
            self._set_headers(204)
        if resource == "postreactions":
            delete_post_reaction(id)
            self._set_headers(204)
        if resource == "comments":
            delete_comment(id)
            self._set_headers(204)
        self.wfile.write("".encode())


def main():
    """Starts the server on port 8088 using the HandleRequests class"""
    host = ""
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
