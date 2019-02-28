import argparse
import pandas as pd
# increase to_string representation of pandas data frames
pd.options.display.max_colwidth = 200

def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--barcode-file", type=str, required=True)
    parser.add_argument("-i", "--input-files", nargs='+')

    args = vars(parser.parse_args())
    if args["input_files"] == "":

        parser.error("-i (--input-file) cannot be equal to the empty string. ")

    if args["barcode_file"] == "":

        parser.error("-b (--barcode-file) cannot be equal to the empty string. ")

    return args

def get_sample_index(sample_table_attributes):

    sample_table_idx = -1
    for idx, attribute in enumerate(sample_table_attributes):

        if attribute == "Sample":

            return idx

def get_sample_names(bc_file):

    samples = set()
    checked_flowcell_summary = False
    all_table_idx = -1
    for idx, df in enumerate(pd.read_html(bc_file)):

        df_str = df.to_string()
        if (
            "[all projects]" in df_str
            and "[all samples]" in df_str
            and "[all barcodes]" in df_str
        ):

            all_table_idx = idx + 2
            continue

        if idx == all_table_idx:

            # convert current sample table to dictionary
            sample_table_dict = df.to_dict()
            # print sample_table_dict
            # grab all column names from the sample table and return them
            sample_table_attributes = [
                str(sample_table_dict[i][0]) for i in range(0, len(sample_table_dict))
            ]
            sample_table_idx = get_sample_index(sample_table_attributes)
            for idx, sample in sample_table_dict[sample_table_idx].items():

                samples.add(sample)


    return samples

def identify_sample_name(input_files, bc_file, samples):

    sample_name = ""
    for idx, fn in enumerate(input_files):

        for sample in samples:

            if sample in str(fn) and idx == 0:

                return sample


    print "ERROR: Sample not found in {}".format(bc_file)
    raise SystemExit


def check_file_consistency(input_files, sample_name):

    for idx, fn in enumerate(input_files):

        if sample_name not in fn:

            print "ERROR: Sample names are not consistent"
            raise SystemExit

    return sample_name

def main():

    args = get_args()
    samples = get_sample_names(args["barcode_file"])
    sample_name = identify_sample_name(args["input_files"], args["barcode_file"], samples)
    print check_file_consistency(args["input_files"], sample_name)

if __name__=="__main__":
    main()
