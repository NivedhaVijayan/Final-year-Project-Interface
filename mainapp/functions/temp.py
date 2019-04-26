from collections import Counter, defaultdict
import enchant


# test = [
#     ['module', 'monolayers', 'lecture', 'surface', 'wave', 'ripple', 'velocity', 'effect', 'surface', 'tension', 'surface', 'compressional', 'modulus', 'damp', 'clean', 'contaminate', 'surface', 'fibers', 'monolayers'], ['wave', 'damp', 'clean', 'surface', 'relate', 'viscosity'], ['wave', 'damp', 'surface', 'active', 'agents', 'concentrations', 'tenth', 'ofmicromolarto', 'millimolar', 'employ', 'wave', 'damp', 'mark', 'damp', 'coefficient', 'easnly', 'calculate', 'iimlt', 'insoluble', 'monolayer', 'completely'], ['equations', 'valid', 'water', 'short', 'wave', 'damplng', 'coefficient', 'vary', 'ilnearly', 'frequency', 'experimental', 'measurement', 'amplitude', 'successive', 'wave', 'trough', 'observe', 'stroboscopic', 'illumination', 'measure', 'focal', 'lengths', 'mirror', 'constitute', 'troughs', 'crest', 'wave'], ['example', 'imagine', 'happen', 'stone', 'throw', 'middle', 'pond', 'stone', 'hit', 'surface', 'water', 'circular', 'pattern', 'wave', 'appear', 'soon', 'turn', 'circular', 'ring', 'wave', 'quiescem', 'center', 'expand', 'ring', 'wave', 'discern', 'individual', 'wavelets', 'differ', 'wavelengths', 'travel', 'different', 'speed', 'longer', 'wave', 'navel', 'fasnar', 'group', 'approach', 'lead', 'edge', 'shorter', 'wave', 'kravel', 'slower', 'emerge', 'trail', 'boundary', 'group'], ['ratio', 'physical', 'mechanism', 'immobilization', 'qulnd', 'flow', 'plane', 'interface', 'prevent', 'passage', 'wave', 'surface', 'viscosity', 'surface', 'measure', 'equation', 'derive', 'equate', 'surface', 'velocity', 'zero', 'pain', 'surface'], ['soluble', 'surface', 'acuve', 'agents', 'damp', 'complicate', 'possibie', 'adsorption', 'desorp', 'surface', 'film', 'passage', 'wave', 'alternate', 'endency', 'expansion', 'rough', 'compression', 'cres', 'cause', 'surface', 'pressure', 'fluctuations', 'reduce', 'adsorption', 'desorption', 'underlie', 'bulk', 'solution', 'passage', 'wave'], ['large', 'wave', 'rough', 'turbulent', 'smaller', 'wave', 'npples', 'surface', 'ianer', 'damp', 'condense', 'surface', 'film', 'make', 'wave', 'smoother', 'turbulent', 'liable', 'break', 'crest', 'drag', 'coefﬁcient', 'consequently', 'reduce', 'lessen', 'formation', 'ripple'], ['surface', 'pressure', 'gradient', 'considerab', 'tendency', 'wave', 'break', 'underthe', 'influence', 'wind', 'reduce', 'sness', 'ofwmd', 'insufﬁcienno', 'pull', 'crest', 'oﬂthe', 'wave', 'consequently', 'materials', 'cetyl', 'alcohol', 'seal', 'blubber', 'fatty', 'acids', 'triglycerides', 'highly', 'effective', 'damp', 'wave', 'oily', 'swell', 'ofthe', 'longer', 'remain', 'kerosene', 'long', 'chain', 'acelamides', 'phenols', 'effective']
# ]



# print(slide_dict)


# print(count_dict)


def computeTF(wd, bow):
    tfDict = {}
    bowcount = len(bow)
    for word, count in wd.items():
        tfDict[word] = count/float(bowcount)
    return tfDict


def computeIDF(doclist):
    import math
    N = len(doclist)
    idfDict = dict.fromkeys(doclist[0].keys(), 0)
    for doc in doclist:
        for word, val in doc.items():
            if val > 0:
                idfDict[word] += 1
    for word, val in idfDict.items():
        idfDict[word] = math.log10(N/float(val))

    return idfDict


def computeTFIDF(tfBow, idfs):
    tfidf = {}
    for word, val in tfBow.items():
        tfidf[word] = val*idfs[word]
    return tfidf


def start_topic_modelling(test):
    slide_dict = {}
    d = enchant.Dict("en_US")
    slide = 1
    for foo in test:
        slide_dict["slide" + str(slide)] = foo
        slide += 1

    all_words = [item for sublist in test for item in sublist]
    temp = []
    for foo in all_words:
        if d.check(foo):
            temp.append(foo)

    count_dict = Counter(all_words)

    tfdict = computeTF(wd=count_dict, bow=all_words)
    idfd = computeIDF(doclist=[count_dict, count_dict])
    final = defaultdict(list)

    # print(computeTFIDF(tfBow=tfdict, idfs=idfd))
    result = sorted(tfdict.items(), key=lambda t: t[1], reverse=True)
    for k, v in result:
        # print(k,v)
        for key, val in slide_dict.items():
            if k in val:
                final[key].append(k)

    print(dict(final))
    return dict(final)



