from argparse import ArgumentParser
from pathlib import Path
import datetime
import yaml
import json

def read_component(file: Path):
    with open(file, 'r', encoding='utf-8') as f:
        component = yaml.safe_load(f)
    
    for required_key in [
        "component-name",
        "component-author",
        "component-version",
        "component-repository",
        "component-license",
        "component-type",
        "component-description",
        "tags",
    ]:
        assert required_key in component, f"{file} missing key: {required_key}"

    # for _tag in component["tags"]:
    #     assert _tag in tags, f'{file} tag: "{str(_tag)}" is not a valid tag'

    try:
        datetime.date.fromisoformat(component.get('added'))
    except:
        # add "added": "YYYY-MM-DD"
        component["added"] = str(datetime.datetime.now().date())
        with open(file, 'w', encoding='utf-8') as f:
            yaml.dump(component, f, default_flow_style=False)
    return component


def read_component_dir(components_dir):
    components = {}
    for f in components_dir.iterdir():
        if f.is_file() and f.suffix.lower() == '.json':        
            component = read_component(f)
            components[component['url']] = component
    return components


def update_index(exts: dict):
    # update existing remove removed and add new components
    with open(build_index_path, 'r', encoding='utf-8') as f:
        existing_components = {component['component-repository']: component for component in json.load(f)['components']}

    for components_url, component in exts.items():
        if components_url in existing_components.keys():
            existing_components[components_url].update(component)
        else:
            existing_components[components_url] = component
    components_list = [component for components_url, component in existing_components.items() if components_url in components]
    component_index = {'components': components_list}

    with open(build_index_path, 'w', encoding='utf-8') as f:
        json.dump(component_index, f, indent=4, ensure_ascii=False)
    return component_index


def update_master_index(index: dict):
    # add keys from master/index that are not in components/tags to components/tags as new master/index
    with open(deploy_index_path, 'r', encoding='utf-8') as f:
        master_exts = {component['component-repository']: component for component in json.load(f)['components']}

    index_ext = {component['component-repository']: component for component in index['components']}
    index_ext_urls = index_ext.keys()
    for master_ext_url, master_ext in master_exts.items():
        if master_ext_url in index_ext_urls:
            index_ext_keys = index_ext[master_ext_url].keys()
            for master_exts_key in master_ext.keys():
                if master_exts_key not in index_ext_keys:
                    index_ext[master_ext_url][master_exts_key] = master_ext[master_exts_key]

    new_master_index = {'components': list(index_ext.values())}
    with open(deploy_index_path, 'w', encoding='utf-8') as f:
        json.dump(new_master_index, f, indent=4, ensure_ascii=False)
    return new_master_index


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--build-branch", "-b", type=str, default='', required=False)
    parser.add_argument("--deploy-branch", "-d", type=str, default='', required=False)
    args = parser.parse_args()
    
    build_index_path = Path(args.build_branch).joinpath('index.json')
    deploy_index_path = Path(args.deploy_branch).joinpath('index.json')
    components_dir = Path(args.build_branch).joinpath('components')

    # # read tags
    # with open(Path(args.build_branch).joinpath('tags.json'), 'r') as f:
    #     tags = yaml.load(f)

    # read entries
    components = read_component_dir(components_dir)

    # update indexs
    component_index_ext = update_index(components)
    component_index_master = update_master_index(component_index_ext)
    
    # # validate
    # validate.validate_index(build_index_path)
    # validate.validate_index(deploy_index_path)

    assert len(component_index_ext["components"]) == len(component_index_master["components"]), f'entry count mismatch: {len(component_index_ext["components"])} {len(component_index_master["components"])}'
    print(f'::notice:: {len(component_index_ext["components"])} components')    