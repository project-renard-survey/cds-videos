# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016 CERN.
#
# Invenio is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

""" IIIF Image Opener """

import tempfile

from wand.image import Image

from invenio_records_files.api import ObjectVersion

from ..xrootd.utils import replace_xrootd, file_opener_xrootd

def image_opener(uuid):
    """ Find a file based on its UUID.

    :param uuid: a UUID in the form bucket:filename
    :returns: a file path or handle to the file or its preview image
    :rtype: string or handle
    """
    bucket, _file = uuid.split(':', 1)
    ret = ObjectVersion.get(bucket, _file).file.uri
    # Open the Image
    opened_image = file_opener_xrootd(ret)
    if '.' in _file:
        ext = _file.split('.')[-1]
        if ext in ['txt', 'pdf']:
            img = Image(opened_image)
            # Get the first page from text and pdf files
            first_page = Image(img.sequence[0])
            tempfile = tempfile.TemporaryFile()
            with first_page.convert(format='png') as converted:
                converted.save(file=tempfile)
            return tempfile
    # Return an open file to IIIF
    return opened_image
