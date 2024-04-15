import random

# Define the Bayesian Network class
class BayesianNetwork:
    def __init__(self):
        self.nodes = {}
    
    # Add a node to the network
    def add_node(self, name, states, parents=None, cpt=None):
        if parents is None:
            parents = []
        if cpt is None:
            cpt = {}
        self.nodes[name] = {'states': states, 'parents': parents, 'cpt': cpt}
    
    # Calculate the probability of a node given its parents' states
    def probability(self, node, parent_states):
        cpt = self.nodes[node]['cpt']
        key = tuple(parent_states[parent] for parent in self.nodes[node]['parents'])
        return cpt[key]
    
    # Sample a state for a node given its parents' states
    def sample(self, node, parent_states):
        p = random.random()
        cumulative_prob = 0
        states = self.nodes[node]['states']
        for state in states:
            cumulative_prob += self.probability(node, parent_states + [state])
            if p <= cumulative_prob:
                return state
    
    # Sample states for all nodes
    def sample_states(self):
        sampled_states = {}
        for node in self.nodes:
            parents = self.nodes[node]['parents']
            parent_states = [sampled_states[parent] for parent in parents]
            sampled_states[node] = self.sample(node, parent_states)
        return sampled_states

# Define conditional probability tables (CPTs)
study_cpt = {
    (): [0.2, 0.6, 0.2]  # P(Study Time)
}
sleep_cpt = {
    (): [0.3, 0.5, 0.2]  # P(Sleep Quality)
}
stress_cpt = {
    (): [0.3, 0.5, 0.2]  # P(Stress Level)
}
exam_cpt = {
    ('Low', 'Low', 'Low'): [0.8, 0.15, 0.05],     # P(Exam Difficulty | Study, Sleep, Stress)
    ('Low', 'Low', 'Medium'): [0.7, 0.2, 0.1],
    ('Low', 'Low', 'High'): [0.6, 0.3, 0.1],
    ('Low', 'Medium', 'Low'): [0.7, 0.2, 0.1],
    ('Low', 'Medium', 'Medium'): [0.6, 0.3, 0.1],
    ('Low', 'Medium', 'High'): [0.5, 0.35, 0.15],
    ('Low', 'High', 'Low'): [0.6, 0.3, 0.1],
    ('Low', 'High', 'Medium'): [0.5, 0.35, 0.15],
    ('Low', 'High', 'High'): [0.4, 0.4, 0.2],
    ('Medium', 'Low', 'Low'): [0.7, 0.2, 0.1],
    ('Medium', 'Low', 'Medium'): [0.6, 0.3, 0.1],
    ('Medium', 'Low', 'High'): [0.5, 0.35, 0.15],
    ('Medium', 'Medium', 'Low'): [0.6, 0.3, 0.1],
    ('Medium', 'Medium', 'Medium'): [0.5, 0.35, 0.15],
    ('Medium', 'Medium', 'High'): [0.4, 0.4, 0.2],
    ('Medium', 'High', 'Low'): [0.5, 0.35, 0.15],
    ('Medium', 'High', 'Medium'): [0.4, 0.4, 0.2],
    ('Medium', 'High', 'High'): [0.3, 0.5, 0.2],
    ('High', 'Low', 'Low'): [0.6, 0.3, 0.1],
    ('High', 'Low', 'Medium'): [0.5, 0.35, 0.15],
    ('High', 'Low', 'High'): [0.4, 0.4, 0.2],
    ('High', 'Medium', 'Low'): [0.5, 0.35, 0.15],
    ('High', 'Medium', 'Medium'): [0.4, 0.4, 0.2],
    ('High', 'Medium', 'High'): [0.3, 0.5, 0.2],
    ('High', 'High', 'Low'): [0.4, 0.4, 0.2],
    ('High', 'High', 'Medium'): [0.3, 0.5, 0.2],
    ('High', 'High', 'High'): [0.2, 0.6, 0.2],
}
health_cpt = {
    ('Low',): [0.1, 0.6, 0.3],     # P(Health | Stress Level)
    ('Medium',): [0.3, 0.5, 0.2],
    ('High',): [0.5, 0.4, 0.1],
}
motivation_cpt = {
    ('Low', 'Low'): [0.1, 0.6, 0.3],    # P(Motivation | Stress Level, Sleep Quality)
    ('Low', 'Medium'): [0.2, 0.6, 0.2],
    ('Low', 'High'): [0.3, 0.5, 0.2],
    ('Medium', 'Low'): [0.2, 0.6, 0.2],
    ('Medium', 'Medium'): [0.3, 0.5, 0.2],
    ('Medium', 'High'): [0.4, 0.4, 0.2],
    ('High', 'Low'): [0.3, 0.5, 0.2],
    ('High', 'Medium'): [0.4, 0.4, 0.2],
    ('High', 'High'): [0.5, 0.3, 0.2],
}
distraction_cpt = {
    ('Low',): [0.7, 0.2, 0.1],    # P(External Distractions)
    ('Medium',): [0.5, 0.3, 0.2],
    ('High',): [0.3, 0.5, 0.2],
}
caffeine_cpt = {
    ('Low',): [0.3, 0.5, 0.2],    # P(Caffeine Intake)
    ('Medium',): [0.5, 0.4, 0.1],
    ('High',): [0.7, 0.2, 0.1],
}
nutrition_cpt = {
    ('Low',): [0.2, 0.6, 0.2],    # P(Nutrition)
    ('Average',): [0.5, 0.4, 0.1],
    ('Good',): [0.8, 0.15, 0.05],
}
social_cpt = {
    ('Low',): [0.3, 0.5, 0.2],    # P(Social Life)
    ('Medium',): [0.5, 0.4, 0.1],
    ('High',): [0.7, 0.2, 0.1],
}

# Initialize Bayesian Network
bn = BayesianNetwork()

# Add nodes to the network with their CPTs
bn.add_node('Study Time', ['Low', 'Medium', 'High'], cpt=study_cpt)
bn.add_node('Sleep Quality', ['Low', 'Medium', 'High'], cpt=sleep_cpt)
bn.add_node('Stress Level', ['Low', 'Medium', 'High'], cpt=stress_cpt)
bn.add_node('Exam Difficulty', ['Easy', 'Medium', 'Hard'], parents=['Study Time', 'Sleep Quality', 'Stress Level'], cpt=exam_cpt)
bn.add_node('Health', ['Good', 'Okay', 'Poor'], parents=['Stress Level'], cpt=health_cpt)
bn.add_node('Motivation', ['Low', 'Medium', 'High'], parents=['Stress Level', 'Sleep Quality'], cpt=motivation_cpt)
bn.add_node('External Distractions', ['Low', 'Medium', 'High'], cpt=distraction_cpt)
bn.add_node('Caffeine Intake', ['Low', 'Medium', 'High'], cpt=caffeine_cpt)
bn.add_node('Nutrition', ['Poor', 'Average', 'Good'], cpt=nutrition_cpt)
bn.add_node('Social Life', ['Low', 'Medium', 'High'], cpt=social_cpt)

# Sample states for all nodes
sampled_states = bn.sample_states()

# Print sampled states
for node, state in sampled_states.items():
    print(f"{node}: {state}")
