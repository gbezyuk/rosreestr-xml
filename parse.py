sample_file_path = './data-samples/doc14350111.xml'


def parse_to_dict(file_path):
    import xmltodict
    return xmltodict.parse(file(file_path).read())    


def dump_dict_to_json(data):
    import json
    return json.dumps(data, sort_keys=True, indent=4)


def extract_required_data(data):
    return data['KPT']['CadastralBlocks']['CadastralBlock']['ObjectsRealty']['ObjectRealty']     

print dump_dict_to_json(extract_required_data(parse_to_dict(sample_file_path)))