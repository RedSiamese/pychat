"""

    pydossier是pycluster2x中档案集相关的模块，包含dossier档案集类等, 通常通过 ```from pycluster2x import pydossier```引入。

    从数据结构上，一个档案集由不同模态（pycluster.FACE,pycluster.BODY等）的数据构成，每个模态由一个或多个档案构成。
    各个模态中管理的每个档案，对应一个该模态的档案id（mid）。
    每个档案都包含若干张抓拍，每张抓拍有唯一rid（record_id）标识。
    通过算法计算，通过聚档、质心重建等接口，汇总档案中所有的抓拍的特征，得到若干个质心特征（通常为1~4个），通常0号质心称为均值质心，每个质心特征是一个特征向量，维度dim通常是256。

    从管理逻辑上，档案集中管理了一个或者多个逻辑人（后简称人），每个人可能包含多个不同模态的档案。
    档案集中管理的逻辑人在档案集中的id称为人的id（person_id,pid），指向同一个pid的不同模态的不同档案相互关联，指向不同pid的档案则不是同一个人的档案，不关联。
    
    可以通过pycluster.cluster_hdl算法句柄构造档案集，算法句柄中包含构造档案集所需要的配置表。
    pydossier中同时也定义了档案集的io接口，当读取已有档案集时也可以通过传入cfg重新配置配置表，例如档案集在服务器间进行迁移的时候，通过cfg配置修改数据缓存路径。

    关键词： 档案  逻辑人  pid   质心特征
    
"""
from __future__ import annotations
import numpy
import pycluster2x.lib.pycluster
import pycluster2x.lib.pypic
import typing
__all__ = ['async_load', 'async_load_big', 'async_load_small', 'async_unser', 'cm_update', 'dossier', 'fuse_e', 'load', 'load_big', 'load_small', 'oc_updates', 'unser']
class cm_update:
    """
    
            一个人的离线合档接口输出结果结构体
        
    """
    check_multi_label: int
    opt: str
    score: float
    src_person: int
    def __init__(self) -> None:
        ...
    def __repr__(self) -> str:
        """
        字符串格式化离线合档结果cm_update结构，格式为形如：{"src_person":31, "check_multi_label":0, "score":0.987, "opt":"self_check"}
        """
class dossier:
    """
    档案集类
    """
    class feature_viewer:
        """
        特征
        """
        def __enter__(self) -> dict[pycluster2x.lib.pycluster.mdl_e, list[numpy.ndarray[numpy.float32]]]:
            ...
        def __exit__(self, arg0: typing.Any, arg1: typing.Any, arg2: typing.Any) -> None:
            ...
    def __add__(self, arg0: dossier) -> dossier:
        """
        将两个档案集合并（管理的档案合并，不去重合档）
        例如：
        ``` python
        
        print(dossier_0+dossier_1)
        ```
        """
    def __contains__(self, rid: str) -> bool:
        """
        根据一个rid，获取该抓拍所在的pid号
        例如：
        ``` python
        
        dossier_0 = dossier.create_empty()
        if "341523210011902306500220210821161147470860603412" in dossier_0:
            print("YES")
        else:
            print("NO")
        ```
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> dossier:
        """
        生成一个仅由该档案中输入pid的这个人生成的档案集
        例如：
        ``` python
        
        dossier_0 = dossier[0]    # 生成一个仅由该档案中pid为0的人的档案集
        ```
        """
    @typing.overload
    def __getitem__(self, arg0: slice) -> dossier:
        """
        按切片获取第pid人的档案
        例如：
        ``` python
        
        dossier_0 = dossier[0:3]    # 生成一个仅由该档案中pid为0,1,2的人的档案集
        ```
        """
    @typing.overload
    def __getitem__(self, arg0: str) -> dossier:
        """
        生成一个仅由该档案中，包含输入rid的人生成的档案集
        例如：
        ``` python
        
        dossier_0 = dossier["341523210011902306500220210821161147470860603412"]    # 生成一个仅由该档案中pid为0的人的档案集
        ```
        """
    @typing.overload
    def __getitem__(self, arg0: pycluster2x.lib.pycluster.mdl_e, arg1: int) -> dossier:
        """
        生成一个仅由该档案中，根据输入的模态和mid获取到的人生成的档案集
        例如：
        ``` python
        
        dossier_0 = dossier[pycluster.FACE, 0]    # 生成一个仅由该档案中人脸mid为0的人的档案集
        ```
        """
    def __getstate__(self) -> list[int]:
        ...
    def __iadd__(self, arg0: dossier) -> dossier:
        """
        将两个档案集合并（管理的档案合并，不去重合档）
        例如：
        ``` python
        
        dossier_0 += dossier_1
        ```
        """
    def __init__(self, cluster_hdl: pycluster2x.lib.pycluster.cluster_hdl) -> None:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, arg0: list[int]) -> None:
        ...
    def add(self, other_dossier: dossier) -> dossier:
        """
        将两个档案集合并（管理的档案合并，不去重合档）
        例如：
        ``` python
        
        dossier_0.add(dossier_1)
        ```
        support asynchronous
        """
    def add_person_from_pic(self, pb_input: pycluster2x.lib.pypic.pic_info) -> None:
        """
        将输入抓拍集中一系列抓拍，认定为同一个人的抓拍，生成一个人的档案，并插入当前档案集
        例如：
        ``` python
        
        info:pypic.pic_info = dossier.get_person_info(0)    # 获取一个人（pid为0的人）档案的抓拍信息
        dossier = pydossier.dossier(pycluster.cluster_hdl([pycluster.FACE, pycluster.BODY], pycluster.default_cfg()))
        dossier.add_person_from_pic(info)   # 将输入的抓拍生成一个人，在档案集中添加这个人
        ```
        support asynchronous
        """
    @typing.overload
    def adsorbed(self, pb_input: pycluster2x.lib.pypic.pic_info) -> dossier:
        """
        吸附接口，输入抓拍集，将抓拍集中可以吸附的抓拍进行吸附，无法吸附的抓拍根据batch结果label进行建档，输出一个新的档案集
        例如：
        ``` python
        
        db = pycache.cluster_data_cache("/data/291223/data/data_cache_ah/")      # 初始化数据缓存
        it:pycache.db_it = db.get_time_it(0)               # 根据时间流，从时间流最开始，获取时间流最初的数据迭代器
        pb_info:pypic.pic_info = it.get(256)              # 从迭代器获取256张图，组成抓拍集，迭代器往后移动256张
        
        dossier = pydossier.load_small("./result/0/")
        print(dossier)
        dossier.adsorbed(pb_info)
        print(dossier)
        ```
        上述代码dossier对pb_info进行吸附，需要保证存在一些rids，既存在于dossier中，也存在于pb_info中，否则无法吸附
        
        dossier为pb_info中的rids设置预设id，对pb_info使用batch接口，这些预设id的抓拍会吸附没有预设id的抓拍，
        
        当没有预设id的抓拍的label和预设的相同时，这些没有预设的抓拍会吸附到dossier中去，没有被吸附的抓拍，即不和任意预设id相同的，会生成新的档案集输出
        
        例如：
        
        dossier底档集为[('a', 'b'), ('c', 'd'), ('e', 'f'), ('g', 'h')]，中括号为档案集，小括号为档案，字符串为抓拍
        
        pb_info 为 'a', 'i', 'x', 'y', 'c', 'g'，其中'a', 'c', 'g'为底档已有抓拍，'i', 'x', 'y'为需要被吸附的抓拍
        
        底档吸附抓拍后为 [('a', 'b', 'i'), ('c', 'd'), ('e', 'f'), ('g', 'h')]，并返回新档案集 [('x','y')] 表示'i'被吸附入'a','b'，而'x','y'无法被吸附，生成新档案集
        support asynchronous
        """
    @typing.overload
    def adsorbed(self, pb_input: pycluster2x.lib.pypic.pic_info, other_dossier: dossier) -> dossier:
        """
        根据另一个档案集中的建档情况作为先验对抓拍集进行吸附，与dossier.adsorbed(pb_info)相比，增加了other档案为pb_info中的rid预设标签
        例如：
        ``` python
        
        db = pycache.cluster_data_cache("/data/291223/data/data_cache_ah/")      # 初始化数据缓存
        it:pycache.db_it = db.get_time_it(0)               # 根据时间流，从时间流最开始，获取时间流最初的数据迭代器
        pb_info:pypic.pic_info = it.get(256)              # 从迭代器获取256张图，组成抓拍集，迭代器往后移动256张
        
        dossier = pydossier.load_small("./result/1/")
        dossier_proxy = dossier.copy()
        
        dossier_tmp:pydossier.dossier = pydossier.dossier(pycluster.cluster_hdl([pycluster.FACE, pycluster.BODY], pycluster.defaule_cfg()))
        dossier_tmp.simple_batch(pb_info)
        dossier_proxy.oc_separate(dossier_tmp)
        
        dossier.adsorbed(pb_info, dossier_proxy)
        print(dossier)
        ```
        上述代码dossier对pb_info进行吸附，需要保证存在一些rids，既存在于dossier_proxy，也存在于pb_info中，否则无法吸附，同时要求存在一些rids，既存在于dossier_proxy，也存在于dossier中
        
        只有同时存在于dossier和dossier_proxy的pid标签，才会为pb_info中的rids设置预设id，对pb_info使用batch接口，这些预设id的抓拍会吸附没有预设id的抓拍，
        
        当没有预设id的抓拍的label和预设的相同时，这些没有预设的抓拍会吸附到dossier中去，没有被吸附的抓拍，即不和任意预设id相同的，会生成新的档案集输出
        
        此接口常用于实时底档生成并吸附一些抓拍后，历史底档仅对实时底档中，吸附入历史档案的抓拍进行预设，对于实时底档中新增的档案进行吸附
        
        例如：
        
        历史底档集为[('a', 'b'), ('c', 'd'), ('e', 'f'), ('g', 'h')]，中括号为档案集，小括号为档案，字符串为抓拍，实时底档为[('a', 'b'), ('c', 'd')]
        
        实时底档吸附抓拍后为，[('a', 'b', 'i'), ('c', 'd'), ('j', 'k'), ('x', 'y')]，新加入了3张抓拍'i', 'x', 'y'，其中'i'进入了历史底档中选出的代理档案('a', 'b')，而('x', 'y')('j', 'k')为新增档案
        
        所以在历史底档吸附'i', 'j', 'k', 'x', 'y'5张图时，只有'i'拥有预设标签，'x', 'y', 'j', 'k'没有预设标签，加如吸附后结果为
        
        [('a', 'b', 'i', 'j', 'k'), ('c', 'd'), ('e', 'f'), ('g', 'h')] 并返回新档案集 [('x', 'y')] 则表示 'j', 'k'被 'i'吸附入历史底档，'x', 'y'位被吸附，进入新的档案集中的档案
        support asynchronous
        """
    @typing.overload
    def adsorbed(self, arg0: pycluster2x.lib.pypic.pic_info, arg1: dict[pycluster2x.lib.pycluster.mdl_e, dict[str, int]]) -> dossier:
        """
        根据另一个表中的rid和label对应情况作为先验对抓拍集进行吸附
        （弃用，被dossier.adsorbed(pb_info, dossier_proxy)代替）
        """
    @typing.overload
    def adsorbed_recommend(self, pb_input: pycluster2x.lib.pypic.pic_info) -> dossier:
        """
        弱标签吸附，与dossier.adsorbed(pb_info)相似，区别在于预设标签为弱标签，可能被算法修改
        support asynchronous
        """
    @typing.overload
    def adsorbed_recommend(self, arg0: pycluster2x.lib.pypic.pic_info, arg1: dossier) -> dossier:
        """
        弱标签吸附，根据另一个档案集中的建档情况作为先验对抓拍集进行吸附，与dossier.adsorbed(pb_info, dossier_proxy)相似，区别在于预设标签为弱标签，可能被算法修改
        support asynchronous
        """
    @typing.overload
    def adsorbed_recommend(self, arg0: pycluster2x.lib.pypic.pic_info, arg1: dict[pycluster2x.lib.pycluster.mdl_e, dict[str, int]]) -> dossier:
        """
        弱标签吸附，根据另一个档案集中的建档情况作为先验对抓拍集进行吸附，与已弃用的dossier.adsorbed(pb_info, r2p_m)相似，区别在于预设标签为弱标签，可能被算法修改
        （弃用，被dossier.adsorbed_recommend(pb_info, dossier_proxy)代替）
        """
    def async_add(self, other_dossier: dossier) -> dossier:
        """
        
        async function of
        add(self: pycluster2x.lib.pydossier.dossier, other_dossier: pycluster2x.lib.pydossier.dossier) -> pycluster2x.lib.pydossier.dossier
            
        """
    def async_add_person_from_pic(self, pb_input: pycluster2x.lib.pypic.pic_info) -> None:
        """
        
        async function of
        add_person_from_pic(self: pycluster2x.lib.pydossier.dossier, pb_input: pycluster2x.lib.pypic.pic_info) -> None
            
        """
    def async_adsorbed(self, *args, **kwargs):
        """
        
        async function of
        adsorbed(self: pycluster2x.lib.pydossier.dossier, pb_input: pycluster2x.lib.pypic.pic_info) -> pycluster2x.lib.pydossier.dossier
        adsorbed(self: pycluster2x.lib.pydossier.dossier, pb_input: pycluster2x.lib.pypic.pic_info, other_dossier: pycluster2x.lib.pydossier.dossier) -> pycluster2x.lib.pydossier.dossier
        adsorbed(self: pycluster2x.lib.pydossier.dossier, arg0: pycluster2x.lib.pypic.pic_info, arg1: dict[pycluster2x.lib.pycluster.mdl_e, dict[str, int]]) -> pycluster2x.lib.pydossier.dossier
            
        """
    def async_adsorbed_recommend(self, *args, **kwargs):
        """
        
        async function of
        adsorbed_recommend(self: pycluster2x.lib.pydossier.dossier, pb_input: pycluster2x.lib.pypic.pic_info) -> pycluster2x.lib.pydossier.dossier
        adsorbed_recommend(self: pycluster2x.lib.pydossier.dossier, arg0: pycluster2x.lib.pypic.pic_info, arg1: pycluster2x.lib.pydossier.dossier) -> pycluster2x.lib.pydossier.dossier
        adsorbed_recommend(self: pycluster2x.lib.pydossier.dossier, arg0: pycluster2x.lib.pypic.pic_info, arg1: dict[pycluster2x.lib.pycluster.mdl_e, dict[str, int]]) -> pycluster2x.lib.pydossier.dossier
            
        """
    def async_batch(self, pb_input: pycluster2x.lib.pypic.pic_info, *, ignore_dossier: bool = False) -> dict[str, dict[pycluster2x.lib.pycluster.mdl_e, list[int]]]:
        """
        
        async function of
        batch(self: pycluster2x.lib.pydossier.dossier, pb_input: pycluster2x.lib.pypic.pic_info, *, ignore_dossier: bool = False) -> dict[str, dict[pycluster2x.lib.pycluster.mdl_e, list[int]]]
            
        """
    def async_check_multi(self, *args, **kwargs):
        """
        
        async function of
        check_multi(self: pycluster2x.lib.pydossier.dossier, oc_res: list[list[pycluster2x.lib.pydossier.oc_updates]], mode: str) -> list[list[pycluster2x.lib.pydossier.cm_update]]
        check_multi(self: pycluster2x.lib.pydossier.dossier, labels: list[list[int]], mode: pycluster2x.lib.pydossier.fuse_e) -> list[list[pycluster2x.lib.pydossier.cm_update]]
            
        """
    def async_copy(self) -> dossier:
        """
        
        async function of
        copy(self: pycluster2x.lib.pydossier.dossier) -> pycluster2x.lib.pydossier.dossier
            
        """
    def async_data2div(self) -> None:
        """
        
        async function of
        data2div(self: pycluster2x.lib.pydossier.dossier) -> None
            
        """
    def async_group(self, arg0: pycluster2x.lib.pypic.pic_info, arg1: dict[pycluster2x.lib.pycluster.mdl_e, list[int]], arg2: list[int]) -> dict[int, list[int]]:
        """
        
        async function of
        group(self: pycluster2x.lib.pydossier.dossier, arg0: pycluster2x.lib.pypic.pic_info, arg1: dict[pycluster2x.lib.pycluster.mdl_e, list[int]], arg2: list[int]) -> dict[int, list[int]]
            
        """
    def async_oc(self, *args, **kwargs):
        """
        
        async function of
        oc(self: pycluster2x.lib.pydossier.dossier, other_dossier: pycluster2x.lib.pydossier.dossier) -> list[list[pycluster2x.lib.pydossier.oc_updates]]
        oc(self: pycluster2x.lib.pydossier.dossier, other_dossier: pycluster2x.lib.pydossier.dossier, vec_mdl: list[pycluster2x.lib.pycluster.mdl_e]) -> list[list[pycluster2x.lib.pydossier.oc_updates]]
            
        """
    def async_oc_separate(self, *args, **kwargs):
        """
        
        async function of
        oc_separate(self: pycluster2x.lib.pydossier.dossier, other_dossier: pycluster2x.lib.pydossier.dossier) -> list[list[pycluster2x.lib.pydossier.oc_updates]]
        oc_separate(self: pycluster2x.lib.pydossier.dossier, other_dossier: pycluster2x.lib.pydossier.dossier, vec_mdl: list[pycluster2x.lib.pycluster.mdl_e]) -> list[list[pycluster2x.lib.pydossier.oc_updates]]
            
        """
    def async_oc_separate_split(self, *args, **kwargs):
        """
        
        async function of
        oc_separate_split(self: pycluster2x.lib.pydossier.dossier, other_dossier: pycluster2x.lib.pydossier.dossier, size: int) -> list[list[pycluster2x.lib.pydossier.oc_updates]]
        oc_separate_split(self: pycluster2x.lib.pydossier.dossier, other_dossier: pycluster2x.lib.pydossier.dossier, size: int, device: list[str]) -> list[list[pycluster2x.lib.pydossier.oc_updates]]
        oc_separate_split(self: pycluster2x.lib.pydossier.dossier, other_dossier: pycluster2x.lib.pydossier.dossier, size: int, device: list[str], vec_mdl: list[pycluster2x.lib.pycluster.mdl_e]) -> list[list[pycluster2x.lib.pydossier.oc_updates]]
            
        """
    def async_precise_adsorbed(self, oc_res: list[list[oc_updates]], batch: int = 5000) -> None:
        """
        
        async function of
        precise_adsorbed(self: pycluster2x.lib.pydossier.dossier, oc_res: list[list[pycluster2x.lib.pydossier.oc_updates]], batch: int = 5000) -> None
            
        """
    def async_proxy_fuse(self, proxy: dossier) -> dict[pycluster2x.lib.pycluster.mdl_e, dict[str, int]]:
        """
        
        async function of
        proxy_fuse(self: pycluster2x.lib.pydossier.dossier, proxy: pycluster2x.lib.pydossier.dossier) -> dict[pycluster2x.lib.pycluster.mdl_e, dict[str, int]]
            
        """
    def async_recreate(self, *args, **kwargs):
        """
        
        async function of
        recreate(self: pycluster2x.lib.pydossier.dossier) -> pycluster2x.lib.pydossier.dossier
        recreate(self: pycluster2x.lib.pydossier.dossier, lower_bound: int, upper_bound: int) -> pycluster2x.lib.pydossier.dossier
            
        """
    def async_recreate_coarse(self, *args, **kwargs):
        """
        
        async function of
        recreate_coarse(self: pycluster2x.lib.pydossier.dossier) -> pycluster2x.lib.pydossier.dossier
        recreate_coarse(self: pycluster2x.lib.pydossier.dossier, lower_bound: int, upper_bound: int) -> pycluster2x.lib.pydossier.dossier
            
        """
    def async_reduce_person_dossier(self) -> None:
        """
        
        async function of
        reduce_person_dossier(self: pycluster2x.lib.pydossier.dossier) -> None
            
        """
    def async_reg_gallery(self, arg0: pycluster2x.lib.pypic.pic_info, arg1: int) -> None:
        """
        
        async function of
        reg_gallery(self: pycluster2x.lib.pydossier.dossier, arg0: pycluster2x.lib.pypic.pic_info, arg1: int) -> None
            
        """
    def async_release_div(self) -> None:
        """
        
        async function of
        release_div(self: pycluster2x.lib.pydossier.dossier) -> None
            
        """
    def async_remove_single(self, *args, **kwargs):
        """
        
        async function of
        remove_single(self: pycluster2x.lib.pydossier.dossier) -> None
        remove_single(self: pycluster2x.lib.pydossier.dossier, arg0: pycluster2x.lib.pycluster.mdl_e) -> None
            
        """
    def async_save(self, path: str) -> None:
        """
        
        async function of
        save(self: pycluster2x.lib.pydossier.dossier, path: str) -> None
            
        """
    def async_save_big(self, path: str) -> None:
        """
        
        async function of
        save_big(self: pycluster2x.lib.pydossier.dossier, path: str) -> None
            
        """
    def async_save_small(self, path: str) -> None:
        """
        
        async function of
        save_small(self: pycluster2x.lib.pydossier.dossier, path: str) -> None
            
        """
    def async_search(self, *args, **kwargs):
        """
        
        async function of
        search(self: pycluster2x.lib.pydossier.dossier, pb_input: pycluster2x.lib.pypic.pic_info, threshold: float = 0.9, top: int = 3) -> dict[pycluster2x.lib.pycluster.mdl_e, list[list[pycluster2x.lib.pydossier.oc_updates]]]
        search(self: pycluster2x.lib.pydossier.dossier, dos: pycluster2x.lib.pydossier.dossier, threshold: float = 0.9, top: int = 3) -> dict[pycluster2x.lib.pycluster.mdl_e, list[list[pycluster2x.lib.pydossier.oc_updates]]]
            
        """
    def async_ser(self) -> bytes:
        """
        
        async function of
        ser(self: pycluster2x.lib.pydossier.dossier) -> bytes
            
        """
    def async_simple_batch(self, *args, **kwargs):
        """
        
        async function of
        simple_batch(self: pycluster2x.lib.pydossier.dossier, pb_info: pycluster2x.lib.pypic.pic_info) -> None
        simple_batch(self: pycluster2x.lib.pydossier.dossier, pb_info: pycluster2x.lib.pypic.pic_info, labels: dict[pycluster2x.lib.pycluster.mdl_e, list[int]], dossier_labels: dict[pycluster2x.lib.pycluster.mdl_e, list[int]]) -> None
            
        """
    def async_split(self, size: int) -> list[dossier]:
        """
        
        async function of
        split(self: pycluster2x.lib.pydossier.dossier, size: int) -> list[pycluster2x.lib.pydossier.dossier]
            
        """
    def async_tidy_up(self) -> None:
        """
        
        async function of
        tidy_up(self: pycluster2x.lib.pydossier.dossier) -> None
            
        """
    def batch(self, pb_input: pycluster2x.lib.pypic.pic_info, *, ignore_dossier: bool = False) -> dict[str, dict[pycluster2x.lib.pycluster.mdl_e, list[int]]]:
        """
        batch聚档接口，将抓拍集中的所有抓拍进行聚类，相似的同一个人的抓拍聚成一个档案。最终得到由抓拍集中抓拍聚档的到的很多档案组成的档案集。
        接口输入为抓拍集pypic.pic_info
        例如：
        ``` python
        
        pb_info:pypic.pic_info = pypic.pb_input_csv('./data0.csv')
        dossier = pydossier.dossier(pycluster.cluster_hdl([pycluster.FACE, pycluster.BODY], pycluster.default_cfg()))
        dossier.batch(pb_info)          # 将抓拍集进行聚档，更新dossier档案集
        print(dossier)
        dossier.save_small('./result/')
        ```
        support asynchronous
        """
    @typing.overload
    def check_multi(self, oc_res: list[list[oc_updates]], mode: str) -> list[list[cm_update]]:
        """
        离线合档接口，离线合档推荐存在于oc结果中，传入oc档案和oc结果，通过字符串设置模式，模式间通过 | 连接
        | 关键字 | 含义 |
        |:---:|:---:|
        | ex_fuse_oc  |        额外合档模式，用于合并人脸推荐的，底档中的额外合档档案，实现底档中的两个不同人的合并                  |
        | assisted_oc |     辅助合档模式，当oc接口通过质心无法确定是否合并时使用，进一步通过子档抓拍进行判断是否进行合并，当前仅用于人体       |
        | self_check  | 当合档接口进行推荐时，会将底档中相似的两个档案标记为相似，离线合档接口通过子档抓拍判断底档中的这两个档案是否需要合并    |
        
        模式填写如："ex_fuse_oc|assisted_oc|self_check"
        例如：
        ``` python
        
        oc_res = dossier_0.oc_separate_split(dossier_1, 80000, ["0", "1"], [pycluster.FACE])
        cm_res = dossier_0.check_multi(oc_res, "ex_fuse_oc|assisted_oc")
        ```
        其中oc_res为合档接口输出结果，cm_res是一个列表，长度和oc_res相同，其中每个元素与oc_res中对应位置的结果一一对应，表示根据oc_res中每个元素的结果进行离线合档的结果。
        离线合档会选择oc合档结果中"fuse_recommend"为JUDGE或者ADSORBED的元素中，label字段对应的人与当前人进行离线合档
        假如一个人的oc结果为:
        ```
        [{"label":222866, "dossier_label":147429, "score":0.8960656, "fuse_recommend":JUDGE, "update":0, "type":FACE}, 
        {"label":267694, "dossier_label":0, "score":100, "fuse_recommend":DST, "update":0, "type":OTHERS}]
        ```
        则它会将这个人（由oc结果中"fuse_recommend"为DST可以看出，这个人在底档中pid为267694）与底档中label值即pid为222866的人进行离线合档，离线合档结果为：
        ```
        [{"src_person":267694, "check_multi_label":0, "score":1, "opt":self_check}, 
        {"src_person":222866, "check_multi_label":0, "score":0.99043024, "opt":self_check}]
        ```
        这是一个列表，列表元素数量为2，每个元素为一个cm_update结构体。
        第一个元素是这个人与自身计算的结果，没有实际作用。
        第一个之后的元素，假如有n个，表示有n个人与这个人做离线合档，每个人的离线合档结果为1个结构体
        support asynchronous
        """
    @typing.overload
    def check_multi(self, labels: list[list[int]], mode: fuse_e) -> list[list[cm_update]]:
        """
        离线合档接口，允许直接触发底档中档案的合并或离线合档
        labels为一个list，数组中每各元素是一个list[int]，即label组，将这组label执行mode操作的
        例如：
        ``` python
        
        cm_res = dossier.check_multi([[0,1,2], [4,5,6]], pydossier.fuse_e.MERGE) # 将档案集中的0,1,2号人作为一组合并，将4,5,6号人作为一组合并
        ```
        输出结果cm_res是一个列表，列表长度和输入labels相同，即2，表示输入labels中每个元素的离线合档对应结果
        假如cm_res第一个元素为：
        ```
        [{"src_person":0, "check_multi_label":0, "score":1, "opt":self_check}, 
        {"src_person":1, "check_multi_label":0, "score":0.990430, "opt":self_check},
        {"src_person":2, "check_multi_label":0, "score":0.985648, "opt":self_check}]
        ```
        这是一个列表，列表元素数量为3，与输入labels中第一个元素的长度一致。
        第一个元素是这个人（pid为0）与自身计算的结果，没有实际作用。
        第一个之后的元素有两个，表示labels第一个元素中指示的pid为1和pid为2这两个人与pid为0这个人做离线合档，每个人的离线合档结果为1个结构体
        support asynchronous
        """
    def check_person_dos(self) -> None:
        ...
    def check_record(self) -> None:
        """
        检查数据探针长度是否与抓拍数量对齐
        例如：
        ``` python
        
        dossier.check_record()
        ```
        """
    def check_rid_matching(self) -> None:
        """
        检查档案集中的关联人脸人体抓拍有没有被错误断开
        例如：
        ``` python
        
        dossier.check_rid_matching()
        ```
        """
    def cluster_num(self) -> dict[pycluster2x.lib.pycluster.mdl_e, int]:
        """
        获取档案集中管理的模态档案数
        例如：
        ``` python
        
        print(dossier.cluster_num())
        ```
        """
    def copy(self) -> dossier:
        """
        把档案集复制一份
        support asynchronous
        """
    def create_empty(self) -> dossier:
        """
        通过当前档案集的各种配置，生成一个空档案集
        例如：
        ``` python
        
        dossier = pydossier.load_small("./result/all")          # 读取已有档案集结果
        dossier_proxy = dossier.create_empty()        # 根据dossier的各种配置创建一个空档案集 
        for i in range(dossier.person_num()):                    # 遍历所有人
            rids:'dict[pycluster.mdl_e, str]' = dossier.get_rid_from_pid(i)      # 获取人id为i的人的所有rids
            if len(sum(rids.values(), []))>4:                   
                dossier_proxy.emplace_from_other(dossier, i)             # 将子档数量大于4的人推入dossier_proxy档案集
        
        print(dossier_proxy)
        ```
        """
    def data2div(self) -> None:
        """
        将一个档案集的质心数据搬运至显卡设备, 合档接口自带，可以不调用
        例如：
        ``` python
        
        dossier_0.data2div()
        dossier_1.data2div()
        print(dossier_0)
        res = dossier_0.oc_separate_split(dossier_1, 80000, ["0", "1"], [pycluster.FACE])
        print(res, dossier_0)
        dossier_0.release_div()
        dossier_1.release_div()
        ```
        support asynchronous
        """
    def emplace_from_other(self, other_dossier: dossier, other_pid: int) -> None:
        """
        将另一个档案集中的一个人的档案加入当前档案集
        例如：
        ``` python
        
        dossier_proxy:pydossier.dossier = dossier.create_empty()          # 根据dossier的各种配置创建一个空档案集 
        for i in range(dossier.person_num()):                    # 遍历所有人
            rids:'dict[pycluster.mdl_e, str]' = dossier.get_rid_from_pid(i)      # 获取人id为i的人的所有rids
            if len(sum(rids.values(), []))>4:                   
                dossier_proxy.emplace_from_other(dossier, i)             # 将子档数量大于4的人推入dossier_proxy档案集
        ```
        """
    def get_alg(self) -> pycluster2x.lib.pycluster.cluster_hdl:
        """
        获取档案集中的算法句柄
        例如：
        ``` python
        
        dossier = pydossier.dossier(pycluster.cluster_hdl([pycluster.FACE, pycluster.BODY], pycluster.default_cfg()))
        alg_hdl:pycluster.cluster_hdl = dossier.get_alg()
        ```
        """
    def get_centriod_num(self) -> dict[pycluster2x.lib.pycluster.mdl_e, int]:
        """
        获得档案集中各个模态的质心类型数量
        例如：
        ``` python
        
        print(dossier.get_centriod_num()) # 获取质心数 打印如 {"pycluster.FACE":4,"pycluster.BODY":1}
        ```
        """
    def get_feature(self) -> dict[pycluster2x.lib.pycluster.mdl_e, list[numpy.ndarray[numpy.float32]]]:
        """
        得到档案集的质心特征的拷贝
        检索方式：
        [模态][第n个质心]: 即某模态的第n类质心的所有档案特征组成的矩阵，是一个shape为[cluster_num,dim]且保存值类型为float的numpy.array
        [模态][第n个质心][第m个档案]: 即某模态的第n类质心的第m个档案的质心特征向量，是一个shape为[dim]且保存值类型为float的numpy.array
        [模态][第n个质心][第m个档案][d]: 即某模态的第n类质心的第m个档案的质心特征向量的第d个值，是一个float
        返回特征内存额外申请，不与档案集共享内存
        例如：
        ``` python
        
        ftr = dossier.get_feature() 
        # dict[pycluster2x.lib.pycluster.mdl_e, list[numpy.ndarray[numpy.float32]]]
        #     [模态][第n个质心][第m个档案][dim维中的第k个数字]
        arr = ftr[pycluster.FACE][0][0]
        print(arr) #取这个档案集的所有特征
        ```
        """
    def get_feature_as_view(self) -> dossier.feature_viewer:
        """
        获取质心特征的引用，和档案集dossier共享同一块内存，对特征的修改会同步到dossier档案集中
        索引方式和 get_feature() 相同
        通过入口函数保证对象的生命周期内特征有效
        例如：
        ``` python
        
        with dossier.get_feature_as_view() as ftr:
            # dict[pycluster2x.lib.pycluster.mdl_e, list[numpy.ndarray[numpy.float32]]]
            #     [模态][第n个质心][第m个档案][dim维中的第k个数字]
            ftr[pycluster.FACE][0][0][0] = 0.2
        ```
        """
    def get_mid_from_pid(self, mdl: pycluster2x.lib.pycluster.mdl_e, pid: int) -> list[int]:
        """
        根据 pid 查询 mid
        例如：
        ``` python
        
        print(dossier.get_mid_from_pid(pycluster.FACE, 0))
        ```
        """
    def get_mid_from_rid(self, mdl: pycluster2x.lib.pycluster.mdl_e, rid: str) -> int:
        """
        根据特定的模态和rid获取这个人在该档案中这个模态的mid
        例如：
        ``` python
        
        print(dossier.get_mid_from_rid(pycluster.FACE, "JmC2uvB1CK8O5IIUGNAL0220210828024243438990614641"))
        ```
        """
    def get_person_from_pid(self, pid: int) -> dossier:
        """
        生成一个仅由该档案中输入pid的这个人生成的档案集
        例如：
        ``` python
        
        dossier_0 = dossier.get_person_from_pid(0)    # 生成一个仅由该档案中pid为0的人的档案集
        ```
        """
    def get_person_from_rid(self, rid: str) -> dossier:
        """
        生成一个仅由该档案中，包含输入rid的人生成的档案集
        例如：
        ``` python
        
        dossier_0 = dossier.get_person_from_rid("341523210011902306500220210821161147470860603412")    # 生成一个仅由该档案中pid为0的人的档案集
        ```
        """
    def get_person_info(self, this_pid: int) -> pycluster2x.lib.pypic.pic_info:
        """
        从档案集中，根据档案集中记录的子档信息，按pid获取一个人的抓拍集信息，依赖本地数据缓存
        如果pid不存在会抛异常
        例如：
        ``` python

        print(dossier.get_person_info(0))              # 获取0号人的所有抓拍集            
        ```
        """
    def get_person_info_include_scrap(self, this_pid: int) -> pycluster2x.lib.pypic.pic_info:
        """
        从档案集中，根据档案集中记录的子档信息，按pid获取一个人的抓拍集信息，依赖本地数据缓存
        通过该接口获得的抓拍会包含废片
        如果pid不存在会抛异常
        例如：
        ``` python

        print(dossier.get_person_info_include_scrap(0))              # 获取0号人的所有抓拍集            
        ```
        """
    def get_pid_from_mid(self, mdl: pycluster2x.lib.pycluster.mdl_e, mid: int) -> int:
        """
        根据特定的模态和mid获取这个人在该档案中的pid
        例如：
        ``` python
        
        print(dossier.get_pid_from_mid(pycluster.FACE, 0))
        ```
        """
    def get_pid_from_rid(self, rid: str) -> int:
        """
        根据一个rid，获取该抓拍所在的pid号
        例如：
        ``` python
        
        dossier_0 = dossier.create_empty()
        rids = ["341523210011902306500220210821161147470860603412"]
        pids = [dossier.get_pid_from_rid(rid) for rid in rids]
        for i in pids:
            dossier_0.emplace_from_other(dossier, i)
        ```
        """
    def get_pid_from_uuid(self, uuid: str) -> int:
        """
        根据uuid，获取pid
        例如：
        ``` python
        
        print(dossier.get_pid_from_uuid("tnz0qj9e"))        # 获取uuid为tnz0qj9e的人的pid
        ```
        """
    def get_r2p_map(self) -> dict[pycluster2x.lib.pycluster.mdl_e, dict[str, int]]:
        """
        得到所有rid和其对应的pid的映射表
        例如：
        ``` python
        
        print(dossier.get_rid2pid())
        ```
        """
    def get_rid2mid(self) -> dict[pycluster2x.lib.pycluster.mdl_e, dict[str, int]]:
        """
        得到所有rid和其对应的pid的映射表
        例如：
        ``` python
        
        print(dossier.get_rid2mid())
        ```
        """
    def get_rid2pid(self) -> dict[pycluster2x.lib.pycluster.mdl_e, dict[str, int]]:
        """
        得到所有rid和其对应的pid的映射表
        例如：
        ``` python
        
        print(dossier.get_rid2pid())
        ```
        """
    def get_rid_from_mid(self, mdl: pycluster2x.lib.pycluster.mdl_e, mid: int) -> list[str]:
        """
        根据pid，获取该人在档案集中所有的抓拍rid
        例如：
        ``` python
        
        print(dossier.get_rid_from_mid(pycluster.FACE, 0))      # 打印0号人脸档案所管理的这个人的所有rid
        ```
        """
    def get_rid_from_pid(self, this_pid: int) -> dict[pycluster2x.lib.pycluster.mdl_e, list[str]]:
        """
        根据pid，获取该人在档案集中所有的抓拍rid
        例如：
        ``` python
        
        print(dossier.get_rid_from_pid(0))        # 获取档案集为0的人的所有rid
        ```
        """
    def get_subnum_from_pid(self, this_pid: int) -> dict[pycluster2x.lib.pycluster.mdl_e, int]:
        """
        根据pid，获取该人在档案集中的子档数量
        例如：
        ``` python
        
        print(dossier.get_subnum_from_pid(0))        # 获取档案集为0的人的子档数量
        ```
        """
    def get_uuid_from_pid(self, this_pid: int) -> str:
        """
        根据pid，获取该人的最新uuid
        例如：
        ``` python
        
        print(dossier.get_uuid_from_pid(0))        # 获取pid为0的人的最新uuid
        ```
        """
    def get_uuids_from_pid(self, this_pid: int) -> set[str]:
        """
        根据pid，获取该人的所有uuids
        例如：
        ``` python
        
        print(dossier.get_uuids_from_pid(0))        # 获取pid为0的人的所有uuid
        ```
        """
    def group(self, arg0: pycluster2x.lib.pypic.pic_info, arg1: dict[pycluster2x.lib.pycluster.mdl_e, list[int]], arg2: list[int]) -> dict[int, list[int]]:
        """
        分类接口（group），输入为抓拍集、对应的档案集和分类类别
        support asynchronous
        """
    @typing.overload
    def is_feature_effective(self) -> dict[pycluster2x.lib.pycluster.mdl_e, list[list[int]]]:
        """
        返回特征有效性矩阵
        索引方式：
        [模态][第n个质心][第m个档案]: 即某模态的第n类质心的第m个档案的质心是否有效，有效为非0，无效为0
        例如：
        ``` python
        
        print(dossier.is_feature_effective()) #取这个档案集的所有特征
        ```
        """
    @typing.overload
    def is_feature_effective(self, e: pycluster2x.lib.pycluster.mdl_e, centriod: int, mid: int) -> int:
        """
        检查某个模态某类质心的某个档案特征是否有效
        centriod表示质心类别，mid表示档案id
        例如：
        ``` python
        
        print(dossier.is_feature_effective(pycluster.FACE, 1, 1)) #取人脸的第一个质心的第一个特征
        ```
        """
    def is_person_exists(self, this_pid: int) -> bool:
        """
        判断某个人id在该档案集中是否存在（任意模态有数据，如果这个人所有模态都没有数据则判定为不存在）
        例如：
        ``` python
        
        print(dossier.is_person_exists(0))             # 判断人0是否至少有一个模态档案是有效的          
        ```
        """
    @typing.overload
    def is_person_single(self, this_pid: int) -> bool:
        """
        判断一个pid人是不是单模态人
        例如：
        ``` python
        
        print(dossier.is_person_single(0))              # 判断0号人是否只存在单模态档案          
        ```
        """
    @typing.overload
    def is_person_single(self, mdl: pycluster2x.lib.pycluster.mdl_e, this_pid: int) -> bool:
        """
        判断一个pid人是某一特定的单模态人
        例如：
        ``` python
        
        print(dossier.is_person_single(pycluster.FACE, 0))     # 判断0号人是不是只有人脸模态             
        ```
        """
    @typing.overload
    def oc(self, other_dossier: dossier) -> list[list[oc_updates]]:
        """
        合档接口，通过相似度计算等算法，将另一个档案集中，算法判断与当前档案集中管理的某个人相同的人的档案进行合并，
        无法与当前档案集中人匹配的人添加到当前档案集中，并输出另一个档案集中所有人在当前档案集中计算的比对结果。
        接口结果是一个数组，另一个档案集中管理的每个人输出一个结果，
        每个人的结果是一个数组，表示这个人在另一个档案集中匹配的topN，包含分数等信息
        例如：
        ``` python
        
        res:'list[list[pydossier.oc_updates]]' = dossier0.oc(dossier1)        
        ```
        其中dossier0为底档，结果res是一个列表，其中每个元素每个表示输入档案dossier1中每个人的合档结果。
        进一步的，假如dossier1中一个人的合档结果为：
        ```
        [{"label":19873, "dossier_label":19873, "score":0.99611187, "fuse_recommend":MERGE, "update":1, "type":FACE}, 
        {"label":59820, "dossier_label":59820, "score":0.9077666, "fuse_recommend":JUDGE, "update":0, "type":FACE}, 
        {"label":19873, "dossier_label":19873, "score":0.99611187, "fuse_recommend":DST, "update":1, "type":FACE}]
        ```
        这是一个列表，列表元素数量为3，每个元素为一个oc_updates结构体。前两个"fuse_recommend"不为DST的，表示这个人的两个oc输出结果。
        最后一个"fuse_recommend"为DST的，表示根据这个oc输出结果，最终采纳oc输出结果中{"label":19873,"dossier_label":19873,"score":0.99611187,"update":1,"type":FACE}这条结果，将这个人合入底档中"label"为19873，即pid为19873的人的档案中
        support asynchronous
        """
    @typing.overload
    def oc(self, other_dossier: dossier, vec_mdl: list[pycluster2x.lib.pycluster.mdl_e]) -> list[list[oc_updates]]:
        """
        合档接口，功能和输出结果结构与 pydossier.dossier.oc(other_dossier:pydossier.dossier) 接口相似，区别在于只比对指定的模态
        例如：
        ``` python
        
        res:'list[list[pydossier.oc_updates]]' = dossier_0.oc(dossier_1, [pycluster.FACE])
        ```
        support asynchronous
        """
    @typing.overload
    def oc_separate(self, other_dossier: dossier) -> list[list[oc_updates]]:
        """
        合档接口，功能和输出结果结构与 pydossier.dossier.oc(other_dossier:pydossier.dossier) 接口相同，比对算法使用分模态的算法
        例如：
        ``` python
        
        res:'list[list[pydossier.oc_updates]]' = dossier_0.oc_separate(dossier_1)
        ```
        support asynchronous
        """
    @typing.overload
    def oc_separate(self, other_dossier: dossier, vec_mdl: list[pycluster2x.lib.pycluster.mdl_e]) -> list[list[oc_updates]]:
        """
        合档接口，功能和输出结果结构与 pydossier.dossier.oc_separate(other_dossier:pydossier.dossier) 接口相似，区别在于只比对指定的模态
        例如：
        ``` python
        
        res:'list[list[pydossier.oc_updates]]' = dossier_0.oc_separate(dossier_1, [pycluster.FACE])
        ```
        support asynchronous
        """
    @typing.overload
    def oc_separate_split(self, other_dossier: dossier, size: int) -> list[list[oc_updates]]:
        """
        合档接口，功能和输出结果结构与 pydossier.dossier.oc(other_dossier:pydossier.dossier) 接口相似，使用分布式算法，
        通过size设置分布式任务规模，常见size为2400000。
        例如：
        ``` python
        
        res = dossier_0.oc_separate_split(dossier_1, 2400000)
        ```
        support asynchronous
        """
    @typing.overload
    def oc_separate_split(self, other_dossier: dossier, size: int, device: list[str]) -> list[list[oc_updates]]:
        """
        合档接口，功能和输出结果结构与 pydossier.dossier.oc_separate_split(other_dossier:pydossier.dossier, size:int) 接口相似，使用分布式算法，
        通过size设置分布式任务规模，常见size为2400000，通过device参数设置可用的设备id。
        例如：
        ``` python
        
        res = dossier_0.oc_separate_split(dossier_1, 80000, ["0", "1"])
        ```
        support asynchronous
        """
    @typing.overload
    def oc_separate_split(self, other_dossier: dossier, size: int, device: list[str], vec_mdl: list[pycluster2x.lib.pycluster.mdl_e]) -> list[list[oc_updates]]:
        """
        合档接口，功能和输出结果结构与 pydossier.dossier.oc_separate_split(other_dossier:pydossier.dossier, size:int) 接口相似，使用分布式算法，
        通过size设置分布式任务规模，常见size为2400000，通过device参数设置可用的设备id，通过vec_mdl指定需要比对的模态。
        例如：
        ``` python
        
        res = dossier_0.oc_separate_split(dossier_1, 80000, ["0", "1"], [pycluster.FACE])
        ```
        support asynchronous
        """
    def person_mdl(self, this_pid: int) -> list[pycluster2x.lib.pycluster.mdl_e]:
        """
        获取一个pid人的所有有效模态
        例如：
        ``` python
        
        print(dossier.person_mdl(0))         # 获取0号人的所有有效模态，例如如果人脸档案不存在，人体档案存在，则这里会返回[pycluster.BODY]
        ```
        """
    def person_num(self) -> int:
        """
        获取档案集中管理的人数
        例如：
        ``` python
        
        print(dossier.person_num())
        ```
        """
    def precise_adsorbed(self, oc_res: list[list[oc_updates]], batch: int = 5000) -> None:
        """
        离线合档接口，离线合档推荐存在于oc结果中，传入oc档案和oc结果
        需要在oc后做，不能在离线合档或其他会改变底档的接口后做
        support asynchronous
        """
    def proxy_fuse(self, proxy: dossier) -> dict[pycluster2x.lib.pycluster.mdl_e, dict[str, int]]:
        """
        输入另一个档案集，根据获取另一个档案集和本档案集的交集人，所吸附的额外抓拍产生的字典
        例如：
        ``` python
        
        def dos_adsorbed_impl(pb:pypic.pic_info, proxy:pydossier.dossier, dossier:pydossier.dossier):
            proxy_res = dossier.proxy_fuse(proxy)
            dossier_tmp = dossier.adsorbed(pb, proxy_res)
            return dossier_tmp
        ```
        support asynchronous
        """
    @typing.overload
    def recreate(self) -> dossier:
        """
        整理档案集，重新生成档案集中管理的每个人的质心，档案抓拍中不包含废片
        例如：
        ``` python
        
        dossier = dossier.recreate()
        ```
        support asynchronous
        """
    @typing.overload
    def recreate(self, lower_bound: int, upper_bound: int) -> dossier:
        """
        整理档案集，重新生成档案集中管理的pid的[lower_bound,upper_bound)的人的质心
        例如：
        ``` python
        
        dossier = dossier.recreate(1, 10)
        ```
        support asynchronous
        """
    @typing.overload
    def recreate_coarse(self) -> dossier:
        """
        整理档案集，重新生成档案集中管理的每个人的质心，档案抓拍中包含废片
        例如：
        ``` python
        
        dossier = dossier.recreate()
        ```
        support asynchronous
        """
    @typing.overload
    def recreate_coarse(self, lower_bound: int, upper_bound: int) -> dossier:
        """
        整理档案集，重新生成档案集中管理的pid的[lower_bound,upper_bound)的人的质心，档案抓拍中包含废片
        例如：
        ``` python
        
        dossier = dossier.recreate(1, 10)
        ```
        support asynchronous
        """
    def reduce_person_dossier(self) -> None:
        """
        整理档案集，缩减其中档案数过多的人的档案
        例如：
        ``` python
        
        dossier.dossier_reduce()
        ```
        support asynchronous
        """
    def reg_database(self, database_obj: typing.Any) -> None:
        """
        注册外部数据缓存, database_obj 参数需要继承于 pycache.abstract_database
        注册的database_obj的方法会多线程调用，需要保证线程安全
        """
    def reg_gallery(self, arg0: pycluster2x.lib.pypic.pic_info, arg1: int) -> None:
        """
        注册底库接口，输入为底库抓拍集和分类类别
        support asynchronous
        """
    def release_div(self) -> None:
        """
        释放质心显卡数据，参见data2div
        support asynchronous
        """
    def remove_person(self, this_pid: int) -> None:
        """
        删除档案集中人id为入参的人的档案
        例如：
        ``` python
        
        dossier.remove_person(0) # 将dos中的0号人删除
        ```
        """
    @typing.overload
    def remove_single(self) -> None:
        """
        删除档案集中的单模态档案，包含所有模态
        例如：
        ``` python
        
        dossier.remove_single()                    # 删除所有仅有单模态的档案
        ```
        support asynchronous
        """
    @typing.overload
    def remove_single(self, arg0: pycluster2x.lib.pycluster.mdl_e) -> None:
        """
        删除档案集中的某个模态的单模态档案，模态枚举由输入确定
        例如：
        ``` python
        
        dossier.remove_single(pycluster.BODY)               # 删除所有纯人体档案
        ```
        support asynchronous
        """
    def replace_from_other(self, this_pid: int, other_dossier: dossier, other_pid: int) -> None:
        """
        将另一个档案集中的一个人的档案和当前档案集的一个档案进行交换
        例如：
        ``` python
        
        dossier.replace_from_other(0, dossier1, 0)      # 将两个档案集中的人id为0的人相互交换
        ```
        """
    def rid_unique_num(self) -> dict[pycluster2x.lib.pycluster.mdl_e, int]:
        """
        得到所有不重复的rid数量
        例如：
        ``` python
        
        print(dossier.rid_unique_num())
        ```
        """
    def save(self, path: str) -> None:
        """
        保存档案集
        例如：
        ``` python
        
        dossier = pydossier.load("./result/0/")
        dossier.save("./record/")
        ```
        support asynchronous
        """
    def save_big(self, path: str) -> None:
        """
        用最大（易于阅读）的方式，保存档案集
        例如：
        ``` python
        
        dossier = pydossier.load_big("./result/0/")
        dossier.save_big("./record/")
        ```
        support asynchronous
        """
    def save_small(self, path: str) -> None:
        """
        用最小最快的方式，保存档案集，最常用
        例如：
        ``` python
        
        dossier = pydossier.load_small("./result/0/")
        dossier.save_small("./record/")
        ```
        support asynchronous
        """
    @typing.overload
    def search(self, pb_input: pycluster2x.lib.pypic.pic_info, threshold: float = 0.9, top: int = 3) -> dict[pycluster2x.lib.pycluster.mdl_e, list[list[oc_updates]]]:
        """
        根据输入的抓拍集，根据抓拍集中的抓拍在底档中搜索每张抓拍对应的人
        例如：
        ``` python
        
        db = pycache.cluster_data_cache("/data/291223/data/data_cache_ah/")      # 初始化数据缓存
        it:pycache.db_it = db.get_time_it(0)               # 根据时间流，从时间流最开始，获取时间流最初的数据迭代器
        pb_info:pypic.pic_info = it.get(256)             # 从迭代器获取256张图，组成抓拍集，迭代器往后移动256张
        
        dossier_tmp = pydossier.dossier(pycluster.cluster_hdl([pycluster.FACE, pycluster.BODY], pycluster.default_cfg()))        # 构造一个空档案集
        res = dossier_tmp.search(pb_info)
        print(res)
        ```
        support asynchronous
        """
    @typing.overload
    def search(self, dos: dossier, threshold: float = 0.9, top: int = 3) -> dict[pycluster2x.lib.pycluster.mdl_e, list[list[oc_updates]]]:
        """
        根据输入的抓拍集，根据抓拍集中的抓拍在底档中搜索每张抓拍对应的人
        例如：
        ``` python
        
        db = pycache.cluster_data_cache("/data/291223/data/data_cache_ah/")      # 初始化数据缓存
        it:pycache.db_it = db.get_time_it(0)               # 根据时间流，从时间流最开始，获取时间流最初的数据迭代器
        pb_info:pypic.pic_info = it.get(256)             # 从迭代器获取256张图，组成抓拍集，迭代器往后移动256张
        dos.simple_batch(pb_info)
        
        dossier_tmp = pydossier.dossier(pycluster.cluster_hdl([pycluster.FACE, pycluster.BODY], pycluster.default_cfg()))        # 构造一个空档案集
        res = dossier_tmp.search(dos)
        print(res)
        ```
        support asynchronous
        """
    def ser(self) -> bytes:
        """
        序列化
        例如：
        ``` python
        
        dos_ser = dossier.ser()
        dossier_tmp = pydossier.unser(dos_ser)
        print(dossier, dossier_tmp)  # dossier 和 dossier_tmp 相同
        ```
        support asynchronous
        """
    @typing.overload
    def set_cfg(self, key: str, value: str) -> None:
        """
        设置一个cfg键值对
        例如：
        ``` python
        
        dossier.set("device_id", "1")               # 设置dossier的"device_id"为"1"          
        ```
        """
    @typing.overload
    def set_cfg(self, cfg: dict[str, str]) -> None:
        """
        通过字典设置多个cfg键值对
        例如：
        ``` python
        
        cfg:'dict[str, str]' = {
                "feature" : "fp16",
                "face_feat_threshold" : "0.92"
            }
        
        dossier.set(cfg)                # 设置dossier里面的配置 
        ```
        """
    def set_dim(self, mdl: pycluster2x.lib.pycluster.mdl_e, dim: int) -> None:
        """
        将档案集中人体模态隐藏
        例如：
        ``` python
        
        dossier.set_dim(pycluster.FACE, 1)
        ```
        """
    def shadow(self) -> None:
        """
        将档案集中人体模态隐藏
        例如：
        ``` python
        
        dossier.shadow()    # 隐藏人体模态
        dossier.shadow_restore()  # 恢复人体模态
        ```
        """
    def shadow_restore(self) -> None:
        """
        恢复档案集中人体模态隐藏的档案，参见shadow()
        """
    @typing.overload
    def simple_batch(self, pb_info: pycluster2x.lib.pypic.pic_info) -> None:
        """
        根据输入的抓拍集，每张抓拍作为一个人，分别构建成一个档案，组成档案集
        例如：
        ``` python
        
        db = pycache.cluster_data_cache("/data/291223/data/data_cache_ah/")      # 初始化数据缓存
        it:pycache.db_it = db.get_time_it(0)               # 根据时间流，从时间流最开始，获取时间流最初的数据迭代器
        pb_info:pypic.pic_info = it.get(256)                # 从迭代器获取256张图，组成抓拍集，迭代器往后移动256张
        
        dossier_tmp = pydossier.dossier(pycluster.cluster_hdl([pycluster.FACE, pycluster.BODY], pycluster.default_cfg()))        # 构造一个空档案集
        dossier_tmp.simple_batch(pb_info)
        ```
        support asynchronous
        """
    @typing.overload
    def simple_batch(self, pb_info: pycluster2x.lib.pypic.pic_info, labels: dict[pycluster2x.lib.pycluster.mdl_e, list[int]], dossier_labels: dict[pycluster2x.lib.pycluster.mdl_e, list[int]]) -> None:
        """
        根据输入的抓拍集和已知的标签，构建档案
        当已知输入抓拍集中每张抓拍和这些抓拍所对应的pid和mid时，可以通过入参labels和dossier_labels对batch的pid和mid进行预设
        接口不会经历聚档的过程而直接根据预设生成档案集。
        例如:
        ```python
        
        # 已知rid0，rid1，rid2，rid3是同一个人的一个档案，rid4是这个人的另一个档案，rid5又是这个人的另一个档案，rid6，rid7是另一个人的一个档案，则可通过
        pb_info:pypic.pic_info = pypic.pb_input_csv("./data.csv") # 抓拍集为rid0，rid1，rid2，rid3，rid4，rid5，rid6，rid7组成的抓拍集

        dossier_tmp.simple_batch(pb_info, labels = {pycluster.FACE:[0,0,0,0,0,0,1,1]}, dossier_labels = {pycluster.FACE:[0,0,0,0,1,2,0,0]}) 
        ```
        其中labels和dossier_labels都分模态，每个模态的长度应和抓拍集中对应模态的抓拍数相同，从而给每张抓拍预设label(pid)和dossier_label(mid)
        labels字段中，数字相同为同一个人，其数值表示pid，dossier_labels表示对应到labels中这个人的每张抓拍分到这个人几号档案中，对于同一个人，dossier_labels相同表示这些抓拍在这个人的同一个档案中，数值不同表示在不同档案中。
        由于pb_info中有8张人脸抓图，所以labels和dossier_labels长度都为8，表示每张抓拍对应的人的pid和档案id标记。
        由于前6张抓拍都是pid为0的人的抓拍，所以labels前6个数字为0，后两张为pid1的人的抓拍，所以labels后两个数字为1。
        由于前4张抓拍，第5张抓拍，第6张抓拍分别为0号人的不同档案的抓拍，所以前6张图的dossier_labels为[0,0,0,0,1,2]，1号人两张抓拍都在1个档案中，所以dossier_labels都是0。
        support asynchronous
        """
    def simple_info(self) -> str:
        """
        输出简单的档案集信息
        例如：
        ``` python
        
        print(dossier.simple_info())
        ```
        """
    def split(self, size: int) -> list[dossier]:
        """
        将该档案集按照一定的数量进行分割，分成多个档案集列表
        例如：
        ``` python
        
        def split_dossier(dos:pydossier.dossier, count:int):
            tmp = dos.create_empty()
            for i in range(dos.person_num()):
                if dos.is_person_exists(i):
                    tmp.emplace_from_other(dos, i)
                    if tmp.person_num() >= count:
                yield tmp
                tmp = dos.create_empty()
            yield tmp
                
        for dos in split_dossier(dossier_1, 50000):
            dossier_0.oc_separate(dos)
        ```
        support asynchronous
        """
    def tidy_up(self) -> None:
        """
        整理档案集，删除其中的空档案
        例如：
        ``` python
        
        dossier.tidy_up()
        ```
        support asynchronous
        """
    @typing.overload
    def use_mmap(self, path: str) -> None:
        """
        使用内存映射
        例如：
        ``` python
        
        dossier.use_mmap("./mmap/")
        ```
        """
    @typing.overload
    def use_mmap(self, path: str, mdl: pycluster2x.lib.pycluster.mdl_e) -> None:
        """
        对特定模态使用内存映射
        例如：
        ``` python
        
        dossier.use_mmap("./mmap/", pycluster.FACE)
        ```
        """
class fuse_e:
    """
    
            是否推荐融合。
        
    
    Members:
    
      UNKNOW : UNKNOW 即未知 DHIVS_CLUSTER_FUSE_RECOMMEND_UNKNOW
    
      MERGE : MERGE 即融合 DHIVS_CLUSTER_FUSE_RECOMMEND_MERGE
    
      JUDGE : JUDGE 即需要进一步判断 DHIVS_CLUSTER_FUSE_RECOMMEND_JUDGE
    
      ADSORBED : JUDGE 即需要进一步判断 DHIVS_CLUSTER_FUSE_RECOMMEND_ADSORBED
    
      DST : DST 即输入档案本身，表示oc流程后，这个oc结果对应的人，最终合到的base档案集中的位置
    """
    ADSORBED: typing.ClassVar[fuse_e]  # value = <fuse_e.ADSORBED: 3>
    DST: typing.ClassVar[fuse_e]  # value = <fuse_e.DST: 2147483647>
    JUDGE: typing.ClassVar[fuse_e]  # value = <fuse_e.JUDGE: 2>
    MERGE: typing.ClassVar[fuse_e]  # value = <fuse_e.MERGE: 1>
    UNKNOW: typing.ClassVar[fuse_e]  # value = <fuse_e.UNKNOW: 0>
    __members__: typing.ClassVar[dict[str, fuse_e]]  # value = {'UNKNOW': <fuse_e.UNKNOW: 0>, 'MERGE': <fuse_e.MERGE: 1>, 'JUDGE': <fuse_e.JUDGE: 2>, 'ADSORBED': <fuse_e.ADSORBED: 3>, 'DST': <fuse_e.DST: 2147483647>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class oc_updates:
    """
    
            一个人的合档接口输出结果结构体
        
    """
    dossier_label: int
    fuse_recommend: fuse_e
    label: int
    score: float
    type: pycluster2x.lib.pycluster.mdl_e
    update: int
    def __init__(self) -> None:
        ...
    def __repr__(self) -> str:
        """
        字符串格式化合档结果oc_update结构，格式为形如：{"label":135, "dossier_label":246, "score":0.997, "fuse_recommend":MERGE, "update":1, "type":FACE}
        """
def async_load(*args, **kwargs):
    """
    
    async function of
    load(path: str) -> pycluster2x.lib.pydossier.dossier
    load(path: str, cfg: dict[str, str]) -> pycluster2x.lib.pydossier.dossier
        
    """
def async_load_big(*args, **kwargs):
    """
    
    async function of
    load_big(path: str) -> pycluster2x.lib.pydossier.dossier
    load_big(path: str, cfg: dict[str, str]) -> pycluster2x.lib.pydossier.dossier
        
    """
def async_load_small(*args, **kwargs):
    """
    
    async function of
    load_small(path: str) -> pycluster2x.lib.pydossier.dossier
    load_small(path: str, cfg: dict[str, str]) -> pycluster2x.lib.pydossier.dossier
        
    """
def async_unser(arg0: str) -> dossier:
    """
    
    async function of
    unser(arg0: str) -> pycluster2x.lib.pydossier.dossier
        
    """
@typing.overload
def load(path: str) -> dossier:
    """
            读取档案，对应通过save保存的档案格式
            例如：
            ``` python
    
            dossier.save("./result/")
            dossier_0:pydossier.dossier = pydossier.load("./result/")
            ```
            support asynchronous
    """
@typing.overload
def load(path: str, cfg: dict[str, str]) -> dossier:
    """
            读取档案，对应通过save保存的档案格式，同时重新指定配置表参数
            例如：
            ``` python
    
            dossier.save("./result/")
            dossier:pydossier.dossier = pydossier.load("./result/", pycluster.default_cfg())
            ```
            support asynchronous
    """
@typing.overload
def load_big(path: str) -> dossier:
    """
            读取档案，对应save_big保存的档案格式
            例如：
            ``` python
    
            dossier.save_big("./result/")
            dossier_0:pydossier.dossier = pydossier.load_big("./result/")
            ```
            support asynchronous
    """
@typing.overload
def load_big(path: str, cfg: dict[str, str]) -> dossier:
    """
            读取档案，对应通过save_big保存的档案格式，同时重新指定配置表参数
            例如：
            ``` python
    
            dossier.save_big("./result/")
            dossier_0:pydossier.dossier = pydossier.load_big("./result/", pycluster.default_cfg())
            ```
            support asynchronous
    """
@typing.overload
def load_small(path: str) -> dossier:
    """
            读取档案，对应通过save_small保存的档案格式
            例如：
            ``` python
    
            dossier.save_small("./result/")
            dossier_0:pydossier.dossier = pydossier.load_small("./result/")
            ```
            support asynchronous
    """
@typing.overload
def load_small(path: str, cfg: dict[str, str]) -> dossier:
    """
            读取档案，对应通过save_small保存的档案格式，同时重新指定配置表参数
            例如：
            ``` python
    
            dossier.save_small("./result/")
            dossier:pydossier.dossier = pydossier.load_small("./result/", pycluster.default_cfg())
            ```
            support asynchronous
    """
def unser(arg0: str) -> dossier:
    """
            档案集反序列化
            例如：
            ``` python
    
            dos_ser = dossier.ser()
            dossier_tmp = pydossier.unser(dos_ser)
            print(dossier, dossier_tmp)  # dossier 和 dossier_tmp 相同
            ```
            support asynchronous
    """
