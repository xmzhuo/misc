import argparse

ATTRIBUTES_OF_INTEREST = {
    "DBSNP_TITV": -1,
    "HET_HOMVAR_RATIO": -1,
    "TOTAL_SNPS": -1,
    "TOTAL_INDELS": -1,
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
    for attribute in ["DBSNP_TITV", "HET_HOMVAR_RATIO", "TOTAL_SNPS", "TOTAL_INDELS"]:

        metrics = reported_metrics[attribute]
        if calc_metrics:

            # app, qc_metrics, reported?, calculated?, Field
            if attribute == "DBSNP_TITV" and metrics != None:
                print "PicardVariantCallingMetrics,Ti/Tv ratio,yes,{},{}".format(
                    sum(metrics) / len(metrics), attribute
                )
            elif attribute == "HET_HOMVAR_RATIO" and metrics != None:
                print "PicardVariantCallingMetrics, Het/Hom ratio,yes,{},{}".format(
                    sum(metrics) / len(metrics), attribute
                )
            elif attribute == "TOTAL_SNPS" and metrics != None:
                print "PicardVariantCallingMetrics,SNPs,yes,{},{}".format(
                    sum(metrics), attribute
                )
            elif attribute == "TOTAL_INDELS" and metrics != None:
                print "PicardVariantCallingMetrics,INDELs,yes,{},{}".format(
                    sum(metrics), attribute
                )
            elif attribute == "DBSNP_TITV" and metrics == None:
                print "PicardVariantCallingMetrics,Ti/Tv ratio,no,NA,{}".format(
                    attribute
                )
            elif attribute == "HET_HOMVAR_RATIO" and metrics == None:
                print "PicardVariantCallingMetrics,Het/Hom ratio,no,NA,{}".format(
                    attribute
                )
            elif attribute == "TOTAL_SNPS" and metrics == None:
                print "PicardVariantCallingMetrics,SNPs,no,NA,{}".format(attribute)
            else:
                print "PicardVariantCallingMetrics,INDELs,no,NA,{}".format(attribute)

        else:

            # app, qc_metrics, reported?, Field
            if attribute == "DBSNP_TITV" and metrics != None:
                print "PicardVariantCallingMetrics,Ti/Tv ratio,yes,{}".format(attribute)
            elif attribute == "HET_HOMVAR_RATIO" and metrics != None:
                print "PicardVariantCallingMetrics, Het/Hom ratio,yes,{}".format(
                    attribute
                )
            elif attribute == "TOTAL_SNPS" and metrics != None:
                print "PicardVariantCallingMetrics,SNPs,yes,{}".format(attribute)
            elif attribute == "TOTAL_INDELS" and metrics != None:
                print "PicardVariantCallingMetrics,INDELs,yes,{}".format(attribute)
            elif attribute == "DBSNP_TITV" and metrics == None:
                print "PicardVariantCallingMetrics,Ti/Tv ratio,no,{}".format(attribute)
            elif attribute == "HET_HOMVAR_RATIO" and metrics == None:
                print "PicardVariantCallingMetrics,Het/Hom ratio,no,{}".format(
                    attribute
                )
            elif attribute == "TOTAL_SNPS" and metrics == None:
                print "PicardVariantCallingMetrics,SNPs,no,{}".format(attribute)
            else:
                print "PicardVariantCallingMetrics,INDELs,no,{}".format(attribute)


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
