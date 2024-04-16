import random
import itertools

# Define the Bayesian Network class
class BayesianNetwork:
    def __init__(self):
        self.nodes = {}
    
    # Add a node to the network
    def add_node(self, name, states, cpt, parents=[]):

        # Check if the node already exists in the network
        if name in self.nodes:
            print(f"Node '{name}' already exists in the network.")
            return
        
        # Check if the node has at least one state
        if len(states) == 0:
            print(f"Node '{name}' must have at least one state.")
            return
        
        # Check if all parent nodes exist in the network
        for parent in parents:
            if parent not in self.nodes:
                print(f"Parent node '{parent}' does not exist in the network.")
                return

        # Check if the CPT is valid
        for parent_combination in itertools.product(*[self.nodes[parent]['states'] for parent in parents]):
            if parent_combination not in cpt or len(cpt[parent_combination]) != len(states) or sum(cpt[parent_combination]) != 1:
                print(f"Invalid CPT for node '{name}'.")
                return
            print(f"Valid CPT for node '{name}'. Combination: {parent_combination} -> {cpt[parent_combination]}")

        self.nodes[name] = {'states': states, 'parents': parents, 'cpt': cpt}
    
    # Calculate the probability of a state of a node given its parents' states
    def probability(self, node, parent_states, state):
        states = self.nodes[node]['states']
        return self.nodes[node]['cpt'][parent_states][states.index(state)]
    
    # Sample a state for a node given its parents' states
    def sample(self, node, parent_states):
        print('sampling node:', node, 'with parent states:', parent_states, '...')
        p = random.random()
        cumulative_prob = 0
        states = self.nodes[node]['states']
        for state in states:
            probability = self.probability(node, parent_states, state)
            cumulative_prob += probability
            if p <= cumulative_prob:
                return state, probability
    
    # Sample states for all nodes
    def sample_states(self):
        sampled_states = {}
        joint_probability = 1
        for node in self.nodes:
            parents = self.nodes[node]['parents']
            parent_states = tuple(sampled_states[parent] for parent in parents)
            sampled_states[node], probaility = self.sample(node, parent_states)
            joint_probability *= probaility
        return sampled_states, joint_probability

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
    (): [0.7, 0.2, 0.1]    # P(External Distractions)
}
caffeine_cpt = {
    (): [0.3, 0.5, 0.2]    # P(Caffeine Intake)
}
nutrition_cpt = {
    (): [0.2, 0.6, 0.2]    # P(Nutrition)
}
social_cpt = {
    (): [0.3, 0.5, 0.2]    # P(Social Life)
}

print("Bayesian Network for Student Performance Prediction\n")

# Initialize Bayesian Network
bn = BayesianNetwork()

# Add nodes to the network with their CPTs
bn.add_node('Study Time', ['Low', 'Medium', 'High'], cpt=study_cpt)
bn.add_node('Sleep Quality', ['Low', 'Medium', 'High'], cpt=sleep_cpt)
bn.add_node('Stress Level', ['Low', 'Medium', 'High'], cpt=stress_cpt)
bn.add_node('Exam Difficulty', ['Easy', 'Medium', 'Hard'], cpt=exam_cpt, parents=['Study Time', 'Sleep Quality', 'Stress Level'])
bn.add_node('Health', ['Good', 'Okay', 'Poor'], cpt=health_cpt, parents=['Stress Level'])
bn.add_node('Motivation', ['Low', 'Medium', 'High'], cpt=motivation_cpt, parents=['Stress Level', 'Sleep Quality'])
bn.add_node('External Distractions', ['Low', 'Medium', 'High'], cpt=distraction_cpt)
bn.add_node('Caffeine Intake', ['Low', 'Medium', 'High'], cpt=caffeine_cpt)
bn.add_node('Nutrition', ['Poor', 'Average', 'Good'], cpt=nutrition_cpt)
bn.add_node('Social Life', ['Low', 'Medium', 'High'], cpt=social_cpt)

# Sample states for all nodes
sampled_states, joint_probability = bn.sample_states()

# Print sampled states
for node, state in sampled_states.items():
    print(f"{node}: {state}")

# Print joint probability
print(f"Joint Probability: {joint_probability}")