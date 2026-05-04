# Reference: logical excerpts from ../analyse_ahp.ipynb (do not run this file alone).
#
# Cell ~8: load all three AHP variants on the same CSV
#   %run function_ahp_belief_2.py
#   resultat_word, resultat_final_normalised, resultat_final, df_category, index = ahp_belief('survey_42.csv')
#   %run function_ahp_geometric_2.py
#   resultat_word_2, resultat_final_normalised_2, ... = ahp_weight('survey_42.csv')
#   %run function_ahp_classique_2.py
#   resultat_word_3, resultat_final_normalised_3, ... = ahp_classique('survey_42.csv')
#
# Cell ~18: flat index for the "word" bar chart x-axis
#   key_index = [x for xs in index for x in xs]
#
# Cell ~13: plot_elbow_(resultat_final_normalised_3, name, color, n_components)
#   fig.write_image("%s_mixture.pdf" % (name))
#   # fig.write_image("%s_word.pdf" % (name))  # was commented out in the notebook
#
# Cell ~15: calls that produce C-AHP, B-AHP, W-AHP
#   plot_elbow_(resultat_final_normalised_3, 'C-AHP', px.colors.qualitative.Set1[2], 5)
#   plot_elbow_(resultat_final_normalised, 'B-AHP', px.colors.qualitative.Set1[1], 3)
#   plot_elbow_(resultat_final_normalised_2, 'W-AHP', px.colors.qualitative.Set1[0], 4)
