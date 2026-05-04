import numpy as np
import re
import pandas as pd
from itertools import product

def coef_attenuation(data):
    jugment_scale={'Equally':1,'A':2,'Strongly':3,'Extremely':4}
    alpha={'No expertise':0.1,'Beginner Level':0.3,'Intermediate Level':0.5,
        'Advanced Level':0.8,'Expert Level':1}
    list_of_value={}
    weight=[]
    expertise=[]
    #pandas_ahp_norm_list=[]
   
    for h in range(0,len(data['list_index'])): 
        list_of_value=[]
        expertise.append(alpha[data['expertise_leve'][h]])
 
    return expertise

def weight_list(data):
    jugment_scale={'Equally':1,'A':2,'Strongly':3,'Extremely':4}
    alpha={'No expertise':0.1,'Beginner Level':0.3,'Intermediate Level':0.5,
        'Advanced Level':0.8,'Expert Level':1}
    list_of_value={}
    weight=[]
    expertise=[]
    #pandas_ahp_norm_list=[]
    if len(data['columns_name'])==12:   
        for h in range(0,len(data['list_index'])): 
            list_of_value=[]
            expertise.append(alpha[data['expertise_leve'][h]])
            expet=alpha[data['expertise_leve'][h]]
            for colums_index in range(4,10):
                filtre_columns=data['data'].iloc[h, colums_index]  # question response values
                list_of_filtre=filtre_columns
                value_comparer=re.findall(r'\[([^\]]+)\]',data['data'].iloc[:,colums_index].name)[0].lower()  # declared comparison subject
                if value_comparer in list_of_filtre:  # inverse scale if focus term is in the answer
                    list_of_value.append(1/(jugment_scale[list_of_filtre.split()[0]]))
                else:
                    list_of_value.append(1*jugment_scale[list_of_filtre.split()[0]])

            
            matrix_ahp=[[1]+list_of_value[:3],
            [round(1/list_of_value[0],2)]+[1]+list_of_value[3:5],
            [round(1/list_of_value[1],2),round(1/list_of_value[3],2)]+[1]+[list_of_value[5]],
            [round(1/list_of_value[2],2),round(1/list_of_value[4],2),round(1/list_of_value[5],2)]+[1]]
            matrix_ahp=1*np.array(matrix_ahp)
            # --- value names ---

            nom_value=[]
            for i in data['columns_name'][:4]:
                nom_value.append(re.findall(r'\[([^\]]+)\]',i)[0].lower())


            # --- pairwise matrix as DataFrame ---

            pandas_ahp=pd.DataFrame(matrix_ahp, columns=nom_value, index=nom_value)
            pandas_ahp_norm=pd.DataFrame( np.array(matrix_ahp) / np.array(matrix_ahp).sum(axis=0), columns=nom_value, index=nom_value)
            eigenvalues, eigenvectors =np.linalg.eig(np.array(matrix_ahp)/expet)
            CI_value=(max(eigenvalues)-len(matrix_ahp))/(len(matrix_ahp)-1)
            CR_value=CI_value/0.9
            #print(pandas_ahp)
            
            weight.append(ahp_normalisation_poids_matrice(np.array(matrix_ahp)))
            
        return weight
    #return pd.DataFrame(data={"weight":apply_betP_test(weight)},index=nom_value)#pd.DataFrame(data={"weight":apply_betP_test(weight)},index=nom_value)#expertise,matrix_ahp,ahp_normalisation_poids_matrice(np.array(matrix_ahp)),nom_value,pandas_ahp,pandas_ahp_norm,CR_value
    
    else:
        for h in range(0,len(data['list_index'])): 
            list_of_value=[]
            expertise.append(alpha[data['expertise_leve'][h]])
            expet=alpha[data['expertise_leve'][h]]
            for colums_index in range(5,15):
                filtre_columns=data['data'].iloc[h, colums_index]  # question response values
                list_of_filtre=filtre_columns
                value_comparer=re.findall(r'\[([^\]]+)\]',data['data'].iloc[:,colums_index].name)[0].lower()  # declared comparison subject
                if value_comparer in list_of_filtre:  # inverse scale if focus term is in the answer
                    list_of_value.append(1/(jugment_scale[list_of_filtre.split()[0]]))
                else:
                    list_of_value.append(1*jugment_scale[list_of_filtre.split()[0]])

            
            matrix_ahp=[[1]+list_of_value[:4],
            [round(1/list_of_value[0],2)]+[1]+list_of_value[4:7],
            [round(1/list_of_value[1],2),round(1/list_of_value[4],2)]+[1]+list_of_value[7:9],
            [round(1/list_of_value[2],2),round(1/list_of_value[5],2),round(1/list_of_value[7],2)]+[1]+[list_of_value[9]],
            [round(1/list_of_value[3],2),round(1/list_of_value[6],2),round(1/list_of_value[8],2),round(1/list_of_value[9],2)]+[1]]
            matrix_ahp=np.array(matrix_ahp)
            # --- value names ---

            nom_value=[]
            for i in data['columns_name'][:5]:
                nom_value.append(re.findall(r'\[([^\]]+)\]',i)[0].lower())


            # --- pairwise matrix as DataFrame ---

            pandas_ahp=pd.DataFrame(matrix_ahp, columns=nom_value, index=nom_value)
            pandas_ahp_norm=pd.DataFrame( np.array(matrix_ahp) / np.array(matrix_ahp).sum(axis=0), columns=nom_value, index=nom_value)
            eigenvalues, eigenvectors =np.linalg.eig(matrix_ahp)
            CI_value=(max(eigenvalues)-len(matrix_ahp))/(len(matrix_ahp)-1)
            CR_value=CI_value/1.2
            #print(pandas_ahp)
            #weight.append(ahp_normalisation_poids_matrice(np.array(matrix_ahp)))
            weight.append(ahp_normalisation_poids_matrice(np.array(matrix_ahp)))
  

        return weight
    #return pd.DataFrame(data={"weight":apply_betP_test(weight)},index=nom_value)
def ahp_normalisation_poids_matrice(matrix):
    """
    Run the Analytic Hierarchy Process (AHP) normalization step.

    Args:
        matrix: Pairwise comparison matrix.

    Returns:
        Normalized weight vector (row averages of the normalized matrix).
    """
    # Normalize columns of the pairwise comparison matrix
    normalized_matrix = matrix / matrix.sum(axis=0)

    # Row averages as weights
    row_average = normalized_matrix.mean(axis=1)

    

    return row_average


### Group close values (tolerance-based merging)
def inverser_dictionnaire(dictionnaire, tolerance):
    groupes_valeurs = {}  # index groups -> representative value

    for indice, valeur in dictionnaire.items():
        # Try to merge with an existing group within tolerance
        ajouté = False
        for groupes_indices, ref_valeur in groupes_valeurs.items():
            if (1 - tolerance) * ref_valeur <= valeur <= (1 + tolerance) * ref_valeur:
                # Extend group and average member values
                nouveaux_indices = groupes_indices + (indice,)
                ref_valeur=[]
                for index in list(nouveaux_indices):
                    ref_valeur.append(dictionnaire[index])  # average over grouped indices
                groupes_valeurs[nouveaux_indices] = sum(ref_valeur)/len(ref_valeur)
                del groupes_valeurs[groupes_indices]  # drop old key before re-insert
                ajouté = True
                break
        
        if not ajouté:
            # New singleton group
            groupes_valeurs[(indice,)] = valeur

    return groupes_valeurs
def betP_test(weight_1,weight_2,expertise_1,expertise_2):
    ##### First weight #######

    a=list(weight_1*(expertise_1))
    a.append(1-sum(weight_1)*(expertise_1))
    weight_bis_0=np.array(a)

    ##### Second weight #######
    b=list(weight_2*(expertise_2))
    b.append(1-sum(weight_2)*(expertise_2))
    weight_bis_1=np.array(b)

    ##### BetP mix without full frame mass
    table_dempster_sans=[]
    sum_a=[]
    for j in range(0,len(weight_list_value[1])):
        weight_0_normal=weight_1*(expertise_1)
        weight_1_normal=weight_2*(expertise_2)
        b=weight_0_normal*weight_1_normal[j]
        table_dempster_sans.append(b)

    empty_answer=[]
    for i in range(0,len(table_dempster_sans)):
        empty_answer+=list(np.delete(table_dempster_sans[i], i, 0))
    K=1/(1-sum(empty_answer))

    ##### BetP mix with full frame mass
    table_dempster=[]

    for j in range(0,len(weight_bis_1)):
        b=np.array(weight_bis_0)*weight_bis_1[j]
        sum_a.append(b)
        table_dempster.append(b)

    table_dempster_norm=table_dempster#/sum(sum(sum_a))

    ###### Combined values
    values=[]
    for i in range(0,len(table_dempster_norm)-1):
        sum_ma=table_dempster_norm[i][i]+table_dempster_norm[i][-1]+table_dempster_norm[len(table_dempster_norm)-1][i]+table_dempster_norm[len(table_dempster_norm)-1][-1]/len(weight_list_value)
        values.append(sum_ma)

    new_betP=K*np.array(values)
    return new_betP,table_dempster_norm

def apply_betP_test(weights):
    result = weights[-1]
    for weight in reversed(weights[:-1]):
        result = betP_test(weight, result)
    return result

#### On creer le dictionnaire des reponses modifier
def dictionaire_reponse_belied(weight,poids): #### On faite on va rassemble les valeurs communes
    weight_1_dict={}
    tuple_anwser=[]
    for i in range(0,len(weight)):
        weight_1_dict[i+1]=weight[i]*poids 
        tuple_anwser.append(i+1)

    nouveau_weight_1_dict = inverser_dictionnaire(weight_1_dict, tolerance=0.05) ### #Rassemblement les valeurs
    nouveau_weight_1_dict[tuple(tuple_anwser)]=1-sum(weight*poids) #### On creer le dictionnaire des reponse modifier
    return nouveau_weight_1_dict

def dictionaire_reponse_belief_sans(weight,poids): #### On faite on va rassemble les valeurs communes
    weight_1_dict={}
    tuple_anwser=[]
    for i in range(0,len(weight)):
        weight_1_dict[i+1]=weight[i]*poids 
        tuple_anwser.append(i+1)

    nouveau_weight_1_dict = inverser_dictionnaire(weight_1_dict, tolerance=-0.01) ### #Rassemblement les valeurs
    nouveau_weight_1_dict[tuple(tuple_anwser)]=1-sum(weight*poids) #### On creer le dictionnaire des reponse modifier
    return nouveau_weight_1_dict

from collections import defaultdict

def multiply_dicts(dict1, dict2):
    result = defaultdict(float)

    # Multiply matching entries across the two dicts
    for key1, value1 in dict1.items():
        for key2, value2 in dict2.items():
            # Produit des valeurs
            product_value = value1 * value2

            # Shared key (intersection)
            common_key = tuple(set(key1) & set(key2))

            # Accumulate product into result
            if len(common_key)>0:
                result[common_key] += product_value/len(common_key)
            else:
                result[common_key] += product_value
    # Add keys that appear in only one dict
   
    return result

def all_multiply_dicts(weight_list_value,coef_att):
    for i in range(1,len(weight_list_value)):
        if i==1:
            test_a=multiply_dicts(dictionaire_reponse_belied(weight_list_value[i-1],coef_att[i-1]), dictionaire_reponse_belied(weight_list_value[i],coef_att[i]))
        else:
            test_a=multiply_dicts(test_a, dictionaire_reponse_belied(weight_list_value[i],coef_att[i]))
            
    return test_a
    
def all_multiply_sans(weight_list_value,coef_att):
    for i in range(1,len(weight_list_value)):
        if i==1:
            test_a=multiply_dicts(dictionaire_reponse_belief_sans(weight_list_value[i-1],coef_att[i-1]), dictionaire_reponse_belief_sans(weight_list_value[i],coef_att[i]))
        else:
            test_a=multiply_dicts(test_a, dictionaire_reponse_belief_sans(weight_list_value[i],coef_att[i]))
            
    return test_a
    
def fusion_response(data): 
    weight_list_value=weight_list(data) ### Weight of criterias by expert
    coef_att=coef_attenuation(data) #### Weight of the expert
    if len(data['columns_name'])==12: 
        nom_value=[]
        for i in data['columns_name'][:4]:
            nom_value.append(re.findall(r'\[([^\]]+)\]',i)[0].lower())
    else:
        nom_value=[]
        for i in data['columns_name'][:5]:
            nom_value.append(re.findall(r'\[([^\]]+)\]',i)[0].lower())
            
        


    # Multiplication des dictionnaires
    result_dict = all_multiply_dicts(weight_list_value,coef_att)
    if sum(result_dict.values())==0:
        result_dict= all_multiply_sans(weight_list_value,coef_att)
    dictionaire_fusion={}
    for i in range(0,len(list(result_dict.keys())[-1])):
        dictionaire_fusion[(i+1,)]=[]


    dictionaire_fusion.items()

    aggregate_dict = defaultdict(float)

    # Aggregate values by key length
    for key_1 in dictionaire_fusion.keys():
        for key_2, value_2 in result_dict.items():
            if len(tuple(set(key_1) & set(key_2)))==1:
                aggregate_dict[key_1] += value_2

    for key_1 in aggregate_dict:
        dictionaire_fusion[key_1]=aggregate_dict[key_1]/(1-result_dict[()])
    
    return pd.DataFrame(data={"weight":np.array(list(dictionaire_fusion.values()))/sum(list(dictionaire_fusion.values()))},index=nom_value)

# --- Part 2 comparisons ---
def fusion_response_simple(data):
    expertise=[]
    weight=[]
    jugment_scale={'Equality':1,'A':2,'Strongly':3,'Extremely':4}
    alpha={'No expertise':0.1,'Beginner Level':0.3,'Intermediate Level':0.5,
        'Advanced Level':0.8,'Expert Level':1}
    
    for h in range(0,len(data['data'])): 
        filtre_columns=data['data'].iloc[h, -2]
        list_of_filtre=filtre_columns
        value_comparer=data['name_comparaison_2']
        list_of_value=[]
        expertise.append(alpha[data['expertise_leve'][h]])
        expet=alpha[data['expertise_leve'][h]]

        if 'T-Intersection' in data['name_comparaison_2']:
            if value_comparer[0] in list_of_filtre:
                list_of_value.append(jugment_scale[list_of_filtre.split()[0]])
            elif 'Congested' in list_of_filtre:
                list_of_value.append(1/jugment_scale[list_of_filtre.split()[0]])
            else:
                list_of_value.append(1)

        else:
        
            if value_comparer[0] in list_of_filtre:  # inverse scale if focus term is in the answer
                list_of_value.append(jugment_scale[list_of_filtre.split()[0]])
            elif value_comparer[1] in list_of_filtre:
                list_of_value.append(1/jugment_scale[list_of_filtre.split()[0]])
            else:
                list_of_value.append(1)


        # --- AHP pairwise matrix (2x2) ---
        matrix_ahp=[[1,list_of_value[0]],[1/list_of_value[0],1]]

        # --- value names ---
        nom_value=value_comparer

        # --- pairwise matrix as DataFrame ---

        pandas_ahp=pd.DataFrame(matrix_ahp, columns=nom_value, index=nom_value)
        pandas_ahp_norm=pd.DataFrame( np.array(matrix_ahp) / np.array(matrix_ahp).sum(axis=0), columns=nom_value, index=nom_value)
        eigenvalues, eigenvectors =np.linalg.eig(matrix_ahp)
        CI_value=(max(eigenvalues)-len(matrix_ahp))/(len(matrix_ahp)-1)
        CR_value=CI_value/0.9
       
        weight.append(ahp_normalisation_poids_matrice(np.array(matrix_ahp)))
    
    result_dict = all_multiply_dicts(weight,expertise)
    if sum(result_dict.values())==0:
        result_dict= all_multiply_sans(weight,expertise)
    dictionaire_fusion={}
    for i in range(0,len(list(result_dict.keys())[-1])):
        dictionaire_fusion[(i+1,)]=[]


    dictionaire_fusion.items()

    aggregate_dict = defaultdict(float)

    # Aggregate values by key length
    for key_1 in dictionaire_fusion.keys():
        for key_2, value_2 in result_dict.items():
            if len(tuple(set(key_1) & set(key_2)))==1:
                aggregate_dict[key_1] += value_2

    for key_1 in aggregate_dict:
        dictionaire_fusion[key_1]=aggregate_dict[key_1]/(1-result_dict[()])
    
    return pd.DataFrame(data={"weight":np.array(list(dictionaire_fusion.values()))/sum(list(dictionaire_fusion.values()))},index=nom_value)

def fusion_response_extra(data):
    jugment_scale={'Equality':1,'A':2,'Strongly':3,'Extremely':4}
    alpha={'No expertise':0.1,'Beginner Level':0.3,'Intermediate Level':0.5,
            'Advanced Level':0.8,'Expert Level':1}
    new_data=data.iloc[:,-5:-1].dropna()
    expertise_name=list(data.loc[list(new_data.index)].iloc[:,1])
    expertise=[alpha[i] for i in list(data.loc[list(new_data.index)].iloc[:,1])]

    value_a_comparer=[['highway','urban'],['car-following','lane-chaning'],['free-flow','congestioned-flow'],['straight','turn']]
    pandas_all=[]
    for i in range(0,len(new_data.columns)):
        weight=[]
        value_comparer=value_a_comparer[i]
        for h in range(0,len(new_data)): 
            filtre_columns=new_data.iloc[h, i]
            list_of_filtre=filtre_columns
            list_of_value=[]
            if value_comparer[0] in list_of_filtre:  # inverse scale if focus term is in the answer
                list_of_value.append(jugment_scale[list_of_filtre.split()[0]])
            elif value_comparer[1] in list_of_filtre:
                list_of_value.append(1/jugment_scale[list_of_filtre.split()[0]])
            else:
                list_of_value.append(1)

            matrix_ahp=[[1,list_of_value[0]],[1/list_of_value[0],1]]
            nom_value=value_comparer
            weight.append(ahp_normalisation_poids_matrice(np.array(matrix_ahp)))
        result_dict = all_multiply_dicts(weight,expertise)
        if sum(result_dict.values())==0:
            result_dict= all_multiply_sans(weight,expertise)
        dictionaire_fusion={}
        for i in range(0,len(list(result_dict.keys())[-1])):
            dictionaire_fusion[(i+1,)]=[]


        dictionaire_fusion.items()

        aggregate_dict = defaultdict(float)

        # Aggregate values by key length
        for key_1 in dictionaire_fusion.keys():
            for key_2, value_2 in result_dict.items():
                if len(tuple(set(key_1) & set(key_2)))==1:
                    aggregate_dict[key_1] += value_2

        for key_1 in aggregate_dict:
            dictionaire_fusion[key_1]=aggregate_dict[key_1]/(1-result_dict[()])

        pandas_all.append(pd.DataFrame(data={"weight":np.array(list(dictionaire_fusion.values()))/sum(list(dictionaire_fusion.values()))},index=nom_value))
    return pandas_all
            

##### Pour les taux de confiences de simulatioon :


def confidence_by_scenario_ponderation(data):
    jugment_scale_bis={'Not':0,'Low':0.25,'Moderately':0.5,'Strongly':0.75,'Extermely':1}
    alpha={'No expertise':0,'Beginner Level':0.3,'Intermediate Level':0.5,
    'Advanced Level':0.75,'Expert Level':1}
    if 'Stop' in data['columns_name'][0]:
        value_justement=[]
        expertise=[]
        value_justement_layer_2=[]
        expertise_layer_2=[]
        for h in range(0,len(data['data'])): 
            filtre_columns=data['data'].iloc[h,:4]
            value_jugement_by_person=[]
            value_jugement_by_person_layer_2=[]
            
            for i in range(0,len(filtre_columns)):
                if i==0 or i==3:
                    value_jugement_by_person_layer_2.append(jugment_scale_bis[filtre_columns.iloc[i].split()[0]])
                    

                else:

                    value_jugement_by_person.append(jugment_scale_bis[filtre_columns.iloc[i].split()[0]])

                    
            expertise.append(alpha[data['expertise_leve'][h]])
            expertise_layer_2.append(alpha[data['expertise_leve'][h]])
            value_justement.append(np.mean(value_jugement_by_person))
            value_justement_layer_2.append(np.mean(value_jugement_by_person_layer_2))
                    

        value_confidence=sum(np.array(value_justement)*np.array(expertise))/sum(expertise)
        value_confidence_2=sum(np.array(value_justement_layer_2)*np.array(expertise_layer_2))/sum(expertise_layer_2)
        return [value_confidence,value_confidence_2]
    elif 'Two-Lane' in data['columns_name'][0]:
        value_justement=[]
        expertise=[]
        value_justement_layer_3=[]
        expertise_layer_3=[]
        for h in range(0,len(data['data'])): 
            filtre_columns=data['data'].iloc[h,:4]
            value_jugement_by_person=[]
            value_jugement_by_person_layer_3=[]
            for i in range(0,len(filtre_columns)):
                if i==2 or i==3:
                
                    value_jugement_by_person_layer_3.append(jugment_scale_bis[filtre_columns.iloc[i].split()[0]])
                    
                    
                    

                else:
                    
                    value_jugement_by_person.append(jugment_scale_bis[filtre_columns.iloc[i].split()[0]])

                    
                    
            value_justement_layer_3.append(np.mean(value_jugement_by_person_layer_3))
            value_justement.append(np.mean(value_jugement_by_person))
            expertise.append(alpha[data['expertise_leve'][h]])
            expertise_layer_3.append(alpha[data['expertise_leve'][h]])


        value_confidence=sum(np.array(value_justement)*np.array(expertise))/sum(expertise)
        value_confidence_3=sum(np.array(value_justement_layer_3)*np.array(expertise_layer_3))/sum(expertise_layer_3)
        return [value_confidence,value_confidence_3]

    elif len(data['columns_name'])==12:
        value_justement=[]
        expertise=[]
        for h in range(0,len(data['data'])): 
            filtre_columns=data['data'].iloc[h,:4]
            value_jugement_by_person=[]
            for i in filtre_columns:
                value_jugement_by_person.append(jugment_scale_bis[i.split()[0]])

            value_justement.append(np.mean(value_jugement_by_person))
            expertise.append(alpha[data['expertise_leve'][h]])
        value_confidence=sum(np.array(value_justement)*np.array(expertise))/sum(expertise)
        return value_confidence

    else:
        value_justement=[]
        expertise=[]
        for h in range(0,len(data['data'])): 
            filtre_columns=data['data'].iloc[h,:5]
            value_jugement_by_person=[]
            for i in filtre_columns:
                value_jugement_by_person.append(jugment_scale_bis[i.split()[0]])

            value_justement.append(np.mean(value_jugement_by_person))
            expertise.append(alpha[data['expertise_leve'][h]])
        value_confidence=sum(np.array(value_justement)*np.array(expertise))/sum(expertise)
        return value_confidence
    



def value_layer(layer_5_4):

    debut = 0.5
    fin = .85
    #jugment_scale_intervale={'Equality':intervalles[0],'A':intervalles[1],'Strongly':intervalles[2],'Extremely':intervalles[3]}
    jugment_scale={'Equality':1,'A':2,'Strongly':3,'Extremely':4}
    
    # Calcul de la longueur de chaque intervalle
    longueur_interval = (fin - debut) / 4

    # List to collect intervals
    intervalles = []

    # Calcul des intervalles
    for i in range(4):
        if i!=3:
            intervalle_debut = debut + i * longueur_interval
            intervalle_fin = intervalle_debut + longueur_interval
            intervalles.append([intervalle_debut, intervalle_fin])
        else:
            intervalle_debut = debut + i * longueur_interval
            intervalle_fin = intervalle_debut + longueur_interval
            intervalles.append([intervalle_debut, 1.01])

    jugment_scale_intervale={'Equality':intervalles[0],'A':intervalles[1],'Strongly':intervalles[2],'Extremely':intervalles[3]}
    if layer_5_4<0.5:
        a=1-layer_5_4
        for i in range(0,len(intervalles)):
            if a >=intervalles[i][0] and a <intervalles[i][1]:
                value_comparaison=1/jugment_scale[list(jugment_scale_intervale.keys())[i]]

    else:
        a=layer_5_4
        for i in range(0,len(intervalles)):
            if a>=intervalles[i][0] and a <intervalles[i][1]:
                value_comparaison=jugment_scale[list(jugment_scale_intervale.keys())[i]]

    return value_comparaison



def confidence_by_sub_category_ponderation(data):
    jugment_scale_bis={'Not':0,'Low':0.25,'Moderately':0.5,'Strongly':0.75,'Extermely':1}
    alpha={'No expertise':0,'Beginner Level':0.3,'Intermediate Level':0.5,
    'Advanced Level':0.75,'Expert Level':1}
    if 'Plane' in data['columns_name'][0]:
        value_justement=[]
        expertise=[]
        value_justement_layer_2=[]
        expertise_layer_2=[]
        for h in range(0,len(data['data'])): 
            filtre_columns=data['data'].iloc[h,:4]
            value_jugement_by_person=[]
            value_jugement_by_person_layer_2=[]
            for i in range(0,len(filtre_columns)):
                if i==0 or i==1:
            
                    value_jugement_by_person_layer_2.append(jugment_scale_bis[filtre_columns.iloc[i].split()[0]])
                    
                else:
                    
                    value_jugement_by_person.append(jugment_scale_bis[filtre_columns.iloc[i].split()[0]])


            expertise.append(alpha[data['expertise_leve'][h]])
            value_justement.append(alpha[data['expertise_leve'][h]]*np.log(np.mean(value_jugement_by_person)))
            expertise_layer_2.append(alpha[data['expertise_leve'][h]])
            value_justement_layer_2.append(alpha[data['expertise_leve'][h]]*np.log(np.mean(value_jugement_by_person_layer_2)))

        value_confidence=np.exp(sum(value_justement)/sum(expertise))
        value_confidence_2=np.exp(sum(value_justement_layer_2)/sum(expertise_layer_2))
        return [value_confidence_2,value_confidence]
    
    elif 'Stop' in data['columns_name'][0]:
        value_justement=[]
        expertise=[]
        value_justement_layer_2=[]
        expertise_layer_2=[]
        for h in range(0,len(data['data'])): 
            filtre_columns=data['data'].iloc[h,:4]
            value_jugement_by_person=[]
            value_jugement_by_person_layer_2=[]
            for i in range(0,len(filtre_columns)):
                if i==2:
            
                    value_jugement_by_person_layer_2.append(jugment_scale_bis[filtre_columns.iloc[i].split()[0]])
                    
                elif i==1:
                    
                    value_jugement_by_person.append(jugment_scale_bis[filtre_columns.iloc[i].split()[0]])


            expertise.append(alpha[data['expertise_leve'][h]])
            value_justement.append(alpha[data['expertise_leve'][h]]*np.log(np.mean(value_jugement_by_person)))
            expertise_layer_2.append(alpha[data['expertise_leve'][h]])
            value_justement_layer_2.append(alpha[data['expertise_leve'][h]]*np.log(np.mean(value_jugement_by_person_layer_2)))

        value_confidence=np.exp(sum(value_justement)/sum(expertise))
        value_confidence_2=np.exp(sum(value_justement_layer_2)/sum(expertise_layer_2))
        return [value_confidence,value_confidence_2]
    

def normalize(dictionary):
    sum_value = sum(dictionary.values())
    
    normalized_dict = {}
    for key, value in dictionary.items():
        normalized_value = value  / sum_value
        normalized_dict[key] = normalized_value
    return normalized_dict


def ahp_belief(survey):
    data_survey = pd.read_csv(survey)
    data_survey=data_survey.iloc[2:]
    data_survey=data_survey.drop(25)

    ###### PREPROCEDING DES VALEURS DE L'AHP
    list_scenario={}
    list_scenario["Driver's Vision"]={'columns_name':data_survey.columns[3:15]}
    list_scenario["Driver's Vision"]['name_comparaison_2']=['cloudy','rainy']
    list_scenario['Sunny']={'columns_name':data_survey.columns[15:27]}
    list_scenario['Sunny']['name_comparaison_2']=['cloudy','Congestioned']
    list_scenario['Type of user']={'columns_name':data_survey.columns[27:44]}
    list_scenario['Type of user']['name_comparaison_2']=['T-Intersection','Congestioned']
    list_scenario['Intersection']={'columns_name':data_survey.columns[44:56]}
    list_scenario['Intersection']['name_comparaison_2']=['Stop','cycle lane']
    list_scenario['Specific Lane']={'columns_name':data_survey.columns[56:73]}
    list_scenario['Specific Lane']['name_comparaison_2']=['Curve Lane','Cycle lane']
    list_scenario['Exit']={'columns_name':data_survey.columns[73:85]}
    list_scenario['Exit']['name_comparaison_2']=['Divergent','congestion']
    list_scenario['Curved road']={'columns_name':data_survey.columns[85:97]}
    list_scenario['Curved road']['name_comparaison_2']=['Junction','Curve']

    choose_list=list(data_survey[data_survey.columns[2]].drop_duplicates())
    for i in choose_list:
        list_scenario[i]['list_index']=data_survey.index[data_survey[data_survey.columns[2]] == i].tolist() ### ON affecte chaque personne interroger
        list_scenario[i]['data']=data_survey.filter(items=list_scenario[i]['columns_name']).loc[data_survey.index[data_survey[data_survey.columns[2]] == i].tolist()]
        list_scenario[i]['expertise_leve']=list(data_survey[data_survey[data_survey.columns[2]] == i].iloc[:,1])
    #### Prendre les linges ou il y a 

    ##### PONDERATION DES VALEURS LES PLUS BASE DU QUESTIONNAIRE 

    pandas_weight_ponderer=[]
    pandas_weight_ponderer_2=[]
    confience_coef=[]
    for i in list_scenario:
        list_scenario[i]['result_comp_1']=fusion_response(list_scenario[i])
        pandas_weight_ponderer.append(fusion_response(list_scenario[i]))
        list_scenario[i]['result_comp_2']=fusion_response_simple(list_scenario[i])
        pandas_weight_ponderer_2.append(fusion_response_simple(list_scenario[i]))
        list_scenario[i]['confience']=confidence_by_scenario_ponderation(list_scenario[i])
        confience_coef.append(confidence_by_scenario_ponderation(list_scenario[i]))


    pandas_weight_ponderer_3=fusion_response_extra(data_survey)


    ######## VALEURS DE LA PARTIE DEUX


    list_scenario['Partie_2']={}
    list_scenario['Partie_2']['result_comp_1']=pandas_weight_ponderer_3[0]
    list_scenario['Partie_2']['result_comp_2']=pandas_weight_ponderer_3[1]
    list_scenario['Partie_2']['result_comp_3']=pandas_weight_ponderer_3[2]
    list_scenario['Partie_2']['result_comp_4']=pandas_weight_ponderer_3[3]


    ######### VALEURS DE CONFIDENCE 

    confidence_layer_5=(confience_coef[0]+confience_coef[1])/2
    confidence_layer_4=confience_coef[2]
    confidence_layer_3=confience_coef[5][1]
    confidence_layer_2=confience_coef[3][1]
    confidence_layer_1=(confience_coef[4]+confience_coef[3][0]+confience_coef[5][0]+confience_coef[6])/4

    confidence_layer_5_norm=confidence_layer_5/(confidence_layer_5+confidence_layer_4+confidence_layer_3+confidence_layer_2+confidence_layer_1)
    confidence_layer_4_norm=confidence_layer_4/(confidence_layer_5+confidence_layer_4+confidence_layer_3+confidence_layer_2+confidence_layer_1)
    confidence_layer_3_norm=confidence_layer_3/(confidence_layer_5+confidence_layer_4+confidence_layer_3+confidence_layer_2+confidence_layer_1)
    confidence_layer_2_norm=confidence_layer_2/(confidence_layer_5+confidence_layer_4+confidence_layer_3+confidence_layer_2+confidence_layer_1)
    confidence_layer_1_norm=confidence_layer_1/(confidence_layer_5+confidence_layer_4+confidence_layer_3+confidence_layer_2+confidence_layer_1)



    confidence_curve=confience_coef[6]
    confidence_lane=confience_coef[4]
    confidence_junction=confience_coef[5][0]

    confidence_curve_norm=confidence_curve/(confidence_curve+confidence_lane+confidence_junction)
    confidence_lane_norm=confidence_curve/(confidence_curve+confidence_lane+confidence_junction)
    confidence_junction_norm=confidence_curve/(confidence_curve+confidence_lane+confidence_junction)


    ##### AFFECTACTUONB DES VALEURS DE CONFIANCE SUR LES LAYUERS 

    matrice_zero =  np.eye(5)
    #### Pour le layer_5_4
    layer_5_4=list_scenario['Sunny']['result_comp_2'].iloc[0]['weight']
    matrice_zero[0][1]=value_layer(layer_5_4)
    matrice_zero[1][0]=1/value_layer(layer_5_4)

    #### Pour le layer_4_3

    layer_4_3=list_scenario['Exit']['result_comp_2'].iloc[0]['weight']
    matrice_zero[1][2]=value_layer(layer_4_3)
    matrice_zero[2][1]=1/value_layer(layer_4_3)

    #### Pour le layer_4_1

    layer_4_1=list_scenario['Type of user']['result_comp_2'].iloc[:2].sum()['weight']
    matrice_zero[1][4]=value_layer(layer_4_1)
    matrice_zero[4][1]=1/value_layer(layer_4_1)

    #### Pour le layer_3_1

    layer_3_1=list_scenario['Exit']['result_comp_1'].iloc[2:].sum()['weight']
    matrice_zero[2][4]=value_layer(layer_4_1)
    matrice_zero[4][2]=1/value_layer(layer_4_1)

    #### Pour le layer_2_1

    layer_3_1=list_scenario['Intersection']['result_comp_1'].iloc[0]['weight']+list_scenario['Intersection']['result_comp_1'].iloc[-1]['weight']
    matrice_zero[3][4]=value_layer(layer_4_1)
    matrice_zero[4][3]=1/value_layer(layer_4_1)

    ### Le cas de congestion ligne

    #### On voit wue le congestion > T intersetion 

    ## Stop > Cycle Lane 

    ### Or Stop = intersection; cycle lane = cyclist

    #### Congestion == A bit more confident

    ### Stop A bit mot

    ### Donc congestion strongly more confident than user

    matrix_ahp=[[1,1/3],[3,1]]
    nom_value=['Vehicle','volume of traffic']
    poid_conge_cycle=ahp_normalisation_poids_matrice(np.array(matrix_ahp))


    ###################################### CREATION DES DICTIONNAIRES DES LAYERS #######################################

    confident_layer={'layer_5':confidence_layer_5_norm,
                 'layer_4':confidence_layer_4_norm,
                 'layer_3':confidence_layer_3_norm,
                 'layer_2':confidence_layer_2_norm,
                 'layer_1':confidence_layer_1_norm
                 }

    ##### Layer 5
    Illuminiation=list_scenario["Driver's Vision"]['result_comp_2'].iloc[0]['weight']
    Weather=list_scenario["Driver's Vision"]['result_comp_2'].iloc[1]['weight']

    ##### Layer 4
    type_user=poid_conge_cycle[0]
    volume_traffic= poid_conge_cycle[1]

    ##### Layer 3
    lane_close=confience_coef[5][1]
    no_temporary= confience_coef[5][0]

    #### Layer 2 

    light_signage=list_scenario["Intersection"]['result_comp_1'].iloc[1].weight/(list_scenario["Intersection"]['result_comp_1'].iloc[-1].weight+list_scenario["Intersection"]['result_comp_1'].iloc[0].weight)
    signage= list_scenario["Intersection"]['result_comp_1'].iloc[0].weight/(list_scenario["Intersection"]['result_comp_1'].iloc[-1].weight+list_scenario["Intersection"]['result_comp_1'].iloc[0].weight)

    ### Layer 1 
    Junction=confidence_junction_norm
    Geometry=confidence_curve_norm
    Lane_spe=confidence_lane_norm

    confident_category={'layer_5':{'Immumination': Illuminiation/(Illuminiation+Weather),
                               'Weather': Weather/(Illuminiation+Weather)},

                    'layer_4':{'Type of user': type_user/(type_user+volume_traffic),
                               'Volume of traffic': volume_traffic/(type_user+volume_traffic)},

                    'layer_3':{'Lane Closed': lane_close/(lane_close+no_temporary),
                               'No Temperoraty': no_temporary/(lane_close+no_temporary)},


                     'layer_2':{'Light Signage': light_signage/(light_signage+signage),
                               'Signage':  signage/(light_signage+signage)},

                     'layer_1':{'Junction':Junction/(Junction+Geometry+Lane_spe),
                                'Geometry': Geometry/(Junction+Geometry+Lane_spe),
                               'Lane specification': Lane_spe/(Junction+Geometry+Lane_spe)},


                 }


    ##### Geometry

    Horizontal=confidence_by_sub_category_ponderation(list_scenario['Curved road'])[0]
    Longitudial=confidence_by_sub_category_ponderation(list_scenario['Curved road'])[1]

    #### Junction

    Roundabout=confidence_by_sub_category_ponderation(list_scenario['Intersection'])[1]
    Intersection=confidence_by_sub_category_ponderation(list_scenario['Intersection'])[0]


    confident_sub_category={'Geometry':{'Horizontal':Horizontal/(Horizontal+Longitudial),
                                    'Longitudial':Longitudial/(Horizontal+Longitudial)},

                        'Junction': {'Roundabout':Roundabout/(Roundabout+Intersection),
                                     'Intersection':Intersection/(Roundabout+Intersection)}                  

    }




    ##### Values des plus base couches 
    pd_value_concat=pd.concat([pd.concat(pandas_weight_ponderer),pd.concat(pandas_weight_ponderer_2),pd.concat(pandas_weight_ponderer_3)])
    Immumination_bis=list(pd_value_concat.iloc[:4].to_dict().values())[0]
    Weather_bis=list(pd_value_concat.iloc[4:8].to_dict().values())[0]
    Type_of_user=list(pd_value_concat.iloc[8:13].to_dict().values())[0]
    volume_traffic_bis=list(pd.concat(pandas_weight_ponderer_3).iloc[4:6].to_dict().values())[0]
    Roundabout_bis={'PresenceRoundabout':confidence_by_sub_category_ponderation(list_scenario['Intersection'])[1],'NoRoundabout':confidence_by_sub_category_ponderation(list_scenario['Intersection'])[0]}
    Intersection_bis={'simple-junction':list(list(pd.concat(pandas_weight_ponderer_3).iloc[0:2].to_dict().values())[0].values())[0],'crossroad':list(list(pd.concat(pandas_weight_ponderer_3).iloc[0:2].to_dict().values())[0].values())[1]}
    Horizontal_bis=list(pandas_weight_ponderer[-1].iloc[0:2].to_dict().values())[0]
    Longitudinal_bis=list(pandas_weight_ponderer[-1].iloc[[0, 2, 3]].to_dict().values())[0]
    Lane_spe_bis=list(pandas_weight_ponderer[-3].to_dict().values())[0]
    direction_highway=list(pd.concat(pandas_weight_ponderer_3).iloc[2:4].to_dict().values())[0]

    value_direction=list(pd.concat(pandas_weight_ponderer_3).iloc[6:8].to_dict().values())[0].values()
    direction_roundabout={"Straight-direction":list(value_direction)[0],'turn-direction':list(value_direction)[1]}



    confident_sub_sub_category={'Intersection':normalize(Intersection_bis)


    }

    confident_values={'Immumination':normalize(Immumination_bis),
                  'Weather':normalize(Weather_bis),
                  'Type of user':normalize(Type_of_user),
                  'Volume of traffic':normalize(volume_traffic_bis),
                  'Roundabout':normalize(Roundabout_bis),
                 # 'Intersection':normalize(Intersection_bis),
                'Horizontal':normalize(Horizontal_bis),
                'Longitudial':normalize(Longitudinal_bis),
                  'Lane specification':normalize(Lane_spe_bis),
                    'simple-junction':normalize(direction_highway),
                      'crossroad':normalize(direction_roundabout),
                  }

        # Convertir les dictionnaires en DataFrame
    df_layer = pd.DataFrame.from_dict(confident_layer, orient='index')

    # Convertir confident_category en DataFrame en utilisant MultiIndex
    data_category = []
    value_count=[]
    values_by_bloc=[]
    values_by_bloc_word=[]
    for key, value in confident_category.items():
        value_bloc_2=[]
        value_bloc_2_word=[]
        for sub_key, sub_value in value.items():

            if sub_key in confident_sub_category.keys():
                for sub_sub_key in confident_sub_category[sub_key]:


                    if sub_sub_key in confident_sub_sub_category.keys():

                        for sub_sub_key_bis in confident_sub_sub_category[sub_sub_key]:

                            value_bloc=[]
                            value_bloc_word=[]
                            for sub_sub_sub_key in confident_values[sub_sub_key_bis]:

                                data_category.append((key,confident_layer['%s'%key], 
                                                      sub_key,confident_layer['%s'%key]*sub_value,
                                                      sub_sub_key, confident_layer['%s'%key]*sub_value*confident_sub_category[sub_key][sub_sub_key],
                                                      sub_sub_key_bis, confident_layer['%s'%key]*sub_value*confident_sub_category[sub_key][sub_sub_key]*confident_sub_sub_category[sub_sub_key][sub_sub_key_bis]
                                                    ,sub_sub_sub_key))




                                value_bloc.append(confident_layer['%s'%key]*sub_value*confident_sub_category[sub_key][sub_sub_key]*confident_sub_sub_category[sub_sub_key][sub_sub_key_bis]*confident_values[sub_sub_key_bis][sub_sub_sub_key])
                                value_bloc_word.append(sub_sub_sub_key)
                                #print(value_bloc)
                            # values_by_bloc.append([confident_layer['%s'%key]*sub_value*confident_sub_category[sub_key][sub_sub_key]*confident_values[sub_sub_key][sub_sub_sub_key]])
                            values_by_bloc.append(value_bloc)

                            value_bloc_word.append(value_bloc_word)


                    else:
                        if sub_sub_key in confident_values.keys():
                            value_bloc=[]
                            value_bloc_word=[]
                            for sub_sub_sub_key in confident_values[sub_sub_key]:
                                data_category.append((key,confident_layer['%s'%key], sub_key,confident_layer['%s'%key]*sub_value,sub_sub_key, 
                                                    confident_layer['%s'%key]*sub_value*confident_sub_category[sub_key][sub_sub_key],sub_sub_sub_key
                                                    ))




                                value_bloc.append(confident_layer['%s'%key]*sub_value*confident_sub_category[sub_key][sub_sub_key]*confident_values[sub_sub_key][sub_sub_sub_key])
                                value_bloc_word.append(sub_sub_sub_key)
                                value_count.append(confident_layer['%s'%key]*sub_value*confident_sub_category[sub_key][sub_sub_key]*confident_values[sub_sub_key][sub_sub_sub_key])
                            # values_by_bloc.append([confident_layer['%s'%key]*sub_value*confident_sub_category[sub_key][sub_sub_key]*confident_values[sub_sub_key][sub_sub_sub_key]])
                            values_by_bloc.append(value_bloc)
                            value_bloc_word.append(value_bloc_word)

                        else:

                            data_category.append((key,confident_layer['%s'%key], sub_key,confident_layer['%s'%key]*sub_value,sub_sub_key
                                                    ))
                            value_count.append(confident_layer['%s'%key]*sub_value*confident_sub_category[sub_key][sub_sub_key])
                            #   values_by_bloc.append([confident_layer['%s'%key]*sub_value*confident_sub_category[sub_key][sub_sub_key]])

            else:

                if sub_key in confident_values.keys():
                    value_bloc=[]
                    value_bloc_word=[]
                    for sub_sub_key in confident_values[sub_key]:
                        data_category.append((key,confident_layer['%s'%key], sub_key,confident_layer['%s'%key]*sub_value,sub_sub_key))
                        value_count.append(confident_layer['%s'%key]*sub_value*confident_values[sub_key][sub_sub_key])
                        value_bloc.append(confident_layer['%s'%key]*sub_value*confident_values[sub_key][sub_sub_key])
                        value_bloc_word.append(sub_sub_key)
                        #  values_by_bloc.append([confident_layer['%s'%key]*sub_value*confident_values[sub_key][sub_sub_key]])
                    values_by_bloc.append(value_bloc)
                    values_by_bloc_word.append(value_bloc_word)
                else: 
                    data_category.append((key,confident_layer['%s'%key], sub_key))
                    value_count.append(confident_layer['%s'%key]*sub_value)
                    value_bloc_2.append(confident_layer['%s'%key]*sub_value)
                    value_bloc_2_word.append(sub_key)
                    if len(value_bloc_2)==2: 
                        values_by_bloc.append(value_bloc_2)
                        values_by_bloc_word.append(value_bloc_2_word)


    index_category =pd.MultiIndex.from_tuples(data_category)
    df_category_2 = pd.DataFrame(data_category, index=index_category)


    # List of attribute lists
    liste = values_by_bloc
    liste_word = values_by_bloc_word=[['sunny', 'cloudy', 'night', 'night w/ artificial illumination'],
    ['no disturbance', 'windy', 'rainy', 'snowy'],
    ['car', 'truck', 'pedestrian', 'bicycle', 'motorcycle'],
    ['free-flow', 'congestioned-flow'],
    ['Lane Closed', 'No Temperoraty'],
    ['Light Signage', 'Signage'],
    ['PresenceRoundabout','NoRoundabout'],
    #['simple-junction','crossroad'],
    ["car-following","lane-changing"],
    ["Straight-direction",'turn-direction'],
    ['straight ','curve'],
    ['plane','upward-slope','downward-slope'],
    ['traffic lane', 'two directions', 'bus lane', 'cycle lane', 'tram lane']]
    # Cartesian product across sub-lists

    resultat_1 = list(product(*liste[0:-4]+liste[-3:]))
    resultat_word_1  = list(product(*liste_word[0:-4]+liste_word[-3:]))

    ## Multiply tuple entries for each combination
    resultat_final_1 =[]
    for i in range(0,len(resultat_1)):
       resultat_final_1.append(sum(resultat_1[i]))


    min_value=min(resultat_final_1)
    max_value=max(resultat_final_1)
    resultat_final_normalised_1=[]
    for i in range(0,len(resultat_final_1)):
        resultat_final_normalised_1.append((resultat_final_1[i]-min_value)/(max_value-min_value))


    df_category = pd.DataFrame([x for xs in values_by_bloc for x in xs], columns=['weight'],index=index_category)


    resultat_2 = list(product(*liste[0:-5]+liste[-4:]))
    resultat_word_2  = list(product(*liste_word[0:-5]+liste_word[-4:]))

    ## Multiply tuple entries for each combination
    resultat_final_2 =[]
    for i in range(0,len(resultat_2)):
       resultat_final_2.append(sum(resultat_2[i]))


    min_value=min(resultat_final_2)
    max_value=max(resultat_final_2)
    resultat_final_normalised_2=[]
    for i in range(0,len(resultat_final_2)):
        resultat_final_normalised_2.append((resultat_final_2[i]-min_value)/(max_value-min_value))


    df_category_2 = pd.DataFrame([x for xs in values_by_bloc for x in xs], columns=['weight'])

    resultat_final_normalised=resultat_final_normalised_1+resultat_final_normalised_2
    resultat_word=resultat_word_1+resultat_word_2
    resultat_final=resultat_final_1+resultat_final_2
    #df_category=pd.concat(df_category_1,df_category_2)
    return resultat_word,resultat_final_normalised,resultat_final,df_category,values_by_bloc_word

   