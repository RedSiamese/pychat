"""
读取数据缓存./data_cache_lqy_50w数据缓存，取1-2分区数据做batch
涉及接口包括: pycache.cluster_data_cache  get_partition  batch
"""

def func():
    from pycluster2x import pycluster, pydossier, pycache
    
    cache = pycache.cluster_data_cache("./data_cache_lqy_50w")
    pb = cache.get_partition("1-2")
    dossier_instance = pydossier.dossier(pycluster.cluster_hdl([pycluster.FACE, pycluster.BODY], pycluster.default_cfg()))
    dossier_instance.batch(pb)