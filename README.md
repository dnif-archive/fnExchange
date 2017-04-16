# Overview
fnExchange is a scalable, open source API layer (also called an API "router")
that provides a consistent proxy web interface for invoking various web APIs
without the caller having to write separate, special-purpose code for each of
them.

This works as follows:
- The caller invokes the fnExchange service in the prescribed standard fnExchange API data format
- The fnExchange API server receives this request, and "routes" it to the appropriate plugin (based on request body parameters) with the request data
- The plugin takes in the data, does its magic, and returns data in the prescribed standard format
- The fnExchange handler returns this response with appropriate metadata

fnExchange is packaged as a command line interface executable `fnexchange` which
starts the web service. The CLI also supports a mode to run the service as a daemon.

# Installation
## fnExchange
```
$ pip install fnexchange
```

## Plugins
Publicly fnExchange plugins available on PyPi can simply be installed using pip
```
$ pip install fnexchange-<pluginname>
```

Alternatively, plugins created using the plugin sample project format but
not available on PyPi can be installed using:

```
$ cd /path/to/plugin/source
$ pip install .
```

The only thing required for the plugins to function is that they should be
available on the `$PYTHONPATH`. This enables using standalone plugins that
are not available via PyPi and don't have a setup.py

# Configuration
A configuration file needs to be supplied to the fnExchange server requires
a configuration. A sample configuration for the conf file is provided in the
project.

The configuration file can be validated using the fnexchange CLI by running
```
$ fnexchange configtest --conf=/path/to/conf.yml
```


# Running the API service
The service can simply be run using the following command.
```
$ fnexchange runserver --conf=conf.yml [--port=<port number>] [--background]
```
The conf argument is required. The port number can be provided either in the
conf.yml or via the command line option. If the port is provided in the conf
file, providing it via the CLI is not required. In the case that port numbers
are provided both via CLI and the conf file, the one provided on the CLI is
used.

An optional `--background` flag is also available, using it runs the server
as a background process.
