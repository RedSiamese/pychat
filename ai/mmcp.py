import typing

class MmcpServerBase:
    def __init__(self):
        pass

    def name(self) -> str:
        pass

    def description(self) -> str:
        pass

    async def __call__(self, *args, **kwargs) -> str:
        pass

    # def param(self):
    #     return [{"name":}]

    

class MmcpLocalServers:
    def __init__(self):
        self._server_list = []

    def add_mmcp(self, server:MmcpServerBase):
        self._server_list.append(server)

    def get_mmcp_description(self):
        return {server.name():server.description() for server in self._server_list}

    def get_mmcp_description_str(self)->'list[str]':
        return [f"# {server.name()}\n\n{server.description()}\n\n\n" for server in self._server_list]
    
    def get_mmcp(self, name:'list[str]|str') ->'dict[str, MmcpServerBase] | MmcpServerBase':
        if type(name) == str:
            return [server for server in self._server_list if server.name() == name][0]
        else:
            return {server.name():server for server in self._server_list if server.name() in name}
        
    def __contains__(self, name:str):
        return name in [server.name() for server in self._server_list]
    
    def get_mmcp_name_list(self)->'list[str]':
        return [server.name() for server in self._server_list]


LocalMmcp = MmcpLocalServers()


def create_mmcp(func:typing.Callable) -> MmcpServerBase:
    """
    Create a mmcp server from a function and add it to the local server list.
    """
    class MmcpServer(MmcpServerBase):
        def __init__(self):
            self._func = func

        def name(self) -> str:
            return func.__name__

        def description(self) -> str:
            return func.__doc__

        async def __call__(self, *args, **kwargs) -> str:
            return await self._func(*args, **kwargs)
        
    LocalMmcp.add_mmcp(MmcpServer())
    return LocalMmcp.get_mmcp(func.__name__)