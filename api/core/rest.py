from rest_framework import exceptions, serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.schemas.openapi import AutoSchema, SchemaGenerator
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


class DefaultSchemaGenerator(SchemaGenerator):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("version", "0.1")
        super().__init__(*args, **kwargs)

    def _get_error_schemas(self):
        return {"FieldError": {"type": "array", "items": {"type": "string"}}}

    def _get_security_schemes(self):
        """
        OpenAPI uses the term security scheme for authentication and authorization schemes.

        see: https://swagger.io/docs/specification/authentication/

        # TODO: This uses OAuth 2.0
        """
        return {"bearerAuth": {"type": "http", "scheme": "bearer"}}

    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        error_schemas = self._get_error_schemas()
        schema["components"]["schemas"].update(error_schemas)
        schema["components"].update({"securitySchemes": self._get_security_schemes()})
        schema["security"] = [{"bearerAuth": []}]
        return schema


class DefaultSchema(AutoSchema):
    def _map_serializer_to_error(self, serializer):
        properties = {}

        for field in serializer.fields.values():
            if isinstance(field, serializers.HiddenField):
                continue
            if field.read_only:
                continue

            properties[field.field_name] = {"$ref": "#/components/schemas/FieldError"}

        result = {"type": "object", "properties": properties}

        return result

    def get_error_component_name(self, serializer):
        return f"{self.get_component_name(serializer)}Error"

    def get_components(self, path, method):
        components = super().get_components(path, method)
        if method == "POST":
            serializer = self.get_serializer(path, method)
            error_component_name = self.get_error_component_name(serializer)
            components[error_component_name] = self._map_serializer_to_error(serializer)
        return components

    def _get_error_reference(self, serializer):
        return {
            "$ref": "#/components/schemas/{}".format(
                self.get_error_component_name(serializer)
            )
        }

    def _get_error_response(self, path, method, request_response):

        response_media_types = [media_type for media_type in self.response_media_types]
        serializer = self.get_serializer(path, method)

        error_schema = self._get_error_reference(serializer)

        return {
            "content": {ct: {"schema": error_schema} for ct in response_media_types},
            "description": "",
        }

    def get_responses(self, path, method):
        """
        Update the property example's with the path, host and scheme of the request.
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

        if method == "POST":
            responses["400"] = self._get_error_response(path, method, responses["201"])

        return responses

    def _update_link(self, path, response_property, *keys):
        _property_attrs = response_property
        for key in keys[:-1]:
            _property_attrs = response_property[key]
        if self.view.request:
            host = self.view.request.get_host()
            scheme = self.view.request.scheme
        else:
            host = "localhost.test"
            scheme = "http"

        _property_attrs[keys[-1]] = _property_attrs[keys[-1]].format(
            path=path, host=host, scheme=scheme
        )


class CreateOnlyValidator:
    requires_context = True

    def __call__(self, value, serializer_field):
        instance = serializer_field.parent.instance
        is_update = instance is not None
        if is_update and serializer_field.get_attribute(instance) != value:
            raise exceptions.ValidationError(
                f"Updates to {serializer_field.field_name} are not allowed."
            )


class IsAuthenticatedOrCreateOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True

        return bool(request.user and request.user.is_authenticated)
