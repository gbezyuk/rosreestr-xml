import xmltodict

def get_parcels_and_metadata(file_path):
    file_dict = _parse_to_dict(file_path)
    parcels = _clean_parcels(_get_raw_parcels(file_dict))
    metadata = _get_metadata(file_dict)
    return (parcels, metadata)

def _get_metadata(file_dict):
    return {
        'cadastral_number':
        file_dict['KPT']['CadastralBlocks']['CadastralBlock']['@CadastralNumber']
    }

def _parse_to_dict(file_path):
    import xmltodict
    return xmltodict.parse(open(file_path).read())

def _get_raw_parcels(file_dict):
    return [parcel for parcel
            in file_dict['KPT']['CadastralBlocks']['CadastralBlock']['Parcels']['Parcel']
            if 'EntitySpatial' in parcel
           ]


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
            if 'ns3:SpatialElement' in parcel['EntitySpatial']
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
