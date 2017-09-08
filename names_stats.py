#!/usr/bin/env python
import os
import pathlib

import requests
import requests_cache
import rows
import rows.utils


def download_name_data(name, sex):
    api_url = 'http://servicodados.ibge.gov.br/api/v1/censos/nomes/basica?nome={name}&sexo={sex}'
    response = requests.get(api_url.format(name=name, sex=sex))
    data = response.json()
    if not data:
        return None

    assert len(data) == 1
    return {
            'name': data[0]['nome'],
            'frequency': data[0]['freq'],
            'alternative_names': data[0]['nomes'].split(','),
    }


def download_name_stats(name):
    name = rows.plugins.utils.slug(name).replace('_', ' ')

    female = download_name_data(name, 'f')
    male = download_name_data(name, 'm')

    if female is None and male is None:
        return None

    alternative_names = []
    if female is not None:
        alternative_names += female['alternative_names']
    if male is not None:
        alternative_names += male['alternative_names']
    name = female['name'] if female is not None else male['name']
    female_frequency = female['frequency'] if female is not None else None
    male_frequency = male['frequency'] if male is not None else None

    return {
            'name': name,
            'frequency_female': female_frequency,
            'frequency_male': male_frequency,
            'alternative_names': sorted(set(alternative_names)),
            }


def unique_names(csv_filename):
    return set(row.name
               for row in rows.import_from_csv(str(csv_filename.absolute())))


def main():
    csv_filename = pathlib.Path('data/names.csv')
    output = pathlib.Path('output/names-stats.csv')
    if not csv_filename.parent.exists():
        os.makedirs(str(csv_filename.parent.absolute()), exist_ok=True)
    if not output.parent.exists():
        os.makedirs(str(output.parent.absolute()), exist_ok=True)
    requests_cache.install_cache('nomes-ibge')

    result = []
    for name in unique_names(csv_filename):
        print(name)
        row = download_name_stats(name)
        if row is None:
            continue
        row['alternative_names'] = '|'.join(row['alternative_names'])
        result.append(row)
    table = rows.import_from_dicts(result)
    table.order_by('name')
    rows.utils.export_to_uri(table, str(output.absolute()))


if __name__ == '__main__':
    main()
