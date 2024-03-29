#!/bin/bash
# gatk_cnv_single 0.0.1
# Generated by dx-app-wizard.
#for gatk4-cnv_single app usage 

# Basic execution pattern: Your app will run on a single machine from
# beginning to end.
#
# Your job's input variables (if any) will be loaded as environment
# variables before this script runs.  Any array inputs will be loaded
# as bash arrays.
#
# Any code outside of main() (or any entry point you may add) is
# ALWAYS executed, followed by running the entry point itself.
#
# See https://wiki.dnanexus.com/Developer-Portal for tutorials on how
# to modify this file.

main() {

    # Fill in your application code here.
    #
    echo "Value of tumor: '$tumor' : '$tumor_name' : '${tumor_prefix[0]}'"
    #echo "Value of normal: '$normal' :'$normal_name'"
    echo "Value of Reference: '$Reference' : '$Reference_name'"
    echo "Value of PoNchoice: '$PoNchoice' : '$PoNchoice_name'"
    echo "Value of SNP_list: '$SNP_list' : '$SNP_list_name'"

    # Make a data directory to mount into the Docker container
    mkdir -p /data/
    mkdir -p /data/in/
    mkdir -p /data/out/
    
    dx-download-all-inputs

    mv in/tumor_bai/* in/tumor/
    #mv in/normal_bai/* in/normal/
    mv in/Reference_fai/* in/Reference/
    mv in/Reference_dict/* in/Reference/

    mv in/* /data/in/
            
    ls /data/in/
    ls /data/out/

    # Mount the /data/ directory to /data in the container and run
    #dx-docker run -v /data/:/gatk/data broadinstitute/gatk gatk CollectReadCounts \
    #-I /gatk/data/in/tumor/${tumor_name[0]} \
    #-L /gatk/data/in/Intervallist/${Intervallist_name[0]} \
    #--interval-merging-rule OVERLAPPING_ONLY \
    #-O /gatk/data/out/${tumor_prefix[0]}.counts.hdf5
    
    chmod +x /data/in/cmd_sh/${cmd_sh_name[0]}

    dx-docker run -v /data/:/gatk/data broadinstitute/gatk /gatk/data/in/cmd_sh/${cmd_sh_name[0]}

    ls /data/out/

    mv /data/out/* out/output/

    ls /out/output/
    dx-upload-all-outputs



    # The following line(s) use the dx command-line tool to download your file
    # inputs to the local file system using variable names for the filenames. To
    # recover the original filenames, you can use the output of "dx describe
    # "$variable" --name".

    
    # Fill in your application code here.
    #
    # To report any recognized errors in the correct format in
    # $HOME/job_error.json and exit this script, you can use the
    # dx-jobutil-report-error utility as follows:
    #
    #   dx-jobutil-report-error "My error message"
    #
    # Note however that this entire bash script is executed with -e
    # when running in the cloud, so any line which returns a nonzero
    # exit code will prematurely exit the script; if no error was
    # reported in the job_error.json file, then the failure reason
    # will be AppInternalError with a generic error message.

    # The following line(s) use the utility dx-jobutil-add-output to format and
    # add output variables to your job's output as appropriate for the output
    # class.  Run "dx-jobutil-add-output -h" for more information on what it
    # does.

    #for i in "${!output[@]}"; do
    #    dx-jobutil-add-output output "${output[$i]}" --class=array:file
    #done
}
