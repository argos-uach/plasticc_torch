# plasticc_torch
Tools to create torch datasets for the PLAsTiCC classification challenge

## Get the data

1. Create a folder
1. Run `./scripts/download_plasticc_from_zenodo.sh myfolder`
1. Decompress the csv's you plan to use with `gunzip`
 
## (Optional) Prepare the data

If you plan to use the lazy (explanation below) generate light curve torch tensors with 

`python src/plasticc_create_lightcurves.py myfolder`

## Data Sets

Use the `get_plasticc_datasets` function in `src/plasticc_dataset_torch.py` to create a torch dataset from the decompressed csv's

You can choose between
- Eager loading: The dataset has all the light curves in RAM, this makes data loaders faster but uses a lot of memory
- Lazy loading: The dataset search the light curves in disk. Data loader will be slower but less memory consuming

Check the `dataset_eager_vs_lazy` notebook for a comparison between these two



TODO: Evaluate dask

