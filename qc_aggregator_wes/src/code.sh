#!/bin/bash
set -e -x -o pipefail 

check_file_inputs () {

    sample_file_names=()
    for i in "${!input_files[@]}"; do
       
        input_file_name=$(dx describe "${input_files[$i]}" --name)
        dx download "${input_files[$i]}" -o "${input_file_name}"
        if [[ "${input_file_name}" == *.alignment_summary_metrics ]]; then

            sample_file_names+=( "${input_file_name}" )

        elif [[ "${input_file_name}" == *.hsmetrics.txt ]]; then

            sample_file_names+=( "${input_file_name}" )     
 
        elif [[ "${input_file_name}" == *.variant_calling_detail_metrics ]]; then 

            sample_file_names+=( "${input_file_name}" )

        elif [[ "${input_file_name}" == *.get_callrate_gender.out ]]; then

            sample_file_names+=( "${input_file_name}" )

        elif [ "${input_file_name}" == "all_barcodes.html" ]; then

            echo "Barcodes file: ${input_file_name} is present." 

        else

            dx-jobutil-report-error "ERROR: file ${input_file_name} does not match the required suffix. Ensure input filenames are in correct format and are named according to the apps input specifications."

        fi

    done

}


check_sample_consistency_and_cat_inputs() {

    sample_name=$(python get_sample_name.py -b all_barcodes.html -i "${sample_file_names[@]}")
    echo "Samples names are all consistent"

    python html2text.py all_barcodes.html >> "${sample_name}.concatenated_inputs"
    cat "${sample_file_names[@]}" >> "${sample_name}.concatenated_inputs"
    echo "Input files have been concatenated!"

}


fill_sentieon_report() {

    
    if [ "${report_metrics}" == "true" ]; then

        echo "app,file,qc metric,reported?,calculated?,Field" >> "${sample_name}.sentieon_report.csv"        
        python get_barcode_metrics.py -a all_barcodes.html -s "${sample_name}" -c >> "${sample_name}.sentieon_report.csv"
        python get_alignment_summary_metrics.py -i *.alignment_summary_metrics -c >> "${sample_name}.sentieon_report.csv"
        python get_hsmetrics.py -i *.hsmetrics.txt -c >> "${sample_name}.sentieon_report.csv"
        python get_variant_calling_metrics.py -i *.variant_calling_detail_metrics -c >> "${sample_name}.sentieon_report.csv"
        python get_callrate_gender.py -i *.get_callrate_gender.out -c >> "${sample_name}.sentieon_report.csv"
    
    else

        echo "app,file,qc metric,reported?,Field" >> "${sample_name}.sentieon_report.csv"
        python get_barcode_metrics.py -a all_barcodes.html -s "${sample_name}" >> "${sample_name}.sentieon_report.csv"
        python get_alignment_summary_metrics.py -i *.alignment_summary_metrics >> "${sample_name}.sentieon_report.csv"
        python get_hsmetrics.py -i *.hsmetrics.txt >> "${sample_name}.sentieon_report.csv"
        python get_variant_calling_metrics.py -i *.variant_calling_detail_metrics >> "${sample_name}.sentieon_report.csv"
        python get_callrate_gender.py -i *.get_callrate_gender.out >> "${sample_name}.sentieon_report.csv"

    fi

}

main() {
    
    
    # get html2text.py in path
    mv /usr/share/html2text.py /home/dnanexus
	
    # download all of the input files 
    check_file_inputs  
    echo "All inputs files are present!"
 
    # check sample names have same pattern and the output suffixes are what
    # they should be 
    check_sample_consistency_and_cat_inputs
    echo "Input files have been concatenated!"

    # fill out csv table for Sentieon output report
    fill_sentieon_report

    # upload outputs 
    concat_out_file_id=$(dx upload "${sample_name}.concatenated_inputs" --brief)
    dx-jobutil-add-output concat_out "${concat_out_file_id}" --class file

    report_file_id=$(dx upload "${sample_name}.sentieon_report.csv" --brief)
    dx-jobutil-add-output  csv_out "${report_file_id}" --class file
     
}
