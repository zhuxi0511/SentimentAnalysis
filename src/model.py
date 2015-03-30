#!/user/bin/env python
# coding: utf-8

import os
import sys
import util

def update_model_info(local_model_info, name, date):
    """update_model_info(local_model_info, name, date)

    Create or update the model_info file.
    """
    fopt = open(local_model_info, 'w')
    fopt.write('This model is train by algorithm %s, the model\'s update date is %s\n' % (name, date))
    fopt.close()
    return 0

