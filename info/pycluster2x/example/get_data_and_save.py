"""
读取数据缓存./data_cache_lqy_50w数据缓存，取1-2分区数据，存到另一个新数据缓存里面
涉及接口包括: pycache.cluster_data_cache  get_partition  save
"""

def func():
    from pycluster2x import pycache
    
    cache = pycache.cluster_data_cache("./data_cache_lqy_50w")
    dst_cache = pycache.cluster_data_cache("./new_data_cache_lqy_50w")
    pb = cache.get_partition("1-2")
    dst_cache.save(pb, "1-2")