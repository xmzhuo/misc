import argparse, os
import pandas as pd

# increase to_string representation of pandas data frames
pd.options.display.max_colwidth = 200
# our expected attributes
ATTRIBUTES_WE_NEED = {
    "Yield (Mbases)": -1,
    "% PFClusters": -1,
    "% >= Q30bases": -1,
    "Mean QualityScore": -1
}


def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--all-barcodes", type=str, required=True)
    parser.add_argument("-s", "--sample", type=str, required=True)
    parser.add_argument("-c", "--calc-metrics", action="store_true", required=False)

    args = vars(parser.parse_args())
    if args["all_barcodes"] == "":

        parser.error("-a (--all-barcodes) cannot be equal to the empty string. ")

    if args["sample"] == "":

        parser.error("-s (--sample) cannot be equal to the empty string. ")

    if not os.path.exists(args["all_barcodes"]):

        print "ERROR: no such file or directory - {}".format(args["all_barcodes"])
        raise SystemExit

    return args


def get_sample_idices(sample_table_attributes, sample_table_dict, sample_of_interest):

    sample_table_idx = -1
    for idx, attribute in enumerate(sample_table_attributes):

        if attribute == "Sample":

            sample_table_idx = idx

        if attribute in ATTRIBUTES_WE_NEED:

            ATTRIBUTES_WE_NEED[attribute] = idx

    sample_indices = []
    for idx, sample in sample_table_dict[sample_table_idx].items():

        if sample == sample_of_interest:

            sample_indices.append(idx)

    return sample_indices, sample_table_idx


def get_metrics_from_html(bc_file, sample, calc_metrics):

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
            sample_indices, sample_table_idx = get_sample_idices(
                sample_table_attributes, sample_table_dict, sample
            )

            unreported_metrics = []
            # for attribute, idx1 in ATTRIBUTES_WE_NEED.items():
            for attribute in [
                "Yield (Mbases)",
                "% PFClusters",
                "% >= Q30bases",
                "Mean QualityScore"
            ]:

                idx1 = ATTRIBUTES_WE_NEED[attribute]
                if idx1 == -1:

                    unreported_metrics.append(attribute)

                else:

                    qc_metric = ""
                    sample_metrics = []
                    for idx2, value in sample_table_dict[idx1].items():

                        if idx2 == 0:

                            qc_metric = value

                        elif idx2 in sample_indices:

                            sample_metrics.append(float(value))

                    # report metrics to csv file
                    report_metrics_to_csv(qc_metric, sample_metrics, calc_metrics)

            for qc_metric in unreported_metrics:

                if calc_metrics:
                    # bcl2fastq, qc_metrix, reported?, calculated?, Field
                    print "bcl2fastq,{},no,NA,{}".format(qc_metric, qc_metric)
                else:
                    # bcl2fastq, qc_metrix, reported?, Field
                    print "bcl2fastq,{},no,{}".format(qc_metric, qc_metric)


def report_metrics_to_csv(qc_metric, sample_metrics, calc_metrics):

    # report metrics
    if calc_metrics:

        # bcl2fastq, qc_metrix, reported?, calculated?, Field
        if qc_metric == "Yield (Mbases)":
            print "bcl2fastq,{},yes,{},{}".format(
                qc_metric, sum(sample_metrics), qc_metric
            )
        elif len(sample_metrics) == 0:
            print "bcl2fastq,{},yes,{},{}".format(
                qc_metric, 0.0, qc_metric
            ) 
        else:
            print "bcl2fastq,{},yes,{},{}".format(
                qc_metric, sum(sample_metrics) / len(sample_metrics), qc_metric
            )

    else:

        # bcl2fastq, qc_metrix, reported?, Field
        if qc_metric == "Yield (Mbases)":
            print "bcl2fastq,{},yes,{}".format(qc_metric, qc_metric)
        else:
            print "bcl2fastq,{},yes,{}".format(qc_metric, qc_metric)


def main():

    args = get_args()
    sample = get_metrics_from_html(
        args["all_barcodes"], args["sample"], args["calc_metrics"]
    )


if __name__ == "__main__":
    main()
