#!/usr/bin/env python3

def parse_to_dict(file_path):
    import xmltodict
    return xmltodict.parse(open(file_path).read())    


def dump_dict_to_json(data):
    import json
    return json.dumps(data, sort_keys=True, indent=4)


def find_parcel_node(data):
    if 'KPT' in data:
        return data['KPT']['CadastralBlocks']['CadastralBlock']['Parcels']['Parcel']
    if 'KVZU' in data:
        return data['KVZU']['Parcels']['Parcel']


def get_raw_parcels(data):
    return [parcel for parcel in find_parcel_node(data) if 'EntitySpatial' in parcel]


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
    with open(output_file_path, 'wt') as csvfile:
        csv_writer = csv.writer(csvfile)#, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['cadastral_number', 'su_nmb', 'x', 'y'])
        for parcel in parcels:
            for point in parcel['path']:
                csv_writer.writerow([parcel['cadastral_number'], point['su_nmb'], point['x'], point['y']])


def get_parcels(input_file_path):
    return clean_parcels(get_raw_parcels(parse_to_dict(input_file_path))),

# sample_input_path = './data-samples/doc14350111.xml'
# sample_output_path = './parcels.csv'

# store_as_csv(get_parcels(input_path), output_path)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path", help="input xml file to parse", type=str)
    parser.add_argument("-c", "--csv_output_file_path", help="output csv file to export data", type=str)
    parser.add_argument("-j", "--json_output_file_path", help="output csv file to export data", type=str)
    parser.add_argument("-H", "--html_output_file_path", help="create an html file with navigateable JSON representation", type=str)
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")    
    args = parser.parse_args()

    if args.verbose:
        print("Parsing original document...")
    document_as_dict = parse_to_dict(args.input_file_path)
    if args.verbose:
        print("Parsing original document DONE")

    if args.json_output_file_path:
        if args.verbose:
            print("Storing JSON file...")
        with open(args.json_output_file_path, 'wt') as jsonfile:
            jsonfile.write(dump_dict_to_json(document_as_dict))
        if args.verbose:
            print("Storing JSON file DONE")

    if args.html_output_file_path:
        if args.verbose:
            print("Storing HTML file...")
        if args.verbose:
            with open(args.html_output_file_path, 'wt') as htmlfile:
                htmlfile.write("""<html>
<head></head>
<body>
<p>use <b>window.data</b> in console</p>
<script type="text/javascript">
window.data = %s;
</script>
</body>
</html>
                """ % (dump_dict_to_json(document_as_dict,)))
            print("Storing HTML file DONE")

    if args.csv_output_file_path:
        if args.verbose:
            print("Extracting Parcels...")
        parcels = clean_parcels(get_raw_parcels(document_as_dict))
        if args.verbose:
            print("Extracting Parcels DONE")

        if args.verbose:
            print("Storing CSV file...")
        store_as_csv(parcels, args.csv_output_file_path)
        if args.verbose:
            print("Storing CSV file DONE")