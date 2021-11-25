import numpy as np
from os import listdir
from os.path import isfile, join
import json
import argparse
from collections import defaultdict
from tqdm import tqdm

class APD:
    """
    A class to load and filter the Aschaffenburg Pose Dataset.

    ...

    Attributes
    ----------
    data : dict
        data of the Aschaffenburg Pose Dataset

    Methods
    -------
    filter:
        Filter the dataset for certain vru_types, sets and data fields.
    """

    NESTED_DATA_FIELDS = ['pose2d', 'pose3d', 'motion_primitives']

    def __init__(self, data_path, vru_types=[], sets=[], data_fields=[], pose3d_joints=[], pose2d_joints=[]):
        """
        Loads the selected data from the json files.

        Parameters
        ----------
            data_path : str
                path to the json files
            vru_types : list of str, optional
                load only the selected vru types ('ped', 'bike'). All vru types are loaded if the list is empty
                (default).
            sets : list of str, optional
                load only the selected set ('train', 'valid', 'test'). All sets are loaded if the list is empty
                (default).
            data_fields : list of str, optional
                load only the selected data fields ('vru_type', 'set', 'timestamps', 'head_smoothed', 'pose2d',
                'pose3d', 'motion_primitives'). All datafields are loaded if the list is empty (default).
            pose3d_joints : list of str, optional
                load only the trajectories of the selected joints of pose3d ('head', 'thorax', 'lshoulder', 'rshoulder',
                'lelbow', 'relbow', 'lwrist', 'rwrist', 'lhip', 'rhip', 'lknee', 'rknee', 'lfoot', 'rfoot').
                All trajectories are loaded if the list is empty (default).
            pose2d_joints : list of str, optional
                load only the trajectories of the selected joints of pose2d ('nose', 'neck', 'rshoulder', 'relbow',
                'rwrist', 'lshoulder', 'lelbow', 'lwrist', 'rhip', 'rknee', 'rankle', 'lhip', 'lknee', 'lankle', 'reye',
                'leye', 'rear', 'lear'). All trajectories are loaded if the list is empty (default).
        """
        self.data = dict()
        data_types = {'pose2d': np.float32, 'pose3d': np.float32, 'motion_primitives': np.uint8,
                      'head_smoothed': np.float32, 'timestamps': np.uint64}

        json_files = [join(data_path, f) for f in listdir(data_path) if
                      isfile(join(data_path, f)) and f.endswith('.json')]

        for f in tqdm(json_files, desc ="Loading Dataset"):
            with open(f) as c_file:
                json_data = json.load(c_file)
                if (json_data['vru_type'] in vru_types or len(vru_types) == 0) and (
                        json_data['set'] in sets or len(sets) == 0):  # filter for vru_type and set
                    for k, v in json_data.items():
                        if k in data_fields or len(data_fields) == 0:
                            if k not in self.data:
                                if k in self.NESTED_DATA_FIELDS:
                                    self.data[k] = defaultdict(list)
                                else:
                                    self.data[k] = list()
                            if k in self.NESTED_DATA_FIELDS:
                                for sub_k in v:
                                    if (k == 'pose2d' and (sub_k in pose2d_joints or len(pose2d_joints) == 0)) or (
                                                k == 'pose3d' and (sub_k in pose3d_joints or len(
                                                pose3d_joints) == 0) or k == 'motion_primitives'):
                                        self.data[k][sub_k].append(np.array(v[sub_k], dtype=data_types[k]))
                            else:
                                if k in ['head_smoothed', 'timestamps']:
                                    v = np.array(v, dtype=data_types[k])
                                self.data[k].append(v)

        # convert remaining lists to np.arrays
        for k, v in self.data.items():
            if k in self.NESTED_DATA_FIELDS:
                for sub_k in v:
                    self.data[k][sub_k] = np.array(self.data[k][sub_k])
            else:
                self.data[k] = np.array(v)

    def filter(self, vru_types=[], sets=[], data_fields=[], pose3d_joints=[], pose2d_joints=[]):
        """
        Filter the dataset for certain vru_types, sets and data fields.

        Parameters
        ----------
            vru_types : list of str, optional
                filter for vru types ('ped', 'bike'). All vru types are selected if the list is empty
                (default).
            sets : list of str, optional
                filter for set ('train', 'valid', 'test'). All sets are selected if the list is empty
                (default).
            data_fields : list of str, optional
                filter for data fields ('vru_type', 'set', 'timestamps', 'head_smoothed', 'pose2d', 'pose3d',
                'motion_primitives'). All datafields are selected if the list is empty (default).
            pose3d_joints : list of str, optional
                filter for joints of pose3d ('head', 'thorax', 'lshoulder', 'rshoulder', 'lelbow', 'relbow', 'lwrist',
                'rwrist', 'lhip', 'rhip', 'lknee', 'rknee', 'lfoot', 'rfoot'). All trajectories are selected if the list
                is empty (default).
            pose2d_joints : list of str, optional
                filter for joints of pose2d ('nose', 'neck', 'rshoulder', 'relbow', 'rwrist', 'lshoulder', 'lelbow',
                'lwrist', 'rhip', 'rknee', 'rankle', 'lhip', 'lknee', 'lankle', 'reye', 'leye', 'rear', 'lear'). All
                trajectories are selected if the list is empty (default).

        Returns
        ----------
            filtered dataset : dict
        """
        mask = np.ones_like(list(self.data.keys())[0], dtype=bool)
        if len(vru_types)!=0:
            mask_vru_type = [True if (t in vru_types) else False for t in self.data['vru_type']]
            mask = mask & mask_vru_type
        if len(sets)!=0:
            mask_sets = [True if (t in sets) else False for t in self.data['set']]
            mask = mask & mask_sets

        filtered_data = dict()
        for k, v in self.data.items():
            if k in data_fields or len(data_fields) == 0:
                if k in self.NESTED_DATA_FIELDS:
                    filtered_data[k] = dict()
                    for sub_k in v:
                        if (k == 'pose2d' and (sub_k in pose2d_joints or len(pose2d_joints) == 0)) or (
                                    k == 'pose3d' and (
                                    sub_k in pose3d_joints or len(pose3d_joints) == 0) or k == 'motion_primitives'):
                            filtered_data[k][sub_k] = self.data[k][sub_k][mask]
                else:
                    filtered_data[k] = self.data[k][mask]

        return filtered_data

