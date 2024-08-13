import pytest


def test_generator_test_generate():
    from generator.generate import generate
    openapi_spec = generate()
    expected_keys = ['openapi', 'info', 'servers', 'paths', 'components', 'security']
    actual_keys = openapi_spec.keys()
    assert set(expected_keys) == set(actual_keys)
    expected_keys = ['/{resource_id}', '/search', '/profiles', '/profiles/{item_type}', '/multireport.tsv', '/{file_id}/@@download', '/batch-download', '/access-keys/@@listing', '/analysis-steps/@@listing', '/analysis-step-versions/@@listing', '/awards/@@listing', '/biomarkers/@@listing', '/documents/@@listing', '/human-donors/@@listing', '/rodent-donors/@@listing', '/alignment-files/@@listing', '/configuration-files/@@listing', '/genome-browser-annotation-files/@@listing', '/image-files/@@listing', '/matrix-files/@@listing', '/model-files/@@listing', '/reference-files/@@listing', '/sequence-files/@@listing', '/signal-files/@@listing', '/tabular-files/@@listing', '/analysis-sets/@@listing', '/auxiliary-sets/@@listing', '/construct-library-sets/@@listing', '/curated-sets/@@listing', '/measurement-sets/@@listing', '/model-sets/@@listing', '/prediction-sets/@@listing', '/genes/@@listing', '/images/@@listing', '/institutional-certificates/@@listing', '/labs/@@listing', '/crispr-modifications/@@listing', '/degron-modifications/@@listing', '/assay-terms/@@listing', '/phenotype-terms/@@listing', '/platform-terms/@@listing', '/sample-terms/@@listing', '/open-reading-frames/@@listing', '/pages/@@listing', '/phenotypic-features/@@listing', '/publications/@@listing', '/in-vitro-systems/@@listing', '/multiplexed-samples/@@listing', '/primary-cells/@@listing', '/technical-samples/@@listing', '/tissues/@@listing', '/whole-organisms/@@listing', '/software/@@listing', '/software-versions/@@listing', '/sources/@@listing', '/treatments/@@listing', '/users/@@listing', '/workflows/@@listing']
    actual_keys = openapi_spec['paths'].keys()
    assert set(expected_keys) == set(actual_keys)
    expected_keys = ['query', 'frame', 'limit', 'sort', '@id', 'aliases', 'component', 'contact_pi', 'creation_timestamp', 'description', 'end_date', 'name', 'notes', 'pis', 'project', 'start_date', 'status', 'submitted_by.@id', 'submitted_by.title', 'submitter_comment', 'summary', 'title', 'url', 'uuid', 'viewing_group']
    actual_keys = [x['name'] for x in openapi_spec['paths']['/awards/@@listing']['get']['parameters']]
    assert set(expected_keys) == set(actual_keys)
    expected_keys = ['query', 'frame', 'limit', 'sort', '@id', 'accession', 'aliases', 'alternate_accessions', 'assay_term.@id', 'assay_term.term_name', 'auxiliary_sets.@id', 'auxiliary_sets.accession', 'auxiliary_sets.aliases', 'auxiliary_sets.file_set_type', 'award.@id', 'award.component', 'award.contact_pi.@id', 'award.contact_pi.title', 'award.title', 'collections', 'control_file_sets.@id', 'control_file_sets.accession', 'control_file_sets.aliases', 'control_for.@id', 'control_for.accession', 'control_for.aliases', 'creation_timestamp', 'dbxrefs', 'description', 'documents', 'donors.@id', 'donors.accession', 'donors.aliases', 'donors.sex', 'donors.status', 'donors.taxa', 'external_image_url', 'file_set_type', 'files.@id', 'files.accession', 'files.aliases', 'files.content_type', 'files.creation_timestamp', 'files.file_format', 'files.file_size', 'files.href', 'files.s3_uri', 'files.sequencing_platform.@id', 'files.sequencing_platform.term_name', 'files.submitted_file_name', 'files.upload_status', 'input_file_set_for', 'lab.@id', 'lab.title', 'multiome_size', 'notes', 'preferred_assay_title', 'protocols', 'publications.@id', 'publications.publication_identifiers', 'related_multiome_datasets.@id', 'related_multiome_datasets.accession', 'release_timestamp', 'revoke_detail', 'samples.@id', 'samples.accession', 'samples.aliases', 'samples.cell_fate_change_treatments.@id', 'samples.cell_fate_change_treatments.purpose', 'samples.cell_fate_change_treatments.summary', 'samples.cell_fate_change_treatments.treatment_type', 'samples.classifications', 'samples.construct_library_sets.@id', 'samples.construct_library_sets.accession', 'samples.construct_library_sets.file_set_type', 'samples.construct_library_sets.small_scale_gene_list.@id', 'samples.construct_library_sets.small_scale_gene_list.geneid', 'samples.construct_library_sets.small_scale_gene_list.name', 'samples.construct_library_sets.small_scale_gene_list.summary', 'samples.construct_library_sets.small_scale_gene_list.symbol', 'samples.construct_library_sets.summary', 'samples.disease_terms.@id', 'samples.disease_terms.term_name', 'samples.modifications.@id', 'samples.sample_terms.@id', 'samples.sample_terms.aliases', 'samples.sample_terms.status', 'samples.sample_terms.summary', 'samples.sample_terms.term_name', 'samples.status', 'samples.summary', 'samples.targeted_sample_term.@id', 'samples.targeted_sample_term.term_name', 'samples.taxa', 'samples.treatments.@id', 'samples.treatments.purpose', 'samples.treatments.summary', 'samples.treatments.treatment_type', 'sequencing_library_types', 'status', 'submitted_by.@id', 'submitted_by.title', 'submitted_files_timestamp', 'submitter_comment', 'summary', 'targeted_genes.@id', 'targeted_genes.geneid', 'targeted_genes.name', 'targeted_genes.symbol', 'targeted_genes.synonyms', 'uuid']
    actual_keys = [x['name'] for x in openapi_spec['paths']['/measurement-sets/@@listing']['get']['parameters']]
    assert set(expected_keys) == set(actual_keys)


def test_generator_clean_schema(raw_schemas):
    from generator.generate import clean_schema
    award = raw_schemas['Award']
    clean_award = clean_schema(award)
    assert clean_award['properties']['submitted_by'] == {
        "title": "Submitted By",
        "description": "The user who submitted the object.",
        "type": "string"
    }
    assert clean_award['properties']['pis'] == {
        "title": "Principal Investigators",
        "description": "Principal Investigator(s) of the grant.",
        "type": "array",
        "uniqueItems": True,
        "items": {
            "title": "Investigator",
            "description": "User object of the investigator.",
            "type": "string"
        }
    }


def test_generator_normalize_schema(raw_schemas):
    from generator.generate import clean_schema
    from generator.generate import normalize_schemas
    sequence_file = raw_schemas['SequenceFile']
    clean_sequence_file = clean_schema(sequence_file)
    normalized_sequence_file = normalize_schemas({"SequenceFile": clean_sequence_file})
    assert sequence_file['properties']['content_type'] ==  {
        "title": "Content Type",
        "description": "The type of content in the file.",
        "comment": "Content Type describes the content of the file. Reads are individual sequences of bases corresponding to DNA or RNA fragments in a FASTQ text file format. Subreads are sequences of bases produced using PacBio platforms.",
        "type": "string",
        "submissionExample": {
            "appscript": "reads",
            "igvf_utils": "reads"
        },
        "enum": [
            "Nanopore reads",
            "PacBio subreads",
            "reads"
        ]
    }
    assert normalized_sequence_file['SequenceFile']['properties']['content_type'] == {
        "title": "Content Type",
        "description": "The type of content in the file.",
        "type": "string"
    }


def test_generator_get_slim_embedded_fields(raw_schemas, raw_embedded_fields):
    from generator.generate import get_slim_embedded_fields
    slim_embedded_fields = get_slim_embedded_fields(raw_embedded_fields, raw_schemas)
    actual_keys = slim_embedded_fields['MeasurementSet'].keys()
    expected_keys = [
        'assay_term.@id',
        'assay_term.term_name',
        'auxiliary_sets.@id',
        'auxiliary_sets.accession',
        'auxiliary_sets.aliases',
        'auxiliary_sets.file_set_type',
        'award.@id',
        'award.component',
        'award.contact_pi.@id',
        'award.contact_pi.title',
        'award.title',
        'control_file_sets.@id',
        'control_file_sets.accession',
        'control_file_sets.aliases',
        'control_for.@id',
        'control_for.accession',
        'control_for.aliases',
        'donors.@id',
        'donors.accession',
        'donors.aliases',
        'donors.sex',
        'donors.status',
        'donors.taxa',
        'files.@id',
        'files.accession',
        'files.aliases',
        'files.content_type',
        'files.creation_timestamp',
        'files.file_format',
        'files.file_size',
        'files.href',
        'files.s3_uri',
        'files.sequencing_platform.@id',
        'files.sequencing_platform.term_name',
        'files.submitted_file_name',
        'files.upload_status',
        'lab.@id',
        'lab.title',
        'publications.@id',
        'publications.publication_identifiers',
        'related_multiome_datasets.@id',
        'related_multiome_datasets.accession',
        'samples.@id',
        'samples.@type',
        'samples.accession',
        'samples.aliases',
        'samples.cell_fate_change_treatments.@id',
        'samples.cell_fate_change_treatments.purpose',
        'samples.cell_fate_change_treatments.summary',
        'samples.cell_fate_change_treatments.treatment_type',
        'samples.classifications',
        'samples.construct_library_sets.@id',
        'samples.construct_library_sets.accession',
        'samples.construct_library_sets.file_set_type',
        'samples.construct_library_sets.small_scale_gene_list.@id',
        'samples.construct_library_sets.small_scale_gene_list.geneid',
        'samples.construct_library_sets.small_scale_gene_list.name',
        'samples.construct_library_sets.small_scale_gene_list.summary',
        'samples.construct_library_sets.small_scale_gene_list.symbol',
        'samples.construct_library_sets.summary',
        'samples.disease_terms.@id',
        'samples.disease_terms.term_name',
        'samples.modifications.@id',
        'samples.sample_terms.@id',
        'samples.sample_terms.@type',
        'samples.sample_terms.aliases',
        'samples.sample_terms.status',
        'samples.sample_terms.summary',
        'samples.sample_terms.term_name',
        'samples.status',
        'samples.summary',
        'samples.targeted_sample_term.@id',
        'samples.targeted_sample_term.term_name',
        'samples.taxa',
        'samples.treatments.@id',
        'samples.treatments.purpose',
        'samples.treatments.summary',
        'samples.treatments.treatment_type',
        'submitted_by.@id',
        'submitted_by.title',
        'targeted_genes.@id',
        'targeted_genes.geneid',
        'targeted_genes.name',
        'targeted_genes.symbol',
        'targeted_genes.synonyms'
    ]
    assert set(actual_keys) == set(expected_keys)
    assert slim_embedded_fields['MeasurementSet']['samples.targeted_sample_term.term_name'] == {
        'path': 'samples.targeted_sample_term.term_name',
        'schema': {
            'title': 'Term Name',
            'description': 'Ontology term describing a biological sample, assay, trait, or disease.',
            'comment': 'The term should match the term identifiers specified in term_id.',
            'permission': 'admin_only',
            'pattern': '^(?![\\s"\'])[\\S|\\s]*[^\\s"\']$',
            'type': 'string',
            'readonly': True
        },
        'is_an_item': True
    }
    assert slim_embedded_fields['MeasurementSet']['lab.@id'] == {
        'path': 'lab.@id',
        'schema': {
            'title': 'ID',
            'type': 'string',
            'notSubmittable': True
        },
        'is_an_item': False
    }
    assert slim_embedded_fields['MeasurementSet']['files.creation_timestamp'] == {
        'path': 'files.creation_timestamp',
        'schema': {
            'rdfs:subPropertyOf': 'dc:created',
            'title': 'Creation Timestamp',
            'description': 'The date the object was created.',
            'comment': 'Do not submit. The date the object is created is assigned by the server.',
            'type': 'string',
            'format': 'date-time',
            'serverDefault': 'now',
            'permission': 'admin_only'
        },
        'is_an_item': True
    }


def test_generator_simple_traverse():
    from generator.generate import traverse
    schemas = {
        'Custom': {
            'properties': {
                'thing': {
                    'type': 'string',
                    'linkTo': 'Thing'
                },
                '@id': {
                    'type': 'string',
                    'title': 'A Custom @id',
                }
            }
        },
        'Thing': {
            'properties': {
                'title': {
                    'type': 'string',
                    'title': 'A Thing title'
                },
                '@id': {
                    'type': 'string',
                    'title': 'A Thing @id'
                }
            }
        }
    }
    properties = {'some': {'type': 'string', 'linkTo': 'Custom'}}
    actual = traverse(schemas, properties, 'some.thing', ['@id', 'some', 'thing', 'title'], [])
    expected =  [
        {'path': 'some.@id', 'schema': {'type': 'string', 'title': 'A Custom @id'}, 'is_an_item': False},
        {'path': 'some.thing', 'schema': {'type': 'string', 'linkTo': 'Thing'}, 'is_an_item': False},
        {'path': 'some.thing.@id', 'schema': {'type': 'string', 'title': 'A Thing @id'}, 'is_an_item': False},
        {'path': 'some.thing.title', 'schema': {'type': 'string', 'title': 'A Thing title'}, 'is_an_item': False}
    ]
    assert expected == actual


def test_generator_raw_schema_traverse(raw_schemas):
    from generator.generate import traverse
    properties = {'award': {'type': 'string', 'linkTo': 'Award'}}
    actual = traverse(raw_schemas, properties, 'award.pis.submits_for.submitted_by.lab', ['@id', 'pis', 'title', 'submits_for', 'lab', 'submitted_by'], [])
    expected = [
        {'path': 'award.@id', 'schema': {'title': 'ID', 'type': 'string', 'notSubmittable': True}, 'is_an_item': False},
        {'path': 'award.pis', 'schema': {'title': 'Principal Investigators', 'description': 'Principal Investigator(s) of the grant.', 'comment': 'See user.json for available identifiers.', 'type': 'array', 'minItems': 1, 'uniqueItems': True, 'items': {'title': 'Investigator', 'description': 'User object of the investigator.', 'type': 'string', 'linkTo': 'User'}, 'submissionExample': {'appscript': '["/users/f73829f9-e8a0-4f16-861d-275e7ac392d3/", "login_name@email.edu"]', 'igvf_utils': '/users/f73829f9-e8a0-4f16-861d-275e7ac392d3/, login_name@email.edu'}}, 'is_an_item': False},
        {'path': 'award.title', 'schema': {'rdfs:subPropertyOf': 'dc:title', 'title': 'Title', 'description': 'The grant name from the NIH database, if applicable.', 'type': 'string', 'pattern': '^(\\S+(\\s|\\S)*\\S+|\\S)$', 'submissionExample': {'appscript': 'A Data and Administrative Coordinating Center for the Impact of Genomic Variation on Function Consortium', 'igvf_utils': 'A Data and Administrative Coordinating Center for the Impact of Genomic Variation on Function Consortium'}}, 'is_an_item': False},
        {'path': 'award.submitted_by', 'schema': {'rdfs:subPropertyOf': 'dc:creator', 'title': 'Submitted By', 'description': 'The user who submitted the object.', 'comment': 'Do not submit. The user that created the object is assigned by the server.', 'type': 'string', 'linkTo': 'User', 'serverDefault': 'userid', 'permission': 'admin_only', 'readonly': True}, 'is_an_item': False},
        {'path': 'award.pis.@id', 'schema': {'title': 'ID', 'type': 'string', 'notSubmittable': True}, 'is_an_item': True},
        {'path': 'award.pis.title', 'schema': {'title': 'Title', 'type': 'string', 'description': 'The full name of the user.', 'notSubmittable': True}, 'is_an_item': True},
        {'path': 'award.pis.submits_for', 'schema': {'title': 'Submits For', 'description': 'Labs user is authorized to submit data for.', 'type': 'array', 'minItems': 1, 'uniqueItems': True, 'permission': 'admin_only', 'items': {'title': 'Lab Submittable For', 'description': 'A lab user is authorized to submit for.', 'comment': 'See lab.json for available identifiers.', 'type': 'string', 'linkTo': 'Lab'}, 'readonly': True}, 'is_an_item': True}, {'path': 'award.pis.lab', 'schema': {'title': 'Lab', 'description': 'Lab user is primarily associated with.', 'comment': 'See lab.json for available identifiers.', 'permission': 'admin_only', 'type': 'string', 'linkTo': 'Lab', 'readonly': True}, 'is_an_item': True},
        {'path': 'award.pis.submitted_by', 'schema': {'rdfs:subPropertyOf': 'dc:creator', 'title': 'Submitted By', 'description': 'The user who submitted the object.', 'comment': 'Do not submit. The user that created the object is assigned by the server.', 'type': 'string', 'linkTo': 'User', 'serverDefault': 'userid', 'permission': 'admin_only', 'readonly': True}, 'is_an_item': True}, {'path': 'award.pis.submits_for.@id', 'schema': {'title': 'ID', 'type': 'string', 'notSubmittable': True}, 'is_an_item': True},
        {'path': 'award.pis.submits_for.title', 'schema': {'title': 'Title', 'type': 'string', 'notSubmittable': True}, 'is_an_item': True},
        {'path': 'award.pis.submits_for.submitted_by', 'schema': {'rdfs:subPropertyOf': 'dc:creator', 'title': 'Submitted By', 'description': 'The user who submitted the object.', 'comment': 'Do not submit. The user that created the object is assigned by the server.', 'type': 'string', 'linkTo': 'User', 'serverDefault': 'userid', 'permission': 'admin_only', 'readonly': True}, 'is_an_item': True},
        {'path': 'award.pis.submits_for.submitted_by.@id', 'schema': {'title': 'ID', 'type': 'string', 'notSubmittable': True}, 'is_an_item': True}, {'path': 'award.pis.submits_for.submitted_by.title', 'schema': {'title': 'Title', 'type': 'string', 'description': 'The full name of the user.', 'notSubmittable': True}, 'is_an_item': True},
        {'path': 'award.pis.submits_for.submitted_by.submits_for', 'schema': {'title': 'Submits For', 'description': 'Labs user is authorized to submit data for.', 'type': 'array', 'minItems': 1, 'uniqueItems': True, 'permission': 'admin_only', 'items': {'title': 'Lab Submittable For', 'description': 'A lab user is authorized to submit for.', 'comment': 'See lab.json for available identifiers.', 'type': 'string', 'linkTo': 'Lab'}, 'readonly': True}, 'is_an_item': True},
        {'path': 'award.pis.submits_for.submitted_by.lab', 'schema': {'title': 'Lab', 'description': 'Lab user is primarily associated with.', 'comment': 'See lab.json for available identifiers.', 'permission': 'admin_only', 'type': 'string', 'linkTo': 'Lab', 'readonly': True}, 'is_an_item': True},
        {'path': 'award.pis.submits_for.submitted_by.submitted_by', 'schema': {'rdfs:subPropertyOf': 'dc:creator', 'title': 'Submitted By', 'description': 'The user who submitted the object.', 'comment': 'Do not submit. The user that created the object is assigned by the server.', 'type': 'string', 'linkTo': 'User', 'serverDefault': 'userid', 'permission': 'admin_only', 'readonly': True}, 'is_an_item': True},
        {'path': 'award.pis.submits_for.submitted_by.lab.@id', 'schema': {'title': 'ID', 'type': 'string', 'notSubmittable': True}, 'is_an_item': True},
        {'path': 'award.pis.submits_for.submitted_by.lab.title', 'schema': {'title': 'Title', 'type': 'string', 'notSubmittable': True}, 'is_an_item': True},
        {'path': 'award.pis.submits_for.submitted_by.lab.submitted_by', 'schema': {'rdfs:subPropertyOf': 'dc:creator', 'title': 'Submitted By', 'description': 'The user who submitted the object.', 'comment': 'Do not submit. The user that created the object is assigned by the server.', 'type': 'string', 'linkTo': 'User', 'serverDefault': 'userid', 'permission': 'admin_only', 'readonly': True}, 'is_an_item': True}
    ]
    assert actual == expected
    all_fields = set(f['path'] for f in expected)
    to_remove_fields = []
    for e in expected:
        name = e['path']
        for field in all_fields:
            if field.startswith(name) and len(name) != len(field):
                to_remove_fields.append(name)
    actual = [e for e in expected if e['path'] not in to_remove_fields]
    expected = [
        {'path': 'award.@id', 'schema': {'title': 'ID', 'type': 'string', 'notSubmittable': True}, 'is_an_item': False},
        {'path': 'award.title', 'schema': {'rdfs:subPropertyOf': 'dc:title', 'title': 'Title', 'description': 'The grant name from the NIH database, if applicable.', 'type': 'string', 'pattern': '^(\\S+(\\s|\\S)*\\S+|\\S)$', 'submissionExample': {'appscript': 'A Data and Administrative Coordinating Center for the Impact of Genomic Variation on Function Consortium', 'igvf_utils': 'A Data and Administrative Coordinating Center for the Impact of Genomic Variation on Function Consortium'}}, 'is_an_item': False}, {'path': 'award.submitted_by', 'schema': {'rdfs:subPropertyOf': 'dc:creator', 'title': 'Submitted By', 'description': 'The user who submitted the object.', 'comment': 'Do not submit. The user that created the object is assigned by the server.', 'type': 'string', 'linkTo': 'User', 'serverDefault': 'userid', 'permission': 'admin_only', 'readonly': True}, 'is_an_item': False},
        {'path': 'award.pis.@id', 'schema': {'title': 'ID', 'type': 'string', 'notSubmittable': True}, 'is_an_item': True}, {'path': 'award.pis.title', 'schema': {'title': 'Title', 'type': 'string', 'description': 'The full name of the user.', 'notSubmittable': True}, 'is_an_item': True},
        {'path': 'award.pis.lab', 'schema': {'title': 'Lab', 'description': 'Lab user is primarily associated with.', 'comment': 'See lab.json for available identifiers.', 'permission': 'admin_only', 'type': 'string', 'linkTo': 'Lab', 'readonly': True}, 'is_an_item': True},
        {'path': 'award.pis.submitted_by', 'schema': {'rdfs:subPropertyOf': 'dc:creator', 'title': 'Submitted By', 'description': 'The user who submitted the object.', 'comment': 'Do not submit. The user that created the object is assigned by the server.', 'type': 'string', 'linkTo': 'User', 'serverDefault': 'userid', 'permission': 'admin_only', 'readonly': True}, 'is_an_item': True},
        {'path': 'award.pis.submits_for.@id', 'schema': {'title': 'ID', 'type': 'string', 'notSubmittable': True}, 'is_an_item': True},
        {'path': 'award.pis.submits_for.title', 'schema': {'title': 'Title', 'type': 'string', 'notSubmittable': True}, 'is_an_item': True},
        {'path': 'award.pis.submits_for.submitted_by.@id', 'schema': {'title': 'ID', 'type': 'string', 'notSubmittable': True}, 'is_an_item': True},
        {'path': 'award.pis.submits_for.submitted_by.title', 'schema': {'title': 'Title', 'type': 'string', 'description': 'The full name of the user.', 'notSubmittable': True}, 'is_an_item': True},
        {'path': 'award.pis.submits_for.submitted_by.submits_for', 'schema': {'title': 'Submits For', 'description': 'Labs user is authorized to submit data for.', 'type': 'array', 'minItems': 1, 'uniqueItems': True, 'permission': 'admin_only', 'items': {'title': 'Lab Submittable For', 'description': 'A lab user is authorized to submit for.', 'comment': 'See lab.json for available identifiers.', 'type': 'string', 'linkTo': 'Lab'}, 'readonly': True}, 'is_an_item': True},
        {'path': 'award.pis.submits_for.submitted_by.submitted_by', 'schema': {'rdfs:subPropertyOf': 'dc:creator', 'title': 'Submitted By', 'description': 'The user who submitted the object.', 'comment': 'Do not submit. The user that created the object is assigned by the server.', 'type': 'string', 'linkTo': 'User', 'serverDefault': 'userid', 'permission': 'admin_only', 'readonly': True}, 'is_an_item': True}, {'path': 'award.pis.submits_for.submitted_by.lab.@id', 'schema': {'title': 'ID', 'type': 'string', 'notSubmittable': True}, 'is_an_item': True},
        {'path': 'award.pis.submits_for.submitted_by.lab.title', 'schema': {'title': 'Title', 'type': 'string', 'notSubmittable': True}, 'is_an_item': True},
        {'path': 'award.pis.submits_for.submitted_by.lab.submitted_by', 'schema': {'rdfs:subPropertyOf': 'dc:creator', 'title': 'Submitted By', 'description': 'The user who submitted the object.', 'comment': 'Do not submit. The user that created the object is assigned by the server.', 'type': 'string', 'linkTo': 'User', 'serverDefault': 'userid', 'permission': 'admin_only', 'readonly': True}, 'is_an_item': True}
    ]
    assert actual == expected

'''

 import json
    print(json.dumps(sequence_file, indent=4))
    print('aa;lsdkjf;oafskjsda!!!!!\n\n')
    print(json.dumps(normalized_sequence_file, indent=4))
def test_generator_generate_openapi_spec(schemas, schema_names_to_collection_names, slim_embedded_fields):



def test_generator_get_properties_for_item_type(schemas, item_type):


def test_generator_traverse(all_schemas, properties, path, include, exclude, is_an_item=False, processed=None):


# copied from snovault
def test_generator_ensurelist(value):


# copied from snovault
def test_generator_combine_schemas(a, b):


def test_generator_fill_in_collection_template(schema_name, schema, schema_names_to_collection_names, slim_embedded_fields):


def test_generator_property_is_slim_embedded(prop, embedded_fields_keys):



def test_generator_get_slim_embedded_fields():


def test_generator_get_schema_names_to_collection_names(schema_keys):


def test_generator_clean_schemas(schemas):


def test_generator_get_schemas():


def test_generator_generate():

'''
