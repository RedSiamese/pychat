"""
记录内存, 显存占用和python每条线程的堆栈信息

主要使用接口：
pycluster2x.record
"""
import  pycluster2x
from pycluster2x import pycluster, pydossier, pycache

dc = pycache.cluster_data_cache("./data_cache_dsj")
pb = dc.get_partition("0-5")

# 创建档案集
dossier_instance = pydossier.dossier(pycluster.cluster_hdl([pycluster.FACE, pycluster.BODY], pycluster.default_cfg()))

# 功能依赖pycluster2x扩展包的record函数
# 使用with包裹需要记录的代码块
# 记录内存依赖psutil包
# 记录显存依赖pynvml.smi包
# 记录python堆栈依赖viztracer包
# 记录with包裹的代码块的内存、显存、堆栈信息
# 结果保存在"./info_record.json"路径下
with pycluster2x.record("./info_record.json"): 
    dossier_instance.batch(pb)
