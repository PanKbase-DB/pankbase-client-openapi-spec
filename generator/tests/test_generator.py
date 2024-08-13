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


def test_generator_clean_schema(schemas):
    from generator.generate import clean_schema
    award = schemas['Award']
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


def test_generator_normalize_schema(schemas):
    from generator.generate import clean_schema
    from generator.generate import normalize_schemas
    sequence_file = schemas['SequenceFile']
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


def test_generator_clean_schema(schema):


def test_generator_normalize_schemas(schemas):


def test_generator_get_slim_embedded_fields():


def test_generator_get_schema_names_to_collection_names(schema_keys):


def test_generator_clean_schemas(schemas):


def test_generator_get_schemas():


def test_generator_generate():

'''
