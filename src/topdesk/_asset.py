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
                    "/tas/api/assetmgmt/assets", (self.utils.json_body_without_id(**kwargs))))

    def update(self, asset, **kwargs):
        return self.utils.handle_topdesk_response(
                self.utils.post_to_topdesk(
                    "/tas/api/assetmgmt/assets/{}".format(asset),
                    self.utils.json_body_without_id(**kwargs)))

    def delete(self, **kwargs):
        return self.utils.handle_topdesk_response(
                self.utils.post_to_topdesk(
                    "/tas/api/assetmgmt/assets/delete",
                    self.utils.json_body_without_id(**kwargs)))

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

    def getAssignments(self, asset_id):
        return self.utils.handle_topdesk_response(
                self.utils.request_topdesk(
                    "/tas/api/assetmgmt/assets/{}/assignments".format(asset_id)))

    def deleteAssignment(self, asset_id, linkId):
        return self.utils.handle_topdesk_response(
                self.utils.delete_from_topdesk(
                    "/tas/api/assetmgmt/assets/{}/assignments/{}".format(asset_id, linkId)))

    def linkService(self, **kwargs):
        return self.utils.handle_topdesk_response(
                self.utils.post_to_topdesk(
                    "/tas/api/assetmgmt/assets/linkedService",
                    (self.utils.json_body_without_id(**kwargs))))

    def linkTask(self, **kwargs):
        return self.utils.handle_topdesk_response(
                self.utils.post_to_topdesk(
                    "/tas/api/assetmgmt/assets/linkedTask",
                    (self.utils.add_id_jsonbody(**kwargs))))

    def upload(self, asset_id, filename, content):
        return self.utils.handle_topdesk_response(
                self.utils.upload_to_topdesk(
                    "/tas/api/assetmgmt/uploads/?assetId={}".format(asset_id), filename, content))

    def getDropdownOptions(self, fieldId):
        return self.utils.handle_topdesk_response(
                self.utils.request_topdesk(
                    "/tas/api/assetmgmt/dropdowns/{}/?field=name".format(fieldId)))


if __name__ == "__main__":
    pass
