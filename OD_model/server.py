import mesa
from .model import State, simpleOD_Model


def network_portrayal(G):
    
    def node_color(agent):
        return {State.LOW: "#FF0000", State.HIGH: "#008000"}.get(agent.opinion_state, "#808080")

    def get_agents(source, target):
        return G.nodes[source]["agent"][0], G.nodes[target]["agent"][0]

    portrayal = {}
    portrayal["nodes"] = [
        {
            "size": 6,
            "color": node_color(agents[0]),
            "tooltip": f"id: {agents[0].unique_id}",
        }
        for (_, agents) in G.nodes.data("agent")
    ]

    portrayal["edges"] = [
        {
            "source": source,
            "target": target,
            "color": "#e8e8e8",
            "width": 2,
        }
        for (source, target) in G.edges
    ]

    return portrayal


model_params = {
    "N": mesa.visualization.Slider("Number of agents", 10, 10, 100, 10),
    "avg_node_degree": mesa.visualization.Slider("Avg Node Degree", 3, 3, 8, 1),
    "opinion_update_prob": mesa.visualization.Slider("Opinion Upodate Probability", 0.3, 0.0, 1.0, 0.1),
}

network = mesa.visualization.NetworkModule(network_portrayal, 500, 500)

chart = mesa.visualization.ChartModule(
    [
        {"Label": "low", "Color": "#FF0000"},
        {"Label": "high", "Color": "#008000"},
    ] 
)

server = mesa.visualization.ModularServer(
    simpleOD_Model,
    [network, chart],
    "Simple OD Model",
    model_params,
)
server.port = 8521