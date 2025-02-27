"""
通过一个dossier，获取档案集中所有的人的所有抓拍，合并这些抓拍

主要使用函数：
pydossier.dossier.get_person_info, pypic.pic_info.__add__, person_num
"""

from pycluster2x import pydossier, pypic

def get_info_and_batch(dos1: pydossier.dossier):
    combined_pic_info = pypic.pic_info()
    for pid in range(dos1.person_num()):
        combined_pic_info += dos1.get_person_info(pid)
    return combined_pic_info