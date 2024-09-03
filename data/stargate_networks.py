class Network:
    def __init__(self,
                 name: str,
                 endpointId: int,
                 poolNative: str,
                 ):
        self.name = name
        self.endpointId = endpointId
        self.poolNative = poolNative

    def __str__(self):
        return f'{self.name}'

Etherium = Network(
    name='etherium',
    endpointId=30101,
    poolNative='0x77b2043768d28E9C9aB44E1aBfC95944bcE57931'
)

Arbitrum = Network(
    name='arbitrum',
    endpointId=30110,
    poolNative='0xA45B5130f36CDcA45667738e2a258AB09f4A5f7F'
)

Optimism = Network(
    name='optimism',
    endpointId=30111,
    poolNative='0xe8CDF27AcD73a434D661C84887215F7598e7d0d3'
)