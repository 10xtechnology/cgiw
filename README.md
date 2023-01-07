# CGI Wrapper

This is a lightweight framework for writing CGI scripts in python. It handles the parsing of inputs and composition of outputs so the developer can focus on the logic. The composition of outputs is made to be extensible, but this package comes with a few basic built in helper functions such as composing a json response, or a redirect. (Note that redirects will not work for the built in python cgi server as status codes have not been implemented. Other CGI servers should work though.)
