import mesa
from .model import opinionsModel
# from .agent import State

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# def add_colorbar():
#     fig, ax = plt.subplots(figsize=(10, 0.4))
#     norm = plt.Normalize(0, 1)
#     cmap = plt.get_cmap("viridis")
#     sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
#     sm.set_array([])
#     cb = plt.colorbar(sm, cax=ax, orientation='horizontal')
#     cb.set_label('Opinion Values')
    # plt.show()

def network_portrayal(G):
    
    def node_color(agent):
        # return {State.LOW: "#FF0000", State.HIGH: "#008000"}.get(agent.opinion_state, "#808080")

        # Define a gradient from red to green
        cmap = plt.get_cmap("viridis")
        
        # Map the normalized opinion to a color in the gradient
        rgba_color = cmap(agent.opinion)
        
        # Convert RGBA tuple to hex color code
        hex_color = mcolors.rgb2hex(rgba_color)
    
        return hex_color
    

    def get_agents(source, target):
        return G.nodes[source]["agent"][0], G.nodes[target]["agent"][0]

    portrayal = {}
    portrayal["nodes"] = [
        {
            "size": 6,
            "color": node_color(agents[0]),
            "tooltip": f"id: {agents[0].unique_id} , op: {round(agents[0].opinion, 3)}",
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


# def get_convergence_spead(model):
#     if model.get_current_step() is not None:
#         conv_spead = str(model.get_current_step())
#         return "Opinions Convergence Spead: {} steps.".format(conv_spead)
#     else:
#         return ""
    
def opinion_avg(model):
    avg = sum(a.opinion for a in model.grid.get_all_cell_contents()) / model.num_agents
    return "Opinions Average: {}.".format(round(avg, 4))

    
model_params = {
    "N": mesa.visualization.Slider("Number of agents", 50, 10, 100, 50),
    # "avg_node_degree": mesa.visualization.Slider("Avg Node Degree", 5, 3, 8, 1),
    # "update_opinion_prob": mesa.visualization.Slider("Opinion Upodate Probability", 0.3, 0.0, 1.0, 0.1),
    "inst_info": mesa.visualization.Slider("institution Information", 0.5, 0.0, 1.0, 0.1),
}

network = mesa.visualization.NetworkModule(network_portrayal, 500, 650)

# chart_count = mesa.visualization.ChartModule(
#     [
#         {"Label": "low", "Color": "#FF0000"},
#         {"Label": "high", "Color": "#008000"},
#     ] 
# )

chart_op_avg = mesa.visualization.ChartModule(
    [{"Label": "op_avg", "Color": "#bdd203"},],
    data_collector_name='datacollector' 
)


server = mesa.visualization.ModularServer(
    opinionsModel,
    [network, opinion_avg, chart_op_avg],
    "Opinion Dynamics Model",
    model_params,
)
server.port = 8521
