from copy import deepcopy


def nerf_resources(playfield:dict) -> dict:
    new_playfield = deepcopy(playfield)
    random_resources = new_playfield.get('RandomResources', list())
    new_playfield['RandomResources'] = nerf_resource_list(random_resources)
    return new_playfield


def nerf_resource_node(node:dict):
    out = deepcopy(node)
    count_min, count_max = node.get('CountMinMax')
    size_min, size_max = node.get('SizeMinMax')
    min_available = count_min * size_min
    max_available = count_max * size_max

    min_expected = min(min_available, 30)
    max_expected = min(max_available, 55)

    new_count = [int(min_expected/3), int(max_expected/3)]
    new_size = [3, 5]
    out['CountMinMax'] = new_count
    out['SizeMinMax'] = new_size
    return out


def nerf_resource_list(resource_list:list)->list:
    new_nodes = map(nerf_resource_node, resource_list)
    return list(new_nodes)
