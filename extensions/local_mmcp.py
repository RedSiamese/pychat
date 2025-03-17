
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai.mmcp import LocalMmcp, MmcpServerBase

import mmcp_tool.pycluster2x as pycluster2x
import mmcp_tool.cluster as cluster
import mmcp_tool.cork7 as cork7

class Cork7Mmcp(MmcpServerBase):
    def name(self) -> str:
        return "cork7"

    def description(self) -> str:
        return "cork7 是一个用于读取本地数据缓存的库，提供了读取本地数据缓存的api，用于完成数据读取功能开发"

    async def __call__(self, *args, **kwargs) -> str:
        return await cork7.call(*args, **kwargs)
    

class PyCluster2xMmcp(MmcpServerBase):
    def name(self) -> str:
        return "pycluster2x"
    
    def description(self) -> str:
        return \
"""
PyCluster2x 是聚档项目的Python扩展包
提供了聚档相关的api，用于完成人脸人体各项功能的python开发
其中包括：
- 档案集管理pydossier
- 抓拍集管理pypic
- 聚档数据缓存管理pycache
等模块
"""

    async def __call__(self, *args, **kwargs) -> str:
        return await pycluster2x.call(*args, **kwargs)


class ClusterMmcp(MmcpServerBase):
    def name(self) -> str:
        return "cluster"
    
    def description(self) -> str:
        return \
"""
cluster 是聚档项目流程相关的文档，包含：
- 如何开始聚档项目的文档
- 聚档项目常用的脚本运行方法的文档
- 聚档项目常用的服务器和数据资源的文档
- 聚档扩展包pycluster2x下载地址的文档
- 注意：不涉及代码接口api！
等文档信息。
"""
    
    async def __call__(self, *args, **kwargs) -> str:
        return await cluster.call(*args, **kwargs)
    

LocalMmcp.add_mmcp(Cork7Mmcp())
LocalMmcp.add_mmcp(PyCluster2xMmcp())
LocalMmcp.add_mmcp(ClusterMmcp())