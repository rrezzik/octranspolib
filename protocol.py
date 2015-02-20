import logging
import urlparse
import requests
import functools
import json
import xml
from octranspolib.parsertest import Xml2Json
from StringIO import StringIO

class Api(object):
    """
    This class is responsible for performing the HTTP requests, and error handling.
    """
    #__metaclass__ = abc.ABCMeta

    oc_transpo_server = 'api.octranspo1.com'
    api_base = '/v1.2'

    def __init__(self, app_id=None, api_key=None, requests_sess=None):
        """
        Initialize this protocol client, optionally providing a (shared) :class:`requests.Session`
        object.

        :param access_token: The token that provides access to a specific Strava account.
        :param requests_session: An existing :class:`requests.Session` object to use.
        """
        self.log = logging.getLogger('{0.__module__}.{0.__name__}'.format(self.__class__))
        self.app_id = app_id
        self.api_key = api_key

        if requests_sess:
            self.rsession = requests_session
        else:
            self.rsession = requests.Session()

        logging.basicConfig() 
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

    def _resolve_url(self, url):
        if not url.startswith('http'):
            url = urlparse.urljoin('https://{0}'.format(self.oc_transpo_server), self.api_base + '/' + url.strip('/'))
        return url

    def _request(self, url, params=None, files=None, method='GET', check_for_errors=True):

        url = self._resolve_url(url)
        print url
        self.log.info("{method} {url!r} with params {params!r}".format(method=method, url=url, params=params))
        if params is None:
            params = {}
        if self.app_id:
            params['appID'] = self.app_id
        if self.api_key:
            params['apiKey'] = self.api_key

        print params

        methods = {'GET': self.rsession.get,
                   'POST': functools.partial(self.rsession.post, files=files),
                   'PUT': self.rsession.put,
                   'DELETE': self.rsession.delete}

        try:
            requester = methods[method.upper()]
        except KeyError:
            raise ValueError("Invalid/unsupported request method specified: {0}".format(method))

        raw = requester(url, data=params)

        # create an XMLReader
        #parser = xml.sax.make_parser()
        # turn off namepsaces
        #parser.setFeature(xml.sax.handler.feature_namespaces, 0)

        # override the default ContextHandler
        #Handler = StopHandler()
        #parser.setContentHandler( Handler )
        print raw.text
        json = Xml2Json(raw.text).result
        #string_obj = StringIO(raw.text)
        #parser.parse(string_obj)

        #print raw.text
        if check_for_errors:
            self._handle_protocol_error(raw)

        # 204 = No content
        if raw.status_code in [204]:
            resp = []
        else:
            resp = json
            #resp = raw.json()

        # TODO: We should parse the response to get the rate limit details and
        # update our rate limiter.
        # see: http://strava.github.io/api/#access

        # At this stage we should assume that request was successful and we should invoke
        # our rate limiter.  (Note that this may need to be reviewed; some failures may
        # also count toward the limit?)
        #self.rate_limiter()

        return resp
    def _handle_protocol_error(self, response):
        """
        Parses the raw response from the server, raising a :class:`stravalib.exc.Fault` if the
        server returned an error.

        :param response: The response object.
        :raises Fault: If the response contains an error.
        """
        error_str = None
        try:
            json_response = response.json()
        except ValueError:
            pass
        else:
            if 'message' in json_response or 'errors' in json_response:
                error_str = '{0}: {1}'.format(json_response.get('message', 'Undefined error'), json_response.get('errors'))

        x = None
        if 400 <= response.status_code < 500:
            x = requests.exceptions.HTTPError('%s Client Error: %s [%s]' % (response.status_code, response.reason, error_str))
        elif 500 <= response.status_code < 600:
            x = requests.exceptions.HTTPError('%s Server Error: %s [%s]' % (response.status_code, response.reason, error_str))
        elif error_str:
            x = exc.Fault(error_str)

        if x is not None:
            raise x

        return response

    def _extract_referenced_vars(self, s):
        """
        Utility method to find the referenced format variables in a string.
        (Assumes string.format() format vars.)
        :param s: The string that contains format variables. (e.g. "{foo}-text")
        :return: The list of referenced variable names. (e.g. ['foo'])
        :rtype: list
        """
        d = {}
        while True:
            try:
                s.format(**d)
            except KeyError as exc:
                # exc.args[0] contains the name of the key that was not found;
                # 0 is used because it appears to work with all types of placeholders.
                d[exc.args[0]] = 0
            else:
                break
        return d.keys()

    def post(self, url, files=None, check_for_errors=True, **kwargs):
        """
        Performs a generic POST request for specified params, returning the response.
        """
        referenced = self._extract_referenced_vars(url)
        url = url.format(**kwargs)
        params = dict([(k, v) for k, v in kwargs.items() if not k in referenced])
        return self._request(url, params=params, files=files, method='POST', check_for_errors=check_for_errors)
