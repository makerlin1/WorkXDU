import numpy as np
import matplotlib.pyplot as plt
import density
import datasheet
import csv


def wash_hand(F, M, P_0=0.8, N_0=5, alpha=0.1):
    N = np.sum([int(dF) for dF in F])
    P = np.random.random(N) * 0.1 + P_0
    days = 60
    track = np.zeros(days)
    for day in range(days):
        idx = 0
        tot = 0  # 厕所当前的人数
        last = 0
        wait = 0
        np.random.shuffle(P)
        for t in range(len(F)):
            s = F[t]
            for i in range(int(s)):
                rand = np.random.rand()
                if rand <= P[idx]:
                    tot += 1
                    if tot <= M:
                        P[idx] += max(0, P_0 - P[idx]) * alpha
                        last += 1
                    elif tot <= M + N_0:
                        wait += 1
                    else:
                        P[idx] -= (M + N_0) / tot * alpha
                        tot -= 1
                idx += 1
            tot -= last
            last = min(M, wait)
            wait -= last
        track[day] = np.sum(P) / N
    return track


if __name__ == '__main__':

    d, r= density.get_density(datasheet.number_of_origin_people, datasheet.percent_of_student_with_class)
    with open('simulation_of_washing_hand.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['增设洗手池数目', '平均洗手率'])

        for m in range(0, 26, 2):
            tr_DC = wash_hand(d['DC'], datasheet.number_of_origin_tap['DC'] + m * datasheet.weight['DC'], P_0=0.5, N_0=3, alpha=0.15)
            tr_AB = wash_hand(d['AB'], datasheet.number_of_origin_tap['AB'] + m * datasheet.weight['AB'], P_0=0.4, N_0=2, alpha=0.15)
            tr_CD = wash_hand(d['CD'], datasheet.number_of_origin_tap['CD'] + m * datasheet.weight['CD'], P_0=0.3, N_0=1, alpha=0.15)
            # tr_EFG = wash_hand(d['EFG'], datasheet.number_of_origin_tap['EFG'] + m, P_0=0.6, N_0=1, alpha=0.15)
            p = 1 - (1 - tr_DC) * (1 - tr_AB) * (1 - tr_CD)
            plt.plot(np.arange(len(p)), p)
            print("M={}".format(m))
            writer.writerow([m, p[-1]])
        plt.show()
