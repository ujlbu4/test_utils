# from jinja2 import Template
import os
from jinja2 import Environment, FileSystemLoader
import json

import flex
from test_utils import configs

config = configs.load_config(__file__)

PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, 'templates')),
    # lstrip_blocks=True,
    # keep_trailing_newline=True,
    trim_blocks=True)


def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)


schema = flex.load(configs.config.get("facade.specification_url.v65"))
# schema = flex.load(Settings.url_specification_admin_api)

generate_for_paths = [
    # {'path': '/acc/facebook', 'codes': ['200', '201', '202', '204']},
    # {'path': '/data', 'codes': ['200', '201', '202', '204']},
    # {'path': '/data/want', 'codes': ['200', '201', '202', '204']},
    # {'path': '/data/want/import', 'codes': ['200', '201', '202', '204']},
    # {'path': '/data/want_many', 'codes': ['200', '201', '202', '204']},
    # {'path': '/data/watch', 'codes': ['200', '201', '202', '204']},
    # {'path': '/data/watch/import', 'codes': ['200', '201', '202', '204']},
    # {'path': '/discover/suggestions', 'codes': ['200', '201', '202', '204']},
    # {'path': '/discussions/{discussion_id}', 'codes': ['200', '201', '202', '204']},
    # {'path': '/discussions/{discussion_id}/comments', 'codes': ['200', '201', '202', '204']},
    # {'path': '/discussions/{discussion_id}/likes', 'codes': ['200', '201', '202', '204']},
    # {'path': '/discussions/{discussion_id}/mention_suggests', 'codes': ['200', '201', '202', '204']},
    # {'path': '/explore/selection/hit/{selection_id}', 'codes': ['200', '201', '202', '204']},
    # {'path': '/explore/selection/like/{selection_id}', 'codes': ['200', '201', '202', '204']},
    # {'path': '/explore/selections', 'codes': ['200', '201', '202', '204']},
    # {'path': '/explore/selections/{id}', 'codes': ['200', '201', '202', '204']},
    # {'path': '/explore/widgets', 'codes': ['200', '201', '202', '204']},
    # {'path': '/explore/widgets/{uri}', 'codes': ['200', '201', '202', '204']},
    # {'path': '/friends', 'codes': ['200', '201', '202', '204']},
    # {'path': '/friends/close/{user_id} ', 'codes': ['200', '201', '202', '204']},
    # {'path': '/friends/mute/{user_id}', 'codes': ['200', '201', '202', '204']},
    # {'path': '/friends/search', 'codes': ['200', '201', '202', '204']},
    # {'path': '/friends/watched/{movie_id}/', 'codes': ['200', '201', '202', '204']},
    # {'path': '/friends/{user_id}/in_lists', 'codes': ['200', '201', '202', '204']},
    # {'path': '/movies', 'codes': ['200', '201', '202', '204']},
    # {'path': '/movies/backdrops', 'codes': ['200', '201', '202', '204']},
    # {'path': '/movies/rate', 'codes': ['200', '201', '202', '204']},
    # {'path': '/movies/search', 'codes': ['200', '201', '202', '204']},
    # {'path': '/movies/trailers', 'codes': ['200', '201', '202', '204']},
    # {'path': '/movies/{id}', 'codes': ['200', '201', '202', '204']},
    # {'path': '/movies/{movie_id}/backdrops', 'codes': ['200', '201', '202', '204']},
    # {'path': '/movies/{movie_id}/following', 'codes': ['200', '201', '202', '204']},
    # {'path': '/movies/{movie_id}/rate', 'codes': ['200', '201', '202', '204']},
    # {'path': '/movies/{movie_id}/trailers', 'codes': ['200', '201', '202', '204']},
    # {'path': '/movies/{productId}/update_from_tmdb', 'codes': ['200', '201', '202', '204']},
    # {'path': '/people', 'codes': ['200', '201', '202', '204']},
    # {'path': '/people/want_movie/{movieId}', 'codes': ['200', '201', '202', '204']},
    # {'path': '/people/watched_movie/{movieId}', 'codes': ['200', '201', '202', '204']},
    # {'path': '/people/world_rating_list_with_user_position/user_id/{userId', 'codes': ['200', '201', '202', '204']},
    # {'path': '/persons', 'codes': ['200', '201', '202', '204']},
    # {'path': '/persons/{person_id}', 'codes': ['200', '201', '202', '204']},
    # {'path': '/persons/{person_id}/likes', 'codes': ['200', '201', '202', '204']},
    # {'path': '/persons/{person_id}/products', 'codes': ['200', '201', '202', '204']},
    # {'path': '/products', 'codes': ['200', '201', '202', '204']},
    # {'path': '/products/backdrops', 'codes': ['200', '201', '202', '204']},
    # {'path': '/products/trailers', 'codes': ['200', '201', '202', '204']},
    # {'path': '/products/{product_id}', 'codes': ['200', '201', '202', '204']},
    # {'path': '/products/{product_id}/backdrops', 'codes': ['200', '201', '202', '204']},
    # {'path': '/products/{product_id}/rates/{user_id}', 'codes': ['200', '201', '202', '204']},
    # {'path': '/products/{product_id}/reviews', 'codes': ['200', '201', '202', '204']},
    # {'path': '/products/{product_id}/reviews/{user_id}', 'codes': ['200', '201', '202', '204']},
    # {'path': '/products/{product_id}/sharing_image', 'codes': ['200', '201', '202', '204']},
    # {'path': '/products/{product_id}/trailers', 'codes': ['200', '201', '202', '204']},
    # {'path': '/products/{product_id}/wants', 'codes': ['200', '201', '202', '204']},
    # {'path': '/products/{product_id}/watches', 'codes': ['200', '201', '202', '204']},
    # {'path': '/profile/user_id/{user_id}', 'codes': ['200', '201', '202', '204']},
    # {'path': '/profile/user_id/{user_id}/movie_sharing_image/{product_id}', 'codes': ['200', '201', '202', '204']},
    # {'path': '/profile/user_id/{user_id}/rates', 'codes': ['200', '201', '202', '204']},
    # {'path': '/profile/{uri}', 'codes': ['200', '201', '202', '204']},
    # {'path': '/profile/{uri}/image', 'codes': ['200', '201', '202', '204']},
    {'path': '/push_messages/{notification_id}', 'codes': ['200', '201', '202', '204']},
    # {'path': '/search', 'codes': ['200', '201', '202', '204']},
    # {'path': '/settings', 'codes': ['200', '201', '202', '204']},
    # {'path': '/tracking', 'codes': ['200', '201', '202', '204']},
    # {'path': '/trailerhouse', 'codes': ['200', '201', '202', '204']},
    # {'path': '/trailerhouse/{triler_id}/viewed', 'codes': ['200', '201', '202', '204']},
    # {'path': '/trailers', 'codes': ['200', '201', '202', '204']},
    # {'path': '/trailers/by_product_id', 'codes': ['200', '201', '202', '204']},
    # {'path': '/trailers/{id}', 'codes': ['200', '201', '202', '204']},
    # {'path': '/users', 'codes': ['200', '201', '202', '204']},
    # {'path': '/users/id/{user_id}', 'codes': ['200', '201', '202', '204']},
    # {'path': '/users/id/{user_id}/lists/{list_name}', 'codes': ['200', '201', '202', '204']}
    # {'path': '/users/id/{user_id}/movie_sharing_image/{product_id}', 'codes': ['200', '201', '202', '204']},
    # {'path': '/users/id/{user_id}/rates', 'codes': ['200', '201', '202', '204']},
    # {'path': '/users/id/{user_id}/want', 'codes': ['200', '201', '202', '204']},
    # {'path': '/users/id/{user_id}/watched', 'codes': ['200', '201', '202', '204']},
    # {'path': '/users/search', 'codes': ['200', '201', '202', '204']},
    # {'path': '/users/uri/{uri}', 'codes': ['200', '201', '202', '204']},
    # {'path': '/users/uri/{uri}/image', 'codes': ['200', '201', '202', '204']},
    # {'path': '/users/want_movie/{movie_id}', 'codes': ['200', '201', '202', '204']},
    # {'path': '/users/watched_movie/{movie_id}', 'codes': ['200', '201', '202', '204']},
    # {'path': '/users/world_rating_list_with_user_position/user_id/{user_id}', 'codes': ['200', '201', '202', '204']},
    # {'path': '/users/you_may_know', 'codes': ['200', '201', '202', '204']}
]


def create_index_html():
    fname = "output_contract_tests.py"

    context = {
        'service_name': 'Service.Must.backend_api',
        'schema': schema,
        'prepare_parameters': prepare_parameters,
        'generate_for_paths': generate_for_paths,
        'check_generating_path': check_generating_path,
        'get_generate_for_codes': get_generate_for_codes
    }
    #
    with open(fname, 'w') as f:
        generated_tests = render_template('contract_tests_from_swagger', context)
        f.write(generated_tests)


def get_path_operations(paths, path_value):
    for path in paths.items():
        if path_value == path[0]:
            return path[1]

    return None


def check_generating_path(generate_for_paths, current_path_value):
    if not generate_for_paths:
        # if none of empty — generate for all pathes
        return True

    for acceptable_path in generate_for_paths:
        if acceptable_path['path'] == current_path_value:
            return True
    return False


def get_generate_for_codes(generate_for_paths, current_path_value, swagger_codes):
    if not generate_for_paths:
        # just return all codes
        return swagger_codes

    for item in generate_for_paths:
        if item['path'] == current_path_value:

            if 'codes' not in item:
                return swagger_codes

            intersection_codes = set(item['codes']).intersection(swagger_codes.keys())
            result = {}
            for code in intersection_codes:
                result.update({code: swagger_codes[code]})
            return result

    raise RuntimeError("should be there")


def prepare_parameters(schema, path_value, _type, operation=None):
    marker_for_replace = '__insert_value__'
    path_operations = get_path_operations(paths=schema['paths'], path_value=path_value)

    def resolve_parameters(parameters, schema):
        resolved_params = []
        for param in parameters:
            if '$ref' in param:
                param_name = param['$ref'].split('/')[-1]
                param = schema['parameters'][param_name]

            resolved_params.append(param)

        return resolved_params

    parameters = []
    if path_operations and path_operations.get("parameters"):
        parameters = resolve_parameters(parameters=path_operations['parameters'], schema=schema)

    if _type == 'path':
        if len(parameters) > 0:
            path_params = [param for param in parameters if param['in'] == 'path']
            format_string = "'{path_value}'.format({values})".format(path_value=path_value,
                                                                     values=",".join([param['name'] + '={}'.format(marker_for_replace) for param in
                                                                                      path_params]))
            return format_string
        else:
            return "'{}'".format(path_value)

    if _type == "query:all":
        properties = {}
        query_params = [param for param in parameters if param['in'] == 'query']
        for param in query_params:
            param = {param['name']: param['type']}
            properties.update(param)

        return properties

    elif _type == "query:required":
        properties = {}
        query_params = [param for param in parameters if param['in'] == 'query' and 'required' in param and param['required']]
        for param in query_params:
            param = {param['name']: param['type']}
            properties.update(param)

        return properties

    elif _type == "body":
        properties = None
        if path_operations and path_operations.get(operation) and path_operations[operation].get("parameters"):
            for parameter in path_operations[operation]["parameters"]:
                # print("{} {}".format(operation, path_value))
                if parameter.get('in') and parameter['in'] == "body":
                    innter_schema = parameter['schema']

                    if innter_schema.get('$ref'):
                        properties_to_parse = schema['definitions'][innter_schema['$ref'].replace("#/definitions/", "")]
                    else:
                        properties_to_parse = innter_schema

                    def extract_properties(properties_to_parse):

                        if '$ref' in properties_to_parse:
                            return extract_properties(
                                properties_to_parse=schema['definitions'][properties_to_parse['$ref'].replace("#/definitions/", "")])

                        elif properties_to_parse['type'] == "array":
                            d = []
                            d.append(extract_properties(properties_to_parse['items']))
                        elif properties_to_parse['type'] == "object":
                            d = {}
                            for prop in properties_to_parse['properties'].items():
                                key = prop[0]
                                value = prop[1]

                                if value.get('properties') or value.get('items'):
                                    d.update({key: extract_properties(value)})
                                else:
                                    d.update({key: "{}".format(marker_for_replace)})
                        else:
                            d = marker_for_replace
                        return d

                    properties = extract_properties(properties_to_parse)

        if properties:
            return json.dumps(properties)


def generator_debug():
    paths = schema['paths']
    definitions = schema['definitions']

    for path in sorted(paths.keys()):
        path_value = path
        path_operations = paths[path_value]

        if not check_generating_path(generate_for_paths=generate_for_paths, current_path_value=path_value):
            continue

        print("{path_value}".format(path_value=path_value))

        formatted_path_value = prepare_parameters(schema=schema, path_value=path_value, _type="path")
        print("\t path(formatted): {}".format(formatted_path_value))

        query_properties = prepare_parameters(schema=schema, path_value=path_value, _type="query:all")
        print("\t query (all): {}".format(query_properties))

        query_properties = prepare_parameters(schema=schema, path_value=path_value, _type="query:required")
        print("\t query (required): {}".format(query_properties))

        for operation in path_operations.items():
            operation_method, operation_properties = operation[0], operation[1]
            if operation_method in ('post', 'get', 'put', 'delete', 'patch', 'head', 'options'):
                status_codes = operation_properties['responses']

                for status_code in get_generate_for_codes(generate_for_paths=generate_for_paths, current_path_value=path_value,
                                                          swagger_codes=status_codes).items():
                    status_code_value, status_code_properties = status_code[0], status_code[1]

                    print("\t method: {} {}".format(operation_method, status_code_value))
                    if operation_method == 'get':
                        pass
                    elif operation_method in ('post', 'put', 'patch'):
                        body_properties = prepare_parameters(schema=schema, path_value=path_value, _type="body", operation=operation_method)
                        print("\t\t body:{}".format(body_properties))
                        pass


def main():
    # template = Template('Hello {{name}}!')
    # template.render(name='John Doe')
    #
    # requests.get("/acc/location")

    generator_debug()
    create_index_html()


if __name__ == '__main__':
    main()
