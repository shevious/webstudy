import datasets
from pathlib import Path
import pandas as pd
import torch

class GenreConfig(datasets.BuilderConfig):
    """Builder Config for Food-101"""
 
    def __init__(self, data_url, metadata_urls, **kwargs):
        """BuilderConfig for Food-101.
        Args:
          data_url: `string`, url to download the zip file from.
          metadata_urls: dictionary with keys 'train' and 'validation' containing the archive metadata URLs
          **kwargs: keyword arguments forwarded to super.
        """
        super().__init__(version=datasets.Version("1.0.0"), **kwargs)
        self.data_url = data_url
        self.metadata_urls = metadata_urls

class Genre(datasets.GeneratorBasedBuilder):
    """Genre dataset"""
 
    BUILDER_CONFIGS = [
        GenreConfig(
            name="movie",
            description="Food types commonly eaten during breakfast.",
            data_url="https://link-to-breakfast-foods.zip",
            metadata_urls={
                "train": "https://link-to-breakfast-foods-train.txt", 
                "validation": "https://link-to-breakfast-foods-validation.txt"
            },
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description="my description",
            features=datasets.Features(
                {
                    "input_ids": datasets.Sequence(datasets.Value("int32")),
                    "attention_mask": datasets.Sequence(datasets.Value("int32")),
                    "label": datasets.ClassLabel(names=[i for i in range(15)]),
                    "title": datasets.Value('string'),
                    "vector": datasets.Array2D(shape=(-1,4096), dtype='float32'),
                }
            ),
            supervised_keys=("image", "label"),
            homepage="my homepage",
            citation="citation",
            license="license",
    
        )
        
    def _split_generators(self, dl_manager):
        folder = Path('sequence_classification')
        #archive_path = dl_manager.download(_BASE_URL)
        #split_metadata_paths = dl_manager.download(_METADATA_URLS)
        df_train = pd.read_excel(folder/'genre_train_new.xlsx')
        df_val = pd.read_excel(folder/'genre_val_new.xlsx')
        #df_train = df_train.iloc[0:200]
        train_ids = torch.load(folder/'genre_train.pt', weights_only=False)
        val_ids = torch.load(folder/'genre_val.pt', weights_only=False)
        splitgen_train = datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "df": df_train,
                    "ids": train_ids,
                    "pt_file": [folder/'train'/f'{i:05}.pt' for i in range(len(df_train))]
                },
                #num_examples=len(df_train),
                #split_info = datasets.SplitInfo(
                    ##name=datasets.Split.TRAIN,
                    #num_examples=len(df_train),
                #),
            )
        #print(splitgen_train.split_info)
        splitgen_train.split_info.num_examples = len(df_train)
        splitgen_val = datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    #"images": dl_manager.iter_archive(archive_path),
                    #"metadata_path": split_metadata_paths["test"],
                    "df": df_val,
                    "ids": val_ids,
                    "pt_file": [folder/'val'/f'{i:05}.pt' for i in range(len(df_val))]
                },
                #split_info = datasets.SplitInfo(
                    ##name=datasets.Split.TRAIN,
                    #num_examples=len(df_val),
                #),
            )
        splitgen_val.split_info.num_examples = len(df_val)
        return [
            splitgen_train, splitgen_val,
        ]
    def _generate_examples(self, df, ids, pt_file):
        """Generate images and labels for splits."""
        for i, row in df.iterrows():
            #print(i)
            #print(ids[i]['input_ids'][0].numpy())
            vector = torch.load(pt_file[i])
            #print(pt_file[i], vector.shape)
            out_dict = {
                "input_ids": ids[i]['input_ids'][0],
                "attention_mask": ids[i]['attention_mask'][0],
                "title": row['filename'],
                "label": row['genre_category'],
                "vector": vector.numpy(),
            }
            #print(out_dict)
            yield i, out_dict
