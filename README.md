# octranspolib

octranspolib is a Python module for accessing the OC Transpo API through a client interface. 
Heavily influenced by [hozn/stravalib](https://github.com/hozn/stravalib)

## Autenticated client object

You can create a client object by passing you application ID and API key to the constructor. Once you have a client you can make API calls.

    from octranspolib import Client

    ...

	client = Client(app_id='1234', api_key='123456')

## Summary for stop

You can get a the routes summary for a stop using the __get_route_summary_for_stop__ method.

    from octranspolib import Client

    ...

	client = Client(app_id='1234', api_key='123456')
	routes_summary = client.get_next_trips_for_stop_all_routes('8042')
