import xmltodict


def get_parcels_and_metadata(file_path):
    file_dict = _parse_to_dict(file_path)
    parcels = _clean_parcels(_get_raw_parcels(file_dict))
    metadata = _get_metadata(file_dict)
    return (parcels, metadata)


def _get_metadata(file_dict):
    return {
        'cadastral_number': _get_cadastral_block_number(file_dict),
        'root_node_name': _get_root_node_name(file_dict)
    }

def _get_cadastral_block_number(file_dict):
    if _get_root_node_name(file_dict) == 'KPT':
        return file_dict['KPT']['CadastralBlocks']['CadastralBlock']['@CadastralNumber']
    if _get_root_node_name(file_dict) == 'KVZU':
        return file_dict['KVZU']['Parcels']['Parcel']['CadastralBlock']
            

def _parse_to_dict(file_path):
    import xmltodict
    return xmltodict.parse(open(file_path).read())


def _get_root_node_name(file_dict):
    # return file_dict.keys()[0]
    # results with a "'KeysView' object does not support indexing" error
    # now using workaround below
    for sample in ('KPT', 'KVZU'):
        if sample in file_dict:
            return sample


def _find_parcel_node(file_dict):
    if _get_root_node_name(file_dict) == 'KPT':
        return file_dict['KPT']['CadastralBlocks']['CadastralBlock']['Parcels']['Parcel']
    if _get_root_node_name(file_dict) == 'KVZU':
        return file_dict['KVZU']['Parcels']['Parcel']


def _get_raw_parcels(file_dict):
    if _get_root_node_name(file_dict) == 'KVZU':
        return [_find_parcel_node(file_dict)]
    if _get_root_node_name(file_dict) == 'KPT':
        return [parcel for parcel in _find_parcel_node(file_dict) if 'EntitySpatial' in parcel]
    return []


def _clean_parcels(raw_parcels):
    return [{
        'cadastral_number': parcel['@CadastralNumber'],
        'utilization': parcel['Utilization']['@ByDoc']
                       if 'Utilization' in parcel and '@ByDoc' in parcel['Utilization'] else None,
        'path': [{
            'su_nmb': point['@SuNmb'],
            'x': point['ns3:Ordinate']['@X'],
            'y': point['ns3:Ordinate']['@Y']
            } for point in parcel['EntitySpatial']['ns3:SpatialElement']['ns3:SpelementUnit']]
        } for parcel in raw_parcels
            if 'EntitySpatial' in parcel
            and 'ns3:SpatialElement' in parcel['EntitySpatial']
            and 'ns3:SpelementUnit' in parcel['EntitySpatial']['ns3:SpatialElement']
           ]


def store_as_csv(parcels, output_file_path):
    import csv
    with open(output_file_path, 'wb') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['cadastral_number', 'su_nmb', 'x', 'y'])
        for parcel in parcels:
            for point in parcel['path']:
                csv_writer.writerow([parcel['cadastral_number'],
                                     point['su_nmb'], point['x'], point['y']])
