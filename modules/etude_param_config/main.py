from modules.etude_param_config.adim_number_goal import goal_param,goal_adim, refresh_adim
from modules.etude_param_config.fluid_properties import FluidProperties
from modules.etude_param_config.constraints import constraints
import copy
import random
import matplotlib.pyplot as plt
########################################################################################################################
#                                           INITIALIZATION PROPERTIES
########################################################################################################################
param = copy.deepcopy(goal_param)
param["rho_liq"]=8
#Change param to be in the constraints (next paragraph will check if you did well)



adim = refresh_adim(param)
########################################################################################################################
#                                           Check CONSTRAINTS
########################################################################################################################
def check_constraints(dictionnary,bavard = False):
    for c in constraints:
        key = c
        value = constraints[key]

        if value != None:
            if dictionnary[key]>= value[0] and dictionnary[key]<=value[1]:
                pass
            else:
                if bavard:
                    print(f"Adim param {key=} not in the constraints ({value[0]},{value[1]}). Current value is {adim[key]}.Please change the input")
                return False
    return True
ok = check_constraints(adim, bavard = True)
if not ok:
    raise Exception("See printed things and correct it before continue the execution of the program")




########################################################################################################################
#                                           GENETIC ALOGRITHM
########################################################################################################################
LEN_NEW_PARAMETERS = 100
VARIATION = 0.1 #proportion
SELECTION = 5 #select only the three best part of the evolution
# ONE EVOLUTION STEP
new_param_set, new_adim_set = [], []
best_distance = []
for i in range(15):
    print(i)
    while len(new_param_set) != LEN_NEW_PARAMETERS:
        temp = copy.deepcopy(param)
        for key in temp:
            value = temp[key]
            a,b = value*(1-VARIATION), value*(1+VARIATION)
            temp[key] = random.uniform(a,b)
        temp_adim = refresh_adim(temp)
        if check_constraints(temp_adim):
            new_param_set.append(temp)
            new_adim_set.append(temp_adim)

    # COMPUTE DISTANCE
    d = []
    for elem in new_adim_set:

        temp = 0
        for key in goal_adim:
            temp += (goal_adim[key]-elem[key])**2
        d.append(temp)

    #SELECT WINNERS

    best_distance.append(min(d))
    best = sorted(d, reverse=False)[:3]
    idx_list = []
    for elem in best:
        idx_list.append(d.index(elem))

    old_param_set,old_adim_set = copy.deepcopy(new_param_set), copy.deepcopy(new_adim_set)
    new_param_set, new_adim_set = [], []
    best_param = old_param_set[idx_list[0]]
    best_adim = old_adim_set[idx_list[0]]
    for idx in idx_list:
        new_param_set.append(old_param_set[idx])
        new_adim_set.append(old_adim_set[idx])

plt.plot(best_distance)
plt.show()

print(best_param)
print(goal_param)
print(best_adim)
print(goal_adim)
