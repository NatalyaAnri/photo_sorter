import os
import shutil

from osxmetadata import *

import const

# variables
# rename a file example_const.py to const.py with your personal variables
path_to_unsorted_photos = const.UNSORTED
path_to_root_dir = const.SORTED
dict_tags = const.TAGS


def create_dir(tag_name, created_dttm):
    # create directory for tag if not exists
    root_dir_path_sorted = f'{path_to_root_dir}{tag_name}'
    if os.path.isdir(root_dir_path_sorted) is False:
        os.mkdir(root_dir_path_sorted)

    # create dir for date if not exists
    dir_path_sorted = f'{root_dir_path_sorted}{created_dttm}/'
    if os.path.isdir(dir_path_sorted) is False:
        os.mkdir(dir_path_sorted)

    return dir_path_sorted


if __name__ == '__main__':
    # get files in unsorted files dir
    for root, dirs, files in os.walk(path_to_unsorted_photos):
        for file in files:
            # get metadata like created date and list of tags
            path_file = os.path.join(root, file)
            md = OSXMetaData(path_file)
            created_dttm = md.kMDItemContentCreationDate.date().strftime('%Y%m%d')
            tags = [t.name for t in md.tags]

            # if tag is not exists then create tag 'home'
            if len(tags) == 0:
                tags.append('home')

            # for every tag create a file copy in a need dir
            for t in tags:
                if t in dict_tags:
                    tag_name = dict_tags[t]
                else:
                    tag_name = dict_tags['home']

                dir_path_sorted = create_dir(tag_name, created_dttm)
                shutil.copy(path_file, dir_path_sorted)

            # remove file in unsorted dir
            os.remove(path_file)
