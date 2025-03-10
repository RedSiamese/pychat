"""

    pycluster是pycluster2x中基础功能相关的模块，包含算法句柄类等, 通常通过 ```from pycluster2x import pycluster```引入。

    pycluster中定义了模态枚举（pycluster.FACE,pycluster.BODY等）。
    pycluster中定义了cluster_hdl算法句柄，通过配置表和能力集（支持哪些模态功能）进行构造，通过算法句柄才可以使用算法功能
    pycluster中定义了创建算法句柄的默认配置default_cfg

    关键词： 算法句柄  配置表
    
"""
from __future__ import annotations
import typing
__all__ = ['BODY', 'FACE', 'INT_MAX', 'c_threadid', 'cluster_div_mem_error', 'cluster_hdl', 'cluster_invoke_error', 'cluster_license_error', 'cluster_logic_error', 'default_cfg', 'demo_version', 'detail_info', 'detail_info_viewer', 'lib_version', 'mdl_e', 'platform', 'sdk_version', 'this_platform']
class cluster_div_mem_error(Exception):
    pass
class cluster_hdl:
    @typing.overload
    def __init__(self, arg0: list[mdl_e], arg1: dict[str, str]) -> None:
        """
                根据配置字典构造算法句柄，其字典类型为dict[str, str]， 即键值均为字符串的字典，如：
                例如：
                ``` python
        
                @to_str_dict
                def cfg() -> dict:
                    return {
                        "face_cfg_file" : "../model/face/fcl_v1.6",           # 人脸模型路径
                        "body_cfg_file" : "../model/body/body.json",          # 人体模型路径
                        "device_id" : "1",                                    # 设备id
                        "device_type" : "2",                                  # 设备类型，2为gpu，1为cpu
                        "body_centroid_num" : "4",                            # 人体质心数
                        "face_feat_dim" : "256",                              # 人脸特征维度
                        "body_feat_dim" : "256",                              # 人体特征维度
                        "face_one_max_result_num" : "10",                     # 人脸oc最大结果数
                        "body_one_max_result_num" : "10",                     # 人体oc最大结果数
                        "feature" : "fp16",                                   # 人脸特征类型，fp32不填即可
                        "proxy_sub_lower_bound" : "8"                         # 实时底档筛选规则的底档数量
                    }
        
                alg_hdl = pycluster.cluster_hdl([pycluster.FACE, pycluster.BODY], cfg())
                ```
                上述例子中cfg()构造了一个字典，并使用修饰器将值转化为字符串，并传给pycluster.cluster_hdl构造函数创建了一个算法句柄alg_hdl
                这里cfg也可以使用默认参数 pycluster.default_cfg()
        """
    @typing.overload
    def __init__(self, arg0: list[mdl_e], arg1: str) -> None:
        ...
    def get_cfg(self) -> dict[str, str]:
        ...
class cluster_invoke_error(Exception):
    pass
class cluster_license_error(Exception):
    pass
class cluster_logic_error(Exception):
    pass
class detail_info_viewer:
    """
    信息
    """
    def __enter__(self) -> detail_info_viewer:
        ...
    def __exit__(self, arg0: typing.Any, arg1: typing.Any, arg2: typing.Any) -> None:
        ...
    def __getitem__(self, arg0: str) -> typing.Any:
        ...
    def __repr__(self) -> str:
        ...
    def as_dict(self) -> dict:
        ...
    def clear(self) -> None:
        ...
    def local(self) -> detail_info_viewer:
        ...
class mdl_e:
    """
    
            聚类模态枚举，其中：
            FACE 即 DHIVS_CLUSTER_FACE
            BODY 即 DHIVS_CLUSTER_BODY
        
    
    Members:
    
      FACE : FACE 即人脸模态 DHIVS_CLUSTER_FACE
    
      BODY : BODY 即人体模态 DHIVS_CLUSTER_BODY
    """
    BODY: typing.ClassVar[mdl_e]  # value = <mdl_e.BODY: 2>
    FACE: typing.ClassVar[mdl_e]  # value = <mdl_e.FACE: 1>
    __members__: typing.ClassVar[dict[str, mdl_e]]  # value = {'FACE': <mdl_e.FACE: 1>, 'BODY': <mdl_e.BODY: 2>}
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
class platform:
    """
    
            平台枚举
        
    
    Members:
    
      UNKONWN
    
      X86_CPU
    
      X86_GPU
    
      ARM
    
      ASCEND710
    
      CAMBRICON220
    
      AX650
    """
    ARM: typing.ClassVar[platform]  # value = <platform.ARM: 45>
    ASCEND710: typing.ClassVar[platform]  # value = <platform.ASCEND710: 30>
    AX650: typing.ClassVar[platform]  # value = <platform.AX650: 71>
    CAMBRICON220: typing.ClassVar[platform]  # value = <platform.CAMBRICON220: 35>
    UNKONWN: typing.ClassVar[platform]  # value = <platform.UNKONWN: 0>
    X86_CPU: typing.ClassVar[platform]  # value = <platform.X86_CPU: 1>
    X86_GPU: typing.ClassVar[platform]  # value = <platform.X86_GPU: 65537>
    __members__: typing.ClassVar[dict[str, platform]]  # value = {'UNKONWN': <platform.UNKONWN: 0>, 'X86_CPU': <platform.X86_CPU: 1>, 'X86_GPU': <platform.X86_GPU: 65537>, 'ARM': <platform.ARM: 45>, 'ASCEND710': <platform.ASCEND710: 30>, 'CAMBRICON220': <platform.CAMBRICON220: 35>, 'AX650': <platform.AX650: 71>}
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
def c_threadid() -> int:
    """
            python中获取c风格线程号
            例如：
            ``` python
    
            from pycluster2x import pycluster, pydossier, pypic, pycache
            print(pycluster.c_threadid())
            ```
    """
def default_cfg() -> dict[str, str]:
    """
            默认配置表, 字段和默认值为
            ``` python
            {
                "device_type": "1",                         # 平台相关，cpu为1，gpu为2
                "feature": "fp16",                          # 平台相关，cpu为fp32，gpu为fp16
                "device_id": "0",                           # 平台相关，cpu版本或不支持多卡的版本无效
                "face_feat_dim": "256",                     # 人脸特征维度
                "face_feat_threshold": "0.92",              # 人脸batch阈值，通常0.92
                "face_cluster_feat_threshold": "0.92",      # 人脸oc阈值，通常时空域内小合档0.92，跨时空域大合档0.95
                "face_feat_topK": "3",                      # 针对人脸特征聚类的k近邻参数，通常填3
                "face_one_max_result_num": "10",            # 人脸oc结果输出数量
                "face_centroid_num": "4",                   # 人脸质心数量
                "face_batch_center_threshold": "0.95",      # 人脸选取额外质心时和主质心的介值要求，通常填0.95
                "body_feat_dim": "256",                     # 人体特征维度
                "body_one_max_result_num": "10",            # 人体oc结果输出数量
                "body_centroid_num": "4",                   # 人体质心数量
                "body_batch_center_threshold": "0.95",      # 人体选取额外质心时和主质心的介值要求，通常填0.95
                "body_feat_threshold": "0.92f",             # batch相似度阈值，通常0.92
                "body_cluster_feat_threshold": "0.92f",     # oc相似度阈值，通常时空域内小合档0.92
                "face_cfg_file": "-",                       # 人脸配置目录，填"-"标识跟随扩展包实际路径
                "body_cfg_file": "-",                       # 人体配置目录，填"-"标识跟随扩展包实际路径
                "record": "False",                          # 是否保存rid的中间流转过程用于调试
                "uuid": "False",                            # 是否启用档案uuid
                "data_cache": "./data_cache/",              # 档案集中所有抓拍来源的数据缓存地址
                "base_cfg_file": "-",                       # 基础配置目录，填"-"标识跟随扩展包实际路径
                "body_dossier_attr_len": "2",               # 人体属性长度
                "face_dossier_attr_len": "2",               # 人脸属性长度
                "face_lut_path": "-",                       # 人脸拉伸表目录，填"-"标识跟随扩展包实际路径
                "body_lut_path": "-",                       # 人体拉伸表目录，填"-"标识跟随扩展包实际路径
                "thread_num": "1"                           # 内部多线程数，"0"和"1"代表单线程
            }
            ```
    
            例如：
            ``` python
    
            print(pycluster.default_cfg())
            ```
    """
def demo_version() -> tuple[int, str, str]:
    """
            获取聚类demo库版本号
            例如：
            ``` python
    
            import json
            from pycluster2x import pycluster
            with open("svn.log", "w+") as f:
                svn = {"demo_version":pycluster.demo_version()}
                json.dump(svn, f)
            ```
            上述代码获得了demo版本，并写在了json中
    """
def detail_info() -> detail_info_viewer:
    ...
def lib_version() -> tuple[int, str, str]:
    """
            获取聚类so库版本号
            例如：
            ``` python
    
            import json
            from pycluster2x import pycluster
            with open("svn.log", "w+") as f:
                svn = {"lib_version":pycluster.lib_version()}
                json.dump(svn, f)
            ```
            上述代码获得了库版本，并写在了json中
    """
def sdk_version() -> tuple[int, str, str]:
    """
            获取聚类sdk库版本号
            例如：
            ``` python
    
            import json
            from pycluster2x import pycluster
            with open("svn.log", "w+") as f:
                svn = {"sdk_version":pycluster.sdk_version()}
                json.dump(svn, f)
            ```
            上述代码获得了集成版本，并写在了json中
    """
def this_platform() -> platform:
    """
            获取平台类型
    """
BODY: mdl_e  # value = <mdl_e.BODY: 2>
FACE: mdl_e  # value = <mdl_e.FACE: 1>
INT_MAX: int = 2147483647
