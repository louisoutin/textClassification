def eval_res(realValues, predictedValues):
    dic = {x: {"VP": 0, "FP": 0, "FN": 0} for x in set(realValues)}
    for i in range(len(realValues)):
        if realValues[i] == predictedValues[i]:
            dic[realValues[i]]["VP"] += 1
        else:
            dic[realValues[i]]["FN"] += 1
            dic[predictedValues[i]]["FP"] += 1
    return dic


def printEvalRes(eval_res):
    f_mesureMoyenne = 0
    cpt = 0
    for i in eval_res:
        cpt += 1
        rappel = float(eval_res[i]["VP"]) / (eval_res[i]["VP"] + eval_res[i]["FN"])
        precision = float(eval_res[i]["VP"]) / (eval_res[i]["VP"] + eval_res[i]["FP"])
        f_mesure = 2 * ((precision * rappel) / (precision + rappel))
        f_mesureMoyenne += f_mesure
        print("Classe" + str(i))
        print("Rappel : " + str(rappel) + "      Precision : " + str(precision) + "      F-mesure : " + str(f_mesure))
    print("FMOYENNE : " + str(f_mesureMoyenne / cpt))