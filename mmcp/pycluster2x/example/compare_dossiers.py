"""
两个来源于同一份数据、batch聚档生成的档案，示例中的compare_dossiers函数检查这两个档案集，包括档案数、人数、每个人的抓拍(rid)和特征，是否完全一致

主要使用接口：
pydossier.get_rid_from_pid, pydossier.get_feature_as_view, pydossier.person_num, pydossier.cluster_num
"""

from pycluster2x import pydossier
import numpy as np

def compare_dossiers(dos1: pydossier.dossier, dos2: pydossier.dossier) -> bool:
    # 检查人数是否一致
    if dos1.person_num() != dos2.person_num():
        print("档案人数不一致")
        return False
    # 检查每个模态的档案数是否一致
    cluster_num1 = dos1.cluster_num()
    cluster_num2 = dos2.cluster_num()
    if cluster_num1 != cluster_num2:
        print(f"模态档案数不一致: {cluster_num1} vs {cluster_num2}")
        return False
    # 遍历所有人
    for pid in range(dos1.person_num()):
        # 检查每个模态的rid
        rids1 = dos1.get_rid_from_pid(pid)
        rids2 = dos2.get_rid_from_pid(pid)
        # 检查模态类型是否一致
        if set(rids1.keys()) != set(rids2.keys()):
            print(f"当前人 pid:{pid} 的模态类型不一致")
            return False
        # 检查每个模态的rid列表
        for mdl in rids1.keys():
            if sorted(rids1[mdl]) != sorted(rids2[mdl]):
                print(f"当前人 pid:{pid} 模态 {mdl.name} 的rid列表不一致")
                return False
    # 比较特征数据
    with dos1.get_feature_as_view() as ftr1, dos2.get_feature_as_view() as ftr2:
        for mdl in ftr1.keys():
            # 检查特征维度是否一致
            if len(ftr1[mdl]) != len(ftr2[mdl]):
                print(f"模态 {mdl.name} 的特征数量不一致")
                return False
            # 逐个比较特征向量
            for i in range(len(ftr1[mdl])):
                if not np.array_equal(ftr1[mdl][i], ftr2[mdl][i]):
                    print(f"模态 {mdl.name} 第 {i} 个特征不一致")
                    return False
    print("两个档案集完全一致")
    return True
