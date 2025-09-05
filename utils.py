# Fichier Utils referencement des fonctions 
import pandas as pd

# Fonction pour ne prendre que la data et pas l'entete du json apres le call API en GraphQL
def find_first_list(data_dict):
    """
    Recherche la première liste de dictionnaires dans un dictionnaire imbriqué.
    Utile pour les réponses d'API avec une structure flexible.
    """
    for key, value in data_dict.items():
        if isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
            return value
        if isinstance(value, dict):
            result = find_first_list(value)
            if result is not None:
                return result
    return None

# Fonction recursive pour sortir les jsons des jsons ahahahha ^^


def flatten_node_data(data): 
    all_data = [] 
    
    for item in data: 
        node_data = item['node'] 
        # Normalize the teams list 

        df_teams = pd.json_normalize(node_data['teams']) 

        #  Add parent info (node ID and name) 
        df_teams['node.id'] = node_data['id'] 
        df_teams['node.name'] = node_data['name'] 
        all_data.append(df_teams) 
        # Check for nested nodes and recurse 
        if 'next_node' in node_data and node_data['next_node']: 
            # Create a temporary list to hold the next node for the recursive call 
            next_node_data = [{'node': node_data['next_node']}] 
            all_data.append(flatten_node_data(next_node_data))
            # Concatenate all the individual DataFrames 
        
    return pd.concat(all_data, ignore_index=True)

