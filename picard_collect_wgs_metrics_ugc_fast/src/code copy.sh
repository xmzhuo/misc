#!/bin/bash
# @Modified by Xinming Zhuo @ UPMC with picard v2.18.14 for fast mode
# Copyright (C) 2013 DNAnexus, Inc.
#   This file is part of dnanexus-example-applets.
#   You may use this file under the terms of the Apache License, Version 2.0;
#   see the License.md file for more information.


# The following line causes bash to exit at any point if there is any error
# and to output each line as it is executed -- useful for debugging
set -e -x

# Calculate 90% of memory size, for java
mem_in_mb=`head -n1 /proc/meminfo | awk '{print int($2*0.9/1024)}'`
java="java -Xmx${mem_in_mb}m"

#
# Fetch inputs
#
dx-download-all-inputs

#
# Run CalculateHsMetrics
#
tar -zxvf $genome_fastaindex_path
mkdir -p ~/out/wgsmetrics_file/
$java -jar /picard.jar CollectWgsMetrics I="$bam_path" R=genome.fa O="out/wgsmetrics_file/${bam_prefix}.wgs_metrics" USE_FAST_ALGORITHM="true" $advanced_options

#
# Upload outputs
#
dx-upload-all-outputs
