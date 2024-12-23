dataset_type = 'SARDataset'
data_root = '/data/seekyou/Algos/ARC/data/split_ss_ssdd/'
img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=False)
    # mean=[127.5],  # 灰度图的均值，一般可以取127.5（像素值范围0-255）
    # std=[127.5],
    # to_rgb=False)   # 灰度图的标准差，一般也取127.5)
train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadOBBAnnotations', with_bbox=True,
         with_label=True, obb_as_mask=True),
    dict(type='LoadDOTASpecialInfo'),
    dict(type='Resize', img_scale=(608, 608), keep_ratio=True),
    dict(type='OBBRandomFlip', h_flip_ratio=0.5, v_flip_ratio=0.5),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='RandomOBBRotate', rotate_after_flip=True,
         angles=(0, 0), vert_rate=0.5, vert_cls=['ship']),
    dict(type='Pad', size_divisor=32),
    dict(type='DOTASpecialIgnore', ignore_size=2),
    dict(type='FliterEmpty'),
    dict(type='Mask2OBB', obb_type='obb'),
    dict(type='OBBDefaultFormatBundle'),
    dict(type='OBBCollect', keys=['img', 'gt_bboxes', 'gt_obboxes', 'gt_labels'])
]
test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='MultiScaleFlipRotateAug',
        img_scale=[(608, 608)],
        h_flip=False,
        v_flip=False,
        rotate=False,
        transforms=[
            dict(type='Resize', keep_ratio=True),
            dict(type='OBBRandomFlip'),
            dict(type='Normalize', **img_norm_cfg),
            dict(type='RandomOBBRotate', rotate_after_flip=True),
            dict(type='Pad', size_divisor=32),
            dict(type='ImageToTensor', keys=['img']),
            dict(type='OBBCollect', keys=['img']),
        ])
]

# does evaluation while training
# uncomments it  when you need evaluate every epoch
data = dict(
    samples_per_gpu=2,
    workers_per_gpu=4,
    train=dict(
        type=dataset_type,
        task='Task1',
        ann_file=data_root + 'train/annfiles/',
        img_prefix=data_root + 'train/images/',
        pipeline=train_pipeline),
    val=dict(
        type=dataset_type,
        task='Task1',
        ann_file=data_root + 'test/inshore/annfiles/',
        img_prefix=data_root + 'test/inshore/images/',
        pipeline=test_pipeline),
    test=dict(
        type=dataset_type,
        task='Task1',
        ann_file=data_root + 'test/offshore/annfiles/',
        img_prefix=data_root + 'test/offshore/images/',
        pipeline=test_pipeline))
# evaluation = dict(metric='mAP')
evaluation = dict(interval=1, metric='mAP', save_best='auto')
# disable evluation, only need train and test
# uncomments it when use trainval as train
# data = dict(
#     samples_per_gpu=2,
#     workers_per_gpu=4,
#     train=dict(
#         type=dataset_type,
#         task='Task1',
#         ann_file=data_root + 'train/annfiles/',
#         img_prefix=data_root + 'train/images/',
#         pipeline=train_pipeline),
#     test=dict(
#         type=dataset_type,
#         task='Task1',
#         ann_file=data_root + 'test/annfiles/',
#         img_prefix=data_root + 'test/images/',
#         pipeline=test_pipeline))
# evaluation = None
