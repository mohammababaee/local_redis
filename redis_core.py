from typing import List, Dict, Any
from utils import ParsedCommand, ValidCommands


class RedisStorage:
    def __init__(self):
        self.data: Dict[str, Any] = {}
    
    def set(self, key: str, value: Any) -> None:
        self.data[key] = value
        return value
    
    def get(self, key: str) -> Any:
        return self.data.get(key)
    
    def delete(self, key: str) -> bool:
        if key in self.data:
            del self.data[key]
            return True
        return False
    
    def exists(self, key: str) -> bool:
        return key in self.data


class RedisCommandParser:
    def __init__(self):
        self.storage = RedisStorage()
    
    def parse_command_list(self, command_list: List[str]) -> ParsedCommand:
        if len(command_list) < 2:
            raise ValueError("At least command and key are required.")
        try:
            cmd_type = ValidCommands[command_list[0]]
        except KeyError:
            raise ValueError(f"Invalid command type: {command_list[0]}")
        key = command_list[1]
        value = command_list[2] if len(command_list) > 2 else None
        return ParsedCommand(type=cmd_type, key=key, value=value)
    
    def command_line_parser(self, command: str) -> ParsedCommand:
        command_list = command.split()
        if not command_list:
            raise ValueError("Empty command")
        if command_list[0] not in ValidCommands.__members__:
            raise ValueError(
                f"Invalid Command! Valid commands: {', '.join(ValidCommands.__members__.keys())}"
            )
        return self.parse_command_list(command_list)
    
    def execute_command(self, parsed_command: ParsedCommand) -> Dict[str, Any]:
        command_handlers = {
            ValidCommands.SET: lambda cmd: self.storage.set(cmd.key, cmd.value),
            ValidCommands.GET: lambda cmd: self.storage.get(cmd.key),
            ValidCommands.DELETE: lambda cmd: self.storage.delete(cmd.key),
            ValidCommands.EXISTS: lambda cmd: self.storage.exists(cmd.key)
        }
        
        handler = command_handlers.get(parsed_command.type)
        if not handler:
            raise ValueError(f"Unsupported command: {parsed_command.type}")
        
        result = handler(parsed_command)
        return {"action": True, "message": result}
    
    def process_command(self, command: str) -> Dict[str, Any]:
        try:
            parsed_command = self.command_line_parser(command)
            return self.execute_command(parsed_command)
        except Exception as e:
            return {"action": False, "message": str(e)}


def run_cli():
    redis = RedisCommandParser()
    print("Welcome to Redis CLI!")
    print("Available commands: SET, GET, DELETE, EXISTS")
    print("Example: SET mykey myvalue")
    print("Type 'exit' to quit")
    
    while True:
        try:
            command = input("\nredis> ").strip()
            if command.lower() == 'exit':
                print("Goodbye!")
                break
                
            if not command:
                continue
                
            result = redis.process_command(command)
            if result["action"]:
                print(result["message"])
            else:
                print(f"Error: {result['message']}")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    run_cli()