from requests_toolbelt import MultipartEncoder
from collections import namedtuple
import json
import logging
import re
import requests
import string
import urllib.parse


class utils:

    def __init__(self, topdesk_url, credpair):
        self._topdesk_url = topdesk_url
        self._credpair = credpair
        self._partial_content_container = []

    def is_valid_uuid(self, uuid):
        return re.match(r"^[0-9a-g]{8}-([0-9a-g]{4}-){3}[0-9a-g]{12}$", uuid)

    def is_valid_email_addr(self, email_addr):
        return re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email_addr)

    def print_lookup_canidates(self, possible_canidates):
        if len(possible_canidates) == 1:
            return possible_canidates[0]
        elif len(possible_canidates) > 1:
            print("To many canidates: " + "; ".join(possible_canidates))
            return
        else:
            print("No canidates found.")
            return

    def handle_topdesk_response(self, response):
        logging.info('URL: ' + response.url
                     + ' Status code: ' + str(response.status_code)
                     + ' Headers: ' + str(response.headers))

        returnFormatError = namedtuple("response", ("error", "status_code", "body"))

        if response.status_code == 200 or response.status_code == 201:
            if not self._partial_content_container:

                if response.text == "":
                    return "Success"
                else:
                    if "dataSet" in response.json():
                        return response.json()["dataSet"]
                    elif "results" in response.json():
                        return response.json()["results"]
                    else:
                        return json.loads(response.content.decode('utf-8'))

            else:
                if "dataSet" in response.json():
                    self._partial_content_container.extend(response.json()["dataSet"])
                else:
                    self._partial_content_container.extend(response.json())
                placeHolder = self._partial_content_container
                self._partial_content_container = []

                return placeHolder
        elif response.status_code == 404:
            logging.error("status_code {}, message: {}".format('404', 'Not Found'))
            return returnFormatError(True, response.status_code, "Not Found")
        elif response.status_code == 405:
            logging.error("status_code {}, message: {}".format('405', 'Method not allowed'))
            return returnFormatError(True, response.status_code, "Method not allowed")
        elif response.status_code == 204:
            logging.debug("status_code {}, message: {}".format('204', 'No content'))
            return "success"
        # Partial content returned.
        elif response.status_code == 206:
            # can we make this recursive?
            if "dataSet" in response.json():
                self._partial_content_container.extend(response.json()["dataSet"])
            else:
                self._partial_content_container.extend(response.json())

            # Page size none crashes here.
            page_size = int(re.findall(r'page_size=(\d+)', response.url)[0])
            if 'pageStart=' in response.url:
                # Start allready in url replace value.
                current_start = int(re.findall(r'pageStart=(\d+)', response.url)[0])
                self.new_start = page_size + current_start
                partial_new_url = re.sub(r'pageStart=(\d+)', 'pageStart={}'.format(
                                    str(self.new_start)), response.url)
            else:
                # start= not yet present in URL. insert it.
                partial_new_url = re.sub(r'(page_size=\d+)', r'\1&pageStart={}'.format(
                                    str(page_size)), response.url)
            # Remove base url
            partial_new_url = partial_new_url.replace(self._topdesk_url, "")
            return self.handle_topdesk_response(self.request_topdesk(partial_new_url))
        else:
            # general failure
            status_code = response.status_code
            response = json.loads(response.content.decode('utf-8'))
            if 'errors' in response:
                if 'errorCode' in response['errors'][0]:
                    logging.error("errorCode {}, appliesTo: {}".format(
                                    response['errors'][0]['errorCode'],
                                    response['errors'][0]['appliesTo']))
                else:
                    logging.error("status_code {}, message: {}".format(
                                    status_code, response['errors'][0]['message']))
            else:
                logging.error("status_code {}, message: {}".format(
                                status_code, response))

            return returnFormatError(True, status_code, response)

    def request_topdesk(self, uri, archived=None, page_size=None, query=None, templateId=None,
                        fields=None, custom_uri=None, extended_uri=None):
        headers = {'Authorization': "Basic {}".format(self._credpair),
                   'Accept': 'application/json'}
        if custom_uri:
            uri += urllib.parse.urlencode(custom_uri, quote_via=urllib.parse.quote_plus)
        else:
            if templateId:
                uri += '?templateId={}'.format(templateId)
            if page_size:
                uri += '&' if 'templateId' in uri else '?'
                uri += "page_size={}".format(page_size)
            if extended_uri:
                uri += "&" + urllib.parse.urlencode(extended_uri,
                                                    quote_via=urllib.parse.quote_plus)
            if archived:
                uri += '&' if 'page_size' in uri else '?'
                uri += 'query=archived=={}'.format(archived)
            if fields:
                uri += '&' if 'page_size' in uri else '?'
                uri += 'fields={}'.format(fields)
            if query:
                # Some query param need to be URL encoded.
                query = urllib.parse.quote(query)
                if ('query=' in uri):
                    uri += ';{}'.format(query)
                elif 'page_size' in uri:
                    uri += '&query={}'.format(query)
                else:
                    uri += '?query={}'.format(query)
        logging.debug(uri)
        return requests.get(self._topdesk_url + uri, headers=headers)

    def post_to_topdesk(self, uri, json_body):
        logging.debug(uri)
        logging.debug(json_body)
        headers = {'Authorization': "Basic {}".format(self._credpair),
                   'Accept': 'application/json',
                   'Content-type': 'application/json'}
        return requests.post(self._topdesk_url + uri, headers=headers, json=json_body)

    def put_to_topdesk(self, uri, json_body):
        logging.debug(uri)
        headers = {'Authorization': "Basic {}".format(self._credpair),
                   'Accept': 'application/json',
                   'Content-type': 'application/json'}
        return requests.put(self._topdesk_url + uri, headers=headers, json=json_body)

    def patch_to_topdesk(self, uri, json_body):
        logging.debug(uri)
        headers = {'Authorization': "Basic {}".format(self._credpair),
                   'Accept': 'application/json',
                   'Content-type': 'application/json-patch+json'}
        return requests.patch(self._topdesk_url + uri, headers=headers, json=json_body)

    def delete_from_topdesk(self, uri, json_body=None):
        logging.debug(uri)
        headers = {'Authorization': "Basic {}".format(self._credpair),
                   'Accept': 'application/json',
                   'Content-type': 'application/json'}
        return requests.delete(self._topdesk_url + uri, headers=headers, json=json_body)

    def upload_to_topdesk(self, uri, filename, content):
        logging.debug(uri)

        m = MultipartEncoder(
            fields={'file': (filename, content, 'application/zip')}
        )

        headers = {'Authorization': "Basic {}".format(self._credpair),
                   'Accept': "application/json",
                   'Content-type': m.content_type}

        return requests.post(self._topdesk_url + uri, headers=headers, data=m)

    def add_id_list(self, id_list):
        param = []
        for item in id_list:
            param.append({'id': item})
        return param

    def add_id_jsonbody(self, **kwargs):
        request_body = {}

        # args = posible caller
        if 'caller' in kwargs:
            if self.is_valid_email_addr(kwargs['caller']):
                caller_type = "email"
            elif self.is_valid_uuid(kwargs['caller']):
                caller_type = "id"
            else:
                caller_type = "dynamicName"
            request_body['callerLookup'] = {caller_type: kwargs['caller']}

        for key in kwargs:
            if self.is_valid_uuid(str(kwargs[key])):
                request_body[key] = {'id': kwargs[key]}
            else:
                if key == 'caller':
                    continue
                request_body[key] = kwargs[key]

        if 'taskId' in kwargs:
            if self.is_valid_uuid(kwargs['taskId']):
                request_body['taskId'] = kwargs['taskId']

        return request_body

    def json_body_without_id(self, **kwargs):
        request_body = {}
        for key in kwargs:
            request_body[key] = kwargs[key]
        return request_body

    def find_partial_match_company(self, data, partial):
        matching_data = []
        for item in data:
            name = item['name']
            # Remove punctuation from name and partial
            name_no_punct = re.sub(r'[{}]'.format(string.punctuation), '', name)
            partial_no_punct = re.sub(r'[{}]'.format(string.punctuation), '', partial)

            # Split names into words and compare sets of words
            name_words = set(name_no_punct.lower().split())
            partial_words = set(partial_no_punct.lower().split())
            if partial_words.issubset(name_words):
                matching_data.append(item)
        return matching_data


if __name__ == "__main__":
    pass
