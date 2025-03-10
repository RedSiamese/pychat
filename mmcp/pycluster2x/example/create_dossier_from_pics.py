"""
通过已有的一系列抓拍信息信息，已知这些抓拍的rid，已知这些抓拍中哪些抓拍对应的是同一个人，从而构造档案集。

主要使用函数：
simple_batch  add_person_from_pic
"""

from pycluster2x import pydossier, pypic, pycluster

# 方法1 使用simple_batch预设label和dossier_label的功能
def create_dossier_from_pics_1(pic_info: pypic.pic_info, pid_map: dict[pycluster.mdl_e, list[int]], mid_map: dict[pycluster.mdl_e, list[int]] | None = None) -> pydossier.dossier:
    # 创建算法句柄
    alg = pycluster.cluster_hdl([pycluster.FACE, pycluster.BODY], pycluster.default_cfg())
    # 创建一个新的档案集
    dossier = pydossier.dossier(alg)

    # 当我们只知道每张抓拍对应是哪个人的，但是不知道知道这些抓拍是否分布在这个人的同一个档案中还是这个人的不同档案中
    if mid_map is None:
        mid_map = {}
        for mdl in pid_map.keys():
            mid_map[mdl] = [0] * len(pid_map[mdl])  # 所有抓拍默认在同一个档案中，使用 0 作为 mid

    # 使用 batch 方法进行聚档
    dossier.simple_batch(pic_info, labels=pid_map, dossier_labels=mid_map)
    return dossier


# 方法2 使用add_person_from_pic，这个方法不支持把抓拍分到同一个人的不同档案中
# 它接受多个pypic.pic_info，每个pypic.pic_info是一个人的抓拍信息
def create_dossier_from_pics_2(pic_info: list[pypic.pic_info]) -> pydossier.dossier:
    # 创建算法句柄
    alg = pycluster.cluster_hdl([pycluster.FACE, pycluster.BODY], pycluster.default_cfg())
    # 创建一个新的档案集
    dossier = pydossier.dossier(alg)
    for pb in pic_info:
        dossier.add_person_from_pic(pb)
    return dossier