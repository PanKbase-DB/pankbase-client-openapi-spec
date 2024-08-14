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


def test_generator_ensurelist():
    from generator.generate import ensurelist
    result = ensurelist('a')
    assert result == ['a']


def test_generator_combine_schemas(raw_schemas):
    from generator.generate import combine_schemas
    assert combine_schemas({}, {}) == {}
    actual = combine_schemas(raw_schemas['AccessKey'], raw_schemas['User'])
    expected_keys = set(
        [
            'schema_version',
            'submitter_comment',
            'notes',
            'status',
            'description',
            'summary',
            'aliases',
            '@id',
            'creation_timestamp',
            '@type',
            'submitted_by',
            'uuid',
            'user',
            'secret_access_key_hash',
            'access_key_id',
            'first_name',
            'job_title',
            'submits_for',
            'lab',
            'viewing_groups',
            'email',
            'last_name',
            'groups',
            'title'
        ]
    )
    assert set(actual['properties'].keys()) == expected_keys


def test_generator_property_is_slim_embedded(raw_embedded_fields, raw_schemas):
    from generator.generate import get_slim_embedded_fields
    from generator.generate import property_is_slim_embedded
    slim_embedded_fields = get_slim_embedded_fields(raw_embedded_fields, raw_schemas)
    slim_embedded_keys = slim_embedded_fields['MeasurementSet'].keys()
    assert not property_is_slim_embedded('abc', slim_embedded_keys)
    assert property_is_slim_embedded('assay_term.term_name', slim_embedded_keys)
    assert property_is_slim_embedded(
        'samples.construct_library_sets.small_scale_gene_list.name',
        slim_embedded_keys
    )


def test_generator_fill_in_collection_template(raw_schemas, raw_embedded_fields, collection_names):
    from generator.generate import fill_in_collection_template, get_slim_embedded_fields
    from generator.generate import normalize_schemas, clean_schemas
    schemas = normalize_schemas(clean_schemas(raw_schemas))
    slim_embedded_fields = get_slim_embedded_fields(raw_embedded_fields, raw_schemas)
    actual = fill_in_collection_template('SequenceFile', schemas['SequenceFile'], collection_names, slim_embedded_fields)
    expected = {
        '/sequence-files/@@listing': {
            'get': {
                'tags': ['Collections'],
                'summary': 'List items in the SequenceFile collection.',
                'description': 'Collection endpoint that accepts various query parameters to filter, sort, and paginate SequenceFile items. Supports filtering on fields within SequenceFile items.', 'operationId': 'sequence_files',
                'parameters': [
                    {'name': 'query', 'in': 'query', 'schema': {'type': 'string'}, 'description': 'Query string for searching.', 'example': 'variant flowfish jurkat'},
                    {'name': 'frame', 'in': 'query', 'required': True, 'schema': {'type': 'string', 'enum': ['object']}, 'description': 'Constant value. Do not set.'},
                    {'name': 'limit', 'in': 'query', 'schema': {'$ref': '#/components/schemas/Limit'}, 'description': "Maximum number of results to return. Default is 25. Use 'all' for all results.", 'examples': {'number': {'value': 100}, 'all': {'value': 'all'}}},
                    {'name': 'sort', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'string'}}, 'style': 'form', 'explode': True, 'description': "Fields to sort results by. Prefix with '-' for descending order. Can be repeated for multiple sort fields. Does not work with limit=all.", 'examples': {'file_size': {'value': '-file_size'}, 'lab': {'value': 'lab.title'}}},
                    {'name': '@id', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'string', 'title': 'ID'}}, 'description': 'Filter by @id', 'style': 'form', 'explode': True},
                    {'name': 'accession', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'string', 'title': 'Accession', 'description': 'A unique identifier to be used to reference the object prefixed with IGVF.'}}, 'description': 'Filter by accession', 'style': 'form', 'explode': True},
                    {'name': 'aliases', 'in': 'query', 'schema': {'type': 'array', 'title': 'Aliases', 'items': {'type': 'string', 'title': 'Lab Alias', 'pattern': "^(?:j-michael-cherry|ali-mortazavi|barbara-wold|lior-pachter|grant-macgregor|kim-green|mark-craven|qiongshi-lu|audrey-gasch|robert-steiner|jesse-engreitz|thomas-quertermous|anshul-kundaje|michael-bassik|will-greenleaf|marlene-rabinovitch|lars-steinmetz|jay-shendure|nadav-ahituv|martin-kircher|danwei-huangfu|michael-beer|anna-katerina-hadjantonakis|christina-leslie|alexander-rudensky|laura-donlin|hannah-carter|bing-ren|kyle-gaulton|maike-sander|charles-gersbach|gregory-crawford|tim-reddy|ansuman-satpathy|andrew-allen|gary-hon|nikhil-munshi|maria-chahrour|w-lee-kraus|lea-starita|doug-fowler|luca-pinello|guillaume-lettre|benhur-lee|daniel-bauer|richard-sherwood|benjamin-kleinstiver|marc-vidal|david-hill|frederick-roth|mikko-taipale|anne-carpenter|hyejung-won|karen-mohlke|michael-love|jason-buenrostro|bradley-bernstein|hilary-finucane|chongyuan-luo|noah-zaitlen|kathrin-plath|roy-wollman|jason-ernst|zhiping-weng|manuel-garber|xihong-lin|alan-boyle|ryan-mills|jie-liu|maureen-sartor|joshua-welch|stephen-montgomery|alexis-battle|livnat-jerby|jonathan-pritchard|predrag-radivojac|sean-mooney|harinder-singh|nidhi-sahni|jishnu-das|hao-wu|sreeram-kannan|hongjun-song|alkes-price|soumya-raychaudhuri|shamil-sunyaev|len-pennacchio|axel-visel|jill-moore|ting-wang|feng-yue|buenrostro-bernstein|igvf|igvf-dacc):[a-zA-Z\\d_$.+!*,()'-]+(?:\\s[a-zA-Z\\d_$.+!*,()'-]+)*$", 'description': 'A lab specific identifier to reference an object.'}, 'description': 'Lab specific identifiers to reference an object.'}, 'description': 'Filter by aliases', 'style': 'form', 'explode': True},
                    {'name': 'alternate_accessions', 'in': 'query', 'schema': {'type': 'array', 'title': 'Alternate Accessions', 'items': {'type': 'string', 'title': 'Alternate Accession', 'description': 'An accession previously assigned to an object that has been merged with this object.'}, 'description': 'Accessions previously assigned to objects that have been merged with this object.'}, 'description': 'Filter by alternate_accessions', 'style': 'form', 'explode': True},
                    {'name': 'analysis_step_version', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'string', 'title': 'Analysis Step Version', 'description': 'The analysis step version of the file.'}}, 'description': 'Filter by analysis_step_version', 'style': 'form', 'explode': True},
                    {'name': 'anvil_url', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'string', 'title': 'AnVIL URL', 'description': 'URL linking to the controlled access file that has been deposited at AnVIL workspace.'}}, 'description': 'Filter by anvil_url', 'style': 'form', 'explode': True},
                    {'name': 'award.@id', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'string', 'title': 'ID'}}, 'description': 'Filter by award.@id', 'style': 'form', 'explode': True},
                    {'name': 'award.component', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'string', 'title': 'Project Component', 'description': 'The project component the award is associated with.'}}, 'description': 'Filter by award.component', 'style': 'form', 'explode': True},
                    {'name': 'base_modifications', 'in': 'query', 'schema': {'type': 'array', 'title': 'Base Modifications', 'items': {'type': 'string', 'title': 'Base Modification', 'enum': ['4mC', '5hmC', '5mC', '6mA'], 'description': 'The chemical modification to bases in a DNA sequence that is detected in this file.'}, 'description': 'The chemical modifications to bases in a DNA sequence that are detected in this file.'}, 'description': 'Filter by base_modifications', 'style': 'form', 'explode': True},
                    {'name': 'collections', 'in': 'query', 'schema': {'type': 'array', 'title': 'Collections', 'items': {'type': 'string', 'enum': ['ClinGen', 'ENCODE', 'GREGoR', 'IGVF_catalog_beta_v0.1', 'IGVF_catalog_beta_v0.2', 'IGVF_catalog_beta_v0.3', 'IGVF_catalog_beta_v0.4', 'MaveDB', 'MPRAbase', 'Vista']}, 'description': 'Some samples are part of particular data collections.'}, 'description': 'Filter by collections', 'style': 'form', 'explode': True},
                    {'name': 'content_md5sum', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'string', 'title': 'Content MD5sum', 'pattern': '[a-f\\d]{32}|[A-F\\d]{32}', 'maxLength': 32, 'description': 'The MD5sum of the uncompressed file.'}}, 'description': 'Filter by content_md5sum', 'style': 'form', 'explode': True},
                    {'name': 'content_type', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'string', 'title': 'Content Type', 'description': 'The type of content in the file.'}}, 'description': 'Filter by content_type', 'style': 'form', 'explode': True},
                    {'name': 'controlled_access', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'boolean', 'title': 'Controlled Access', 'description': 'Boolean value, indicating the file being controlled access, if true.'}}, 'description': 'Filter by controlled_access', 'style': 'form', 'explode': True},
                    {'name': 'creation_timestamp', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'string', 'title': 'Creation Timestamp', 'description': 'The date the object was created.'}}, 'description': 'Filter by creation_timestamp', 'style': 'form', 'explode': True},
                    {'name': 'dbxrefs', 'in': 'query', 'schema': {'type': 'array', 'title': 'External Resources', 'items': {'type': 'string', 'title': 'External identifier', 'pattern': '^(SRA:(SRR|SRX)\\d+)$', 'description': 'Identifier from an external resource that may have 1-to-1 or 1-to-many relationships with IGVF file objects.'}, 'description': 'Identifiers from external resources that may have 1-to-1 or 1-to-many relationships with IGVF file objects.'}, 'description': 'Filter by dbxrefs', 'style': 'form', 'explode': True},
                    {'name': 'derived_from', 'in': 'query', 'schema': {'type': 'array', 'title': 'Derived From', 'items': {'type': 'string', 'title': 'File Derived From'}, 'description': 'The files participating as inputs into software to produce this output file.'}, 'description': 'Filter by derived_from', 'style': 'form', 'explode': True},
                    {'name': 'description', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'string', 'title': 'Description', 'pattern': '^(\\S+(\\s|\\S)*\\S+|\\S)$', 'description': 'A plain text description of the object.'}}, 'description': 'Filter by description', 'style': 'form', 'explode': True},
                    {'name': 'documents', 'in': 'query', 'schema': {'type': 'array', 'title': 'Documents', 'items': {'type': 'string', 'title': 'Document', 'description': 'A document that provides additional information (not data file).'}, 'description': 'Documents that provide additional information (not data file).'}, 'description': 'Filter by documents', 'style': 'form', 'explode': True},
                    {'name': 'file_format', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'string', 'title': 'File Format', 'enum': ['bam', 'fastq', 'pod5'], 'description': 'The file format or extension of the file.'}}, 'description': 'Filter by file_format', 'style': 'form', 'explode': True},
                    {'name': 'file_format_specifications', 'in': 'query', 'schema': {'type': 'array', 'title': 'File Format Specifications Documents', 'items': {'type': 'string', 'title': 'File Format Specifications Document'}, 'description': 'Document that further explains the file format.'}, 'description': 'Filter by file_format_specifications', 'style': 'form', 'explode': True},
                    {'name': 'file_set', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'string', 'title': 'File Set', 'description': 'The file set that this file belongs to.'}}, 'description': 'Filter by file_set', 'style': 'form', 'explode': True},
                    {'name': 'file_size', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'integer', 'title': 'File Size', 'minimum': 0, 'description': 'File size specified in bytes.'}}, 'description': 'Filter by file_size', 'style': 'form', 'explode': True},
                    {'name': 'flowcell_id', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'string', 'title': 'Flowcell ID', 'pattern': '^[a-zA-Z0-9-]+$', 'description': 'The alphanumeric identifier for the flowcell of a sequencing machine.'}}, 'description': 'Filter by flowcell_id', 'style': 'form', 'explode': True},
                    {'name': 'gene_list_for', 'in': 'query', 'schema': {'type': 'array', 'title': 'Gene List For', 'items': {'type': 'string', 'title': 'Gene List For'}, 'description': 'File Set(s) that this file is a gene list for.'}, 'description': 'Filter by gene_list_for', 'style': 'form', 'explode': True},
                    {'name': 'href', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'string', 'title': 'Download URL', 'description': 'The download path to obtain file.'}}, 'description': 'Filter by href', 'style': 'form', 'explode': True},
                    {'name': 'illumina_read_type', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'string', 'title': 'Illumina Read Type', 'enum': ['R1', 'R2', 'R3', 'I1', 'I2'], 'description': 'The read type of the file. Relevant only for files produced using an Illumina sequencing platform.'}}, 'description': 'Filter by illumina_read_type', 'style': 'form', 'explode': True},
                    {'name': 'index', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'string', 'title': 'Index', 'description': 'An Illumina index associated with the file.'}}, 'description': 'Filter by index', 'style': 'form', 'explode': True},
                    {'name': 'input_file_for', 'in': 'query', 'schema': {'type': 'array', 'title': 'Input File For', 'items': {'type': 'string', 'title': 'Input File For'}, 'description': 'The files which are derived from this file.'}, 'description': 'Filter by input_file_for', 'style': 'form', 'explode': True},
                    {'name': 'integrated_in', 'in': 'query', 'schema': {'type': 'array', 'title': 'Integrated In', 'items': {'type': 'string', 'title': 'Integrated In'}, 'description': 'Construct library set(s) that this file was used for in insert design.'}, 'description': 'Filter by integrated_in', 'style': 'form', 'explode': True},
                    {'name': 'lab.@id', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'string', 'title': 'ID'}}, 'description': 'Filter by lab.@id', 'style': 'form', 'explode': True},
                    {'name': 'lab.title', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'string', 'title': 'Title'}}, 'description': 'Filter by lab.title', 'style': 'form', 'explode': True},
                    {'name': 'lane', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'integer', 'title': 'Lane', 'minimum': 1, 'description': 'An integer identifying the lane of a sequencing machine.'}}, 'description': 'Filter by lane', 'style': 'form', 'explode': True},
                    {'name': 'loci_list_for', 'in': 'query', 'schema': {'type': 'array', 'title': 'Loci List For', 'items': {'type': 'string', 'title': 'Loci List For'}, 'description': 'File Set(s) that this file is a loci list for.'}, 'description': 'Filter by loci_list_for', 'style': 'form', 'explode': True},
                    {'name': 'maximum_read_length', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'integer', 'title': 'Maximum Read Length', 'minimum': 0, 'maximum': 300000000, 'description': 'For high-throughput sequencing, the maximum number of contiguous nucleotides determined by sequencing.'}}, 'description': 'Filter by maximum_read_length', 'style': 'form', 'explode': True},
                    {'name': 'md5sum', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'string', 'title': 'MD5sum', 'pattern': '[a-f\\d]{32}|[A-F\\d]{32}', 'maxLength': 32, 'description': 'The md5sum of the file being transferred.'}}, 'description': 'Filter by md5sum', 'style': 'form', 'explode': True},
                    {'name': 'mean_read_length', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'number', 'title': 'Mean Read Length', 'minimum': 0, 'maximum': 300000000, 'description': 'For high-throughput sequencing, the mean number of contiguous nucleotides determined by sequencing.'}}, 'description': 'Filter by mean_read_length', 'style': 'form', 'explode': True},
                    {'name': 'minimum_read_length', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'integer', 'title': 'Minimum Read Length', 'minimum': 0, 'maximum': 300000000, 'description': 'For high-throughput sequencing, the minimum number of contiguous nucleotides determined by sequencing.'}}, 'description': 'Filter by minimum_read_length', 'style': 'form', 'explode': True},
                    {'name': 'notes', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'string', 'title': 'Notes', 'pattern': '^(\\S+(\\s|\\S)*\\S+|\\S)$', 'description': 'DACC internal notes.'}}, 'description': 'Filter by notes', 'style': 'form', 'explode': True},
                    {'name': 'read_count', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'integer', 'title': 'Read Count', 'minimum': 0, 'description': 'Number of reads in a fastq file.'}}, 'description': 'Filter by read_count', 'style': 'form', 'explode': True},
                    {'name': 'release_timestamp', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'string', 'title': 'Release Timestamp', 'description': 'The date the object was released.'}}, 'description': 'Filter by release_timestamp', 'style': 'form', 'explode': True},
                    {'name': 'revoke_detail', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'string', 'title': 'Revoke Detail', 'pattern': '^(\\S+(\\s|\\S)*\\S+|\\S)$', 'description': 'Explanation of why an object was transitioned to the revoked status.'}}, 'description': 'Filter by revoke_detail', 'style': 'form', 'explode': True},
                    {'name': 's3_uri', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'string', 'title': 'S3 URI', 'description': 'The S3 URI of public file object.'}}, 'description': 'Filter by s3_uri', 'style': 'form', 'explode': True},
                    {'name': 'seqspecs', 'in': 'query', 'schema': {'type': 'array', 'title': 'Seqspecs', 'items': {'type': 'string', 'title': 'Seqspecs'}, 'description': 'Link(s) to the associated seqspec YAML configuration file(s).'}, 'description': 'Filter by seqspecs', 'style': 'form', 'explode': True},
                    {'name': 'sequencing_kit', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'string', 'title': 'Sequencing Kit', 'enum': ['HiSeq SBS Kit v4', 'HiSeq SR Cluster Kit v4-cBot-HS', 'HiSeq PE Cluster Kit v4-cBot-HS', 'HiSeq SR Rapid Cluster Kit v2', 'HiSeq PE Rapid Cluster Kit v2', 'HiSeq Rapid SBS Kit v2', 'HiSeq 3000/4000 SBS Kit', 'HiSeq 3000/4000 SR Cluster Kit', 'HiSeq 3000/4000 PE Cluster Kit', 'MiSeq Reagent Kit v2', 'NextSeq 500 Mid Output Kit', 'NextSeq 500 High Output Kit', 'NextSeq 500 Mid Output v2 Kit', 'NextSeq 500 High Output v2 Kit', 'NextSeq 500/550 Mid-Output v2.5 Kit', 'NextSeq 500/550 High-Output v2.5 Kit', 'TG NextSeq 500/550 Mid-Output Kit v2.5', 'TG NextSeq 500/550 High-Output Kit v2.5', 'NextSeq 1000/2000 P1 Reagent Kit', 'NextSeq 1000/2000 P2 Reagent Kit', 'NextSeq 1000/2000 P3 Reagent Kit', 'NextSeq 1000/2000 P1 XLEAP-SBS Reagent Kit', 'NextSeq 1000/2000 P2 XLEAP-SBS Reagent Kit', 'NextSeq 2000 P3 XLEAP-SBS Reagent Kit', 'NextSeq 2000 P4 XLEAP-SBS Reagent Kit', 'NovaSeq 6000 SP Reagent Kit v1.5', 'NovaSeq 6000 S1 Reagent Kit v1.5', 'NovaSeq 6000 S2 Reagent Kit v1.5', 'NovaSeq 6000 S4 Reagent Kit v1.5', 'NovaSeq X Series 1.5B Reagent Kit', 'NovaSeq X Series 10B Reagent Kit', 'NovaSeq X Series 25B Reagent Kit', 'ONT Ligation Sequencing Kit V14', 'Sequel sequencing kit 3.0', 'Sequel II sequencing kit 2.0'], 'description': 'A reagent kit used with a library to prepare it for sequencing.'}}, 'description': 'Filter by sequencing_kit', 'style': 'form', 'explode': True},
                    {'name': 'sequencing_platform', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'string', 'title': 'Sequencing Platform', 'description': 'The measurement device used to produce sequencing data.'}}, 'description': 'Filter by sequencing_platform', 'style': 'form', 'explode': True},
                    {'name': 'sequencing_run', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'integer', 'title': 'Sequencing Run', 'minimum': 1, 'description': 'An ordinal number indicating which sequencing run of the associated library that the file belongs to.'}}, 'description': 'Filter by sequencing_run', 'style': 'form', 'explode': True},
                    {'name': 'status', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'string', 'title': 'Status', 'enum': ['in progress', 'released', 'deleted', 'replaced', 'revoked', 'archived'], 'description': 'The status of the metadata object.'}}, 'description': 'Filter by status', 'style': 'form', 'explode': True},
                    {'name': 'submitted_by.@id', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'string', 'title': 'ID'}}, 'description': 'Filter by submitted_by.@id', 'style': 'form', 'explode': True},
                    {'name': 'submitted_by.title', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'string', 'title': 'Title', 'description': 'The full name of the user.'}}, 'description': 'Filter by submitted_by.title', 'style': 'form', 'explode': True},
                    {'name': 'submitted_file_name', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'string', 'title': 'Submitted File Name', 'description': 'Original name of the file.'}}, 'description': 'Filter by submitted_file_name', 'style': 'form', 'explode': True},
                    {'name': 'submitter_comment', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'string', 'title': 'Submitter Comment', 'pattern': '^(\\S+(\\s|\\S)*\\S+|\\S)$', 'description': 'Additional information specified by the submitter to be displayed as a comment on the portal.'}}, 'description': 'Filter by submitter_comment', 'style': 'form', 'explode': True},
                    {'name': 'summary', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'string', 'title': 'Summary', 'description': 'A summary of the sequence file.'}}, 'description': 'Filter by summary', 'style': 'form', 'explode': True},
                    {'name': 'upload_status', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'string', 'title': 'Upload Status', 'enum': ['pending', 'file not found', 'invalidated', 'validated'], 'description': 'The upload/validation status of the file.'}}, 'description': 'Filter by upload_status', 'style': 'form', 'explode': True},
                    {'name': 'uuid', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'string', 'title': 'UUID', 'description': 'The unique identifier associated with every object.'}}, 'description': 'Filter by uuid', 'style': 'form', 'explode': True},
                    {'name': 'validation_error_detail', 'in': 'query', 'schema': {'type': 'array', 'items': {'type': 'string', 'title': 'Validation Error Detail', 'description': 'Explanation of why the file failed the automated content checks.'}}, 'description': 'Filter by validation_error_detail', 'style': 'form', 'explode': True}
                ],
                'responses': {
                    '200': {'description': 'Successful response', 'content': {'application/json': {'schema': {'type': 'object', 'title': 'SequenceFileResults', 'properties': {'@graph': {'type': 'array', 'items': {'$ref': '#/components/schemas/SequenceFile'}}, '@id': {'type': 'string'}, '@type': {'type': 'array', 'items': {'type': 'string'}}, 'total': {'type': 'integer'}, 'facets': {'type': 'array', 'items': {'type': 'object', 'title': 'SearchFacet', 'properties': {'field': {'type': 'string'}, 'title': {'type': 'string'}, 'terms': {'type': 'array', 'items': {'title': 'SearchFacetTermValue', 'type': 'object'}}}}}}}}}}, '400': {'description': 'Bad request', 'content': {'application/json': {'schema': {'type': 'object'}}}},
                    '404': {'description': 'No results found', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/NoResultsResponse'}}}},
                    '500': {'description': 'Internal server error'}}
            }
        }
    }
    assert actual == expected


def test_generator_generate_snapshot(snapshot, raw_schemas, raw_embedded_fields, collection_names):
    import json
    from generator.generate import get_slim_embedded_fields, generate_openapi_spec
    from generator.generate import normalize_schemas, clean_schemas
    schemas = normalize_schemas(clean_schemas(raw_schemas))
    slim_embedded_fields = get_slim_embedded_fields(raw_embedded_fields, raw_schemas)
    spec = generate_openapi_spec(schemas, collection_names, slim_embedded_fields)
    snapshot.assert_match(
        json.dumps(
            spec,
            indent=4,
            sort_keys=True
        ),
        'openapi_spec_snapshot.json'
    )
