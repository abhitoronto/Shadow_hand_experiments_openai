import sys, getopt
import numpy as np
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
import matplotlib.pyplot as plt
import csv
from scipy.ndimage.filters import gaussian_filter1d


def _plot_curve(ax, x, y, label, style):
    ax.grid(True, which='both')
    ysmoothed = gaussian_filter1d(y, sigma=1.0)
    ax.plot(x, y,  style, linewidth=0.75, linestyle=':')
    ax.plot(x, ysmoothed,  style, linewidth=1.5, label=label)
    return


def _create_training_fig(data, title):
    epochs = data[0]
    plt.rc('text', usetex=True)
    fig, ax = plt.subplots(1, 1, sharex='col', sharey='row')
    fig.set_size_inches(4,2)
    _plot_curve(ax, epochs, data[1], '92 Sensors-v0', 'tab:blue')

    ax.legend()
    ax.set_xlabel('epoch')
    ax.set_ylabel('Success rate')
    ax.set_title(title)

    return fig

def _create_training_fig_comparison(no_touch, with_touch, title):
    assert len(no_touch) == len(with_touch)

    epochs = with_touch[0]
    plt.rc('text', usetex=True)
    fig, ax = plt.subplots(1, 1, sharex='col', sharey='row')
    fig.set_size_inches(5,3)
    _plot_curve(ax, epochs, no_touch[1],  'No Sensors', 'tab:red')
    _plot_curve(ax, epochs, with_touch[1],  '92 Touch Sensors-v0', 'tab:blue')

    ax.legend()
    ax.set_xlabel('epoch')
    ax.set_ylabel('Success rate')
    ax.set_title(title)

    return fig

def _parse_progress_csv(directories, train=False):
    """
        This function return the train/test success rate for HMPR progress.csv files
    """
    TEST_COL = 7
    TRAIN_COL = 9
    EPOCH_COL = 0
    data_list = []
    for direc in directories:
        epoch = []
        s_rate = []
        with open(direc + "/progress.csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            count = 0
            for row in csv_reader:
                count += 1
                if count == 1: continue
                if not train:
                    # Return Test success rate data
                    epoch.append(int(row[EPOCH_COL]))
                    s_rate.append(float(row[TEST_COL]))
                else:
                    # Return Train success rate data
                    epoch.append(int(row[EPOCH_COL]))
                    s_rate.append(float(row[TRAIN_COL]))
            data_list.append([epoch, s_rate])
    return data_list

def _read_args(argv) -> (list, str, str):
    input_files = []
    title = 'Test Success Rate Plot'
    output_file = ''
    try:
      opts, args = getopt.getopt(argv,"hi:t:o:",["ifile=", "title=", "ofile="])
    except getopt.GetoptError:
        print("USAGE: hand_manipulator_lc_plotter.py -i < Dir path [touch logs]> -i <Dir path [no touch logs]> -t <title> -o <output file path>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
        print("USAGE: hand_manipulator_lc_plotter.py -i < Dir path [touch logs]> -i <Dir path [no touch logs]> -t <title> -o <output file path>")
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_files.append(arg)
        elif opt in ("-t", "--titile"):
            title = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg
    return input_files, title, output_file

def main():
    # Read Arguments
    input_files, title, output_file = _read_args(sys.argv[1:])
    assert len(input_files) < 3

    # Read file(s)
    print(f'No Touch file: {input_files[0]}')
    print(f'With Touch file: {input_files[1]}')

    training_data = _parse_progress_csv(input_files)

    # Comparison Case
    if len(input_files) == 2:
        if not output_file:
            raise ValueError("Output File Empty")
        fig = _create_training_fig_comparison(training_data[0], training_data[1], title)

        print(f'Saving file: {output_file}')
        fig.savefig(output_file, bbox_inches='tight')
        plt.close(fig)

    # Single plot case
    elif len(input_files) == 1:
        if not output_file:
            output_file = input_files[0] +'_train.pdf'
        fig = _create_training_fig(training_data[0], title)

        print(f'Saving file: {output_file}')
        fig.savefig(output_file, bbox_inches='tight')
        plt.close(fig)
    else:
        raise ValueError('ERROR: No input file provided')

if __name__ == "__main__":
   main()