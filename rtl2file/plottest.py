#
# simple tester for plotting data files
#
# usage:
# python plottest.py file1.bin file2.bin --sample-rate 2.4e6 --output spectrumfilename
#

import argparse
import numpy as np
import matplotlib.pyplot as plt

def parse_arguments():
    parser = argparse.ArgumentParser(description='Plot spectrum of binary files')
    parser.add_argument('files', nargs='+', help='List of binary files to process')
    parser.add_argument('--output', type=str, default='./', help='Output PNG file name prefix')
    parser.add_argument('--sample-rate', type=float, required=True, help='Sample rate used during the recording')
    return parser.parse_args()

def read_binary_file(file_name):
    with open(file_name, 'rb') as f:
        data = np.frombuffer(f.read(), dtype=np.complex64)
    return data

def plot_spectrum(data, sample_rate, output_file):
    plt.figure()
    plt.specgram(data, NFFT=1024, Fs=sample_rate, noverlap=900)
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.title('Spectrum')
    plt.colorbar(label='Intensity (dB)')
    plt.savefig(output_file)
    plt.close()

def main():
    args = parse_arguments()
    
    for file_name in args.files:
        data = read_binary_file(file_name)
        output_file = f"{args.output}_{file_name}.png"
        plot_spectrum(data, args.sample_rate, output_file)
        print(f"Saved spectrum plot for {file_name} as {output_file}")

if __name__ == '__main__':
    main()
