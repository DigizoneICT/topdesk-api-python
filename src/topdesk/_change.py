from . import _utils


class change:

    def __init__(self, topdesk_url, credpair):
        self._topdesk_url = topdesk_url
        self._credpair = credpair
        self.utils = _utils.utils(self._topdesk_url, self._credpair)

    def get(self, id):
        return self.utils.handle_topdesk_response(
                self.utils.request_topdesk("/tas/api/operatorChanges/{}".format(id)))

    def get_list(self, archived=None, page_size=1000, query=None, templateId=None, fields=None):
        return self.utils.handle_topdesk_response(
                self.utils.request_topdesk(
                    "/tas/api/operatorChanges/", archived, page_size, query, templateId, fields))

    def create(self, **kwargs):
        return self.utils.handle_topdesk_response(
                self.utils.post_to_topdesk(
                    "/tas/api/operatorChanges", (self.utils.add_id_jsonbody(**kwargs))))

    def update(self, change, data):
        return self.utils.handle_topdesk_response(
                self.utils.patch_to_topdesk(
                    "/tas/api/operatorChanges/{}".format(change), data))

    def cancel(self, change, **kwargs):
        return self.utils.handle_topdesk_response(
                self.utils.post_to_topdesk(
                    "/tas/api/operatorChanges/{}/cancel".format(change),
                    (self.utils.add_id_jsonbody(**kwargs))))

    def processingstatus(self, change, **kwargs):
        return self.utils.handle_topdesk_response(
                self.utils.post_to_topdesk(
                    "/tas/api/operatorChanges/{}/processingStatusTransitions".format(change),
                    (self.utils.add_id_jsonbody(**kwargs))))


if __name__ == "__main__":
    pass
