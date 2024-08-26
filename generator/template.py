OPENAPI_SPEC_TEMPLATE =  {
    "openapi": "3.1.0",
    "info": {
        "title": "IGVF Project API",
        "version": "0.1.0"
    },
    "servers": [
        {
            "url": "https://api.data.igvf.org"
        }
    ],
    "paths": {
        "/{resource_id}": {
            "get": {
                "tags": ["IGVF"],
                "summary": "Get item information",
                "description": "Retrieve detailed information about a specific item using its @id or uuid.",
                "operationId": "get_by_id",
                "parameters": [
                    {
                        "name": "resource_id",
                        "in": "path",
                        "required": True,
                        "schema": {
                            "type": "string"
                        },
                        "description": "The unique identifier for the resource i.e. @id (`/sequence-files/IGVFFI1165AJSO/`), accession (`IGVFFI1165AJSO`) or UUID (`fffcd64e-af02-4675-8953-7352459ee06a`).",
                        "examples": {
                            "@id": {
                                "value": "/sequence-files/IGVFFI1165AJSO/"
                            },
                            "uuid": {
                                "value": "fffcd64e-af02-4675-8953-7352459ee06a"
                            },
                            "accession": {
                                "value": "IGVFFI1165AJSO"
                            }
                        }
                    },
                    {
                        "name": "frame",
                        "in": "query",
                        "required": True,
                        "schema": {
                            "type": "string",
                            "enum": ["object"]
                        },
                        "description": "Constant value. Do not set."
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "title": "Item",
                                    "oneOf": [],
                                    "discriminator": {
                                        "propertyName": "@type",
                                        "mapping": {}
                                    },
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Object not found",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/search": {
            "get": {
                "tags": ["IGVF"],
                "summary": "Search for items on the IGVF Data Portal.",
                "description": "Search endpoint that accepts various query parameters to filter and sort results. Supports complex filtering on item types and fields within items.",
                "operationId": "search",
                "parameters": [
                    {
                        "name": "query",
                        "in": "query",
                        "schema": {"type": "string"},
                        "description": "Query string for searching."
                    },
                    {
                        "name": "type",
                        "in": "query",
                        "schema": {"type": "array", "items": {"type": "string"}},
                        "style": "form",
                        "explode": True,
                        "description": "Filter by item type."
                    },
                    {
                        "name": "limit",
                        "in": "query",
                        "schema": {
                            "$ref": "#/components/schemas/Limit",
                        },
                        "description": "Maximum number of results to return. Default is 25. Use 'all' for all results.",
                        "example": 100,
                    },
                    {
                        "name": "sort",
                        "in": "query",
                        "schema": {"type": "array", "items": {"type": "string"}},
                        "style": "form",
                        "explode": True,
                        "description": "Fields to sort results by. Prefix with '-' for descending order. Does not work with limit=all."
                    },
                    {
                        "name": "field_filters",
                        "in": "query",
                        "schema": {
                            "type": "object"
                        },
                        "description": "Any field from any item type can be used as a filter. Use '!' at end of field name for negation and 'lt:', 'lte:', 'gt:', 'gte:' with value for range queries on numeric fields. Examples: {'status!': 'in progress', 'file_size': 'gte:30000'}",
                        "style": "form",
                        "explode": True,
                    },
                    {
                        "name": "frame",
                        "in": "query",
                        "required": True,
                        "schema": {
                            "type": "string",
                            "enum": ["object"]
                        },
                        "description": "Constant value. Do not set."
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "title": "SearchResults",
                                    "properties": {
                                        "@graph": {
                                            "type": "array",
                                            "items": {
                                                "title": "SearchResultItem",
                                                "oneOf": [],
                                                "discriminator": {
                                                    "propertyName": "@type",
                                                    "mapping": {}
                                                },
                                            }
                                        },
                                        "@id": {"type": "string"},
                                        "@type": {
                                            "type": "array",
                                            "items": {"type": "string"}
                                        },
                                        "total": {"type": "integer"},
                                        "facets": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "title": "SearchFacet",
                                                "properties": {
                                                    "field": {"type": "string"},
                                                    "title": {"type": "string"},
                                                    "terms": {
                                                        "type": "array",
                                                        "items": {
                                                            "title": "SearchFacetTermValue",
                                                            "type": "object",
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                    },
                    "404": {
                        "description": "No results found",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/NoResultsResponse"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/profiles": {
            "get": {
                "tags": ["IGVF"],
                "summary": "Retrieve JSON schemas for all item types",
                "description": "Returns JSON schemas of all the item types defined in IGVF",
                'operationId': 'schemas',
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/JSONSchema"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/profiles/{item_type}": {
            "get": {
                "tags": ["IGVF"],
                "summary": "Retrieve JSON schema for item type",
                "description": "Returns JSON schemas of all the item types defined in IGVF",
                'operationId': 'schema_for_item_type',
                'parameters': [
                    {
                        "name": "item_type",
                        "in": "path",
                        "required": True,
                        "schema": {
                            "$ref": "#/components/schemas/ItemType"
                        },
                        "description": "The name of the item type"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/JSONSchema"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/multireport.tsv": {
            "get": {
                "tags": ["IGVF"],
                "summary": "Generate a TSV file report based on search query. All results are returned.",
                "description": "Like /search endpoint but returns a TSV file instead of JSON. Must specify item type(s).",
                "operationId": "report",
                "parameters": [
                    {
                        "name": "query",
                        "in": "query",
                        "schema": {"type": "string"},
                        "description": "Query string for searching."
                    },
                    {
                        "name": "type",
                        "in": "query",
                        "schema": {"type": "array", "items": {"type": "string"}},
                        "style": "form",
                        "explode": True,
                        "description": "Filter by item type."
                    },
                    {
                        "name": "limit",
                        "in": "query",
                        "schema": {
                            "$ref": "#/components/schemas/Limit",
                        },
                        "description": "Maximum number of results to return. Default is 25. Use 'all' for all results.",
                        "example": 100,
                    },
                    {
                        "name": "sort",
                        "in": "query",
                        "schema": {"type": "array", "items": {"type": "string"}},
                        "style": "form",
                        "explode": True,
                        "description": "Fields to sort results by. Prefix with '-' for descending order. Does not work with limit=all."
                    },
                    {
                        "name": "field_filters",
                        "in": "query",
                        "schema": {
                            "type": "object"
                        },
                        "description": "Any field from any item type can be used as a filter. Use '!' at end of field name for negation and 'lt:', 'lte:', 'gt:', 'gte:' with value for range queries on numeric fields. Examples: {'status!': 'in progress', 'file_size': 'gte:30000'}",
                        "style": "form",
                        "explode": True,
                    },
                    {
                        "name": "field",
                        "in": "query",
                        "schema": {"type": "array", "items": {"type": "string"}},
                        "style": "form",
                        "explode": True,
                        "description": "Fields to include in the response. Can be repeated for multiple fields."
                    },
                    {
                        "name": "frame",
                        "in": "query",
                        "schema": {
                            "type": "string",
                            "enum": ["object", "embedded"]
                        },
                        "description": "Object with links, or object with some links embedded."
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "text/tab-separated-values": {
                                "schema": {
                                    "type": "string"
                                },
                                "example": "Column1\tColumn2\tColumn3\nValue1\tValue2\tValue3"
                            }
                        }
                    },
                    "400": {
                        "description": "Bad request",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "No results found",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                }
                            }
                        }
                    },
                    "500": {
                        "description": "Internal server error"
                    }
                }
            }
        },
        "/{file_id}/@@download": {
            "get": {
                "tags": ["IGVF"],
                "summary": "Download file.",
                "description": "Returns underlying file associated with file metadata",
                "operationId": "download",
                "parameters": [
                    {
                        "in": "path",
                        "name": "file_id",
                        "schema": {
                            "type": "string"
                        },
                        "required": True,
                        "description": "The unique identifier for the file to download, e.g. @id (/tabular-files/IGVFFI8092FZKL/), accession (IGVFFI8092FZKL), or UUID (fdbdc159-e5b9-40a8-b788-3f72c9886b03)."
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/octet-stream": {
                                "schema": {
                                    "type": "string",
                                    "format": "binary"
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Item not found"
                    },
                    "500": {
                        "description": "Internal server error"
                    }
                }
            }
        },
        "/batch-download": {
            "get": {
                "tags": ["IGVF"],
                "summary": "List files to download based on search query. All results are returned.",
                "description": "Generates TSV of files contained in FileSets in search results.",
                "operationId": "batch_download",
                "parameters": [
                    {
                        "name": "type",
                        "in": "query",
                        "schema": {"type": "array", "items": {"type": "string"}},
                        "style": "form",
                        "explode": True,
                        "required": True,
                        "description": "Type of objects to return. Can be repeated for multiple types."
                    },
                    {
                        "name": "query",
                        "in": "query",
                        "schema": {"type": "string"},
                        "description": "Query string for searching."
                    },
                    {
                        "name": "field_filters",
                        "in": "query",
                        "schema": {
                            "type": "object"
                        },
                        "description": "Any field from any object type can be used as a filter. Use '!' for negation, '*' as a wildcard, and 'lt:', 'lte:', 'gt:', 'gte:' for range queries on numeric fields.",
                        "style": "form",
                        "explode": True,
                    },
                ],
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "text/tab-separated-values": {
                                "schema": {
                                    "type": "string"
                                },
                                "example": "@id\thref\nhref1\thref2"
                            }
                        }
                    },
                    "400": {
                        "description": "Bad request",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "No results found",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                }
                            }
                        }
                    },
                    "500": {
                        "description": "Internal server error"
                    }
                }
            }
        }
    },
    "components": {
        "schemas": {
            "ItemType": {
                "type": "string",
                "enum": [],
                "x-enum-varnames": []
            },
            "JSONSchema": {
                "type": "object",
                "description": "A JSON Schema object"
            },
            "Limit": {
                "oneOf": [
                    {"type": "string"},
                    {"type": "integer"}
                ],
                "default": 25
            },
            "NoResultsResponse": {
                "type": "object",
                "properties": {
                    "@context": {
                        "type": "string"
                    },
                    "@graph": {
                        "type": "array",
                        "items": {}
                    },
                    "@id": {
                        "type": "string"
                    },
                    "@type": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "clear_filters": {
                        "type": "string"
                    },
                    "columns": {
                        "type": "object",
                        "additionalProperties": {
                            "type": "object",
                            "properties": {
                                "title": {
                                    "type": "string"
                                }
                            }
                        }
                    },
                    "facet_groups": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string"
                                },
                                "title": {
                                    "type": "string"
                                },
                                "facet_fields": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    }
                                }
                            }
                        }
                    },
                    "facets": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "field": {
                                    "type": "string"
                                },
                                "title": {
                                    "type": "string"
                                },
                                "terms": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "key": {
                                                "type": "string"
                                            },
                                            "doc_count": {
                                                "type": "integer"
                                            }
                                        }
                                    }
                                },
                                "total": {
                                    "type": "integer"
                                },
                                "type": {
                                    "type": "string"
                                },
                                "appended": {
                                    "type": "boolean"
                                },
                                "open_on_load": {
                                    "type": "boolean"
                                }
                            }
                        }
                    },
                    "filters": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "field": {
                                    "type": "string"
                                },
                                "term": {
                                    "type": "string"
                                },
                                "remove": {
                                    "type": "string"
                                }
                            }
                        }
                    },
                    "notification": {
                        "type": "string"
                    },
                    "sort": {
                        "type": "object",
                        "additionalProperties": {
                            "type": "object",
                            "properties": {
                                "order": {
                                    "type": "string"
                                },
                                "unmapped_type": {
                                    "type": "string"
                                }
                            }
                        }
                    },
                    "title": {
                        "type": "string"
                    },
                    "total": {
                        "type": "integer"
                    }
                }
            }
        },
        "securitySchemes": {
            "basicAuth": {
                "type": "http",
                "scheme": "basic"
            }
        },
    },
    "security": [
        {},
        {"basicAuth": []}
    ]
}


def get_collection_template(collection_name, schema_name):
    return {
        f"/{collection_name}/@@listing": {
            "get": {
                "tags": ["Collections"],
                "summary": f"List items in the {schema_name} collection.",
                "description": f"Collection endpoint that accepts various query parameters to filter and sort {schema_name} items. Supports filtering on fields within {schema_name} items.",
                "operationId": f"{collection_name.replace('-', '_')}",
                "parameters": [
                    {
                        "name": "query",
                        "in": "query",
                        "schema": {"type": "string"},
                        "description": "Query string for searching.",
                        "example": "variant flowfish jurkat"
                    },
                    {
                        "name": "frame",
                        "in": "query",
                        "required": True,
                        "schema": {
                            "type": "string",
                            "enum": ["object"]
                        },
                        "description": "Constant value. Do not set."
                    },
                    {
                        "name": "limit",
                        "in": "query",
                        "schema": {
                            "$ref": "#/components/schemas/Limit",
                        },
                        "description": "Maximum number of results to return. Default is 25. Use 'all' for all results.",
                        "examples": {
                            "number": {"value": 100},
                            "all": {"value": "all"}
                        }
                    },
                    {
                        "name": "sort",
                        "in": "query",
                        "schema": {"type": "array", "items": {"type": "string"}},
                        "style": "form",
                        "explode": True,
                        "description": "Fields to sort results by. Prefix with '-' for descending order. Can be repeated for multiple sort fields. Does not work with limit=all.",
                        "examples": {"file_size": {"value": "-file_size"}, "lab": {"value": "lab.title"}}
                    },
                ],
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "title": f"{schema_name}Results",
                                    "properties": {
                                        "@graph": {
                                            "type": "array",
                                            "items": {
                                                "$ref": f"#/components/schemas/{schema_name}"
                                            }
                                        },
                                        "@id": {"type": "string"},
                                        "@type": {
                                            "type": "array",
                                            "items": {"type": "string"}
                                        },
                                        "total": {"type": "integer"},
                                        "facets": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "title": "SearchFacet",
                                                "properties": {
                                                    "field": {"type": "string"},
                                                    "title": {"type": "string"},
                                                    "terms": {
                                                        "type": "array",
                                                        "items": {
                                                            "title": "SearchFacetTermValue",
                                                            "type": "object",
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Bad request",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "No results found",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/NoResultsResponse"
                                }
                            }
                        }
                    },
                    "500": {
                        "description": "Internal server error"
                    }
                }
            }
        }
    }
