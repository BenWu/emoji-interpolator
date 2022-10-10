# emoji interpolator

Frame interpolation using [FILM](https://github.com/google-research/frame-interpolation) and
[Noto Emoji](https://github.com/googlefonts/noto-emoji).

## Create Custom Sequence

Import images from noto using unicode codepoint into a sequence of numbered png's (`1.png`, ...):
```sh
scripts/import_emoji_images.py \
    --src-dir ./noto-emoji/png/512 \
    --dst-dir ./test_emojis \
    --unicode-list 1F642 1F610 1F642 263A 1F642 1F60C 1F614 1F61E 1F61F 1F641 2639 1F620 2639 1F641 1F615 1FAE4 1F615 1F610 1F611
```

Move images into input format in `input/`:
```sh
scripts/prepare_image_input.py --image-dir ./test_emojis
```

Create video from sequence:
```sh
python3 -m frame-interpolation.eval.interpolator_cli \
     --pattern test_emojis \
     --model_path pretrained_models/film_net/Style/saved_model \
     --times_to_interpolate 5 \
     --fps 30 \
     --output_video
```

## Build emoji name and codepoint mappings

```sh
scripts/build_emoji_name_map.py --dst-dir scripts/
```

## Setup

### Python:

Using python 3.9

```sh
pip install -r requirements.txt
```

### Nvidia CUDA

#### Arch Linux

[cuda](https://archlinux.org/packages/community/x86_64/cuda/) and 
[cudnn](https://archlinux.org/packages/community/x86_64/cudnn/) from community repo:
```sh
pacman -S cuda cudnn
```

### Pretrained models

Pretrained models can be found [here](https://github.com/google-research/frame-interpolation#pre-trained-models).
These are expected to be in `pretrained_models/` in the repo root.
