import argparse
from APD.APD import APD
import matplotlib.pyplot as plt
from tqdm import tqdm

def plot_trajectories(traj):
    """
    Plot x and y coordinates of the passed trajectories.

    Parameters
    ----------
        traj : numpy array
            trajectories for plotting.
    """
    for t in tqdm(traj, desc ="Plotting"):
        plt.plot(t[:,0], t[:,1])
    plt.gca().set_aspect('equal')
    plt.grid()
    plt.title('Aschaffenburg Pose Dataset')
    plt.xlabel("x / m")
    plt.ylabel("y / m")
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Pipeline Arguments')
    parser.add_argument("path", type=str, help="path to json files")
    parser.add_argument('-v', '--vru_types', action='append', type=str,
                        help="select certain vru types for plotting ['ped', 'bike']", default=[])
    parser.add_argument('-s', '--sets', action='append', type=str,
                        help="select certain sets for plotting ['train', 'validation', 'test']", default=[])

    args = parser.parse_args()

    apd = APD(data_path=args.path, vru_types=args.vru_types, sets=args.sets, data_fields=['set', 'head_smoothed'])

    plot_trajectories(apd.data['head_smoothed'])