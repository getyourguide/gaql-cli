"""Script for maintaining autocomplete.py"""
from gaql.lib.click_decorators.state import State
from gaql.lib.google_clients.config import setup_client
from gaql.lib.google_clients.queries import google_fields_query
from gaql.lib.output import to_dict
import json
import pathlib


def attributes_query(resource):
    return f"SELECT name WHERE category='ATTRIBUTE' AND name LIKE '{resource}.%'"


def resources_query():
    return "SELECT name, selectable_with WHERE category = 'RESOURCE'"


def autocomplete_fields():
    """Dumps entity fields from Google, building a single large JSON which provides the seed data for autocompletion"""
    state = State()
    state.format = 'json'

    client = setup_client()
    query_method = google_fields_query(client)

    resources_path = pathlib.Path('gaql/lib/google_clients/completion/entities.json')
    resource_rows = query_method(resources_query())
    resources = {resource.name: to_dict(resource._pb) for resource in resource_rows}
    if resources_path.exists():
        with resources_path.open('r') as f:
            existing_resources = json.load(f)
            for k in existing_resources:
                resources[k] = existing_resources[k]

    for resource_name, resource_dict in resources.items():
        if "fields" in resource_dict:
            continue
        print(f"Dumping {resource_name} to json")

        resource_dict["fields"] = []
        attributes = query_method(attributes_query(resource_name))
        for attribute in attributes:
            resource_dict["fields"].append(attribute.name)

    with resources_path.open('w') as f:
        json.dump(resources, fp=f)


def flatten_completion():
    """flattens all entities into a dictionary { name: fields }, with one aggregating entry { all: all_fields }"""
    resources_path = pathlib.Path('gaql/lib/google_clients/completion/entities.json')
    output_path = pathlib.Path('gaql/lib/google_clients/completion/autocompletions.py')

    with resources_path.open('r') as f:
        autocompletion = json.load(f)
    flattened_autocompletion = {}

    for k in autocompletion:
        raw_fields = autocompletion[k]["fields"] + autocompletion[k].get("selectable_with", [])
        flattened_fields = []

        for field in raw_fields:
            if "." in field:
                flattened_fields.append(field)
            else:
                flattened_fields += autocompletion[field]["fields"]
        flattened_autocompletion[k] = flattened_fields

    all_fields = set()
    for k in flattened_autocompletion:
        for field in flattened_autocompletion[k]:
            all_fields.add(field)

    flattened_autocompletion["all"] = list(sorted(all_fields))

    with output_path.open('w') as f:
        f.write("COMPLETIONS = ")
        json.dump(flattened_autocompletion, fp=f)


if __name__ == "__main__":
    autocomplete_fields()
    flatten_completion()
