pm_ejemplo = np.array([ [3,1,1,0],
                        [1,2,2,0],
                        [1,1,2,1],
                        [0,0,1,4]])

# alpha1
print(most_frequent_alternative_in_each_position(pm_ejemplo))
np.array(["a1", "a2", "a3", "a4"])[most_frequent_alternative_in_each_position(pm_ejemplo)]

# alpha2
print(least_frequent_alternative_in_each_position(pm_ejemplo))
np.array(["a1", "a2", "a3", "a4"])[least_frequent_alternative_in_each_position(pm_ejemplo)]

# n1
num_of_alternatives_with_max_freq_in_each_pos(pm_ejemplo)

# n2
num_of_alternatives_with_min_freq_in_each_pos(pm_ejemplo)