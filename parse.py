sample_file_path = './data-samples/doc14350111.xml'


def parse_to_dict(file_path):
    import xmltodict
    return xmltodict.parse(file(file_path).read())    


def dump_dict_to_json(data):
    import json
    return json.dumps(data, sort_keys=True, indent=4)


def get_raw_parcels(data):
    return [parcel for parcel in data['KPT']['CadastralBlocks']['CadastralBlock']['Parcels']['Parcel']
        if 'EntitySpatial' in parcel
    ]


def clean_parcels(raw_parcels):
    return [{
        'cadastral_number': parcel['@CadastralNumber'],
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
        csv_writer = csv.writer(csvfile)#, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['cadastral_number', 'su_nmb', 'x', 'y'])
        for parcel in parcels:
            for point in parcel['path']:
                csv_writer.writerow([parcel['cadastral_number'], point['su_nmb'], point['x'], point['y']])

store_as_csv(clean_parcels(get_raw_parcels(parse_to_dict(sample_file_path))), './parcels.csv')