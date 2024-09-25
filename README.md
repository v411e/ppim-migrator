> [!NOTE]
> Compatibility: <br>
> v0.0.5 → Immich version 1.106.x - latest<br>
> v0.0.4 → Immich version 1.105.x<br>
> v0.0.2 → Immich version 1.93.x - 1.104.x

[![PyPI version](https://badge.fury.io/py/ppim-migrator.svg)](https://badge.fury.io/py/ppim-migrator)
# Photoprism to Immich migrator
This tool can migrate albums and favorites from Photoprism to Immich. It does not migrate your photo files.

## Prerequisites
1. The tool will only work if you keep the same file structure in immich that you already had in photoprism. This is the case if you take the `originals` folder from photoprism and use it in immich as external library.
2. Photoprism and Immich must both be running at the same time, because the tool communicates with both APIs.

## How it works
![ppim-migrator-diagram](https://github.com/v411e/ppim-migrator/assets/8049779/2231d351-8f67-4750-be28-ce9e3339d1c0)


### Migrate favorites
1. The tool fetches all photos with a `favorite` tag from your photoprism instance
2. For each photo, it retrieves the original `filename` and its respective `path`
3. It connects to immich, tries to find the photo by `filename` and validates potential candidates on the immich side by comparing the file `path`
4. If a match was found, it marks the photo on immich as `favorite`

### Migrate album
1. The tool fetches all photos of a certain `album` from your photoprism instance
2. For each photo, it retrieves the original `filename` and its respective `path`
3. It connects to immich, tries to find the photo by `filename` and validates potential candidates on the immich side by comparing the file `path`
4. If a match was found, it creates a new `album` in immich and adds the matched photos

### Migrate all albums
1. The tool fetches all albums from your photoprism instance (1000 albums by default)
2. For each album found, the migration is launched as described per the previous paragraph.

## Installation
```
pip install ppim-migrator
```

## Configuration
Create a `config.yaml` file in the working directory where you want to run the command.
```
photoprism:
  base_url: https://photoprism.example.com
  username: 
  password: 
immich:
  base_url: https://immich.example.com
  api_key: 
```
Notes:
* The PhotoPrism account must not have two factor authentication enabled
* `base_url` must not end with a slash
  
## Usage
### Migrate all favorites from photoprism to immich
```
python -m ppim-migrator migrate-favorites
```

### Migrate a certain album from photoprism to immich
To get an `album-id` just open the album in photoprism. The id is part of the url. 
Example:
- Url, when opening the album: `https://photoprism.example.com/library/albums/aqrcixa2uf1q45iq/view`
  The `album-id` would be `aqrcixa2uf1q45iq`
```
python -m ppim-migrator migrate-album <album-id-here>
```

### Migrate all albums from photoprism to immich
```
python -m ppim-migrator migrate-all-albums
```
You can overwrite the default 1000 albums cap, by adding a `--count=` option:
```
python -m ppim-migrator migrate-all-albums --count=5000
```

### Migrate JPG+RAW stacks from photoprism to immich
Since Immich does not support auto stacking yet, these stacks can be migrated over from photoprism.
```
python -m ppim-migrator migrate-stacked-raws
```
You can overwrite the default 100000 photos cap, by adding a `--count=` option:
```
python -m ppim-migrator migrate-stacked-raws --count=200000
```
