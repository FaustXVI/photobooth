import time

import configparser
import os

from infrastructure.cluster import Cluster


def main():
    config = configparser.ConfigParser()
    config.read('config')
    with Cluster(config['cluster.co']) as cluster:
        print(cluster.upload(['images/unicorns.jpg','images/start_camera.jpg']))


if __name__ == '__main__':
    main()
