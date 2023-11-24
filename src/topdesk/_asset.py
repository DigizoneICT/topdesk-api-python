from . import _utils


class asset:

    def __init__(self, topdesk_url, credpair):
        self._topdesk_url = topdesk_url
        self._credpair = credpair
        self.utils = _utils.utils(self._topdesk_url, self._credpair)

    def get(self, id):
        return self.utils.handle_topdesk_response(
                self.utils.request_topdesk("/tas/api/assetmgmt/assets/{}".format(id)))

    def get_list(self, archived=False, page_size=50, query=None, templateId=None, fields=None):
        return self.utils.handle_topdesk_response(
                self.utils.request_topdesk("/tas/api/assetmgmt/assets/", archived, page_size,
                                           query, templateId, fields))

    def create(self, **kwargs):
        return self.utils.handle_topdesk_response(
                self.utils.post_to_topdesk(
                    "/tas/api/assetmgmt/assets", (self.utils.add_id_jsonbody(**kwargs))))

    def update(self, asset, **kwargs):
        return self.utils.handle_topdesk_response(
                self.utils.post_to_topdesk(
                    "/tas/api/assetmgmt/assets/{}".format(asset),
                    self.utils.add_id_jsonbody(**kwargs)))

    def archive(self, asset_id, reason_id=None):
        if reason_id:
            param = {'reasonId': reason_id}
        return self.utils.handle_topdesk_response(
                self.utils.post_to_topdesk(
                    "/tas/api/assetmgmt/assets/{}/archive".format(asset_id), param))

    def unarchive(self, asset_id):
        return self.utils.handle_topdesk_response(
                self.utils.post_to_topdesk(
                    "/tas/api/assetmgmt/assets/{}/unarchive".format(asset_id), None))

    def assign(self, asset_id, assignment):
        return self.utils.handle_topdesk_response(
                self.utils.put_to_topdesk(
                    "/tas/api/assetmgmt/assets/{}/assignments".format(asset_id), assignment))


if __name__ == "__main__":
    pass
