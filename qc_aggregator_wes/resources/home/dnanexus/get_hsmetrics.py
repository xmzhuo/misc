import argparse

ATTRIBUTES_OF_INTEREST = {
    "MEAN_BAIT_COVERAGE": -1,
    "MEAN_TARGET_COVERAGE": -1,
    "PCT_TARGET_BASES_10X": -1,
    "PCT_TARGET_BASES_30X": -1,
}


def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-file", type=str, required=True)
    parser.add_argument("-c", "--calc-metrics", action="store_true")

    args = vars(parser.parse_args())
    if args["input_file"] == "":

        parser.error("-i (--input-file) cannot be equal to the empty string. ")

    return args


def index_headers_to_attributes_we_need(headers):

    for idx, header in enumerate(headers):

        if header in ATTRIBUTES_OF_INTEREST:

            ATTRIBUTES_OF_INTEREST[header] = idx


def report_metrics_to_csv(reported_metrics, calc_metrics):

    # report data
    # app, qc_metrics, reported?, calculated?, Field
    for attribute in ["MEAN_BAIT_COVERAGE", "MEAN_TARGET_COVERAGE", "PCT_TARGET_BASES_10X", "PCT_TARGET_BASES_30X"]:

        metrics = reported_metrics[attribute]
        if calc_metrics:

            # app, qc_metrics, reported?, calculated?, Field
            if attribute == "MEAN_BAIT_COVERAGE" and metrics != None:
                print "PicardCollectHsMetrics,MEAN_BAIT_COVERAGE,yes,{},{}".format(
                    sum(metrics) / len(metrics), attribute
                )
            elif attribute == "MEAN_TARGET_COVERAGE" and metrics != None:
                print "PicardCollectHsMetrics,MEAN_TARGET_COVERAGE,yes,{},{}".format(
                    sum(metrics) / len(metrics), attribute
                )
            elif attribute == "PCT_TARGET_BASES_10X" and metrics != None:
                print "PicardCollectHsMetrics,PCT_TARGET_BASES_>_10X,yes,{},{}".format(
                    sum(metrics) / len(metrics), attribute
                )
            elif attribute == "PCT_TARGET_BASES_30X" and metrics != None:
                print "PicardCollectHsMetrics,PCT_TARGET_BASES_>_30X,yes,{},{}".format(
                    sum(metrics) / len(metrics), attribute
                )
            if attribute == "MEAN_BAIT_COVERAGE" and metrics == None:
                print "PicardCollectHsMetrics,MEAN_BAIT_COVERAGE,no,NA,{}".format(attribute)
            elif attribute == "MEAN_TARGET_COVERAGE" and metrics == None:
                print "PicardCollectHsMetrics,MEAN_TARGET_COVERAGE,no,NA,{}".format(
                    attribute
                )
            elif attribute == "PCT_TARGET_BASES_10X" and metrics == None:
                print "PicardCollectHsMetrics,PCT_TARGET_BASES_>_30X,no,NA,{}".format(
                    attribute
                )
            elif attribute == "PCT_TARGET_BASES_30X" and metrics == None:
                print "PicardCollectHsMetrics,PCT_TARGET_BASES_>_30X,no,NA,{}".format(
                    attribute
                )

        else:

            # app, qc_metrics, reported?, Field
            if attribute == "MEAN_BAIT_COVERAGE" and metrics != None:
                print "PicardCollectHsMetrics,MEAN_BAIT_COVERAGE,yes,{}".format(attribute)
            elif attribute == "MEAN_TARGET_COVERAGE" and metrics != None:
                print "PicardCollectHsMetrics,MEAN_TARGET_COVERAGE,yes,{}".format(
                    attribute
                )
            elif attribute == "PCT_TARGET_BASES_10X" and metrics != None:
                print "PicardCollectHsMetrics,PCT_TARGET_BASES_>_10X,yes,{}".format(
                    attribute
                )
            elif attribute == "PCT_TARGET_BASES_30X" and metrics != None:
                print "PicardCollectHsMetrics,PCT_TARGET_BASES_>_30X,yes,{}".format(
                    attribute
                )
            if attribute == "MEAN_BAIT_COVERAGE" and metrics == None:
                print "PicardCollectHsMetrics,MEAN_BAIT_COVERAGE,no,NA,{}".format(attribute)
            elif attribute == "MEAN_TARGET_COVERAGE" and metrics == None:
                print "PicardCollectHsMetrics,MEAN_TARGET_COVERAGE,no,{}".format(
                    attribute
                )
            elif attribute == "PCT_TARGET_BASES_10X" and metrics == None:
                print "PicardCollectHsMetrics,PCT_TARGET_BASES_>_10X,no,{}".format(
                    attribute
                )
            elif attribute == "PCT_TARGET_BASES_30X" and metrics == None:
                print "PicardCollectHsMetrics,PCT_TARGET_BASES_>_30X,no,{}".format(
                    attribute
                )


def main():

    args = get_args()

    reported_metrics = {k: [] for k in ATTRIBUTES_OF_INTEREST}
    headers = []
    header_is_next, in_data = False, False
    with open(args["input_file"]) as multi_metrics:

        for line in multi_metrics:

            line = line.strip()
            if line.startswith("## METRICS CLASS"):

                header_is_next = True
                continue

            if header_is_next:

                index_headers_to_attributes_we_need(line.split())
                in_data, header_is_next = True, False
                continue

            if line.startswith("## HISTOGRAM"):

                break

            if in_data:

                line = line.split()
                if len(line) != 0:
                    for attribute, idx in ATTRIBUTES_OF_INTEREST.items():

                        if idx == -1:

                            reported_metrics[attribute] = None

                        else:

                            reported_metrics[attribute].append(float(line[idx]))

    report_metrics_to_csv(reported_metrics, args["calc_metrics"])


if __name__ == "__main__":
    main()
