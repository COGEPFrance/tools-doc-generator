class NodeIdGenerator:
    @staticmethod
    def generate(value: str) -> str:
        return value.replace(".", "_").replace("-", "_")
