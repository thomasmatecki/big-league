from rest_framework.pagination import PageNumberPagination
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.schemas.utils import is_list_view


class DefaultPagination(PageNumberPagination):
    def get_paginated_response_schema(self, schema: dict) -> dict:
        return {
            "type": "object",
            "properties": {
                "count": {
                    "type": "integer",
                    "example": 123,
                },
                "next": {
                    "type": "string",
                    "nullable": True,
                    "format": "uri",
                    "example": f"{{scheme}}://{{host}}{{path}}?{self.page_query_param}=3",
                },
                "previous": {
                    "type": "string",
                    "nullable": True,
                    "format": "uri",
                    "example": f"{{scheme}}://{{host}}{{path}}?{self.page_query_param}=1",
                },
                "results": schema,
            },
        }


class DefaultSchema(AutoSchema):
    def get_responses(self, path, method):
        """
        Augment the paginated response with the scheme and hostname from the
        request. Also replace the path.
        """
        responses = super().get_responses(path, method)
        if is_list_view(path, method, self.view):

            for response_properties in [
                content["schema"]["properties"]
                for response in responses.values()
                for content in response["content"].values()  # type: ignore
            ]:
                self._update_link(path, response_properties, "previous", "example")
                self._update_link(path, response_properties, "next", "example")

        return responses

    def _update_link(self, path, response_property, *keys):
        _property_attrs = response_property
        for key in keys[:-1]:
            _property_attrs = response_property[key]

        host = self.view.request.get_host() or "localhost.test"
        scheme = self.view.request.scheme or "http"
        _property_attrs[keys[-1]] = _property_attrs[keys[-1]].format(
            path=path, host=host, scheme=scheme
        )
