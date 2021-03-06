# coding: utf-8

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""Test DataProcessor."""

from __future__ import print_function

import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'machine_translation'))

from ..machine_translation.dataprocessor import process_dataset
from ..machine_translation.dataset import TOY


def test_translation_preprocess():
    src_lang = 'en'
    tgt_lang = 'de'
    max_lens = ((10, 10), (0, 0), (-1, -1))
    for (src_max_len, tgt_max_len) in max_lens:
        data_train = TOY('train', src_lang=src_lang, tgt_lang=tgt_lang)
        data_val = TOY('val', src_lang=src_lang, tgt_lang=tgt_lang)
        src_vocab, tgt_vocab = data_train.src_vocab, data_train.tgt_vocab
        data_val_processed = process_dataset(data_val, src_vocab, tgt_vocab,
                                             src_max_len, tgt_max_len)
        for (src, tgt), (preprocessed_src, preprocessed_tgt) in zip(data_val, data_val_processed):
            if src_max_len >= 0:
                assert len(preprocessed_src) == min(len(src.split()), src_max_len) + 1
            else:
                assert len(preprocessed_src) == len(src.split()) + 1
            if tgt_max_len >= 0:
                assert len(preprocessed_tgt) == min(len(tgt.split()), tgt_max_len) + 2
            else:
                assert len(preprocessed_tgt) == len(tgt.split()) + 2

