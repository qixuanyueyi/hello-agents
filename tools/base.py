"""工具基类，工具基类，
统一所有工具的参数、接口（比如run方法），是工具的 “规范模板”"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from pydantic import BaseModel

class ToolParameter(BaseModel):
    """工具参数定义"""
    name: str
    type: str
    description: str
    required: bool = True
    default: Any = None

class Tool(ABC):
    """工具基类"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def run(self, parameters: Dict[str, Any]) -> str:
        """执行工具"""
        pass
    
    @abstractmethod
    def get_parameters(self) -> List[ToolParameter]:
        """获取工具参数定义"""
        pass
    
    # 这个方法可以用来验证传入的参数是否符合工具的要求
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """验证参数"""
        required_params = [p.name for p in self.get_parameters() if p.required] # 获取必需参数列表
        return all(param in parameters for param in required_params)
    
    # 将工具信息转换为字典格式，便于序列化或其他用途
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": [param.dict() for param in self.get_parameters()]
        }
    
    # 字符串表示
    def __str__(self) -> str:
        return f"Tool(name={self.name})"
    
    # 正式字符串表示
    def __repr__(self) -> str:
        return self.__str__()