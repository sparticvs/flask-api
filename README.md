# Flask-API Extension

## Why make this?
While Flask is a great toolkit and library, it doesn't provide the proper
methods to support Web Application APIs. The lifecycle of a single Web App
endpoint varies between versions of the application. In addition, web
development best practices tell us to design the site as an API and and let
client-side scripting handle the page formatting. These best practices also
tell us that developing this way makes it easier for others to consume our
data in an easy manner.

## The end goal
This is simple. Build an extension to Flask that allows for the easy creation
of an API. Don't step on Flask's bootstraps in the process, and keep the
simplicity of development to the bar set by Flask.

## How to use
I like to keep Flask-API very simple, so here is how you implement it in
the WSGI file:

    from flask import Flask
    from flask.ext.api import API

    app = Flask()
    api = API(app)

You can also enforce a specific version of your API with a configuration
variable like so

    # Force version 2 of the API when building URLs
    app.CONFIG['API_EFFECTIVE_VERSION'] = 2

    # Ignore deprecation errors
    app.CONFIG['API_IGNORE_DEPRECATED'] = True

In the code files where you wish to register API endpoints

    @app.route("/", ['GET'])
    def index():
        return "Hello World"

    # This URL endpoint looks like this
    #   /api/0/worlds
    #   /api/1/worlds
    @api.route("/worlds", 0, ['GET'])
    def get_worlds():
        return "list of worlds"

    # This URL endpoint looks like this
    #   /api/1/worlds
    @api.route("/worlds", 1, ['PUT'])
    def add_worlds():
        # Do things with worlds submitted
        return "Ok"

This design allows us to specify API versions when endpoints were first
introduced. Doing so this way allows us to update the application and not break
when others start to use our API. In addition to supporting any API, we need to
be able to handle deprecation of endpoints and can do it like so:

    # Deprecated in this version
    @api.route("/stuff", 0, ['GET'])
    @api.deprecate
    def print_stuff():
        print "Gone"

    # Deprecated starting in version 3
    @api.route("/things", 1, ['GET'])
    @api.deprecate(3)
    def print_things():
        print "Gone"

If no arguments are supplied, the current version is assumed as deprecated.
This is really useless and returns a HTTP 4xx Deprecated. If the version
argument is supplied, then a HTTP 4xx Deprecation Pending is returned to the
API client and the header entity "X-API-Version" will be set to the version
when the endpoint is expected to be deprecated.  The use of the deprecate
decorator will keep you from making an "api\_url\_for()" call by throwing a
DeprecationError exception when attempting to build the URLs for the page.

### Jinja2 Usage
Flask supplies the ability to use "url\_for()" in Jinja2 templates. In order to
keep with that tradition, we supplied a "api\_url\_for()". Due to supporting
multiple API versions wiht our routing, we need a special url\_for function.

Other usage options:

    api_url_for('print_stuff') ## Usage throws DeprecationError
    api_url_for('get_worlds') ## Returns API URL for configuration set version
    api_url_for('get_worlds', 0) ## Returns version 0 API url (don't use)
    api_url_for('add_worlds', 0) ## Usage throws VersionNotImplementedError

### Exceptions
*DeprecationError:* Endpoint deprecated and shouldn't be used anymore

*VersionNotImplementedError:* Endpoint isn't supported in this API version

### Side notes
While it may seem pointless to use certain features for this system, there are
certain cases where the implementation of these features is ideal. Deprecate
is very useful in areas where you are distributing a Library out to others and
want to let them know that what is deprecated.

## License
This software has no license nor warranty. Do whatever you want, I don't care.
If you do manage to meet me some day and want to show your appreciation for
my work then I like tequila. If you don't meet me, then consider donating to
the Electronic Frontier Foundation (EFF) and support their cause for privacy
on the Internet.

## Releases & Liability
Opinions expressed here-in are the author(s) own opinions and do not represent
opinions or views of the author(s) employer(s).

The author(s) will not be held liable for anything you decide to do with this
software.
