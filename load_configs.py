import yaml
import argparse

def importConfigs(path='./default.yaml'):
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default=path)
    args = parser.parse_args()

    with open(args.config) as f:
        config = yaml.load(f,Loader=yaml.Loader)

    for k, v in config.items():
        setattr(args, k, v)

if __name__ == '__main__':
    importConfigs()