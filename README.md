# MS21: A NEW VERSION OF MIXING SECRETS DATASET FOR MUSIC SOURCE SEPARATION

This is an accompanying repository of a submission to Late Breaking Demo of International Society of Music Information Retrieval 2022: 

This repository contains scripts for:
* Data Gathering from [The 'Mixing Secrets' Free Multitrack Download Library](https://cambridge-mt.com/ms/mtk/); 
```
python geturl.py                               # To generate downloadurls.txt, which will be stored in the same folder
python download_zip.py  "path_to_storage"      # To download the zipped multi-track archives and mp3 mixtures using the urls in downloadurls.txt
python unrar.py "path_to_storage"              # To unzip the zipped archives in the "multitrack_zip" folder and put them in the "unzip_multitrack" folder
python unzip_folder_setup.py "path_to_unzip_multitrack_directory"         # To unify the folder structure
```

* Semi-automatically annotation generation;
```
python instrument_classify.py "path_to_unzip_multitrack"                 # To generate annotation .csv
```
* Basic DSP for audio files :Resampling, zero-padding, "monorizing";
```

python soundfile_check.py -h
  --path PATH, -p PATH  Dataset directory
  --samplerate SAMPLERATE, -sr SAMPLERATE
                        Target Sampling Rates
  --bitrate BITRATE, -bt BITRATE
                        Target Bit Rate
  --mono, -m            Stereo: False, Mono: True
  --pad, -pd            For zero-padding, boolean
```
* After splitting the dataset. we can do track-level loudness normalization:
```
python ms21_normalization.py "path_to_dataset" "output_path" -25      # Default target_loudness = -25 LUKS
```
* Automatic Stem generation and Formatting: Same folder structure of MedleyDB and special automatic mixing algorithm for generating stereo backing vocal stem. 
```
python ms21_generate_yaml.py "path_to_the_splitted_and_normalized_dataset" "outpath_to_the_well_structured_dataset"       #Note that within the script target loudness is set to -25 LUFS
```


## Citation
The link to my master thesis: https://zenodo.org/record/7116102#.YzR0L3ZBzBU
```
@phdthesis{huicheng_zhang_2022_7116102,
  author       = {Huicheng Zhang},
  title        = {{Hierarchical Music Source Separation Using Mixing 
                   Secret Multi-track Dataset}},
  school       = {Universitat Pompeu Fabra},
  year         = 2022,
  month        = sep,
  doi          = {10.5281/zenodo.7116102},
  url          = {https://doi.org/10.5281/zenodo.7116102}
}
```
The link to my presentation: https://docs.google.com/presentation/d/1BD4iTVwp2obUxl8mThp9g8DmRBhJg3G42zwxMGK_bLg/edit?usp=sharing
The link to the dataset from zenodo is coming soon!! It is big and I need to contact zenodo to increase my quota.
