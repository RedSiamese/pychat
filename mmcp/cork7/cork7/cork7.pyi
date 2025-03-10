"""

    cork7是一个用于将大量key-value数据在本地硬盘实现快速增/查的库。
    提供类似于c++ std::map api的多种检索接口
    
"""
import typing
class data_cache:
    """
    
            数据缓存类，创建参数 path 为已有的或者希望保存到的数据缓存路径，定义于cork7模块中
            例如：
            ``` python
    
            import cork7
            dc = cork7.data_cache("./data_cache/")
            ```
        
    """
    class table:
        """
        
                数据表类，有数据缓存获取对应字段的数据表得到，定义于cork7.data_cache类中
            
        """
        class iterator:
            """
            
                    数据迭代器类，通过检索数据缓存得到，定义于cork7.data_cache.table模块中
                
            """
            __hash__: typing.ClassVar[None] = None
            def __bool__(self) -> bool:
                """
                        判断这个迭代器是否结束，即是不是end()迭代器
                        如果不是end()，即还未结束，返回true。
                        等于end()，即已结束，返回false。
                """
            def __eq__(self, arg0: data_cache.table.iterator) -> bool:
                """
                        判断迭代器相等
                """
            def __iter__(self) -> data_cache.table.iterator:
                ...
            def __ne__(self, arg0: data_cache.table.iterator) -> bool:
                """
                        判断迭代器不相等
                """
            def __next__(self) -> dict:
                """
                        返回该条目，迭代器前进一步
                """
        def __iter__(self) -> data_cache.table.iterator:
            """
                    返回从小到大遍历这个表的迭代器
            """
        def __len__(self) -> int:
            """
                    返回这个表中的数据总量，即含有该字段的条目数量
            """
        def begin(self) -> data_cache.table.iterator:
            """
                    获得表的begin迭代器
            """
        def check_tree(self) -> dict[int, int]:
            """
                    查看数据缓存树结构，返回每个子树深度组成的list来检查树是否足够平衡
            """
        def count(self, value: typing.Any, value_type: datatype = datatype.AUTO) -> int:
            """
                    找到等于给定元素的元素个数
                    当value_type为 datatype.AUTO时(value_type默认为datatype.AUTO)，value会根据输入数据类型自动转换，例如 "s" 为datatype.STR，0.1为datatype.FP64，12为datatype.INT32
            """
        def end(self) -> data_cache.table.iterator:
            """
                    获得表的end迭代器
            """
        def find(self, value: typing.Any, value_type: datatype = datatype.AUTO) -> data_cache.table.iterator:
            """
                    找到第一个等于给定元素的元素，如果没有找到，则返回 end() 迭代器。
                    当value_type为 datatype.AUTO时(value_type默认为datatype.AUTO)，value会根据输入数据类型自动转换，例如 "s" 为datatype.STR，0.1为datatype.FP64，12为datatype.INT32
                    例如，假如存储的信息为[{"name":"ddd","age":23}, {"name":"bbb","age":18}, {"name":"ccc","age":22}, {"name":"aaa","age":15}, {"name":"eee","age":18}]，
                    通过age字段建表后调用这个函数搜索第一个等于16的age，即find(16)
                    由于没有age为16的条目，所以搜索不到，返回一个end()迭代器
                    如果用这个函数搜索第一个等于18的age，即find(18)
                    由于是查找第一个等于的元素，age等于18的元素有两个，由于name为"bbb"的先插入，所以返回的迭代器it指向{"name":"bbb","age":18}这条数据
                    例如：
                    ``` python
                    
                    dc = cork7.data_cache("./data_cache/")
                    dc.emplace([{"name":"ddd","age":23}, {"name":"bbb","age":18}, {"name":"ccc","age":22}, {"name":"aaa","age":15}, {"name":"eee","age":18}])
                    age_table = dc.get_table("age")
                    for it in name_table.find(16):
                        print(it) # 不会有输出
                    for it in name_table.find(18):
                        print(it) # 会逐条打印出 {"name":"bbb","age":18} {"name":"eee","age":18} {"name":"ccc","age":22} {"name":"ddd","age":23}
                    ```
            """
        def find_eq(self, value: typing.Any, value_type: datatype = datatype.AUTO) -> data_cache.table.iterator:
            """
                    找到第一个等于给定元素的元素，和find的区别在于，他返回的迭代器，只会遍历和给定元素相同的元素。如果没有找到，则返回 end() 迭代器。
                    当value_type为 datatype.AUTO时(value_type默认为datatype.AUTO)，value会根据输入数据类型自动转换，例如 "s" 为datatype.STR，0.1为datatype.FP64，12为datatype.INT32
                    例如，假如存储的信息为[{"name":"ddd","age":23}, {"name":"bbb","age":18}, {"name":"ccc","age":22}, {"name":"aaa","age":15}, {"name":"eee","age":18}]，
                    通过age字段建表后调用这个函数搜索第一个等于16的age，即find_eq(16)
                    由于没有age为16的条目，所以搜索不到，返回一个end()迭代器
                    如果用这个函数搜索第一个等于18的age，即find_eq(18)
                    由于是查找第一个等于的元素，age等于18的元素有两个，由于name为"bbb"的先插入，所以返回的迭代器it指向{"name":"bbb","age":18}这条数据
                    例如：
                    ``` python
                    
                    dc = cork7.data_cache("./data_cache/")
                    dc.emplace([{"name":"ddd","age":23}, {"name":"bbb","age":18}, {"name":"ccc","age":22}, {"name":"aaa","age":15}, {"name":"eee","age":18}])
                    age_table = dc.get_table("age")
                    for it in name_table.find(16):
                        print(it) # 不会有输出
                    for it in name_table.find(18):
                        print(it) # 会逐条打印出 {"name":"bbb","age":18} {"name":"eee","age":18}
                    ```
            """
        def find_multi(self, arg0: list) -> list[data_cache.table.iterator]:
            """
                    和find(...)查询原则相同，区别在于find_multi接口可以同时查找多个元素以提升查找效率
                    输入一个元素的list，返回一个迭代器的list
            """
        def lower_bound(self, value: typing.Any, value_type: datatype = datatype.AUTO) -> data_cache.table.iterator:
            """
                    找到第一个不小于给定元素的元素，即第一个键大于或等于给定键的元素，如果没有找到，则返回 end() 迭代器。
                    当value_type为 datatype.AUTO时(value_type默认为datatype.AUTO)，value会根据输入数据类型自动转换，例如 "s" 为datatype.STR，0.1为datatype.FP64，12为datatype.INT32
                    例如，假如存储的信息为[{"name":"ddd","age":23}, {"name":"bbb","age":18}, {"name":"ccc","age":22}, {"name":"aaa","age":15}]，
                    通过age字段建表后调用这个函数搜索第一个不小于16的age，即lower_bound(16)
                    函数会返回一个迭代器it，迭代器it指向{"name":"bbb","age":18}这条数据，由于是通过age表进行检索得到的迭代器，遍历这个迭代器it会得到所有age大于输入16，并且递增的数据，即{"name":"bbb","age":18}, {"name":"ccc","age":22}, {"name":"ccc","age":23}
                    如果用这个函数搜索第一个不小于18的age，即lower_bound(18)
                    由于是查找第一个不小于的元素，所以返回的迭代器it指向{"name":"bbb","age":18}这条数据
                    例如：
                    ``` python
                    
                    dc = cork7.data_cache("./data_cache/")
                    dc.emplace([{"name":"ddd","age":23}, {"name":"bbb","age":18}, {"name":"ccc","age":22}, {"name":"aaa","age":15}])
                    age_table = dc.get_table("age")
                    for it in name_table.lower_bound(16):
                        print(it) # 会逐条打印出 {"name":"bbb","age":18} {"name":"ccc","age":22} {"name":"ddd","age":23}
                    for it in name_table.lower_bound(18):
                        print(it) # 会逐条打印出 {"name":"bbb","age":18} {"name":"ccc","age":22} {"name":"ddd","age":23}
                    ```
            """
        def reset(self) -> None:
            """
                    重新生成该表以获得更加平衡的树结构
            """
        def unique_size(self) -> int:
            """
                    获得当前表不同值的数量（包含None）
            """
        def unique_value(self) -> list:
            """
                    获得当前表中不同的值组成的list
                    例如，假如存储的信息为[{"name":"ddd","age":23}, {"name":"bbb","age":18}, {"name":"ccc","age":22}, {"name":"aaa"}, {"name":"eee","age":18}]，
                    查找age表不同值，得到的结果为[18,22,23]
            """
        def upper_bound(self, value: typing.Any, value_type: datatype = datatype.AUTO) -> data_cache.table.iterator:
            """
                    找到第一个大于给定元素的元素，用于查找一个键的“上界”，如果没有找到，则返回 end() 迭代器。
                    当value_type为 datatype.AUTO时(value_type默认为datatype.AUTO)，value会根据输入数据类型自动转换，例如 "s" 为datatype.STR，0.1为datatype.FP64，12为datatype.INT32
                    例如，假如存储的信息为[{"name":"ddd","age":23}, {"name":"bbb","age":18}, {"name":"ccc","age":22}, {"name":"aaa","age":15}]，
                    通过age字段建表后调用这个函数搜索第一个大于16的age，即upper_bound(16)
                    函数会返回一个迭代器it，迭代器it指向{"name":"bbb","age":18}这条数据，由于是通过age表进行检索得到的迭代器，遍历这个迭代器it会得到所有age大于输入16，并且递增的数据，即{"name":"bbb","age":18}, {"name":"ccc","age":22}, {"name":"ccc","age":23}
                    如果用这个函数搜索第一个大于18的age，即upper_bound(18)
                    由于是查找第一个大于的元素，所以返回的迭代器it指向{"name":"ccc","age":22}这条数据
                    例如：
                    ``` python
                    
                    dc = cork7.data_cache("./data_cache/")
                    dc.emplace([{"name":"ddd","age":23}, {"name":"bbb","age":18}, {"name":"ccc","age":22}, {"name":"aaa","age":15}])
                    age_table = dc.get_table("age")
                    for it in name_table.upper_bound(16):
                        print(it) # 会逐条打印出 {"name":"bbb","age":18} {"name":"ccc","age":22} {"name":"ddd","age":23}
                    for it in name_table.upper_bound(18):
                        print(it) # 会逐条打印出 {"name":"ccc","age":22} {"name":"ddd","age":23}
                    ```
            """
    def __getitem__(self, arg0: int) -> dict:
        """
                检索某次插入的数据，保续，可按照插入顺序进行索引
                例如：
                ``` python
        
                dc = cork7.data_cache("./data_cache/")
                print(dc[0])
                ```
        """
    def __init__(self, path: str) -> None:
        ...
    def __iter__(self) -> data_cache.table.iterator:
        """
                同traversal，获取数据缓存完整遍历迭代器，通过遍历迭代器可以遍历所有已保存的数据，遍历不保续，即和输入时数据顺序可能不同。
                例如：
                ``` python
        
                dc = cork7.data_cache("./data_cache/")
                for it in dc:
                    it: cork7.data_cache.table.iterator
                    print(it)
                ```
        """
    def __len__(self, arg0: int) -> int:
        """
                获得总插入数据量。
                例如：
                ``` python
        
                dc = cork7.data_cache("./data_cache/")
                print(len(dc))
                ```
        """
    def check_data(self, start_data_file_idx: int = -1) -> bool:
        """
                检查数据是否全部可读
        """
    def check_data_keys(self) -> list[str]:
        """
                获取所有数据中存在的字段名
        """
    @typing.overload
    def emplace(self, data: dict) -> None:
        """
                将数据插入数据缓存
                数据类型为一个dict[str, int|float|str|bytes]
                即，存入字典键类型为字符串str，值类型支持：
                    int 
                    float
                    str
                    bytes
                例如：
                ``` python
        
                dc = cork7.data_cache("./data_cache/")
                dc.emplace({"name":"abc", "age":25, "weight":67.45})
                ```
        """
    @typing.overload
    def emplace(self, data: list) -> None:
        """
                将多条数据插入数据缓存，
                数据类型为一个list[dict[str, int|float|str|bytes]]，
                即，存入字典键类型为字符串str，值类型支持：
                    int 
                    float
                    str
                    bytes
                例如：
                ``` python
        
                dc = cork7.data_cache("./data_cache/")
                dc.emplace([{"name":"aaa", "age":25, "weight":67.45}, {"name":"bbb", "age":23, "weight":57.85}, {"name":"ccc", "age":31, "weight":62.00}])
                ```
        """
    def get_table(self, arg0: str) -> data_cache.table:
        """
                获得某个键的数据表，用于后续用数据表进行数据检索。
                例如：
                ``` python
        
                dc = cork7.data_cache("./data_cache/")
                name_table = dc.get_table("name")
                for it in name_table.find_eq("aaa"):
                    print(it)
                ```
        """
    def get_tables(self) -> list[str]:
        """
                获取所有表名
        """
    def reset_table(self, arg0: str) -> None:
        """
                重整索引表，将所有索引表全部重新生成，可能会消耗大量时间
        """
    def traversal(self) -> data_cache.table.iterator:
        """
                获取数据缓存完整遍历迭代器，通过遍历迭代器可以遍历所有已保存的数据，遍历不保续，即和输入时数据顺序可能不同。
                例如：
                ``` python
        
                dc = cork7.data_cache("./data_cache/")
                it: cork7.data_cache.table.iterator = dc.traversal()
                print(it)
                it.next()
                print(it)
                ```
        """
    def write_down(self) -> None:
        """
                清空缓冲区，再插入数据时，数据会先进入缓冲区，积累到一定数量后，再被写入文件中。
                调用该函数即使所有缓存区中的数据全部写入文件中。
                例如：
                ``` python
        
                dc = cork7.data_cache("./data_cache/")
                dc.emplace([{"name":"aaa", "age":25, "weight":67.45}, {"name":"bbb", "age":23, "weight":57.85}, {"name":"ccc", "age":31, "weight":62.00}])
                dc.write_down()
                ```
                主要用于多数据缓存对象访问同一数据缓存时进行信息同步，如果不写入文件，另一个数据缓存对象可能访问不到。
                如果只有单一数据缓存对象不存在这个问题。
        """
class datatype:
    """
        数据类型
    """
    AUTO: typing.ClassVar[datatype]  # value = <datatype.AUTO: 0>
    BYTES: typing.ClassVar[datatype]  # value = <datatype.BYTES: 5>
    FP64: typing.ClassVar[datatype]  # value = <datatype.FP64: 3>
    INT32: typing.ClassVar[datatype]  # value = <datatype.INT32: 1>
    INT64: typing.ClassVar[datatype]  # value = <datatype.INT64: 2>
    STR: typing.ClassVar[datatype]  # value = <datatype.STR: 4>
    __members__: typing.ClassVar[dict[str, datatype]]  # value = {'AUTO': <datatype.AUTO: 0>, 'INT32': <datatype.INT32: 1>, 'INT64': <datatype.INT64: 2>, 'FP64': <datatype.FP64: 3>, 'STR': <datatype.STR: 4>, 'BYTES': <datatype.BYTES: 5>}

class range:
    """
    数据范围迭代器类，通过两个迭代器构造该迭代器，分别表示begin和end，迭代该迭代器从begin迭代至end
    """
    def __init__(self, begin: data_cache.table.iterator, end: data_cache.table.iterator) -> None:
        ...
    def __iter__(self) -> range:
        ...
    def __next__(self) -> dict:
        ...
