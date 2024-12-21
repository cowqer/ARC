# optimizer
optimizer = dict(type='SGD', lr=0.0025, momentum=0.9, weight_decay=0.0001)#sample_per_gpu =16 gpu=2 lr =0.01------sample_per_gpu =8 gpu=2 lr =0.005
optimizer_config = dict(grad_clip=dict(max_norm=35, norm_type=2))
# learning policy
lr_config = dict(
    policy='step',
    warmup='linear',
    warmup_iters=500,
    warmup_ratio=0.001,
    step=[48, 66])
total_epochs = 72
# default_hooks = dict(
#     checkpoint=dict(
#         type="CheckpointHook",
#         save_best="coco/bbox_mAP",
#         rule="greater"
#     )
# )