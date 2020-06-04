# Expects a valid directory to download the data
if [ "$#" -ne 1 ] || ! [ -d "$1" ]; then
  echo "Please specify a valid directory to download the data" >&2
  exit 1
fi
echo "Downloading files on $1"

# Download metadata
wget -nc --directory-prefix=$1 https://zenodo.org/record/2539456/files/plasticc_train_metadata.csv.gz; 
wget -nc --directory-prefix=$1 https://zenodo.org/record/2539456/files/plasticc_test_metadata.csv.gz; 

# Download lightcurves
wget -nc --directory-prefix=$1  https://zenodo.org/record/2539456/files/plasticc_train_lightcurves.csv.gz; 
for i in {01..11}; 
    do wget -nc --directory-prefix=$1 https://zenodo.org/record/2539456/files/plasticc_test_lightcurves_$i.csv.gz; 
done

# Files should be decompressed using gunzip