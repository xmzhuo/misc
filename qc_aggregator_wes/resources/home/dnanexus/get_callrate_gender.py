import argparse


ATTRIBUTES_OF_INTEREST = {
    "Call rate": -1,
    "Pass callrate": -1,
    "Gender": -1,
    "Pass gender": -1,
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
    for attribute in ["Call rate", "Pass callrate", "Gender", "Pass gender"]:

        metrics = reported_metrics[attribute]
        if calc_metrics:

            # app, qc_metrics, reported?, calculated?, Field
            if attribute == "Call rate" and metrics != None:
                print "get_callrate_gender_from_bam-readcount,Call rate,yes,{},{}".format(
                    metrics[0], attribute
                )
            elif attribute == "Pass callrate" and metrics != None:
                print "get_callrate_gender_from_bam-readcount,Pass callrate,yes,{},{}".format(
                    metrics[0], attribute
                )
            elif attribute == "Gender" and metrics != None:
                print "get_callrate_gender_from_bam-readcount,Gender,yes,{},{}".format(
                    metrics[0], attribute
                )
            elif attribute == "Pass gender" and metrics != None:
                print "get_callrate_gender_from_bam-readcount,Pass gender,yes,{},{}".format(
                    metrics[0], attribute
                )
            elif attribute == "Call rate" and metrics == None:
                print "get_callrate_gender_from_bam-readcount,Call rate,no,NA,{}".format(
                    attribute
                )
            elif attribute == "Pass callrate" and metrics == None:
                print "get_callrate_gender_from_bam-readcount,Pass callrate,no,NA,{}".format(
                    attribute
                )
            elif attribute == "Gender" and metrics == None:
                print "get_callrate_gender_from_bam-readcount,Gender,no,NA,{}".format(
                    attribute
                )
            else:
                print "get_callrate_gender_from_bam-readcount,Pass gender,no,NA,{}".format(
                    attribute
                )

        else:

            # app, qc_metrics, reported?, Field
            if attribute == "Call rate" and metrics != None:
                print "get_callrate_gender_from_bam-readcount,Call rate,yes,{}".format(
                    attribute
                )
            elif attribute == "Pass callrate" and metrics != None:
                print "get_callrate_gender_from_bam-readcount,Pass callrate,yes,{}".format(
                    attribute
                )
            elif attribute == "Gender" and metrics != None:
                print "get_callrate_gender_from_bam-readcount,Gender,yes,{}".format(
                    attribute
                )
            elif attribute == "Pass gender" and metrics != None:
                print "get_callrate_gender_from_bam-readcount,Pass gender,yes,{}".format(
                    attribute
                )
            elif attribute == "Call rate" and metrics == None:
                print "get_callrate_gender_from_bam-readcount,Call rate,no,{}".format(
                    attribute
                )
            elif attribute == "Pass callrate" and metrics == None:
                print "get_callrate_gender_from_bam-readcount,Pass callrate,no,{}".format(
                    attribute
                )
            elif attribute == "Gender" and metrics == None:
                print "get_callrate_gender_from_bam-readcount,Gender,no,{}".format(
                    attribute
                )
            else:
                print "get_callrate_gender_from_bam-readcount,Pass gender,no,{}".format(
                    attribute
                )


def main():

    args = get_args()

    reported_metrics = {k: [] for k in ATTRIBUTES_OF_INTEREST}
    with open(args["input_file"]) as multi_metrics:

        for idx, line in enumerate(multi_metrics):

            line = line.strip().split(",")
            if idx == 0:

                index_headers_to_attributes_we_need(line)

            else:

                if len(line) != 0:
                    for attribute, idx in ATTRIBUTES_OF_INTEREST.items():

                        if idx == -1:

                            reported_metrics[attribute] = None

                        else:

                            reported_metrics[attribute].append(line[idx])

    report_metrics_to_csv(reported_metrics, args["calc_metrics"])


if __name__ == "__main__":
    main()
