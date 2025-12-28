"""消息系统"""

from typing import Optional, Dict, Any, Literal
from datetime import datetime
from pydantic import BaseModel

MessageRole = Literal["user", "assistant", "system", "tool"] # 定义消息角色的字面量类型

class Message(BaseModel):
    """消息类"""
    
    content: str
    role: MessageRole
    timestamp: datetime = None # 消息时间戳
    metadata: Optional[Dict[str, Any]] = None 
    
    # 初始化方法，设置默认时间戳和元数据
    def __init__(self, content: str, role: MessageRole, **kwargs):
        super().__init__(
            content=content,
            role=role,
            timestamp=kwargs.get('timestamp', datetime.now()),
            metadata=kwargs.get('metadata', {})
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式（OpenAI API格式）"""
        return {
            "role": self.role,
            "content": self.content
        }
    
    # 字符串表示方法
    def __str__(self) -> str:
        return f"[{self.role}] {self.content}"
