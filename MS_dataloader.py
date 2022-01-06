# the sample code in pytorch example combines dataloader and datasets in the same part.
# whereas in asteroid x-umx code, they are separated, 
# it is good to separated when there are more than one dataset are trained on.

from pathlib import Path
import torch.utils.data
import random
import torch
import tqdm
import soundfile as sf
import os
import pandas as pd
# import musedb

class MS_21Dataset(torch.utils.data.Dataset):
    """MS_21 music separation dataset

    The dataset consists of 150 full lengths music tracks (~10h duration) of
    different genres along with their raw multitracks:
    

    This dataset asssumes music raw multi-tracks in (sub)folders where each folder
    has a various number of sources. 
    A linear mix is performed on the fly by summing up the sources according to 
    the grouping information in the .csv file.
    In order to be compatible to MUSDB_18 dataset, one can utilize the grouping information
    to generate the traditional four stems:
        'drums', 'vocals', 'bass', 'other'
    

    Folder Structure:
        >>> #train/1/lead_vocals.wav ------------|
        >>> #train/1/backing_vocals.wav ---------|
        >>> #train/1/drums.wav ---------------+--> input (mix),
        >>> #train/1/bass.wav -------------------|
        >>> #train/1/accordin.wav ---------------|
        >>> #train/1/bell.wav -------------------/

        >>> #train/1/lead_vocals.wav ------------> output[target]

    Args:
        root (str): Root path of dataset
        sources (:obj:`list` of :obj:`str`, optional): List of source names
            that composes the mixture.
            Defaults to MUSDB18 4 stem scenario: `vocals`, `drums`, `bass`, `other`.
        targets (list or None, optional): List of source names to be used as
            targets. If None, a dict with the 4 stems is returned.
             If e.g [`vocals`, `drums`], a tensor with stacked `vocals` and
             `drums` is returned instead of a dict. Defaults to None.
        suffix (str, optional): Filename suffix, defaults to `.wav`.
        split (str, optional): Dataset subfolder, defaults to `train`.
        subset (:obj:`list` of :obj:`str`, optional): Selects a specific of
            list of tracks to be loaded, defaults to `None` (loads all tracks).
        segment (float, optional): Duration of segments in seconds,
            defaults to ``None`` which loads the full-length audio tracks.
        samples_per_track (int, optional):
            Number of samples yielded from each track, can be used to increase
            dataset size, defaults to `1`.
        random_segments (boolean, optional): Enables random offset for track segments.
        random_track_mix boolean: enables mixing of random sources from
            different tracks to assemble mix.
        source_augmentations (:obj:`list` of :obj:`callable`): list of augmentation
            function names, defaults to no-op augmentations (input = output)
        sample_rate (int, optional): Samplerate of files in dataset.

    Attributes:
        root (str): Root path of dataset
        sources (:obj:`list` of :obj:`str`, optional): List of source names.
            Defaults to MUSDB18 4 stem scenario: `vocals`, `drums`, `bass`, `other`.
        suffix (str, optional): Filename suffix, defaults to `.wav`.
        split (str, optional): Dataset subfolder, defaults to `train`.
        subset (:obj:`list` of :obj:`str`, optional): Selects a specific of
            list of tracks to be loaded, defaults to `None` (loads all tracks).
        segment (float, optional): Duration of segments in seconds,
            defaults to ``None`` which loads the full-length audio tracks.
        samples_per_track (int, optional):
            Number of samples yielded from each track, can be used to increase
            dataset size, defaults to `1`.
        random_segments (boolean, optional): Enables random offset for track segments.
        random_track_mix boolean: enables mixing of random sources from
            different tracks to assemble mix.
        source_augmentations (:obj:`list` of :obj:`callable`): list of augmentation
            function names, defaults to no-op augmentations (input = output)
        sample_rate (int, optional): Samplerate of files in dataset.
        tracks (:obj:`list` of :obj:`Dict`): List of track metadata

    References
        "The 2018 Signal Separation Evaluation Campaign" Stoter et al. 2018.
    """

    dataset_name = "MS_21"

    def __init__(
        self,
        root,
        csv_file_path,
        grouping_info = {'percussion':['Drum_Kick','Drum_Snare','Drum_HiHat','Drum_Cymbals','Drum_Overheads','Drum_Tom','Drum_Room','Percussion'
],'vocals':['Lead_Vocal','Backing_Vocal'],'bass':'Bass','other':['Acoustic_Guitar','Electric_Guitar','Piano','Electric_Piano','Brass','String','WoodWind','Other'
]}, # default traditional four stems grouping style
        sources=["vocals", "bass", "drums", "other"],
        targets=None,
        suffix=".wav",
        split="train",
        subset=None,
        segment=None,
        samples_per_track=1,
        random_segments=False,
        random_track_mix=False,
        source_augmentations=lambda audio: audio,
        sample_rate=44100,
    ):

        self.root = Path(root).expanduser()
        self.csv_info = pd.read_csv(csv_file_path)
        
        self.grouping_info = grouping_info
        self.split = split
        self.sample_rate = sample_rate
        self.segment = segment
        self.random_track_mix = random_track_mix
        self.random_segments = random_segments
        self.source_augmentations = source_augmentations
        self.sources = sources
        self.targets = targets
        self.suffix = suffix
        self.subset = subset
        self.samples_per_track = samples_per_track
        self.tracks = list(self.get_tracks())
        #print(self.tracks)
        if not self.tracks:
            raise RuntimeError("No tracks found.")
        # self.__getitem__(index = 1)

    def __getitem__(self, index):
        # create a dict for storing stem grouping rule
        
        
        
        # assemble the mixture of target and interferers
        audio_sources = {}

        # get track_id
        track_id = index // self.samples_per_track
        #print(track_id)
        
        
        if self.random_segments:
            start = random.uniform(0, self.tracks[track_id]["min_duration"] - self.segment)
        else:
            start = 0

        # create sources based on multitracks
        for source in self.sources:
            # optionally select a random track for each source
            if self.random_track_mix:
                # load a different track
                track_id = random.choice(range(len(self.tracks)))
                if self.random_segments:
                    start = random.uniform(0, self.tracks[track_id]["min_duration"] - self.segment)

            # loads the full track duration
            start_sample = int(start * self.sample_rate)
            # check if dur is none
            if self.segment:
                # stop in soundfile is calc in samples, not seconds
                stop_sample = start_sample + int(self.segment * self.sample_rate)
            else:
                # set to None for reading complete file
                stop_sample = None

            # load actual audio
#             audio, _ = sf.read(
#                 Path(self.tracks[track_id]["path"] / source).with_suffix(self.suffix),
#                 always_2d=True,
#                 start=start_sample,
#                 stop=stop_sample,
#             )
            # load multitracks and be ready to do linear mix
            for i in self.grouping_info:
                print(i) # get source names
                stem_tracks = []
                # get all instrument name within one stem
                for j in self.grouping_info[i]:
                    # get all multitrack filename within one instrument
                    for m in j:
                        print(m)
                        stem_tracks.append(self.csv_info.iloc[track_id][m])
                    
                # apply linear mix within one source (stem) later can intergrate with data augmentation
                # first load one multitrack
                source_multitrack = {}
                for k in stem_tracks:
                    audio,_ = sf.read(
                        Path(self.tracks[track_id]['path'] / k),
                    always_2d=True,
                    start=start_sample,
                    stop=stop_sample,
                    )
                    # convert to torch tensor
                    audio = torch.tensor(audio.T, dtype=torch.float)

                    # apply multitrack-wise augmentations
                    # audio = self.multitrack_augmentation(audio)
                    source_multitrack[k] = audio
                   
                # apply linear mix over all multitracks within one source index=0
                source_mix = torch.stack(list(source_multitrack.values())).sum(0)
                audio_sources[i] = source_mix
                # apply source-wise augmentations
                # source_mix = self.source_augmentations(source_mix)
            
            audio_mix = torch.stack(list(audio_sources.values())).sum(0)
            if self.targets:
                audio_sources = torch.stack(
                    [wav for src, wav in audio_sources.items() if src in self.targets], dim=0
            )
        # audio_mix a mixture over the sources, audio_sources is a concatenation of all sources
        return audio_mix, audio_sources

    def __len__(self):
        return len(self.tracks) * self.samples_per_track

    def get_tracks(self):
        """Loads input and output tracks"""
        """load tracks that contain all the required sources tracks"""
        p = Path(self.root, self.split) # train and test folder
        # p = Path(self.root)
        
        for track_path in tqdm.tqdm(p.iterdir()):
            #print(track_path)
            if track_path.is_dir():
                if self.subset and track_path.stem not in self.subset:
                    # skip this track
                    continue

                
                # source_paths = [track_path / (s + self.suffix) for s in self.sources] # 固定命名
                
                multitrack_paths = []
                for s in os.listdir(track_path):
                    if s.split('.')[-1]=='wav' and s.split('.')[0]!='':
                        multitrack_paths.append(track_path / s )
                #print(len(multitrack_paths))
                # 改成先读取所有wav文件，返回所有path
                # 然后通过csv文件进行linear mix生成sources,直接读成tensor
                if not all(sp.exists() for sp in multitrack_paths):
                    print("Exclude track due to non-existing source", track_path)
                    continue

                # get metadata
                infos = list(map(sf.info, multitrack_paths))
                if not all(i.samplerate == self.sample_rate for i in infos):
                    print("Exclude track due to different sample rate ", track_path)
                    continue

                if self.segment is not None:
                    # get minimum duration of track
                    min_duration = min(i.duration for i in infos)
                    if min_duration > self.segment:
                        yield ({"path": track_path, "min_duration": min_duration})
                else:
                    yield ({"path": track_path, "min_duration": None})

    def get_infos(self):
        """Get dataset infos (for publishing models).

        Returns:
            dict, dataset infos with keys `dataset`, `task` and `licences`.
        """
        infos = dict()
        infos["dataset"] = self.dataset_name
        infos["task"] = "enhancement"
        infos["licenses"] = [musdb_license]
        return infos


musdb_license = dict()
