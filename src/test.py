"""
author: Charles 'sparticvs' Timko, @sparticvs
"""
from functools import wraps
from flask import request 

def api_url_for(endpoint, version=None, **options):
    """Return URL for endpoint in a specific API version"""

class API:
    """Wraps Flask App and does special routing"""

    def __init__(self, flask_app):
        self.app = flask_app

    def add_url_rule(self, f, **options):
        pass

    def route(self, rule, version, **options):
        """ API Routing Decorator

            We like flask, but we will solve the routing

                @api.route("/tables/", [0])
                def get_tables():
                    # ... code ...

            :params:
                rule:   the URL rule as a string (will have API prefixed)
             version:   version number endpoint is introduced
            endpoint:   the endpoint for the registered URL. Assumes name
                        of decorated function
             options:   the options to be forwarded to the underlying
                        Werkzeug
        """
        def decorator(f):
            # TODO rely on self.config['API_VERSION']
            endpoint = options.pop('endpoint', None)
            if rule[0] != "/":
                rule = "/" + rule
            versions = []
            if isinstance(version, int):
                versions.append(version)
            rule = "/api/%d%s" % rule
            return self.add_url_rule(rule, endpoint, f, **options)
        return decorator

    def deprecated(self, version=None):
        """ Decorator to deprecate an endpoint

                @api.route("/tables/", [0,2])
                @api.deprecated
                def get_tables():
                    # ... code ...
        """
        def decorator(f):
            # Should return the appropriate error code to
            # let the user know of deprecation.
            pass
        return decorator
