import numpy as np
import matplotlib.pyplot as plt
from utils import *
import graph
import csv
import datasheet

def get_density(number_of_origin_people, percent_of_student_with_class, T=120, sigma=20, flag=False, batch=3):
    G = graph.Graph(*load_graph())
    Dorm = datasheet.Dorm
    Canteen = datasheet.Canteen
    TeachingBuilding = datasheet.TeachingBuilding
    Corresponeding = datasheet.Corresponeding
    dur = datasheet.dur
    P = datasheet.P
    v = datasheet.v
    K = datasheet.K

    number_of_delta_people = dict()
    delay = dict()
    V = 83.333333
    for dorm in Dorm:
        if flag:
            dT = T / batch
            dsigma = sigma / batch
            number_of_delta_people[dorm] = np.hstack([Normal(np.arange(dT), dT * v[dorm], dsigma) * number_of_origin_people[dorm] / batch] * batch)
        else:
            number_of_delta_people[dorm] = Normal(np.arange(T), T * v[dorm], sigma) * number_of_origin_people[dorm]

        delay[dorm] = dict()
        delay[dorm][Corresponeding[dorm]] = int(G.get_min_distance(dorm, Corresponeding[dorm]) / V)
        for teachingbuilding in TeachingBuilding:
            delay[dorm][teachingbuilding] = int(G.get_min_distance(dorm, teachingbuilding) / V)
    for canteen in Canteen:
        number_of_delta_people[canteen] = np.zeros(T)

        delay[canteen] = dict()
        for teachingbuilding in TeachingBuilding:
            delay[canteen][teachingbuilding] = int(G.get_min_distance(canteen, teachingbuilding) / V)
    for teachingbuilding in TeachingBuilding:
        number_of_delta_people[teachingbuilding] = np.zeros(T)

    for t in range(T):
        for i in range(len(Dorm)):
            for j in range(len(TeachingBuilding)):
                if t >= delay[Dorm[i]][TeachingBuilding[j]]:
                    number_of_delta_people[TeachingBuilding[j]][t] += number_of_delta_people[Dorm[i]][t - delay[Dorm[i]][TeachingBuilding[j]]] * percent_of_student_with_class[Dorm[i]]
                if t >= delay[Dorm[i]][Canteen[i]] + dur[Canteen[i]]:
                    number_of_delta_people[TeachingBuilding[j]][t] += number_of_delta_people[Canteen[i]][t - delay[Dorm[i]][Canteen[i]] - dur[Canteen[i]]] * percent_of_student_with_class[Dorm[i]] * K[TeachingBuilding[j]]
            if t >= delay[Dorm[i]][Canteen[i]]:
                number_of_delta_people[Canteen[i]][t] += number_of_delta_people[Dorm[i]][t - delay[Dorm[i]][Canteen[i]]] * (1 - P[Dorm[i]])

    number_of_remained_people = dict()
    for dorm in Dorm:
        number_of_remained_people[dorm] = get_erosion(number_of_delta_people[dorm], number_of_origin_people[dorm])
    for canteen in Canteen:
        number_of_remained_people[canteen] = get_traffic(number_of_delta_people[canteen], dur[canteen])
    for teachingbuilding in TeachingBuilding:
        number_of_remained_people[teachingbuilding] = get_accumulation(number_of_delta_people[teachingbuilding])
    return number_of_delta_people, number_of_remained_people


if __name__ == '__main__':
    N = datasheet.number_of_origin_people
    u = datasheet.percent_of_student_with_class
    translation = datasheet.translation


    d, r = get_density(N, u, T=120, flag=True, batch=3)
    for node in r:
        plt.plot(np.arange(len(r[node])), r[node])
    plt.show()

