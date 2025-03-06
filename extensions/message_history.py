"""
我正在写一个聊天机器人的后端代码，我现在的数据结构中，用户发来的对话上下文是一个list，其中每个元素代表每条数据，形如：
[{'id': '11', 'role': 'user', 'content': 'hi'}, 
 {'id': '22', 'role': 'assistant', 'content': 'Hello!'}, 
 {'id': '33', 'role': 'user', 'content': '你好'}]
每条信息包含一个id、角色和内容。
由于上下文有连续性，所以所有的消息可以组成一个链表，例如例子中'11'为根节点，子节点为"22"再然后为"33"
用户可能会重新基于根节点发起另一段对话，例如另一个分支为
[{'id': '11', 'role': 'user', 'content': 'hi'}, 
 {'id': '44', 'role': 'assistant', 'content': 'Hello!'},
 {'id': '55', 'role': 'user', 'content': '你好'}]
'44'也是'11'的子节点，所以这实际是一棵树。
当我们从后往前遍历消息列表，如果某一子节点能被找到，由于这条分支已经被建立，那他的根节点应该都能被找到。
我要用python将用户和ai的对话记录在服务器上，我打算用sqlite3。
帮我写这段代码，把所有的数据记录在数据库中，当用户发来一个上下文消息时，例如：
[{'id': '11', 'role': 'user', 'content': 'hi'}, 
 {'id': '66', 'role': 'assistant', 'content': 'Hello!'},
 {'id': '77', 'role': 'user', 'content': '你好'}]
从后往前遍历，寻找对话id的节点，如果某个子节点没找到，将他后面的对话记录在数据库中，并创建这棵树的一个分支，
如果所有的节点都找不到，例如
[{'id': '88', 'role': 'user', 'content': 'hi'}, 
 {'id': '99', 'role': 'assistant', 'content': 'Hello!'},
 {'id': '121', 'role': 'user', 'content': '你好'}]
则创建一颗新树
这个结构和所有聊天记录都需要保存，方便重启服务器时读取
"""



import sqlite3
import threading
import time,os
from datetime import datetime, timedelta

this_dir = os.path.dirname(os.path.abspath(__file__))

class ChatDatabase:
    def __init__(self, db_path=f'{this_dir}/db/'):
        os.makedirs(db_path, exist_ok=True)
        self.db_name = db_path + "/chat.db"
        self.conn = sqlite3.connect(self.db_name)
        self._init_db()
        self.schedule_cleanup()

    def _init_db(self):
        """初始化数据库和索引"""
        with self.conn:
            # 创建主表
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id TEXT PRIMARY KEY,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    parent_id TEXT,
                    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(parent_id) REFERENCES messages(id) ON DELETE CASCADE
                )
            ''')
            # 创建索引
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_last_accessed ON messages(last_accessed)')
            self.conn.execute('CREATE INDEX IF NOT EXISTS idx_parent_id ON messages(parent_id)')
            self.conn.execute('PRAGMA foreign_keys = ON')
            self.conn.execute('PRAGMA journal_mode = WAL')

    def _update_access_chain(self, node_id):
        """递归更新时间戳（使用WITH RECURSIVE）"""
        with self.conn:
            self.conn.execute('''
                WITH RECURSIVE access_path(id) AS (
                    SELECT :node_id
                    UNION ALL
                    SELECT m.parent_id
                    FROM messages m
                    JOIN access_path ap ON m.id = ap.id
                    WHERE m.parent_id IS NOT NULL
                )
                UPDATE messages
                SET last_accessed = CURRENT_TIMESTAMP
                WHERE id IN (SELECT id FROM access_path)
            ''', {'node_id': node_id})

    def save_conversation(self, messages):
        """
        保存对话上下文并更新访问时间
        """
        with self.conn:
            cursor = self.conn.cursor()
            parent_id = None
            insert_start = 0
            
            # 查找已存在的最近节点
            for i in reversed(range(len(messages))):
                cursor.execute('SELECT 1 FROM messages WHERE id = ?', (messages[i]['id'],))
                if cursor.fetchone():
                    parent_id = messages[i]['id']
                    insert_start = i + 1
                    break
            else:  # 全新对话
                insert_start = 0

            # 插入新节点
            last_id = None
            for msg in messages[insert_start:]:
                # 检查ID冲突
                cursor.execute('SELECT 1 FROM messages WHERE id = ?', (msg['id'],))
                if cursor.fetchone():
                    raise ValueError(f"Duplicate message ID: {msg['id']}")

                cursor.execute('''
                    INSERT INTO messages (id, role, content, parent_id)
                    VALUES (?, ?, ?, ?)
                ''', (msg['id'], msg['role'], msg['content'], parent_id))
                
                last_id = msg['id']
                parent_id = last_id

            # 更新时间戳链
            if last_id:
                self._update_access_chain(last_id)

    def get_conversation_branch(self, branch_tail_id, max_count = None):
        """
        获取完整对话链（从根节点开始）
        """
        self._update_access_chain(branch_tail_id)  # 先更新时间戳
        
        conversation = []
        with self.conn:
            cursor = self.conn.cursor()
            current_id = branch_tail_id
            
            while current_id:
                cursor.execute('''
                    SELECT id, role, content, parent_id
                    FROM messages
                    WHERE id = ?
                ''', (current_id,))
                msg = cursor.fetchone()
                
                if not msg:
                    break
                    
                conversation.insert(0, {
                    'id': msg[0],
                    'role': msg[1],
                    'content': msg[2]
                })
                current_id = msg[3]
        
        if max_count is None or len(conversation) < max_count:
            return conversation
        else:
            return conversation[-max_count:]
        
    def get_full_conversation_tree(self):
        """
        获取完整对话树结构
        """
        def build_tree(parent_id=None):
            with self.conn:
                cursor = self.conn.cursor()
                if parent_id is None:
                    cursor.execute('SELECT * FROM messages WHERE parent_id IS NULL')
                else:
                    cursor.execute('SELECT * FROM messages WHERE parent_id = ?', (parent_id,))
                
                nodes = []
                for row in cursor.fetchall():
                    node = {
                        'id': row[0],
                        'role': row[1],
                        'content': row[2],
                        'last_accessed': row[4],
                        'children': build_tree(row[0])
                    }
                    nodes.append(node)
                return nodes
        
        return build_tree()

    def _cleanup_old_nodes(self):
        """执行数据清理"""
        cutoff = datetime.utcnow() - timedelta(hours=48)
        conn = sqlite3.connect(self.db_name)
        try:
            with conn:
                conn.execute('PRAGMA foreign_keys = ON')
                # 级联删除过期节点
                conn.execute('''
                    DELETE FROM messages
                    WHERE id IN (
                        SELECT id FROM messages
                        WHERE last_accessed < ?
                    )
                ''', (cutoff.isoformat(),))
        finally:
            conn.close()
        
        # 重新安排清理任务
        self.schedule_cleanup()

    def schedule_cleanup(self):
        """调度清理任务"""
        timer = threading.Timer(3600, self._cleanup_old_nodes)
        timer.daemon = True
        timer.start()

    def close(self):
        """关闭数据库连接"""

    

# 使用示例
if __name__ == '__main__':
    db = ChatDatabase()
    
    # # 示例对话1（新树）
    # dialog1 = [
    #     {'id': '11', 'role': 'user', 'content': 'hi'},
    #     {'id': '22', 'role': 'assistant', 'content': 'Hello!'},
    #     {'id': '33', 'role': 'user', 'content': '你好'}
    # ]
    # db.save_conversation(dialog1)
    
    # # 示例对话2（创建分支）
    # dialog2 = [
    #     {'id': '11', 'role': 'user', 'content': 'hi'},
    #     {'id': '44', 'role': 'assistant', 'content': 'Bonjour!'},
    #     {'id': '55', 'role': 'user', 'content': 'Hola'}
    # ]
    # db.save_conversation(dialog2)
    
    # # 示例对话2（创建分支）
    # dialog2 = [
    #     {'id': '66', 'role': 'user', 'content': '今天天气如何？'},
    #     {'id': '77', 'role': 'assistant', 'content': '晴天，气温11-18摄氏度'},
    #     {'id': '88', 'role': 'user', 'content': '好的'}
    # ]
    # db.save_conversation(dialog2)
    
    # 获取对话分支
    print("对话分支：")
    for branch in db.get_conversation_branch('11'):
        print(branch)

    # 获取对话分支
    print("对话分支：")
    for branch in db.get_conversation_branch('44'):
        print(branch)

    # 获取对话分支
    print("对话分支：")
    for branch in db.get_conversation_branch('88'):
        print(branch)
    
    # 获取完整对话树
    print("\n完整对话树：")
    print(db.get_full_conversation_tree())


# # 增强测试用例
# if __name__ == '__main__':
#     # 初始化测试数据库
#     db = ChatDatabase()
    
#     # 测试基础功能
#     dialog1 = [
#         {'id': '11', 'role': 'user', 'content': 'hi'},
#         {'id': '22', 'role': 'assistant', 'content': 'Hello!'},
#         {'id': '33', 'role': 'user', 'content': '你好'}
#     ]
#     db.save_conversation(dialog1)
    
#     # 验证时间戳更新
#     cursor = db.conn.cursor()
#     cursor.execute('SELECT last_accessed FROM messages WHERE id = "11"')
#     assert cursor.fetchone()[0] is not None
    
#     # 测试自动清理
#     print("模拟过期数据清理...")
#     # sleep 超过_cleanup_old_nodes等待时间
#     db._cleanup_old_nodes()
    
#     cursor.execute('SELECT COUNT(*) FROM messages')
#     assert cursor.fetchone()[0] == 0  # 确认数据已被清理
    
#     print("所有测试通过！")