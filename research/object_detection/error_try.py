# from tensorflow.python.util import compat
# from tensorflow.python import _pywrap_file_io
# path=compat.path_to_str('D:/pycharm_community/tensorflow_object_detection_API/models_master/research/object_detection/TL_training/ssd_mobilenet_v2_raccoon.config')
# _read_buf = _pywrap_file_io.BufferedInputStream(
#     path, 1024 * 512)
# print(path)
# print(_read_buf)

# from tensorflow.python import pywrap_tensorflow
# import os
#
# checkpoint_path=r'D:\pycharm_community\tensorflow_object_detection_API\models_master\research\object_detection\TL_model/model.ckpt-1649'
# reader=pywrap_tensorflow.NewCheckpointReader(checkpoint_path)
# var_to_shape_map=reader.get_variable_to_shape_map()
# for key in var_to_shape_map:
#     print('tensor_name: ',key)

import tensorflow as tf
_CONVERSION = {
    'LegacyParallelInterleaveDatasetV2': 'ParallelMapDatasetV2',
}
saver = tf.train.import_meta_graph("./TL_model/model.ckpt-1649.meta", clear_devices=True)
print(saver)