import yaml


def extract_sector_names(sector: dict) -> list:
    playfields:list[list[str]] = sector['Playfields']
    playfield_names = [(x[1], x[2]) for x in playfields]
    return playfield_names

sector_file_path_format = "{}/Sectors/Sectors.yaml"


def parse_sectors(scenario_path:str) -> map:
    sector_file_path = sector_file_path_format.format(scenario_path)
    with open(sector_file_path, "rb") as stream:
        contents = stream.read()
        data = contents.decode("utf-8")

    doc = yaml.load(data)

    if isinstance(doc, list):
        sectors: list = doc
    else:
        sectors: list = doc.get('Sectors')

    sector_name_groups = map(extract_sector_names, sectors)
    sector_names = [x
                    for sector in sector_name_groups
                    for x in sector
                    ]

    return sector_names
