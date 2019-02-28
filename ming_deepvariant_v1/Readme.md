<!-- dx-header -->
# Ming DeepVariant (DNAnexus Platform App)


This is the source code for an app that runs on the DNAnexus Platform.
For more information about how to run or modify it, see
https://wiki.dnanexus.com/.
<!-- /dx-header -->
https://github.com/google/deepvariant/blob/r0.7/docs/deepvariant-quick-start.md


<!-- Insert a description of your app here -->
DeepVariant quick start
This is an explanation of how to use DeepVariant.

Background
To get started, you'll need the DeepVariant programs (and some packages they depend on), some test data, and of course a place to run them.

We've provided a docker image, and some test data in a bucket on Google Cloud Storage. The instructions below show how to download those using the gsutil command, which you can get by installing the Cloud SDK.

Warning: there is an Ubuntu package with the same name, but it is a different thing!

Update since r0.7 : using docker instead of copying binaries.
Starting from the 0.7 release, we use docker to run the binaries instead of copying binaries to local machines first. You can still read about the previous approach in the Quick Start in r0.6. We recognize that there might be some overhead of using docker run. But using docker makes this case study easier to generalize to different versions of Linux systems. For example, we have verified that you can use docker to run DeepVariant on other Linux systems such as CentOS 7.

If you want to compile the DeepVariant binaries for yourself (from the source distribution on github) and run with your own data, that's fine too. Just replace the steps in this document that fetch those things. The binaries we ship are not compiled with aggressive optimizations, so they can run on more platforms, so it may be worth tuning those flags for your hardware.

A Cloud platform can provide a convenient place to run, with both CPU, GPU, or TPU support, if you don't have an available Linux machine of your own. We find it handy to do these sort of exercises in that way, since DeepVariant requires a number of extra system packages to be installed.

We made some notes about Google Cloud Platform which might be useful.

Get docker image, models, and test data
Before you start running, you need to have the following input files:

A reference genome in FASTA format and its corresponding index file (.fai). We'll refer to this as ${REF} below.

An aligned reads file in BAM format and its corresponding index file (.bai). We'll refer to this as ${BAM} below. You get this by aligning the reads from a sequencing instrument, using an aligner like BWA for example.

A model checkpoint for DeepVariant. We'll refer to this as ${MODEL} below.

BUCKET="gs://deepvariant"
BIN_VERSION="0.7.0"
MODEL_VERSION="0.7.0"

MODEL_NAME="DeepVariant-inception_v3-${MODEL_VERSION}+data-wgs_standard"
MODEL_BUCKET="${BUCKET}/models/DeepVariant/${MODEL_VERSION}/${MODEL_NAME}"
DATA_BUCKET="${BUCKET}/quickstart-testdata"

sudo apt -y update
sudo apt-get -y install docker.io
sudo docker pull gcr.io/deepvariant-docker/deepvariant:"${BIN_VERSION}"
Download a model
Models file are stored in a shared Cloud Storage bucket:

gs://deepvariant/models

In this bucket models are organized into subdirectories by program name and version, such as for the model to run on whole genome sequencing data:

DeepVariant/0.7.0/DeepVariant-inception_v3-0.7.0+data-wgs_standard/
and for the model to run on whole exome sequencing data.

DeepVariant/0.7.0/DeepVariant-inception_v3-0.7.0+data-wes_standard/
The model files are tagged with the program name and version, model name and the data used to train the model. The CL number (google's code commit identifier) may be safely ignored.

IMPORTANT: Models are tied to specific software versions. For example, you can use model version 0.2.* with any software version 0.2.*. We recommend using the latest software and the latest model.

Once you've selected an appropriate model directory, you can download it with the gsutil command. The path to these model checkpoint files can then be provided to call_variants.

For example, let's download from the repository:

gsutil cp -R "${MODEL_BUCKET}" .
This should create a subdirectory in the current directory containing three files:

ls -1 "${MODEL_NAME}/"
producing:

model.ckpt.data-00000-of-00001
model.ckpt.index
model.ckpt.meta
These files are in the standard TensorFlow checkpoint format.

Download test data
We've prepared a small test data bundle for use in this quick start guide that can be downloaded to your instance with the gsutil command.

Download the test bundle:

gsutil cp -R "${DATA_BUCKET}" .
This should create a subdirectory in the current directory containing the actual data files:

ls -1 quickstart-testdata/
outputting:

NA12878_S1.chr20.10_10p1mb.bam
NA12878_S1.chr20.10_10p1mb.bam.bai
test_nist.b37_chr20_100kbp_at_10mb.bed
test_nist.b37_chr20_100kbp_at_10mb.vcf.gz
test_nist.b37_chr20_100kbp_at_10mb.vcf.gz.tbi
ucsc.hg19.chr20.unittest.fasta
ucsc.hg19.chr20.unittest.fasta.fai
ucsc.hg19.chr20.unittest.fasta.gz
ucsc.hg19.chr20.unittest.fasta.gz.fai
ucsc.hg19.chr20.unittest.fasta.gz.gzi
Run the pipeline
DeepVariant consists of 3 main binaries: make_examples, call_variants, and postprocess_variants. For this quick start guide we'll store the output in a new directory on the instance and set up variables to refer to the test data we downloaded above:

OUTPUT_DIR=/home/${USER}/quickstart-output
mkdir -p "${OUTPUT_DIR}"
REF=/home/${USER}/quickstart-testdata/ucsc.hg19.chr20.unittest.fasta
BAM=/home/${USER}/quickstart-testdata/NA12878_S1.chr20.10_10p1mb.bam
MODEL="/home/${USER}/${MODEL_NAME}/model.ckpt"
make_examples
make_examples is the command used to extract pileup images from your BAM files, encoding each as tf.Example (a kind of protocol buffer that TensorFlow knows about) in "tfrecord" files. This tool is used as the first step of both training and inference pipelines.

Here is an example command that would be used in inference (variant "calling") mode:

sudo docker run \
  -v /home/${USER}:/home/${USER} \
  gcr.io/deepvariant-docker/deepvariant:"${BIN_VERSION}" \
  /opt/deepvariant/bin/make_examples \
  --mode calling   \
  --ref "${REF}"   \
  --reads "${BAM}" \
  --regions "chr20:10,000,000-10,010,000" \
  --examples "${OUTPUT_DIR}/examples.tfrecord.gz"
If your machine has multiple cores, you can utilize them by running multiple make_examples using the --task flag, which helps you split the input and generates sharded output. Here is an example:

First install the GNU parallel tool to allow running multiple processes.

sudo apt-get -y install parallel
LOGDIR=/home/${USER}/logs
N_SHARDS=3

mkdir -p "${LOGDIR}"
time seq 0 $((N_SHARDS-1)) | \
  parallel --eta --halt 2 --joblog "${LOGDIR}/log" --res "${LOGDIR}" \
  sudo docker run \
    -v /home/${USER}:/home/${USER} \
    gcr.io/deepvariant-docker/deepvariant:"${BIN_VERSION}" \
    /opt/deepvariant/bin/make_examples \
    --mode calling \
    --ref "${REF}" \
    --reads "${BAM}" \
    --examples "${OUTPUT_DIR}/examples.tfrecord@${N_SHARDS}.gz" \
    --regions '"chr20:10,000,000-10,010,000"' \
    --task {}
To explain what sharded output is, for example, if N_SHARDS is 3, you'll get three output files from the above command:

${OUTPUT_DIR}/examples.tfrecord-00000-of-00003.gz
${OUTPUT_DIR}/examples.tfrecord-00001-of-00003.gz
${OUTPUT_DIR}/examples.tfrecord-00002-of-00003.gz
In this example command above, we also used the --regions '"chr20:10,000,000-10,010,000"' flag, which means we'll only process 10 kilobases of chromosome 20.

call_variants
Once we have constructed the pileup images as "examples", we can then invoke the variant calling tool to perform inference---identifying and labeling genomic variants. We need to tell the call_variants command where to find the trained machine learning model, using the --checkpoint argument.

Example command:

CALL_VARIANTS_OUTPUT="${OUTPUT_DIR}/call_variants_output.tfrecord.gz"

sudo docker run \
  -v /home/${USER}:/home/${USER} \
  gcr.io/deepvariant-docker/deepvariant:"${BIN_VERSION}" \
  /opt/deepvariant/bin/call_variants \
 --outfile "${CALL_VARIANTS_OUTPUT}" \
 --examples "${OUTPUT_DIR}/examples.tfrecord@${N_SHARDS}.gz" \
 --checkpoint "${MODEL}"
Notice that the output of this command is another "tfrecord.gz" file---this, again, is serialized protocol buffer data.

postprocess_variants
To convert the tfrecord output of call_variants into the VCF format that is familiar to bioinformaticists, we need to invoke the postprocess_variants tool.

An example command is below. Note that the output file should end with either .vcf or .vcf.gz.

FINAL_OUTPUT_VCF="${OUTPUT_DIR}/output.vcf.gz"

sudo docker run \
  -v /home/${USER}:/home/${USER} \
  gcr.io/deepvariant-docker/deepvariant:"${BIN_VERSION}" \
  /opt/deepvariant/bin/postprocess_variants \
  --ref "${REF}" \
  --infile "${CALL_VARIANTS_OUTPUT}" \
  --outfile "${FINAL_OUTPUT_VCF}"
Evaluating the results
Here we use the hap.py (https://github.com/Illumina/hap.py) program from Illumina to evaluate the resulting 10 kilobase vcf file. This serves as a quick check to ensure the three DeepVariant commands ran correctly.

sudo docker pull pkrusche/hap.py
sudo docker run -it -v /home/${USER}:/home/${USER} \
  pkrusche/hap.py /opt/hap.py/bin/hap.py \
  /home/${USER}/quickstart-testdata/test_nist.b37_chr20_100kbp_at_10mb.vcf.gz \
  "${FINAL_OUTPUT_VCF}" \
  -f /home/${USER}/quickstart-testdata/test_nist.b37_chr20_100kbp_at_10mb.bed \
  -r "${REF}" \
  -o "${OUTPUT_DIR}/happy.output" \
  --engine=vcfeval \
  -l chr20:10000000-10010000

############################
<!--
TODO: This app directory was automatically generated by dx-app-wizard;
please edit this Readme.md file to include essential documentation about
your app that would be helpful to users. (Also see the
Readme.developer.md.) Once you're done, you can remove these TODO
comments.

For more info, see https://wiki.dnanexus.com/Developer-Portal.
-->
