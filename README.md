# odtp-zoo-db
Zoo index for Open Digital Twin Platform

ODTP accesses `index.json` from this repo to list all compatible components and metadata. 

## How to submit a component.

In order to submit a component you need to make an entry in `components` directory using `component_template.yaml`. Please fill the template with all requested info and then open a pull request. 

### Step by step instructions.

1. Fork this repository.
2. Copy the `odtp.yml` and rename it as `component_version.yaml`.
3. Place the file into `components` directory.
5. Submit a pull request and wait for review. 
    - Components pull requests target `components` branch, after merging it will get automatically deployed to `main`.
    - Do not edit `index.json` directly, and do not modify any other file. 
    - The added date will be automatically populated after the merge. 

## Notes

- Only functional components will be accepted. You can make your tool compatible using the [`odtp-component-template`](https://github.com/odtp-org/odtp-component-template). 
- If you want to have your component removed, please open an issue or pull request. 

## Credit

Heavily inspired by `stable-diffusion-webui-extensions`.

## Development

Developed by SDSC/CSFM.