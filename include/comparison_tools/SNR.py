import numpy as np


def SignaltoNoiseRatio(groundTruth, estimation):
    """
    Computes the Signal-to-Noise-Ratio (SNR in dB) which stands for the quadratic error between
    the ground truth and estimation.
    :param groundTruth: ndarray of shape (deps, days) -- or (days,)
    :param estimation: ndarray of shape (deps, days) -- or (days,)
    :return: SNR(groundTruth, estimation)
    """
    normOrder = 2
    assert (len(groundTruth) == len(estimation))
    errorMean = (np.sum(np.abs(estimation[1:] - groundTruth[1:])) / (len(groundTruth) - 1))
    if (estimation[0] - groundTruth[0]) / errorMean > 100000:
        SquaredError = np.sum(np.abs(estimation[1:] - groundTruth[1:]) ** normOrder)
    else:
        SquaredError = np.sum(np.abs(estimation - groundTruth) ** normOrder)
    return 10 * np.log10(np.sum(np.abs(groundTruth) ** normOrder) / SquaredError)


def SignaltoNoiseRatioMC(groundTruth, estimations):
    """
    Compute the Signal-to-Noise-Ratio (SNR in dB) for multiple draws in Monte-Carlo simulations, which R estimations are
    gathered in 'estimations'.
    Returns meanSNR, errorSNR such that SNR(estimations) = meanSNR +/- errorSNR.
    :param groundTruth: ndarray of shape (deps, days) --- or (days,)
    :param estimations: ndarray of shape (nbDraws, deps, days) --- or (nbDraws, days)
    :return: meanSNR: float
             errorSNR: float
    """
    nbDraws, days = np.shape(estimations)
    assert (days == len(groundTruth))

    SNREstim = np.zeros(nbDraws)
    for draw in range(nbDraws):
        SNREstim[draw] = SignaltoNoiseRatio(groundTruth, estimations[draw])
    return (1 / nbDraws) * np.sum(SNREstim), (1.96 / np.sqrt(nbDraws)) * np.std(SNREstim)


def SNRByDep_indic(groundTruth, estimation):
    """
    :param estimation: ndarray of shape (nbDeps, days)
    :param groundTruth: ndarray of shape (nbDeps, days)
    :return:
    """
    nbDeps, days = np.shape(estimation)
    assert (nbDeps == np.shape(groundTruth)[0])
    assert (days == np.shape(groundTruth)[1])

    indicators = np.zeros(nbDeps)
    for d in range(nbDeps):
        indicators[d] = SignaltoNoiseRatio(groundTruth[d], estimation[d])
    return indicators  # we should maximize this criteria


def SNRMean_indic(groundTruth, estimation):
    """
    :param estimation: ndarray of shape (nbDeps, days)
    :param groundTruth: ndarray of shape (nbDeps, days)
    :return:
    """
    nbDeps, days = np.shape(estimation)
    assert (nbDeps == np.shape(groundTruth)[0])
    assert (days == np.shape(groundTruth)[1])

    indicatorsByDep = SNRByDep_indic(groundTruth, estimation)
    # assert (extremum == 'minimum')
    assert (len(indicatorsByDep) == nbDeps)
    indicators = 1 / nbDeps * np.sum(indicatorsByDep)

    return indicators  # we should minimize this criteria
