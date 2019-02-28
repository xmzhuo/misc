import argparse

ATTRIBUTES_OF_INTEREST = {
    "TOTAL_READS": -1,
    "PF_READS_ALIGNED": -1,
    "PCT_PF_READS_ALIGNED": -1,
    "MEAN_READ_LENGTH": -1
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
    for attribute in ["TOTAL_READS", "PF_READS_ALIGNED", "PCT_PF_READS_ALIGNED", "MEAN_READ_LENGTH"]:

        metrics = reported_metrics[attribute]
        if calc_metrics:

            # app, qc_metrics, reported?, calculated?, Field
            if attribute == "TOTAL_READS" and metrics != None:
                print "PicardCollectMultipleMetrics,Total input reads,yes,{},{}".format(
                    sum(metrics), attribute
                )
            elif attribute == "PF_READS_ALIGNED" and metrics != None:
                print "PicardCollectMultipleMetrics,Mapped reads,yes,{},{}".format(
                    sum(metrics), attribute
                )
            elif attribute == "PCT_PF_READS_ALIGNED" and metrics != None:
                print "PicardCollectMultipleMetrics,Percent Mapped Reads,yes,{},{}".format(
                    sum(metrics) / len(metrics), attribute
                )
            elif attribute == "MEAN_READ_LENGTH" and metrics != None:
                print "PicardCollectMultipleMetrics,Estimated Read Length,yes,{},{}".format(    
                    sum(metrics) / len(metrics), attribute
                )
            elif attribute == "TOTAL_READS" and metrics == None:
                print "PicardCollectMultipleMetrics,Total input reads,no,NA,{}".format(
                    attribute
                )
            elif attribute == "PF_READS_ALIGNED" and metrics == None:
                print "PicardCollectMultipleMetrics,Mapped reads,no,NA,{}".format(
                    attribute
                )
            elif attribute == "PCT_PF_READS_ALIGNED" and metrics == None:
                print "PicardCollectMultipleMetrics,Percent Mapped Reads,no,NA,{}".format(
                    attribute
                )
            else:
                print "PicardCollectMultipleMetrics,Estimated Read Length,no,NA,{}".format(
                    attribute
                )

        else:

            # app, qc_metrics, reported?, Field
            if attribute == "TOTAL_READS" and metrics != None:
                print "PicardCollectMultipleMetrics,Total input reads,yes,{}".format(
                    attribute
                )
            elif attribute == "PF_READS_ALIGNED" and metrics != None:
                print "PicardCollectMultipleMetrics,Mapped reads,yes,{}".format(
                    attribute
                )
            elif attribute == "PCT_PF_READS_ALIGNED" and metrics != None:
                print "PicardCollectMultipleMetrics,Percent Mapped Reads,yes,{}".format(
                    attribute
                )
            elif attribute == "MEAN_READ_LENGTH" and metrics != None:
                print "PicardCollectMultipleMetrics,Estimated Read Length,yes,{}".format(
                    attribute
                )
            elif attribute == "TOTAL_READS" and metrics == None:
                print "PicardCollectMultipleMetrics,Total input reads,no,{}".format(
                    attribute
                )
            elif attribute == "PF_READS_ALIGNED" and metrics == None:
                print "PicardCollectMultipleMetrics,Mapped reads,no,{}".format(
                    attribute
                )
            elif attribute == "PCT_PF_READS_ALIGNED" and metrics == None:
                print "PicardCollectMultipleMetrics,Percent Mapped Reads,no,{}".format(
                    attribute
                )
            else:
                print "PicardCollectMultipleMetrics,Estimated Read Length,no,{}".format(
                    attribtue
                )


def main():

    args = get_args()

    reported_metrics = {k: [] for k in ATTRIBUTES_OF_INTEREST}
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
