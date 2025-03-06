"""
通过一个pid列表，获取档案集中这些pid管理的人的所有抓拍，合并这些抓拍，进行batch聚类，返回聚类结果

主要使用函数：
pydossier.dossier.get_person_info, pypic.pic_info.__add__, cluster_hdl, batch
"""

from pycluster2x import pycluster, pydossier, pypic

def get_info_and_batch(dos1: pydossier.dossier, pids:'list[int]'):
    combined_pic_info = pypic.pic_info()
    for pid in pids:
        combined_pic_info += dos1.get_person_info(pid)

    alg = pycluster.cluster_hdl([pycluster.FACE, pycluster.BODY], pycluster.default_cfg())
    new_dossier = pydossier.dossier(alg)
    new_dossier.batch(combined_pic_info)

    return new_dossier