import json

import requests

from functools import reduce

from .template import OPENAPI_SPEC_TEMPLATE
from .template import get_collection_template


URL = 'https://api.data.igvf.org'

SCHEMAS_CACHE = {}


def get_version():
    return requests.get(f'{URL}').json()['app_version']


def generate_openapi_spec(schemas, schema_names_to_collection_names, slim_embedded_fields, version=None):
    openapi_spec = OPENAPI_SPEC_TEMPLATE
    openapi_spec['info']['version'] = get_version() if version is None else version

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

    # Fill in collection details.
    for schema_name, schema in schemas.items():
        collection_template = fill_in_collection_template(schema_name, schema, schema_names_to_collection_names, slim_embedded_fields)
        openapi_spec["paths"].update(collection_template)
   
    return openapi_spec


def get_properties_for_item_type(schemas, item_type):
    if item_type not in SCHEMAS_CACHE:
        if item_type not in schemas:
            print(item_type, 'not in schemas, searching abstract')
            SCHEMAS_CACHE[item_type] = requests.get(f'{URL}/profiles/{item_type}').json()['properties']
        else:
            SCHEMAS_CACHE[item_type] = schemas[item_type]['properties']
    return SCHEMAS_CACHE[item_type]


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
    if isinstance(value, str):
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


def fill_in_collection_template(schema_name, schema, schema_names_to_collection_names, slim_embedded_fields):
    collection_name = schema_names_to_collection_names[schema_name]
    collection_template = get_collection_template(collection_name, schema_name)
    embedded_fields = slim_embedded_fields[schema_name]
    embedded_fields_keys = embedded_fields.keys()
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
                "schema": sort_dict(clean_schema(filtered_prop_schema if not add_as_item else {"type": "array", "items": filtered_prop_schema})),
                "description": f"Filter by {prop}",
                "style": "form",
                "explode": True,
            }
        )
    for k, v in embedded_fields.items():
        prop = v['path']
        prop_schema = v['schema']
        add_as_item = 'items' not in prop_schema # We always want to be able to enter multiple search values.
        exclude = ['default', 'uniqueItems', 'notSubmittable', 'readonly', 'permission', 'submissionExample', 'serverDefault', 'minItems', 'format', 'oneOf', 'anyOf', 'enum']
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
                "schema": sort_dict(clean_schema(filtered_prop_schema if not add_as_item else {"type": "array", "items": filtered_prop_schema})),
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


def normalize_schemas(schemas):
    for k in schemas.keys():
        if 'required' in schemas[k]:
            del schemas[k]['required']
        if 'not' in schemas[k]:
            del schemas[k]['not']
        # Normalize content_type, input_content_types, output_content_types so they don't generate multiple OpenAPI models.
        if 'content_type' in schemas[k]['properties']:
            schemas[k]['properties']['content_type'].pop('enum', None)
            schemas[k]['properties']['content_type'].pop('oneOf', None)
            schemas[k]['properties']['content_type'].pop('anyOf', None)
        if 'input_content_types' in schemas[k]['properties']:
            schemas[k]['properties']['input_content_types']['items'].pop('anyOf', None)
        if 'output_content_types' in schemas[k]['properties']:
            schemas[k]['properties']['output_content_types']['items'].pop('anyOf', None)
    return schemas


def get_raw_embedded_fields():
    return requests.get(f'{URL}/embedded-fields').json()


def get_slim_embedded_fields(raw_embedded_fields, raw_schemas):
    final = {}
    embedded_fields = raw_embedded_fields
    all_schemas = raw_schemas
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


def get_schema_names_to_collection_names():
    return requests.get(f'{URL}/collection-names').json()


def clean_schemas(schemas):
    schemas = {
        k: clean_schema(v)
        for k, v in schemas.items()
    }
    return schemas


def get_schemas():
    res = requests.get(f'{URL}/profiles').json()
    schemas = {
        k: v for
        k, v in res.items()
        if not k.startswith('_') and not k.startswith('@')
    }
    return schemas


def sort_dict(d):
    sorted_dict = {}
    for k, v in sorted(d.items(), reverse=True):
        if isinstance(v, dict):
            sorted_dict[k] = sort_dict(v)
        else:
            sorted_dict[k] = v
    return sorted_dict


def generate():
    raw_schemas = get_schemas()
    schemas = normalize_schemas(clean_schemas(raw_schemas))
    schema_names_to_collection_names = get_schema_names_to_collection_names()
    raw_embedded_fields = get_raw_embedded_fields()
    slim_embedded_fields = get_slim_embedded_fields(raw_embedded_fields, raw_schemas)
    openapi_spec = generate_openapi_spec(schemas, schema_names_to_collection_names, slim_embedded_fields)
    return openapi_spec


def generate_and_save():
    openapi_spec = generate()
    with open('openapi_spec.json', 'w') as f:
        json.dump(openapi_spec, f, indent=2)
        print('OpenAPI specification has been generated and saved to openapi_spec.json')
