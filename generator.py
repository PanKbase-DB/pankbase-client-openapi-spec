import json
import requests
from functools import reduce


def generate_openapi_spec(schemas):
    openapi_spec = {
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
                    "summary": "Search for items in the IGVF Project.",
                    "description": "Search endpoint that accepts various query parameters to filter, sort, and paginate results. Supports complex filtering on types and fields within JSON objects.",
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
                    "summary": "Generate a report based on search query. All results are returned.",
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

    RESERVED_KEYS = [
        'datastore',
        'debug',
        'field',
        'format',
        'frame',
        'from',
        'limit',
        'mode',
        'sort',
        'type',
        'config',
        'advancedQuery',
        'query',
    ]

    search_description = openapi_spec["paths"]["/search"]["get"]["description"]
    search_description += f"\n\nReserved query parameters: {', '.join(RESERVED_KEYS)}"
    search_description += "\nThese parameters have special meanings and cannot be used as field names for filtering."

    # Add all schemas to components/schemas and refs to @graph items
    for schema_name, schema in schemas.items():
        openapi_spec["components"]["schemas"][schema_name] = schema
        openapi_spec["paths"]["/{resource_id}"]["get"]["responses"]["200"]["content"]["application/json"]["schema"]["oneOf"].append(
            {"$ref": f"#/components/schemas/{schema_name}"}
        )
        openapi_spec["paths"]["/search"]["get"]["responses"]["200"]["content"]["application/json"]["schema"]["properties"]["@graph"]["items"]["oneOf"].append(
            {"$ref": f"#/components/schemas/{schema_name}"}
        )
        openapi_spec["components"]["schemas"]["ItemType"]["enum"].append(schema_name)
        openapi_spec["components"]["schemas"]["ItemType"]["x-enum-varnames"].append(schema_name)

    # Add an example that demonstrates expanded parameters
    complex_example = {
        "summary": "Complex search with multiple parameters",
        "description": "Search for experiments, sort by multiple fields, and specify multiple types",
        "value": {
            "type": ["Experiment", "Dataset"],
            "assay_title": "ChIP-seq",
            "target.label": "CTCF",
            "biosample_ontology.organ_slims": "brain",
            "status": "released",
            "lab.name": "john-stamatoyannopoulos",
            "sort": ["-date_created", "@id"],
            "field": ["@id", "accession", "description", "assay_title", "biosample_ontology.term_name"],
            "from": "25",
            "limit": "25",
            "format": "json",
            "frame": "object"
        }
    }
    # openapi_spec["paths"]["/search"]["get"]["examples"] = [complex_example]
    for schema_name, schema in schemas.items():
        collection_template = fill_in_collection_template(schema_name, schema)
        openapi_spec["paths"].update(collection_template)
   
    return openapi_spec


url = 'http://localhost:8000'


schemas_cache = {}


def get_properties_for_item_type(schemas, item_type):
    if item_type not in schemas_cache:
        if item_type not in schemas:
            print(item_type, 'not in schemas, searching abstract')
            schemas_cache[item_type] = requests.get(f'{url}/profiles/{item_type}').json()['properties']
        else:
            schemas_cache[item_type] = schemas[item_type]['properties']
    return schemas_cache[item_type]


def traverse(all_schemas, properties, path, include, exclude, is_an_item=False, processed=None):
    if processed is None:
        processed = []
    is_an_item = is_an_item
    fields = []
    item_type = None
    if isinstance(path, str):
        path = path.split('.')
    if not path:
        return fields
    name = path[0]
    remaining = path[1:]
    value = properties.get(name)
    if value is None:
        return fields
    if 'items' in value:
        is_an_item = True
        value = value['items']
    if 'linkTo' in value:
        item_type = value['linkTo']
    elif 'linkFrom' in value:
        item_type = value['linkFrom'].split('.')[0]
    if item_type is not None:
        if isinstance(item_type, list):
            print('reducing', item_type, 'in', processed, path)
            value = reduce(
                combine_schemas,
                (
                    get_properties_for_item_type(all_schemas, it)
                    for it in item_type
                )
            )
        else:
            value = get_properties_for_item_type(all_schemas, item_type)
    else:
        if 'properties' in value:
            value = value['properties']
        else:
            raise ValueError(f'item type is none and no properties {value} {name} {remaining} {path}')
    if exclude:
        raise ValueError('handle exclude!')
    elif include:
        for field in include:
            if field in value:
                fields.append(
                    {
                        'path': '.'.join([x for x in processed + [name] + [field]]),
                        'schema': value[field],
                        'is_an_item': is_an_item,
                    }
                )
    processed.append(name)
    fields.extend(traverse(all_schemas, value, remaining, include, exclude, is_an_item, processed))
    return fields


# copied from snovault
def ensurelist(value):
    if isinstance(value, basestring):
        return [value]
    return value


# copied from snovault
def combine_schemas(a, b):
    if a == b:
        return a
    if not a:
        return b
    if not b:
        return a
    combined = {}
    for name in set(a.keys()).intersection(b.keys()):
        if a[name] == b[name]:
            combined[name] = a[name]
        elif name == 'type':
            combined[name] = sorted(set(ensurelist(a[name]) + ensurelist(b[name])))
        elif name == 'properties':
            combined[name] = {}
            for k in set(a[name].keys()).intersection(b[name].keys()):
                combined[name][k] = combine_schemas(a[name][k], b[name][k])
            for k in set(a[name].keys()).difference(b[name].keys()):
                combined[name][k] = a[name][k]
            for k in set(b[name].keys()).difference(a[name].keys()):
                combined[name][k] = b[name][k]
        elif name == 'items':
            combined[name] = combine_schemas(a[name], b[name])
        elif name == 'columns':
            combined[name] = {}
            combined[name].update(a[name])
            combined[name].update(b[name])
        elif name == 'fuzzy_searchable_fields':
            combined[name] = list(
                sorted(
                    set(a[name]).union(set(b[name]))
                )
            )
    for name in set(a.keys()).difference(b.keys(), ['facets']):
        combined[name] = a[name]
    for name in set(b.keys()).difference(a.keys(), ['facets']):
        combined[name] = b[name]
    return combined


def get_slim_embedded_fields():
    final = {}
    embedded_fields = requests.get(f'{url}/embedded-fields').json()
    all_schemas = {k: v for k, v in requests.get(f'{url}/profiles').json().items() if '@' not in k and '_' not in k}
    for item_type in all_schemas.keys():
        fields = []
        print('ITEM', item_type)
        properties = all_schemas[item_type]['properties']
        for embedded_field in embedded_fields[item_type]['embedded_with_frame']:
            path = embedded_field['path']
            print('working on path', path)
            include = embedded_field['include']
            exclude = embedded_field['exclude']
            fields.extend(traverse(all_schemas, properties, path, include, exclude))
        all_fields = set(f['path'] for f in fields)
        to_remove_fields = []
        for f in fields:
            fname = f['path']
            for afname in all_fields:
                if afname.startswith(fname) and len(fname) != len(afname):
                    print('removing -------->', fname, afname)
                    to_remove_fields.append(fname)
        fields = {
            f['path']: f
            for f in fields
            if f['path'] not in to_remove_fields
        }
        fields = dict(sorted(fields.items(), key=lambda x: x[1]['path']))
        final[item_type] = fields
        for embedded_field in embedded_fields[item_type]['embedded']:
            if 'Testing' in item_type:
                continue
            raise ValueError(f'Found full embedded field, handle it {item_type} {embedded_fields[item_type]}')
    return final


slim_embedded_fields = get_slim_embedded_fields()

res = requests.get('https://api.data.igvf.org/profiles').json()

subtypes = res['_subtypes']

schemas = {
    k: v for
    k, v in res.items()
    if not k.startswith('_') and not k.startswith('@')
}


def get_schema_names_to_collection_names(schema_keys):
    d = requests.get('https://api.data.igvf.org/collection-titles').json()
    del d['@type']
    rs = {v: k for k, v in d.items() if k in schema_keys}
    collection_names = {}
    for k, v in d.items():
        if v not in rs:
            continue
        if k in schema_keys:
            continue
        if k.istitle():
            continue
        if '_' in k:
            continue
        if f'{k}s' in d:
            continue
        collection_names[rs[v]] = k
    return collection_names


schema_names_to_collection_names = get_schema_names_to_collection_names(schemas.keys())


def fill_in_collection_template(schema_name, schema):
    collection_name = schema_names_to_collection_names[schema_name]
    collection_template = {
        f"/{collection_name}/@@listing": {
            "get": {
                "tags": ["Collections"],
                "summary": f"List items in the {schema_name} collection.",
                "description": f"Collection endpoint that accepts various query parameters to filter, sort, and paginate {schema_name} items. Supports filtering on fields within {schema_name} items.",
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
    embedded_fields = slim_embedded_fields[schema_name]
    embedded_fields_keys = embedded_fields.keys()
#    print(schema_name, embedded_fields_keys)
    to_add = []
    for prop, prop_schema in schema["properties"].items():
        if property_is_slim_embedded(prop, embedded_fields_keys):
            continue
        add_as_item = 'items' not in prop_schema # We always want to be able to enter multiple search values.
        exclude = ['default', 'uniqueItems', 'notSubmittable', 'readonly', 'permission', 'submissionExample', 'serverDefault', 'minItems', 'format']
        filtered_prop_schema = {k: v for k, v in prop_schema.items() if k not in exclude}
        if prop == '@type':
            continue
        if prop == 'schema_version':
            continue
        if prop == 'upload_credentials':
            continue
        if 'properties' in prop_schema:
            print('skipping', prop, 'as query param')
            continue
        to_add.append(
            {
                "name": f"{prop}",
                "in": "query",
                "schema": filtered_prop_schema if not add_as_item else {"type": "array", "items": filtered_prop_schema},
                "description": f"Filter by {prop}",
                "style": "form",
                "explode": True,
            }
        )
    for k, v in embedded_fields.items():
        prop = v['path']
        prop_schema = v['schema']
        add_as_item = 'items' not in prop_schema # We always want to be able to enter multiple search values.
        exclude = ['default', 'uniqueItems', 'notSubmittable', 'readonly', 'permission', 'submissionExample', 'serverDefault', 'minItems', 'format']
        filtered_prop_schema = {k: v for k, v in prop_schema.items() if k not in exclude}
        if '@type' in prop:
            continue
        if prop == 'upload_credentials':
            continue
        if prop == 'schema_version':
            continue
        if 'properties' in prop_schema:
            print('skipping', prop, 'as query param')
            continue
        to_add.append(
            {
                "name": f"{prop}",
                "in": "query",
                "schema": filtered_prop_schema if not add_as_item else {"type": "array", "items": filtered_prop_schema},
                "description": f"Filter by {prop}",
                "style": "form",
                "explode": True,
            }
        )
    for param in sorted(to_add, key=lambda x: x['name']):
        collection_template[f"/{collection_name}/@@listing"]["get"]["parameters"].append(param)
    return collection_template


def property_is_slim_embedded(prop, embedded_fields_keys):
    for key in embedded_fields_keys:
        if key.startswith(prop):
            print('SKIPPING', prop, 'found', key)
            return True
    return False


def clean_schema(schema):
        valid_attrs = [
            "type", "properties", "required", "additionalProperties",
            "items", "allOf", "anyOf", "oneOf", "not", "enum",
            "const", "multipleOf", "maximum", "exclusiveMaximum",
            "minimum", "exclusiveMinimum", "maxLength", "minLength",
            "pattern", "uniqueItems",
            "maxContains", "minContains", "maxProperties", "minProperties",
            "title", "description", "linkTo",
        ]
        cleaned = {}
        for key, value in schema.items():
            if key in valid_attrs:
                if key == "properties":
                    cleaned[key] = {k: clean_schema(v) for k, v in value.items()}
                elif key == "required" and not isinstance(value, list):
                    cleaned[key] = list(value)  # Convert to list if it's not already
                elif isinstance(value, dict):
                    cleaned[key] = clean_schema(value)
                else:
                    cleaned[key] = value
        if 'linkTo' in schema or 'linkFrom' in schema:
            cleaned['type'] = 'string'
            cleaned.pop('linkTo', None)
            cleaned.pop('linkFrom', None)
        return cleaned

schemas = {
    k: clean_schema(v)
    for k, v in schemas.items()
}


for k in schemas.keys():
    if 'required' in schemas[k]:
        del schemas[k]['required']
    # Normalize content_type, input_content_types, output_content_types so they don't generate multiple OpenAPI models.
    if 'content_type' in schemas[k]['properties']:
        schemas[k]['properties']['content_type'].pop('enum', None)
        schemas[k]['properties']['content_type'].pop('oneOf', None)
        schemas[k]['properties']['content_type'].pop('anyOf', None)
    if 'input_content_types' in schemas[k]['properties']:
        schemas[k]['properties']['input_content_types']['items'].pop('anyOf', None)
    if 'output_content_types' in schemas[k]['properties']:
        schemas[k]['properties']['output_content_types']['items'].pop('anyOf', None)



#print(json.dumps(schemas, indent=4))

openapi_spec = generate_openapi_spec(schemas)


with open('api_spec.json', 'w') as f:
    json.dump(openapi_spec, f, indent=2)


print("OpenAPI specification has been generated and saved to 'api_spec.json'")
